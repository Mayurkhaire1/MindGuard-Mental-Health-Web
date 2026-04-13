from app import db
from datetime import datetime
from sqlalchemy import Text, Float, Integer, String, DateTime, Boolean, JSON

class User(db.Model):
    """User model for storing user information"""
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationship to analysis sessions
    sessions = db.relationship('AnalysisSession', backref='user', lazy=True)

class AnalysisSession(db.Model):
    """Model for storing text analysis sessions"""
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    input_text = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Depression prediction results
    depression_score = db.Column(db.Float, default=0.0)
    risk_level = db.Column(db.String(20), default='low')  # low, moderate, high, crisis
    confidence = db.Column(db.Float, default=0.0)
    
    # Emotion detection results
    emotions = db.Column(db.JSON)  # Store emotion scores as JSON
    dominant_emotion = db.Column(db.String(20))
    
    # Text analysis metrics
    word_count = db.Column(db.Integer, default=0)
    sentence_count = db.Column(db.Integer, default=0)
    negative_word_count = db.Column(db.Integer, default=0)
    positive_word_count = db.Column(db.Integer, default=0)
    
    # Clinical indicators
    depression_indicators = db.Column(db.JSON)  # Store identified indicators
    crisis_keywords = db.Column(db.JSON)  # Store crisis-related keywords found
    
    # Analysis results
    detailed_analysis = db.Column(db.JSON)  # Store comprehensive analysis results

class EmotionLexicon(db.Model):
    """Model for storing emotion lexicon data"""
    id = db.Column(db.Integer, primary_key=True)
    word = db.Column(db.String(100), unique=True, nullable=False)
    emotion = db.Column(db.String(20), nullable=False)  # anger, fear, joy, sadness, disgust, surprise
    intensity = db.Column(db.Float, default=0.5)  # 0.0 to 1.0
    category = db.Column(db.String(20), default='general')  # general, clinical, slang

class DepressionLexicon(db.Model):
    """Model for storing depression-related terms and their weights"""
    id = db.Column(db.Integer, primary_key=True)
    term = db.Column(db.String(100), unique=True, nullable=False)
    weight = db.Column(db.Float, nullable=False)  # Negative values for depression indicators
    category = db.Column(db.String(30), nullable=False)  # hopelessness, worthlessness, fatigue, etc.
    clinical_relevance = db.Column(db.Float, default=0.5)  # Clinical significance score

class CrisisKeywords(db.Model):
    """Model for storing crisis intervention keywords"""
    id = db.Column(db.Integer, primary_key=True)
    keyword = db.Column(db.String(100), unique=True, nullable=False)
    severity = db.Column(db.String(20), nullable=False)  # high, critical
    immediate_response = db.Column(db.Boolean, default=False)  # Requires immediate intervention
    category = db.Column(db.String(30))  # suicide, self_harm, violence, etc.

class AnalysisMetrics(db.Model):
    """Model for storing system performance metrics"""
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, default=datetime.utcnow)
    total_analyses = db.Column(db.Integer, default=0)
    high_risk_detections = db.Column(db.Integer, default=0)
    crisis_interventions = db.Column(db.Integer, default=0)
    average_response_time = db.Column(db.Float, default=0.0)  # in seconds
    accuracy_score = db.Column(db.Float, default=0.0)  # Model accuracy metrics

class VoiceAnalysisData(db.Model):
    """Model for storing simulated voice analysis questionnaire data"""
    id = db.Column(db.Integer, primary_key=True)
    session_id = db.Column(db.Integer, db.ForeignKey('analysis_session.id'), nullable=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Voice pattern questions
    speaking_pace_change = db.Column(db.String(20))  # slower, normal, faster, much_slower, much_faster
    voice_volume_change = db.Column(db.String(20))  # quieter, normal, louder, much_quieter, much_louder
    speech_hesitation = db.Column(db.String(20))  # never, rarely, sometimes, often, always
    voice_trembling = db.Column(db.String(20))  # never, rarely, sometimes, often, always
    speech_clarity = db.Column(db.String(20))  # very_clear, clear, unclear, very_unclear, mumbling
    
    # Calculated scores
    voice_stress_score = db.Column(db.Float, default=0.0)  # 0.0 to 1.0
    speech_pattern_score = db.Column(db.Float, default=0.0)  # 0.0 to 1.0

class FacialExpressionData(db.Model):
    """Model for storing simulated facial expression analysis data"""
    id = db.Column(db.Integer, primary_key=True)
    session_id = db.Column(db.Integer, db.ForeignKey('analysis_session.id'), nullable=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Facial expression questions
    smile_frequency = db.Column(db.String(20))  # never, rarely, sometimes, often, always
    facial_tiredness = db.Column(db.String(20))  # never, rarely, sometimes, often, always
    eye_contact_comfort = db.Column(db.String(20))  # very_comfortable, comfortable, uncomfortable, very_uncomfortable
    facial_tension = db.Column(db.String(20))  # relaxed, slightly_tense, tense, very_tense
    expression_control = db.Column(db.String(20))  # easy, normal, difficult, very_difficult
    
    # Calculated scores
    facial_emotion_score = db.Column(db.Float, default=0.0)  # 0.0 to 1.0
    expression_wellness_score = db.Column(db.Float, default=0.0)  # 0.0 to 1.0

class HeartRateData(db.Model):
    """Model for storing simulated heart rate and physical symptom data"""
    id = db.Column(db.Integer, primary_key=True)
    session_id = db.Column(db.Integer, db.ForeignKey('analysis_session.id'), nullable=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Physical symptom questions
    resting_heart_rate = db.Column(db.Integer)  # BPM (estimated by user)
    heart_racing_frequency = db.Column(db.String(20))  # never, rarely, sometimes, often, always
    chest_tightness = db.Column(db.String(20))  # never, rarely, sometimes, often, always
    breathing_difficulty = db.Column(db.String(20))  # never, rarely, sometimes, often, always
    physical_anxiety = db.Column(db.String(20))  # none, mild, moderate, severe, extreme
    sweating_frequency = db.Column(db.String(20))  # never, rarely, sometimes, often, always
    
    # Calculated scores
    cardiovascular_stress_score = db.Column(db.Float, default=0.0)  # 0.0 to 1.0
    physical_anxiety_score = db.Column(db.Float, default=0.0)  # 0.0 to 1.0
