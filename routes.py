from flask import render_template, request, jsonify, redirect, url_for, flash, session
from app import app, db

# Delayed model imports to avoid circular dependency
def get_models():
    from models import AnalysisSession, User, AnalysisMetrics, VoiceAnalysisData, FacialExpressionData, HeartRateData
    return AnalysisSession, User, AnalysisMetrics, VoiceAnalysisData, FacialExpressionData, HeartRateData

from nlp_engine import NLPEngine
from emotion_detector import EmotionDetector
from depression_predictor import DepressionPredictor
from crisis_intervention import CrisisInterventionSystem
from voice_analyzer import VoiceAnalyzer
from facial_analyzer import FacialAnalyzer  
from heart_rate_analyzer import HeartRateAnalyzer
import json
from datetime import datetime, timedelta
import logging

# Initialize NLP components within app context
def init_components():
    with app.app_context():
        return (NLPEngine(), EmotionDetector(), DepressionPredictor(), 
                CrisisInterventionSystem(), VoiceAnalyzer(), FacialAnalyzer(), 
                HeartRateAnalyzer())

# Initialize components
nlp_engine, emotion_detector, depression_predictor, crisis_system, voice_analyzer, facial_analyzer, hr_analyzer = init_components()

def analyze_wellness_journey(wellness_data):
    """Analyze complete wellness journey data and provide personalized results"""
    if not wellness_data:
        return {
            'risk_level': 'unknown',
            'risk_score': 0,
            'protective_factors_level': 'unknown',
            'recommendations': ['Please complete the full assessment for personalized results.'],
            'crisis_risk': False
        }
    
    risk_score = 0
    protective_score = 0
    crisis_indicators = []
    recommendations = []
    
    # Analyze stress factors (Step 2)
    stress_factors = wellness_data.get('stress_factors', {})
    stress_count = len([k for k, v in stress_factors.items() if k.startswith('stress_factors') and v])
    if stress_count >= 4:
        risk_score += 3
        recommendations.append("You're experiencing multiple stressors. Consider stress management techniques.")
    elif stress_count >= 2:
        risk_score += 2
        recommendations.append("Managing stress is important for your wellbeing.")
    
    # Analyze emotional symptoms (Step 3) - PHQ-9 style scoring
    symptoms = wellness_data.get('symptoms', {})
    symptom_score = 0
    for symptom in ['sadness', 'anhedonia', 'sleep_issues', 'fatigue', 'appetite', 'concentration']:
        value = symptoms.get(symptom, '0')
        if value.isdigit():
            symptom_score += int(value)
    
    risk_score += symptom_score
    
    if symptom_score >= 15:
        recommendations.append("⚠️ You're experiencing significant depressive symptoms. Please consider speaking with a mental health professional.")
    elif symptom_score >= 10:
        recommendations.append("You're experiencing moderate depressive symptoms. Support and self-care are important.")
    elif symptom_score >= 5:
        recommendations.append("You're experiencing some depressive symptoms. Monitor your mood and practice self-care.")
    
    # Analyze safety factors (Step 4) - CRITICAL
    safety = wellness_data.get('safety', {})
    
    # Self-harm thoughts
    harm_thoughts = safety.get('self_harm_thoughts', 'never')
    if harm_thoughts in ['often', 'sometimes']:
        risk_score += 5
        crisis_indicators.append("Frequent thoughts of self-harm")
        recommendations.append("🚨 IMMEDIATE: You mentioned thoughts of self-harm. Please contact TeleMANAS (14416 / 1-8008914416) or emergency services.")
    elif harm_thoughts == 'rarely':
        risk_score += 2
        recommendations.append("⚠️ Please talk to someone you trust about these thoughts.")
    
    # Access to means
    access_means = safety.get('access_means', 'no')
    if access_means == 'yes_with_plan':
        risk_score += 6
        crisis_indicators.append("Access to means with planning")
        recommendations.append("🚨 CRISIS: Please seek immediate local emergency help. Emergency contacts directory: https://sarkarilist.in/government-helpline-numbers/")
    elif access_means == 'yes_but_no_plan':
        risk_score += 3
        recommendations.append("⚠️ Consider removing access to means of harm and speaking with a professional.")
    
    # Past attempts
    past_attempts = safety.get('past_attempts', 'never')
    if past_attempts == 'within_year':
        risk_score += 4
        recommendations.append("⚠️ Given your history, please maintain regular contact with mental health professionals.")
    elif past_attempts == 'more_than_year':
        risk_score += 2
        recommendations.append("Continue with your support systems and professional care.")
    
    # Social support (PROTECTIVE FACTOR)
    social_support = safety.get('social_support', 'no_support')
    if social_support == 'strong_support':
        protective_score += 3
    elif social_support == 'some_support':
        protective_score += 2
    elif social_support == 'little_support':
        protective_score += 1
        recommendations.append("Building social connections can greatly improve mental health.")
    else:  # no_support
        risk_score += 2
        recommendations.append("⚠️ Social isolation increases risk. Consider joining support groups or reaching out to family/friends.")
    
    # Counseling willingness (PROTECTIVE FACTOR)
    counseling = safety.get('counseling_willingness', 'not_willing')
    if counseling in ['very_willing', 'somewhat_willing']:
        protective_score += 2
        recommendations.append("✅ Your willingness to seek help is a strong protective factor.")
    elif counseling == 'unsure':
        protective_score += 1
        recommendations.append("Consider exploring therapy options - it can be very helpful.")
    else:
        recommendations.append("Professional support can be valuable even when it feels difficult to start.")
    
    # CRITICAL: Analyze reflection text (Step 5) BEFORE risk calculation!
    reflection = wellness_data.get('reflection', {})
    if reflection:
        reflection_texts = [
            reflection.get('current_feelings', ''),
            reflection.get('main_challenges', ''),
            reflection.get('reasons_living', ''),
            reflection.get('additional_thoughts', '')
        ]
        
        # Combine all text for analysis
        full_text = ' '.join(reflection_texts).lower()
        
        if full_text.strip():
            # COMPREHENSIVE crisis keywords detection
            crisis_keywords = [
                'kill myself', 'want to die', 'suicide', 'end it all', 'better off dead', 
                'no hope', 'hopeless', 'end everything', 'way out is to end', 'meaningless',
                'broken and abandoned', 'nobody I can trust', 'only way out', 'finish myself',
                'take my own life', 'not worth living', 'want to disappear', 'give up on life',
                'end my life', 'kill me', 'rather be dead'
            ]
            
            crisis_detected = False
            detected_keywords = []
            for keyword in crisis_keywords:
                if keyword in full_text:
                    risk_score += 10  # MASSIVE penalty for crisis language
                    crisis_indicators.append(f"Crisis language detected: '{keyword}'")
                    detected_keywords.append(keyword)
                    crisis_detected = True
            
            if crisis_detected:
                recommendations.insert(0, "🚨 IMMEDIATE CRISIS: Your words indicate suicidal thoughts. Please call TeleMANAS (14416 / 1-8008914416) immediately.")
                recommendations.insert(1, "🚨 Crisis support: TeleMANAS (14416 / 1-8008914416) and Jeevan Aastha Helpline (1800 233 3330).")
                recommendations.insert(2, "🚨 You are not alone. Emergency help is available 24/7.")
            
            # Additional concerning language patterns
            concerning_phrases = ['broken', 'abandoned', 'meaningless', 'worthless', 'nobody', 'alone', 'isolated', 'torture', 'fights']
            concerning_count = sum(1 for phrase in concerning_phrases if phrase in full_text)
            if concerning_count >= 3:
                risk_score += 5
                recommendations.append("⚠️ Your emotional state shows multiple concerning factors. Please reach out for professional support immediately.")

    # Calculate final risk level AFTER text analysis
    if risk_score >= 15 or crisis_indicators:
        risk_level = 'crisis'
        risk_color = 'danger'
    elif risk_score >= 10:
        risk_level = 'high'
        risk_color = 'warning'
    elif risk_score >= 5:
        risk_level = 'moderate'
        risk_color = 'info'
    else:
        risk_level = 'low'
        risk_color = 'success'
    
    # Calculate protective factors level
    if protective_score >= 5:
        protective_level = 'strong'
        protective_color = 'success'
    elif protective_score >= 3:
        protective_level = 'moderate'
        protective_color = 'info'
    elif protective_score >= 1:
        protective_level = 'weak'
        protective_color = 'warning'
    else:
        protective_level = 'minimal'
        protective_color = 'danger'

    # Add emergency recommendations for crisis situations
    if risk_level in ['crisis', 'high']:
        recommendations.insert(0, "📞 Emergency contacts: TeleMANAS (14416 / 1-8008914416), Jeevan Aastha Helpline (1800 233 3330). Emergency contacts directory: https://sarkarilist.in/government-helpline-numbers/")
    
    if protective_level in ['minimal', 'weak']:
        recommendations.append("🤝 Focus on building support systems and healthy coping strategies.")
    
    if not recommendations:
        recommendations.append("Continue monitoring your mental health and practicing self-care.")
    
    
    return {
        'risk_level': risk_level.title(),
        'risk_color': risk_color,
        'risk_score': risk_score,
        'protective_factors_level': protective_level.title(),
        'protective_color': protective_color,
        'protective_score': protective_score,
        'recommendations': recommendations,
        'crisis_risk': len(crisis_indicators) > 0,
        'crisis_indicators': crisis_indicators
    }

@app.route('/')
def index():
    """Main landing page"""
    return render_template('index.html')

@app.route('/dashboard')
def dashboard():
    """Main dashboard with overview statistics"""
    # Get recent analysis statistics
    week_ago = datetime.utcnow() - timedelta(days=7)
    
    # Query recent sessions
    AnalysisSession, User, AnalysisMetrics, VoiceAnalysisData, FacialExpressionData, HeartRateData = get_models()
    recent_sessions = AnalysisSession.query.filter(
        AnalysisSession.timestamp >= week_ago
    ).order_by(AnalysisSession.timestamp.desc()).limit(10).all()
    
    # Calculate statistics
    total_analyses = AnalysisSession.query.count()
    high_risk_count = AnalysisSession.query.filter(
        AnalysisSession.risk_level == 'concerning'
    ).count()
    
    # Emotion distribution
    emotion_stats = {}
    for session in recent_sessions:
        if session.dominant_emotion:
            emotion_stats[session.dominant_emotion] = emotion_stats.get(session.dominant_emotion, 0) + 1
    
    # Risk level distribution
    risk_stats = {}
    for session in recent_sessions:
        risk_stats[session.risk_level] = risk_stats.get(session.risk_level, 0) + 1
    
    return render_template('dashboard.html', 
                         total_analyses=total_analyses,
                         high_risk_count=high_risk_count,
                         recent_sessions=recent_sessions,
                         emotion_stats=emotion_stats,
                         risk_stats=risk_stats)

@app.route('/analyze', methods=['GET', 'POST'])
def analyze():
    """Text analysis page"""
    if request.method == 'POST':
        input_text = request.form.get('text', '').strip()
        
        if not input_text:
            flash('Please enter some text to analyze.', 'warning')
            return render_template('analysis.html')
        
        if len(input_text) < 10:
            flash('Please enter at least 10 characters for meaningful analysis.', 'warning')
            return render_template('analysis.html')
        
        try:
            # Start analysis timer
            start_time = datetime.utcnow()
            
            # Perform NLP preprocessing
            processed_text = nlp_engine.preprocess_text(input_text)
            tokens = nlp_engine.tokenize(processed_text)
            features = nlp_engine.extract_features(tokens)
            
            # Emotion detection
            emotion_scores = emotion_detector.detect_emotions(processed_text)
            dominant_emotion = max(emotion_scores.items(), key=lambda x: x[1])[0]
            
            # Depression prediction
            depression_result = depression_predictor.predict_depression(processed_text, features)
            
            # Crisis assessment
            crisis_assessment = crisis_system.assess_crisis_risk(processed_text)
            
            # Calculate analysis time
            analysis_time = (datetime.utcnow() - start_time).total_seconds()
            
            # Create analysis session
            AnalysisSession, User, AnalysisMetrics, VoiceAnalysisData, FacialExpressionData, HeartRateData = get_models()
            session_data = AnalysisSession(
                input_text=input_text,
                depression_score=depression_result['score'],
                risk_level=depression_result['risk_level'],
                confidence=depression_result['confidence'],
                emotions=emotion_scores,
                dominant_emotion=dominant_emotion,
                word_count=len(tokens),
                sentence_count=len(nlp_engine.split_sentences(input_text)),
                negative_word_count=features.get('negative_words', 0),
                positive_word_count=features.get('positive_words', 0),
                depression_indicators=depression_result['indicators'],
                crisis_keywords=crisis_assessment['keywords'],
                detailed_analysis={
                    'emotion_breakdown': emotion_scores,
                    'depression_analysis': depression_result,
                    'crisis_assessment': crisis_assessment,
                    'linguistic_features': features,
                    'analysis_time': analysis_time
                }
            )
            
            db.session.add(session_data)
            db.session.commit()
            
            # Check for crisis intervention — ONLY based on depression_score
            if depression_result['score'] > 0.5:
                return redirect(url_for('crisis_intervention', session_id=session_data.id))
            
            return render_template('analysis.html', 
                                 analysis=session_data,
                                 show_results=True)
            
        except Exception as e:
            logging.error(f"Analysis error: {str(e)}")
            flash('An error occurred during analysis. Please try again.', 'error')
            return render_template('analysis.html')
    
    return render_template('analysis.html')

@app.route('/crisis/<int:session_id>')
def crisis_intervention(session_id):
    """Crisis intervention page"""
    AnalysisSession, User, AnalysisMetrics, VoiceAnalysisData, FacialExpressionData, HeartRateData = get_models()
    session_data = AnalysisSession.query.get_or_404(session_id)
    
    # Get crisis resources and recommendations
    crisis_resources = crisis_system.get_crisis_resources()
    recommendations = crisis_system.get_recommendations(session_data.detailed_analysis['crisis_assessment'])
    
    return render_template('crisis.html', 
                         session=session_data,
                         resources=crisis_resources,
                         recommendations=recommendations)

@app.route('/reports')
def reports():
    """Analysis reports and history"""
    AnalysisSession, User, AnalysisMetrics, VoiceAnalysisData, FacialExpressionData, HeartRateData = get_models()
    page = request.args.get('page', 1, type=int)
    per_page = 20
    
    # Get paginated sessions
    sessions = AnalysisSession.query.order_by(
        AnalysisSession.timestamp.desc()
    ).paginate(page=page, per_page=per_page, error_out=False)
    
    # Generate summary statistics
    total_sessions = AnalysisSession.query.count()
    
    # Risk level distribution
    risk_distribution = db.session.query(
        AnalysisSession.risk_level,
        db.func.count(AnalysisSession.id)
    ).group_by(AnalysisSession.risk_level).all()
    
    # Emotion distribution
    emotion_distribution = db.session.query(
        AnalysisSession.dominant_emotion,
        db.func.count(AnalysisSession.id)
    ).group_by(AnalysisSession.dominant_emotion).filter(
        AnalysisSession.dominant_emotion.isnot(None)
    ).all()

    risk_distribution_dict = {risk: count for risk, count in risk_distribution if risk is not None}
    emotion_distribution_dict = {emotion: count for emotion, count in emotion_distribution if emotion is not None}
    
    # Weekly trend data
    today = datetime.utcnow().date()
    start_date = today - timedelta(days=6)
    start_dt = datetime.combine(start_date, datetime.min.time())

    weekly_sessions = AnalysisSession.query.filter(
        AnalysisSession.timestamp >= start_dt
    ).order_by(AnalysisSession.timestamp).all()

    # Group by day (always include last 7 days with zeros)
    daily_counts = {}
    for i in range(6, -1, -1):
        day = today - timedelta(days=i)
        key = day.strftime('%Y-%m-%d')
        daily_counts[key] = 0

    for session in weekly_sessions:
        day_key = session.timestamp.strftime('%Y-%m-%d')
        if day_key in daily_counts:
            daily_counts[day_key] += 1
        else:
            daily_counts[day_key] = 1
    
    return render_template('reports.html',
                         sessions=sessions,
                         total_sessions=total_sessions,
                         risk_distribution=risk_distribution,
                         risk_distribution_dict=risk_distribution_dict,
                         emotion_distribution=emotion_distribution,
                         emotion_distribution_dict=emotion_distribution_dict,
                         daily_counts=daily_counts)

@app.route('/api/analysis/<int:session_id>')
def get_analysis_details(session_id):
    """API endpoint to get detailed analysis results"""
    AnalysisSession, User, AnalysisMetrics, VoiceAnalysisData, FacialExpressionData, HeartRateData = get_models()
    session_data = AnalysisSession.query.get_or_404(session_id)
    
    return jsonify({
        'id': session_data.id,
        'timestamp': session_data.timestamp.isoformat(),
        'depression_score': session_data.depression_score,
        'risk_level': session_data.risk_level,
        'confidence': session_data.confidence,
        'emotions': session_data.emotions,
        'dominant_emotion': session_data.dominant_emotion,
        'word_count': session_data.word_count,
        'sentence_count': session_data.sentence_count,
        'indicators': session_data.depression_indicators,
        'detailed_analysis': session_data.detailed_analysis
    })

@app.route('/download-report/<int:session_id>')
def download_report(session_id):
    """Generate and download an individual analysis report as PDF"""
    AnalysisSession, User, AnalysisMetrics, VoiceAnalysisData, FacialExpressionData, HeartRateData = get_models()
    session_data = AnalysisSession.query.get_or_404(session_id)

    from reportlab.lib.pagesizes import A4
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.units import inch
    from reportlab.lib.colors import red, blue
    from io import BytesIO

    buffer = BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        topMargin=0.5 * inch,
        bottomMargin=0.5 * inch,
        leftMargin=0.75 * inch,
        rightMargin=0.75 * inch
    )

    styles = getSampleStyleSheet()
    title_style = ParagraphStyle('Title', parent=styles['Heading1'], fontSize=20, textColor=blue, spaceAfter=20, alignment=1)
    heading_style = ParagraphStyle('Heading', parent=styles['Heading2'], fontSize=14, textColor=blue, spaceBefore=12, spaceAfter=8, borderPadding=5, borderBottomWidth=1, borderBottomColor=blue)
    normal_style = styles['Normal']
    crisis_style = ParagraphStyle('Crisis', parent=styles['Normal'], fontSize=11, textColor=red, spaceAfter=6, leading=14)

    story = []
    story.append(Paragraph('MINDGUARD ANALYSIS REPORT', title_style))
    story.append(Paragraph(f"<b>Report ID:</b> {session_data.id}", normal_style))
    story.append(Paragraph(f"<b>Generated:</b> {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S UTC')}", normal_style))
    story.append(Paragraph(f"<b>Assessment Date:</b> {session_data.timestamp.strftime('%Y-%m-%d %H:%M:%S UTC')}", normal_style))
    story.append(Spacer(1, 15))

    story.append(Paragraph('EXECUTIVE SUMMARY', heading_style))
    story.append(Paragraph(f"<b>Risk Level:</b> {session_data.risk_level.upper()}", normal_style))
    story.append(Paragraph(f"<b>Depression Score:</b> {session_data.depression_score:.3f}", normal_style))
    story.append(Paragraph(f"<b>Detection Confidence:</b> {round((session_data.confidence or 0) * 100)}%", normal_style))
    story.append(Paragraph(f"<b>Dominant Emotion:</b> {session_data.dominant_emotion.capitalize() if session_data.dominant_emotion else 'N/A'}", normal_style))
    story.append(Spacer(1, 12))

    story.append(Paragraph('ANALYZED CONTENT', heading_style))
    story.append(Paragraph(session_data.input_text or 'No text provided.', normal_style))
    story.append(Spacer(1, 12))

    if session_data.depression_indicators:
        story.append(Paragraph('DETECTED INDICATORS', heading_style))
        for ind in session_data.depression_indicators:
            indicator_text = ind.get('indicator', str(ind)) if isinstance(ind, dict) else str(ind)
            story.append(Paragraph(f"• {indicator_text}", normal_style))
        story.append(Spacer(1, 12))

    # Add Recommendations
    recommendations = []
    if session_data.detailed_analysis and 'depression_analysis' in session_data.detailed_analysis:
        recommendations = session_data.detailed_analysis['depression_analysis'].get('recommendations', [])
    
    if recommendations:
        story.append(Paragraph('RECOMMENDATIONS', heading_style))
        for rec in recommendations:
            story.append(Paragraph(f"• {rec}", normal_style))
        story.append(Spacer(1, 12))

    story.append(Paragraph('EMERGENCY & SUPPORT RESOURCES', heading_style))
    story.append(Paragraph('<b>TeleMANAS:</b> 14416', crisis_style))
    story.append(Paragraph('<b>TeleMANAS (Toll-Free):</b> 1-8008914416', crisis_style))
    story.append(Paragraph('<b>Jeevan Aastha Helpline:</b> 1800 233 3330', crisis_style))
    story.append(Paragraph('<b>Emergency Directory:</b> sarkarilist.in/government-helpline-numbers', crisis_style))
    story.append(Spacer(1, 15))

    story.append(Paragraph('DISCLAIMER', heading_style))
    story.append(Paragraph('This assessment is generated by an AI system for educational and self-awareness purposes. It does NOT constitute a clinical diagnosis. Please consult a professional or contact the helplines listed above.', normal_style))

    doc.build(story)

    pdf_data = buffer.getvalue()
    buffer.close()

    from flask import Response
    response = Response(
        pdf_data,
        mimetype='application/pdf',
        headers={
            'Content-Disposition': f'attachment; filename=MindGuard_Analysis_Report_{session_data.id}_{datetime.utcnow().strftime("%Y%m%d_%H%M%S")}.pdf'
        }
    )
    return response

@app.route('/api/dashboard-stats')
def dashboard_stats():
    """API endpoint for dashboard statistics"""
    AnalysisSession, User, AnalysisMetrics, VoiceAnalysisData, FacialExpressionData, HeartRateData = get_models()
    # Calculate various statistics
    total_analyses = AnalysisSession.query.count()
    
    # Risk level counts
    risk_counts = {}
    for level in ['positive', 'neutral', 'concerning']:
        count = AnalysisSession.query.filter_by(risk_level=level).count()
        risk_counts[level] = count
    
    # Recent emotion trends
    recent_sessions = AnalysisSession.query.filter(
        AnalysisSession.timestamp >= datetime.utcnow() - timedelta(days=7)
    ).all()
    
    emotion_trends = {}
    for session in recent_sessions:
        if session.emotions:
            for emotion, score in session.emotions.items():
                if emotion not in emotion_trends:
                    emotion_trends[emotion] = []
                emotion_trends[emotion].append(score)
    
    # Average scores
    for emotion in emotion_trends:
        emotion_trends[emotion] = sum(emotion_trends[emotion]) / len(emotion_trends[emotion])
    
    return jsonify({
        'total_analyses': total_analyses,
        'risk_distribution': risk_counts,
        'emotion_trends': emotion_trends,
        'last_updated': datetime.utcnow().isoformat()
    })

@app.route('/voice-analysis', methods=['GET', 'POST'])
def voice_analysis():
    """Voice-based text analysis using speech-to-text transcript"""
    if request.method == 'POST':
        transcript_text = request.form.get('text', '').strip()

        if not transcript_text:
            flash('Please record or type some text to analyze.', 'warning')
            return render_template('voice_analysis.html')

        if len(transcript_text) < 10:
            flash('Please provide at least 10 characters for meaningful analysis.', 'warning')
            return render_template('voice_analysis.html')

        try:
            start_time = datetime.utcnow()

            processed_text = nlp_engine.preprocess_text(transcript_text)
            tokens = nlp_engine.tokenize(processed_text)
            features = nlp_engine.extract_features(tokens)

            emotion_scores = emotion_detector.detect_emotions(processed_text)
            dominant_emotion = max(emotion_scores.items(), key=lambda x: x[1])[0]

            depression_result = depression_predictor.predict_depression(processed_text, features)
            crisis_assessment = crisis_system.assess_crisis_risk(processed_text)

            analysis_time = (datetime.utcnow() - start_time).total_seconds()

            AnalysisSession, User, AnalysisMetrics, VoiceAnalysisData, FacialExpressionData, HeartRateData = get_models()
            session_data = AnalysisSession(
                input_text=transcript_text,
                depression_score=depression_result['score'],
                risk_level=depression_result['risk_level'],
                confidence=depression_result['confidence'],
                emotions=emotion_scores,
                dominant_emotion=dominant_emotion,
                word_count=len(tokens),
                sentence_count=len(nlp_engine.split_sentences(transcript_text)),
                negative_word_count=features.get('negative_words', 0),
                positive_word_count=features.get('positive_words', 0),
                depression_indicators=depression_result['indicators'],
                crisis_keywords=crisis_assessment['keywords'],
                detailed_analysis={
                    'emotion_breakdown': emotion_scores,
                    'depression_analysis': depression_result,
                    'crisis_assessment': crisis_assessment,
                    'linguistic_features': features,
                    'analysis_time': analysis_time,
                    'input_source': 'voice'
                }
            )

            db.session.add(session_data)
            db.session.commit()

            if crisis_assessment['immediate_intervention']:
                return redirect(url_for('crisis_intervention', session_id=session_data.id))

            return render_template('analysis.html', analysis=session_data, show_results=True)
        except Exception as e:
            logging.error(f"Voice transcript analysis error: {str(e)}")
            flash('An error occurred during voice analysis. Please try again.', 'error')
            return render_template('voice_analysis.html')
    
    return render_template('voice_analysis.html')

@app.route('/facial-analysis', methods=['GET', 'POST'])
def facial_analysis():
    """Facial-based text analysis using speech-to-text transcript (camera preview on client)"""
    if request.method == 'POST':
        transcript_text = request.form.get('text', '').strip()

        if not transcript_text:
            flash('Please record or type some text to analyze.', 'warning')
            return render_template('facial_analysis.html')

        if len(transcript_text) < 10:
            flash('Please provide at least 10 characters for meaningful analysis.', 'warning')
            return render_template('facial_analysis.html')

        try:
            start_time = datetime.utcnow()

            processed_text = nlp_engine.preprocess_text(transcript_text)
            tokens = nlp_engine.tokenize(processed_text)
            features = nlp_engine.extract_features(tokens)

            emotion_scores = emotion_detector.detect_emotions(processed_text)
            dominant_emotion = max(emotion_scores.items(), key=lambda x: x[1])[0]

            depression_result = depression_predictor.predict_depression(processed_text, features)
            crisis_assessment = crisis_system.assess_crisis_risk(processed_text)

            analysis_time = (datetime.utcnow() - start_time).total_seconds()

            AnalysisSession, User, AnalysisMetrics, VoiceAnalysisData, FacialExpressionData, HeartRateData = get_models()
            session_data = AnalysisSession(
                input_text=transcript_text,
                depression_score=depression_result['score'],
                risk_level=depression_result['risk_level'],
                confidence=depression_result['confidence'],
                emotions=emotion_scores,
                dominant_emotion=dominant_emotion,
                word_count=len(tokens),
                sentence_count=len(nlp_engine.split_sentences(transcript_text)),
                negative_word_count=features.get('negative_words', 0),
                positive_word_count=features.get('positive_words', 0),
                depression_indicators=depression_result['indicators'],
                crisis_keywords=crisis_assessment['keywords'],
                detailed_analysis={
                    'emotion_breakdown': emotion_scores,
                    'depression_analysis': depression_result,
                    'crisis_assessment': crisis_assessment,
                    'linguistic_features': features,
                    'analysis_time': analysis_time,
                    'input_source': 'facial'
                }
            )

            db.session.add(session_data)
            db.session.commit()

            if crisis_assessment['immediate_intervention']:
                return redirect(url_for('crisis_intervention', session_id=session_data.id))

            return render_template('analysis.html', analysis=session_data, show_results=True)
        except Exception as e:
            logging.error(f"Facial transcript analysis error: {str(e)}")
            flash('An error occurred during facial analysis. Please try again.', 'error')
            return render_template('facial_analysis.html')
    
    return render_template('facial_analysis.html')

@app.route('/heart-rate-analysis', methods=['GET', 'POST'])
def heart_rate_analysis():
    """Heart rate and physical symptoms analysis questionnaire"""
    if request.method == 'POST':
        hr_data = {
            'resting_heart_rate': int(request.form.get('resting_heart_rate', 70)),
            'heart_racing_frequency': request.form.get('heart_racing_frequency'),
            'chest_tightness': request.form.get('chest_tightness'),
            'breathing_difficulty': request.form.get('breathing_difficulty'),
            'physical_anxiety': request.form.get('physical_anxiety'),
            'sweating_frequency': request.form.get('sweating_frequency')
        }
        
        # Analyze heart rate data
        hr_result = hr_analyzer.analyze_heart_rate_data(hr_data)
        
        # Create database entry
        hr_db_data = HeartRateData(
            session_id=None,  # Will link to analysis session later
            resting_heart_rate=hr_data['resting_heart_rate'],
            heart_racing_frequency=hr_data['heart_racing_frequency'],
            chest_tightness=hr_data['chest_tightness'],
            breathing_difficulty=hr_data['breathing_difficulty'],
            physical_anxiety=hr_data['physical_anxiety'],
            sweating_frequency=hr_data['sweating_frequency'],
            cardiovascular_stress_score=hr_result['cardiovascular_stress_score'],
            physical_anxiety_score=hr_result['physical_anxiety_score']
        )
        
        db.session.add(hr_db_data)
        db.session.commit()
        
        return render_template('heart_rate_analysis.html', 
                             results=hr_result,
                             recommendations=hr_analyzer.get_hr_recommendations(hr_result),
                             show_results=True)
    
    return render_template('heart_rate_analysis.html')

@app.route('/wellness-journey', methods=['GET', 'POST'])
def wellness_journey():
    """Comprehensive wellness journey with complete assessment flow"""
    # Get step from form data or URL parameter
    step = request.form.get('current_step') or request.args.get('step', '1')
    
    if request.method == 'POST':
        # Store form data in session for later analysis
        if 'wellness_data' not in session:
            session['wellness_data'] = {}
        
        # Make session permanent to prevent data loss
        session.permanent = True
            
        # Handle form submissions for different steps
        if step == '1':  # Consent and basic info
            session['wellness_data']['consent'] = dict(request.form)
            return redirect(url_for('wellness_journey', step='2'))
        elif step == '2':  # Stress factors
            session['wellness_data']['stress_factors'] = dict(request.form)
            return redirect(url_for('wellness_journey', step='3'))
        elif step == '3':  # Emotional symptoms
            session['wellness_data']['symptoms'] = dict(request.form)
            return redirect(url_for('wellness_journey', step='4'))
        elif step == '4':  # Safety questions
            session['wellness_data']['safety'] = dict(request.form)
            return redirect(url_for('wellness_journey', step='5'))
        elif step == '5':  # Text introspection
            session['wellness_data']['reflection'] = dict(request.form)
            session.permanent = True  # Make sure session persists
            return redirect(url_for('wellness_journey', step='results'))
        elif step == 'results':
            # Perform comprehensive analysis using collected data
            wellness_data = session.get('wellness_data', {})
            wellness_analysis = analyze_wellness_journey(wellness_data)
            return render_template('wellness_journey.html', step='results', 
                                 analysis_results=wellness_analysis, show_results=True)
    
    # For GET requests, also check if we're on results step and have session data
    if step == 'results':
        wellness_data = session.get('wellness_data', {})
        if wellness_data:
            wellness_analysis = analyze_wellness_journey(wellness_data)
            return render_template('wellness_journey.html', step='results', 
                                 analysis_results=wellness_analysis, show_results=True)
    
    return render_template('wellness_journey.html', step=step)

@app.route('/download-wellness-report')
def download_wellness_report():
    """Generate and download comprehensive wellness report as PDF"""
    wellness_data = session.get('wellness_data', {})
    if not wellness_data:
        flash('Please complete the wellness assessment first.', 'warning')
        return redirect(url_for('wellness_journey'))
    
    # Generate analysis
    wellness_analysis = analyze_wellness_journey(wellness_data)
    
    # Generate PDF report
    from reportlab.lib.pagesizes import letter, A4
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.units import inch
    from reportlab.lib.colors import red, blue, green, orange
    from io import BytesIO
    
    # Create PDF in memory
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4, 
                          topMargin=1*inch, bottomMargin=1*inch,
                          leftMargin=1*inch, rightMargin=1*inch)
    
    # Get styles
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle('CustomTitle', parent=styles['Heading1'], 
                                fontSize=20, textColor=blue, spaceAfter=20)
    heading_style = ParagraphStyle('CustomHeading', parent=styles['Heading2'], 
                                 fontSize=14, textColor=blue, spaceAfter=12)
    crisis_style = ParagraphStyle('Crisis', parent=styles['Normal'], 
                                fontSize=12, textColor=red, spaceAfter=6)
    
    # Build PDF content
    story = []
    
    # Title
    story.append(Paragraph("MINDGUARD WELLNESS JOURNEY REPORT", title_style))
    story.append(Paragraph(f"Generated: {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S UTC')}", styles['Normal']))
    story.append(Spacer(1, 20))
    
    # Assessment Results
    story.append(Paragraph("ASSESSMENT RESULTS", heading_style))
    story.append(Paragraph(f"<b>Risk Level:</b> {wellness_analysis['risk_level']} (Score: {wellness_analysis['risk_score']}/20+)", styles['Normal']))
    story.append(Paragraph(f"<b>Protective Factors:</b> {wellness_analysis['protective_factors_level']} (Score: {wellness_analysis['protective_score']}/5+)", styles['Normal']))
    story.append(Paragraph(f"<b>Crisis Risk:</b> {'YES' if wellness_analysis['crisis_risk'] else 'NO'}", crisis_style if wellness_analysis['crisis_risk'] else styles['Normal']))
    story.append(Spacer(1, 20))
    
    # Crisis Indicators
    if wellness_analysis['crisis_indicators']:
        story.append(Paragraph("⚠️ CRISIS INDICATORS DETECTED", crisis_style))
        for indicator in wellness_analysis['crisis_indicators']:
            story.append(Paragraph(f"• {indicator}", crisis_style))
        story.append(Spacer(1, 20))
    
    # Recommendations
    story.append(Paragraph("PERSONALIZED RECOMMENDATIONS", heading_style))
    for i, rec in enumerate(wellness_analysis['recommendations'], 1):
        story.append(Paragraph(f"{i}. {rec}", styles['Normal']))
    story.append(Spacer(1, 20))
    
    # DETAILED USER RESPONSES
    story.append(Paragraph("DETAILED USER RESPONSES", heading_style))
    
    # Stress Factors
    stress_factors = wellness_data.get('stress_factors', {})
    story.append(Paragraph("<b>Stress Factors Selected:</b>", styles['Normal']))
    stress_count = 0
    for key, value in stress_factors.items():
        if key.startswith('stress_factors') and value:
            stress_count += 1
            stress_name = key.replace('stress_factors_', '').replace('_', ' ').title()
            story.append(Paragraph(f"• {stress_name}", styles['Normal']))
    if stress_count == 0:
        story.append(Paragraph("• No stress factors selected", styles['Normal']))
    story.append(Spacer(1, 12))
    
    # Emotional Symptoms 
    symptoms = wellness_data.get('symptoms', {})
    story.append(Paragraph("<b>Emotional Symptoms (0=Never, 3=Nearly every day):</b>", styles['Normal']))
    symptom_labels = {
        'sadness': 'Feeling sad, down, or hopeless',
        'anhedonia': 'Little interest or pleasure in activities',
        'sleep_issues': 'Sleep problems (too much/too little)',
        'fatigue': 'Feeling tired or low energy',
        'appetite': 'Appetite changes',
        'concentration': 'Difficulty concentrating'
    }
    for key, label in symptom_labels.items():
        value = symptoms.get(key, '0')
        story.append(Paragraph(f"• {label}: {value}/3", styles['Normal']))
    story.append(Spacer(1, 12))
    
    # Safety Assessment
    safety = wellness_data.get('safety', {})
    story.append(Paragraph("<b>Safety Assessment Responses:</b>", styles['Normal']))
    story.append(Paragraph(f"• Self-harm thoughts: {safety.get('self_harm_thoughts', 'Not answered')}", styles['Normal']))
    story.append(Paragraph(f"• Access to means of harm: {safety.get('access_means', 'Not answered')}", styles['Normal']))
    story.append(Paragraph(f"• Past suicide attempts: {safety.get('past_attempts', 'Not answered')}", styles['Normal']))
    story.append(Paragraph(f"• Social support: {safety.get('social_support', 'Not answered')}", styles['Normal']))
    story.append(Paragraph(f"• Willingness for counseling: {safety.get('counseling_willingness', 'Not answered')}", styles['Normal']))
    story.append(Spacer(1, 12))
    
    # Text Reflection - FULL USER RESPONSES
    reflection = wellness_data.get('reflection', {})
    if reflection:
        story.append(Paragraph("<b>Personal Reflection - Your Words:</b>", styles['Normal']))
        
        if reflection.get('current_feelings'):
            story.append(Paragraph("<b>Current feelings:</b>", styles['Normal']))
            story.append(Paragraph(f'"{reflection.get("current_feelings", "")}"', styles['Normal']))
            story.append(Spacer(1, 8))
            
        if reflection.get('main_challenges'):
            story.append(Paragraph("<b>Main challenges:</b>", styles['Normal']))
            story.append(Paragraph(f'"{reflection.get("main_challenges", "")}"', styles['Normal']))
            story.append(Spacer(1, 8))
            
        if reflection.get('reasons_living'):
            story.append(Paragraph("<b>Reasons for living:</b>", styles['Normal']))
            story.append(Paragraph(f'"{reflection.get("reasons_living", "")}"', styles['Normal']))
            story.append(Spacer(1, 8))
            
        if reflection.get('additional_thoughts'):
            story.append(Paragraph("<b>Additional thoughts:</b>", styles['Normal']))
            story.append(Paragraph(f'"{reflection.get("additional_thoughts", "")}"', styles['Normal']))
    else:
        story.append(Paragraph("No personal reflection provided", styles['Normal']))
    
    story.append(Spacer(1, 20))
    
    # Emergency Contacts
    story.append(Paragraph("EMERGENCY CONTACTS", heading_style))
    story.append(Paragraph("🚨 TeleMANAS: 14416", crisis_style))
    story.append(Paragraph("🚨 TeleMANAS (Toll-Free): 1-8008914416", crisis_style))
    story.append(Paragraph("🚨 Jeevan Aastha Helpline: 1800 233 3330", crisis_style))
    story.append(Paragraph("🚨 Emergency contacts directory: https://sarkarilist.in/government-helpline-numbers/", crisis_style))
    story.append(Spacer(1, 20))
    
    # Disclaimer
    story.append(Paragraph("DISCLAIMER", heading_style))
    story.append(Paragraph("This assessment is for educational and self-help purposes only. It is not a medical diagnosis or substitute for professional mental health care. If you are in crisis, please contact emergency services immediately.", styles['Normal']))
    story.append(Spacer(1, 12))
    story.append(Paragraph(f"Report ID: WJ-{datetime.utcnow().strftime('%Y%m%d%H%M%S')}", styles['Normal']))
    
    # Build PDF
    doc.build(story)
    
    # Get PDF data
    pdf_data = buffer.getvalue()
    buffer.close()
    
    # Create response with PDF download
    from flask import Response
    response = Response(
        pdf_data,
        mimetype='application/pdf',
        headers={
            'Content-Disposition': f'attachment; filename=MindGuard_Wellness_Report_{datetime.utcnow().strftime("%Y%m%d_%H%M%S")}.pdf'
        }
    )
    return response

@app.route('/live-demo', methods=['GET', 'POST'])
def live_demo():
    """Live demo interface for real-time social media content analysis"""
    from models import AnalysisSession
    
    if request.method == 'POST':
        input_text = request.form.get('text', '').strip()
        content_source = request.form.get('content_source', 'social_media')
        
        if not input_text:
            flash('Please paste some content to analyze.', 'warning')
            return render_template('live_demo.html')
        
        if len(input_text) < 10:
            flash('Please paste at least 10 characters for meaningful analysis.', 'warning')
            return render_template('live_demo.html')
        
        try:
            # Start analysis timer
            start_time = datetime.utcnow()
            
            # Perform NLP preprocessing
            processed_text = nlp_engine.preprocess_text(input_text)
            tokens = nlp_engine.tokenize(processed_text)
            features = nlp_engine.extract_features(tokens)
            
            # Emotion detection
            emotion_scores = emotion_detector.detect_emotions(processed_text)
            dominant_emotion = max(emotion_scores.items(), key=lambda x: x[1])[0]
            
            # Depression prediction
            depression_result = depression_predictor.predict_depression(processed_text, features)
            
            # Crisis assessment
            crisis_assessment = crisis_system.assess_crisis_risk(processed_text)
            
            # Calculate analysis time
            analysis_time = (datetime.utcnow() - start_time).total_seconds()
            
            # Create analysis session for demo
            session_data = AnalysisSession(
                input_text=input_text,
                depression_score=depression_result['score'],
                risk_level=depression_result['risk_level'],
                confidence=depression_result['confidence'],
                emotions=emotion_scores,
                dominant_emotion=dominant_emotion,
                word_count=len(tokens),
                sentence_count=len(nlp_engine.split_sentences(input_text)),
                negative_word_count=features.get('negative_words', 0),
                positive_word_count=features.get('positive_words', 0),
                depression_indicators=depression_result['indicators'],
                crisis_keywords=crisis_assessment['keywords'],
                detailed_analysis={
                    'content_source': content_source,
                    'emotion_breakdown': emotion_scores,
                    'depression_analysis': depression_result,
                    'crisis_assessment': crisis_assessment,
                    'linguistic_features': features,
                    'analysis_time': analysis_time,
                    'demo_mode': True
                }
            )
            
            db.session.add(session_data)
            db.session.commit()
            
            # Check for crisis intervention
            if crisis_assessment['immediate_intervention']:
                return redirect(url_for('crisis_intervention', session_id=session_data.id))
            
            return render_template('live_demo.html', 
                                 analysis=session_data,
                                 content_source=content_source,
                                 show_results=True)
            
        except Exception as e:
            logging.error(f"Live demo analysis error: {str(e)}")
            flash('An error occurred during analysis. Please try again.', 'error')
            return render_template('live_demo.html')
    
    return render_template('live_demo.html')

@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('500.html'), 500
