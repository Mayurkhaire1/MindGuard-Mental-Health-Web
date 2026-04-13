import json
import os
import logging
from datetime import datetime

class DataManager:
    """Manages data initialization and sample data population"""
    
    def __init__(self):
        self.data_initialized = False
        
    def initialize_database(self):
        """Initialize database with sample data if not already populated"""
        try:
            # Import here to avoid circular imports
            from app import db
            from models import EmotionLexicon, DepressionLexicon, CrisisKeywords, AnalysisSession, User
            
            # Check if data already exists
            emotion_count = EmotionLexicon.query.count()
            if emotion_count > 50:  # We expect hundreds of words, so 50+ means initialized
                logging.info(f"Database already initialized with {emotion_count} emotion words")
                return
            
            logging.info("Initializing database with sample data...")
            
            # Initialize emotion lexicon
            self._populate_emotion_lexicon(db, EmotionLexicon)
            
            # Initialize depression lexicon
            self._populate_depression_lexicon(db, DepressionLexicon)
            
            # Initialize crisis keywords
            self._populate_crisis_keywords(db, CrisisKeywords)
            
            # Create sample analysis sessions  
            self._create_sample_sessions(db, AnalysisSession, User)
            
            db.session.commit()
            self.data_initialized = True
            logging.info("Database initialization completed successfully")
            
        except Exception as e:
            logging.error(f"Error initializing database: {str(e)}")
            db.session.rollback()
            # Continue anyway - database might have partial data
    
    def _populate_emotion_lexicon(self, db, EmotionLexicon):
        """Populate emotion lexicon with comprehensive word list"""
        emotion_words = {
            # Joy/Happiness
            'joy': [
                ('happy', 0.8), ('joy', 0.9), ('joyful', 0.8), ('cheerful', 0.7),
                ('glad', 0.6), ('pleased', 0.6), ('delighted', 0.8), ('excited', 0.7),
                ('thrilled', 0.9), ('elated', 0.9), ('euphoric', 1.0), ('ecstatic', 1.0),
                ('wonderful', 0.8), ('amazing', 0.8), ('fantastic', 0.8), ('great', 0.7),
                ('excellent', 0.7), ('perfect', 0.8), ('beautiful', 0.7), ('love', 0.9),
                ('adore', 0.8), ('blissful', 0.9), ('content', 0.6), ('satisfied', 0.6),
                ('peaceful', 0.6), ('optimistic', 0.7), ('hopeful', 0.7), ('enthusiastic', 0.8)
            ],
            
            # Sadness
            'sadness': [
                ('sad', 0.8), ('sadness', 0.8), ('depressed', 0.9), ('depression', 0.9),
                ('down', 0.7), ('blue', 0.6), ('melancholy', 0.8), ('gloomy', 0.7),
                ('sorrowful', 0.8), ('grief', 0.9), ('mourning', 0.8), ('heartbroken', 0.9),
                ('devastated', 0.9), ('crying', 0.7), ('tears', 0.6), ('weeping', 0.8),
                ('sobbing', 0.8), ('miserable', 0.9), ('hopeless', 0.9), ('despair', 1.0),
                ('anguish', 0.9), ('suffering', 0.8), ('pain', 0.7), ('hurt', 0.7),
                ('lonely', 0.8), ('isolated', 0.8), ('abandoned', 0.8), ('worthless', 0.9),
                ('empty', 0.7), ('numb', 0.6), ('disappointed', 0.6), ('discouraged', 0.7)
            ],
            
            # Anger
            'anger': [
                ('angry', 0.8), ('anger', 0.8), ('mad', 0.7), ('furious', 0.9),
                ('rage', 1.0), ('irritated', 0.6), ('annoyed', 0.5), ('frustrated', 0.7),
                ('aggravated', 0.7), ('livid', 0.9), ('enraged', 0.9), ('hate', 0.9),
                ('hatred', 0.9), ('despise', 0.8), ('loathe', 0.8), ('detest', 0.8),
                ('abhor', 0.8), ('hostile', 0.8), ('resentful', 0.7), ('bitter', 0.7),
                ('outraged', 0.9), ('indignant', 0.7), ('wrathful', 0.9), ('incensed', 0.8),
                ('seething', 0.8), ('fuming', 0.8), ('irate', 0.8), ('cross', 0.6)
            ],
            
            # Fear
            'fear': [
                ('afraid', 0.7), ('scared', 0.7), ('fear', 0.8), ('terrified', 0.9),
                ('frightened', 0.8), ('anxious', 0.7), ('anxiety', 0.7), ('worry', 0.6),
                ('worried', 0.6), ('nervous', 0.6), ('panic', 0.9), ('panicked', 0.9),
                ('dread', 0.8), ('terror', 1.0), ('horror', 0.9), ('apprehensive', 0.6),
                ('uneasy', 0.5), ('disturbed', 0.6), ('alarmed', 0.7), ('startled', 0.6),
                ('shocked', 0.7), ('overwhelmed', 0.7), ('threatened', 0.7), ('vulnerable', 0.6),
                ('paranoid', 0.8), ('petrified', 0.9), ('timid', 0.5), ('cautious', 0.4)
            ],
            
            # Disgust
            'disgust': [
                ('disgusting', 0.8), ('disgust', 0.8), ('revolting', 0.9), ('nauseating', 0.8),
                ('repulsive', 0.8), ('gross', 0.7), ('sick', 0.6), ('vomit', 0.7),
                ('repugnant', 0.8), ('abhorrent', 0.8), ('loathsome', 0.8), ('vile', 0.8),
                ('offensive', 0.6), ('distasteful', 0.6), ('unpleasant', 0.5), ('awful', 0.7),
                ('horrible', 0.7), ('nasty', 0.6), ('foul', 0.7), ('putrid', 0.8)
            ],
            
            # Surprise
            'surprise': [
                ('surprised', 0.7), ('surprise', 0.7), ('amazed', 0.8), ('astonished', 0.8),
                ('shocked', 0.8), ('stunned', 0.8), ('bewildered', 0.7), ('confused', 0.6),
                ('unexpected', 0.6), ('sudden', 0.5), ('startled', 0.7), ('baffled', 0.6),
                ('perplexed', 0.6), ('mystified', 0.6), ('flabbergasted', 0.9), ('astounded', 0.8),
                ('dumbfounded', 0.8), ('speechless', 0.7), ('taken aback', 0.7)
            ]
        }
        
        for emotion, words in emotion_words.items():
            for word, intensity in words:
                # Check if word already exists
                existing = EmotionLexicon.query.filter_by(word=word).first()
                if not existing:
                    emotion_entry = EmotionLexicon(
                        word=word,
                        emotion=emotion,
                        intensity=intensity,
                        category='general'
                    )
                    db.session.add(emotion_entry)
    
    def _populate_depression_lexicon(self, db, DepressionLexicon):
        """Populate depression lexicon with clinical terms"""
        depression_terms = {
            # Hopelessness (strongest predictors)
            'hopelessness': [
                ('hopeless', -0.9, 0.95), ('pointless', -0.8, 0.85), ('meaningless', -0.8, 0.80),
                ('worthless', -0.9, 0.90), ('useless', -0.7, 0.75), ('failure', -0.7, 0.70),
                ('give up', -0.8, 0.85), ('no point', -0.8, 0.80), ('what\'s the use', -0.8, 0.80),
                ('nothing matters', -0.9, 0.90), ('no hope', -0.9, 0.95), ('trapped', -0.8, 0.85),
                ('stuck', -0.7, 0.75), ('no way out', -0.8, 0.85), ('doomed', -0.8, 0.80)
            ],
            
            # Fatigue and energy
            'fatigue': [
                ('exhausted', -0.6, 0.70), ('drained', -0.6, 0.65), ('tired', -0.4, 0.50),
                ('fatigued', -0.7, 0.75), ('weary', -0.5, 0.55), ('no energy', -0.7, 0.80),
                ('can\'t move', -0.8, 0.85), ('too tired', -0.6, 0.70), ('sluggish', -0.5, 0.60),
                ('lethargic', -0.6, 0.70), ('weak', -0.5, 0.55), ('heavy', -0.5, 0.50)
            ],
            
            # Isolation and loneliness
            'isolation': [
                ('alone', -0.5, 0.60), ('lonely', -0.7, 0.80), ('isolated', -0.8, 0.85),
                ('abandoned', -0.8, 0.85), ('no friends', -0.7, 0.75), ('nobody cares', -0.8, 0.80),
                ('by myself', -0.4, 0.45), ('cut off', -0.7, 0.70), ('disconnected', -0.6, 0.65),
                ('withdrawn', -0.7, 0.75), ('rejected', -0.7, 0.75), ('unwanted', -0.7, 0.75)
            ],
            
            # Self-harm and suicidal ideation
            'self_harm': [
                ('kill myself', -1.0, 1.0), ('suicide', -1.0, 1.0), ('want to die', -1.0, 1.0),
                ('end it all', -0.95, 0.95), ('not worth living', -0.95, 0.95),
                ('better off dead', -0.95, 0.95), ('wish i was dead', -0.9, 0.90),
                ('hurt myself', -0.9, 0.90), ('self harm', -0.9, 0.90), ('cut myself', -0.9, 0.90),
                ('overdose', -0.9, 0.90), ('jump', -0.8, 0.85), ('pills', -0.7, 0.80)
            ],
            
            # Worthlessness and self-criticism
            'worthlessness': [
                ('hate myself', -0.8, 0.85), ('disgusted with myself', -0.8, 0.80),
                ('not good enough', -0.7, 0.75), ('pathetic', -0.7, 0.70), ('loser', -0.6, 0.65),
                ('disappointing', -0.6, 0.60), ('burden', -0.8, 0.80), ('waste of space', -0.8, 0.85),
                ('stupid', -0.5, 0.50), ('idiot', -0.5, 0.50), ('mess up', -0.5, 0.55)
            ],
            
            # Sleep disturbances
            'sleep_issues': [
                ('can\'t sleep', -0.6, 0.70), ('insomnia', -0.7, 0.80), ('sleep problems', -0.6, 0.65),
                ('restless sleep', -0.5, 0.60), ('tossing and turning', -0.5, 0.55),
                ('sleep too much', -0.6, 0.65), ('always tired', -0.6, 0.70), ('nightmares', -0.6, 0.65),
                ('wake up early', -0.5, 0.55), ('can\'t stay asleep', -0.6, 0.65)
            ]
        }
        
        for category, terms in depression_terms.items():
            for term, weight, clinical_relevance in terms:
                # Check if term already exists
                existing = DepressionLexicon.query.filter_by(term=term).first()
                if not existing:
                    depression_entry = DepressionLexicon(
                        term=term,
                        weight=weight,
                        category=category,
                        clinical_relevance=clinical_relevance
                    )
                    db.session.add(depression_entry)
    
    def _populate_crisis_keywords(self, db, CrisisKeywords):
        """Populate crisis keywords for intervention"""
        crisis_data = [
            # Critical - immediate response
            ('suicide', 'critical', True, 'suicide'),
            ('kill myself', 'critical', True, 'suicide'),
            ('want to die', 'critical', True, 'suicide'),
            ('end it all', 'critical', True, 'suicide'),
            ('plan to die', 'critical', True, 'suicide'),
            ('going to kill', 'critical', True, 'suicide'),
            ('tonight i will', 'critical', True, 'planning'),
            
            # High - urgent response
            ('better off dead', 'high', True, 'suicide'),
            ('not worth living', 'high', True, 'suicide'),
            ('hurt myself', 'high', True, 'self_harm'),
            ('cut myself', 'high', True, 'self_harm'),
            ('self harm', 'high', True, 'self_harm'),
            ('overdose', 'high', True, 'self_harm'),
            ('pills to die', 'high', True, 'self_harm'),
            
            # Moderate - monitor closely
            ('no hope', 'moderate', False, 'hopelessness'),
            ('hopeless', 'moderate', False, 'hopelessness'),
            ('trapped', 'moderate', False, 'hopelessness'),
            ('no way out', 'moderate', False, 'hopelessness'),
            ('can\'t go on', 'moderate', False, 'hopelessness'),
            ('give up', 'moderate', False, 'hopelessness')
        ]
        
        for keyword, severity, immediate_response, category in crisis_data:
            # Check if keyword already exists
            existing = CrisisKeywords.query.filter_by(keyword=keyword).first()
            if not existing:
                crisis_entry = CrisisKeywords(
                    keyword=keyword,
                    severity=severity,
                    immediate_response=immediate_response,
                    category=category
                )
                db.session.add(crisis_entry)
    
    def _create_sample_sessions(self, db, AnalysisSession, User):
        """Create sample analysis sessions for demonstration"""
        sample_texts = [
            {
                'text': "I'm feeling really happy today! Everything seems to be going well and I'm excited about the future.",
                'expected_risk': 'minimal',
                'dominant_emotion': 'joy'
            },
            {
                'text': "I've been feeling down lately. Nothing seems to matter anymore and I just feel empty inside.",
                'expected_risk': 'moderate',
                'dominant_emotion': 'sadness'
            },
            {
                'text': "I'm so angry about what happened. This whole situation is just frustrating and unfair.",
                'expected_risk': 'low',
                'dominant_emotion': 'anger'
            },
            {
                'text': "I'm really worried about the presentation tomorrow. I keep thinking about all the things that could go wrong.",
                'expected_risk': 'low',
                'dominant_emotion': 'fear'
            },
            {
                'text': "Sometimes I feel like I'm worthless and that everyone would be better off without me. I don't see the point in anything anymore.",
                'expected_risk': 'high',
                'dominant_emotion': 'sadness'
            },
            {
                'text': "I feel sick thinking about what happened. This is disgusting and makes me want to vomit.",
                'expected_risk': 'low',
                'dominant_emotion': 'disgust'
            }
        ]
        
        # Create a sample user
        sample_user = User(
            username='demo_user',
            email='demo@example.com'
        )
        db.session.add(sample_user)
        db.session.flush()  # Get the user ID
        
        # Create sample sessions
        for i, sample in enumerate(sample_texts):
            session = AnalysisSession(
                user_id=sample_user.id,
                input_text=sample['text'],
                depression_score=0.0,  # Will be calculated by actual analysis
                risk_level=sample['expected_risk'],
                confidence=0.85,
                emotions={sample['dominant_emotion']: 0.9},
                dominant_emotion=sample['dominant_emotion'],
                word_count=len(sample['text'].split()),
                sentence_count=2,
                negative_word_count=0,
                positive_word_count=0,
                depression_indicators=[],
                crisis_keywords=[],
                detailed_analysis={
                    'sample_data': True,
                    'expected_risk': sample['expected_risk'],
                    'dominant_emotion': sample['dominant_emotion']
                }
            )
            db.session.add(session)
    
    def get_sample_data_status(self):
        """Get status of sample data initialization"""
        try:
            from app import db
            from models import EmotionLexicon, DepressionLexicon, CrisisKeywords, AnalysisSession
            
            emotion_count = EmotionLexicon.query.count()
            depression_count = DepressionLexicon.query.count()
            crisis_count = CrisisKeywords.query.count()
            session_count = AnalysisSession.query.count()
            
            return {
                'initialized': emotion_count > 0,
                'emotion_words': emotion_count,
                'depression_terms': depression_count,
                'crisis_keywords': crisis_count,
                'sample_sessions': session_count
            }
        except Exception as e:
            logging.error(f"Error getting sample data status: {str(e)}")
            return {
                'initialized': False,
                'error': str(e)
            }
    
    def export_lexicons(self):
        """Export lexicons to JSON files for backup/sharing"""
        try:
            # Export emotion lexicon
            emotion_data = []
            for entry in EmotionLexicon.query.all():
                emotion_data.append({
                    'word': entry.word,
                    'emotion': entry.emotion,
                    'intensity': entry.intensity,
                    'category': entry.category
                })
            
            # Export depression lexicon
            depression_data = []
            for entry in DepressionLexicon.query.all():
                depression_data.append({
                    'term': entry.term,
                    'weight': entry.weight,
                    'category': entry.category,
                    'clinical_relevance': entry.clinical_relevance
                })
            
            # Export crisis keywords
            crisis_data = []
            for entry in CrisisKeywords.query.all():
                crisis_data.append({
                    'keyword': entry.keyword,
                    'severity': entry.severity,
                    'immediate_response': entry.immediate_response,
                    'category': entry.category
                })
            
            return {
                'emotion_lexicon': emotion_data,
                'depression_lexicon': depression_data,
                'crisis_keywords': crisis_data
            }
            
        except Exception as e:
            logging.error(f"Error exporting lexicons: {str(e)}")
            return None
