import json
import math
import re
from typing import Dict, List, Tuple, Any
import logging

class DepressionPredictor:
    """Custom depression prediction system using multiple analytical approaches"""
    
    def __init__(self):
        self.depression_lexicon = self._load_depression_lexicon()
        self.crisis_keywords = self._load_crisis_keywords()
        self.depression_patterns = self._initialize_depression_patterns()
        self.cognitive_patterns = self._initialize_cognitive_patterns()
        self.weights = self._initialize_feature_weights()
        self.positive_phrases = self._initialize_positive_phrases()
        self.neutral_phrases = self._initialize_neutral_phrases()

    def _initialize_positive_phrases(self) -> List[str]:
        return [
            'feel great',
            'feeling great',
            'excited about',
            'looking forward',
            'optimistic',
            'happy',
            'motivated',
            'energized',
            'energetic',
            'life is great'
        ]

    def _initialize_neutral_phrases(self) -> List[str]:
        return [
            'nothing special',
            'nothing special happened',
            'normal day',
            'regular day',
            'just a normal day',
            'nothing much',
            'same as usual',
            'nothing out of the ordinary',
            'routine',
            'routine day',
            'as expected',
            'just another day'
        ]
        
    def _load_depression_lexicon(self) -> Dict[str, Dict[str, float]]:
        """Load depression-related terms and their weights from database"""
        lexicon = {}
        
        try:
            # Load from database (delayed import to avoid circular dependency)
            from app import db
            from models import DepressionLexicon
            depression_terms = DepressionLexicon.query.all()
            
            for term_entry in depression_terms:
                term = term_entry.term.lower()
                weight = term_entry.weight
                category = term_entry.category
                clinical_relevance = term_entry.clinical_relevance
                
                if term not in lexicon:
                    lexicon[term] = {}
                
                lexicon[term] = {
                    'weight': weight,
                    'category': category,
                    'clinical_relevance': clinical_relevance
                }
                
        except Exception as e:
            logging.warning(f"Could not load depression lexicon from database: {e}")
            lexicon = self._create_default_depression_lexicon()
        
        if not lexicon:
            lexicon = self._create_default_depression_lexicon()
            
        return lexicon
    
    def _create_default_depression_lexicon(self) -> Dict[str, Dict[str, float]]:
        """Create comprehensive default depression lexicon based on clinical research"""
        lexicon = {}
        
        # Hopelessness indicators (strong predictors of depression)
        hopelessness_terms = {
            'hopeless': {'weight': -0.9, 'clinical_relevance': 0.95},
            'pointless': {'weight': -0.8, 'clinical_relevance': 0.85},
            'meaningless': {'weight': -0.9, 'clinical_relevance': 0.95},
            'worthless': {'weight': -0.9, 'clinical_relevance': 0.90},
            'useless': {'weight': -0.7, 'clinical_relevance': 0.75},
            'failure': {'weight': -0.7, 'clinical_relevance': 0.70},
            'give up': {'weight': -0.8, 'clinical_relevance': 0.85},
            'no point': {'weight': -0.8, 'clinical_relevance': 0.80},
            'what\'s the use': {'weight': -0.8, 'clinical_relevance': 0.80},
            'nothing matters': {'weight': -0.9, 'clinical_relevance': 0.90},
            'no hope': {'weight': -0.9, 'clinical_relevance': 0.95},
            'broken and abandoned': {'weight': -0.9, 'clinical_relevance': 0.90},
            'nobody I can trust': {'weight': -0.8, 'clinical_relevance': 0.85}
        }
        
        # Fatigue and energy indicators
        fatigue_terms = {
            'exhausted': {'weight': -0.6, 'clinical_relevance': 0.70},
            'drained': {'weight': -0.6, 'clinical_relevance': 0.65},
            'tired': {'weight': -0.4, 'clinical_relevance': 0.50},
            'fatigued': {'weight': -0.7, 'clinical_relevance': 0.75},
            'weary': {'weight': -0.5, 'clinical_relevance': 0.55},
            'no energy': {'weight': -0.7, 'clinical_relevance': 0.80},
            'can\'t move': {'weight': -0.8, 'clinical_relevance': 0.85},
            'too tired': {'weight': -0.6, 'clinical_relevance': 0.70}
        }
        
        # Isolation and loneliness
        isolation_terms = {
            'alone': {'weight': -0.5, 'clinical_relevance': 0.60},
            'lonely': {'weight': -0.7, 'clinical_relevance': 0.80},
            'isolated': {'weight': -0.8, 'clinical_relevance': 0.85},
            'abandoned': {'weight': -0.8, 'clinical_relevance': 0.85},
            'no friends': {'weight': -0.7, 'clinical_relevance': 0.75},
            'nobody cares': {'weight': -0.8, 'clinical_relevance': 0.80},
            'by myself': {'weight': -0.4, 'clinical_relevance': 0.45},
            'cut off': {'weight': -0.7, 'clinical_relevance': 0.70},
            'broken': {'weight': -0.7, 'clinical_relevance': 0.75},
            'torture': {'weight': -0.8, 'clinical_relevance': 0.80},
            'fights': {'weight': -0.6, 'clinical_relevance': 0.65}
        }
        
        # Self-harm and suicidal ideation (highest clinical relevance)
        self_harm_terms = {
            'kill myself': {'weight': -1.0, 'clinical_relevance': 1.0},
            'suicide': {'weight': -1.0, 'clinical_relevance': 1.0},
            'want to die': {'weight': -1.0, 'clinical_relevance': 1.0},
            'end it all': {'weight': -1.0, 'clinical_relevance': 1.0},
            'end everything': {'weight': -1.0, 'clinical_relevance': 1.0},
            'way out is to end': {'weight': -1.0, 'clinical_relevance': 1.0},
            'only way out': {'weight': -1.0, 'clinical_relevance': 1.0},
            'take my own life': {'weight': -1.0, 'clinical_relevance': 1.0},
            'not worth living': {'weight': -1.0, 'clinical_relevance': 1.0},
            'better off dead': {'weight': -1.0, 'clinical_relevance': 1.0},
            'want to disappear': {'weight': -0.95, 'clinical_relevance': 0.95},
            'give up on life': {'weight': -0.95, 'clinical_relevance': 0.95},
            'rather be dead': {'weight': -0.95, 'clinical_relevance': 0.95},
            'finish myself': {'weight': -0.95, 'clinical_relevance': 0.95},
            'end my life': {'weight': -0.95, 'clinical_relevance': 0.95},
            'wish i was dead': {'weight': -0.9, 'clinical_relevance': 0.90},
            'hurt myself': {'weight': -0.9, 'clinical_relevance': 0.90},
            'self harm': {'weight': -0.9, 'clinical_relevance': 0.90},
            'cut myself': {'weight': -0.9, 'clinical_relevance': 0.90}
        }
        
        # Worthlessness and self-criticism
        worthlessness_terms = {
            'hate myself': {'weight': -0.8, 'clinical_relevance': 0.85},
            'disgusted with myself': {'weight': -0.8, 'clinical_relevance': 0.80},
            'not good enough': {'weight': -0.7, 'clinical_relevance': 0.75},
            'pathetic': {'weight': -0.7, 'clinical_relevance': 0.70},
            'loser': {'weight': -0.6, 'clinical_relevance': 0.65},
            'disappointing': {'weight': -0.6, 'clinical_relevance': 0.60},
            'burden': {'weight': -0.8, 'clinical_relevance': 0.80}
        }
        
        # Sleep disturbances
        sleep_terms = {
            'can\'t sleep': {'weight': -0.6, 'clinical_relevance': 0.70},
            'insomnia': {'weight': -0.7, 'clinical_relevance': 0.80},
            'sleep problems': {'weight': -0.6, 'clinical_relevance': 0.65},
            'restless sleep': {'weight': -0.5, 'clinical_relevance': 0.60},
            'tossing and turning': {'weight': -0.5, 'clinical_relevance': 0.55},
            'sleep too much': {'weight': -0.6, 'clinical_relevance': 0.65},
            'always tired': {'weight': -0.6, 'clinical_relevance': 0.70}
        }
        
        # Combine all categories
        categories = {
            'hopelessness': hopelessness_terms,
            'fatigue': fatigue_terms,
            'isolation': isolation_terms,
            'self_harm': self_harm_terms,
            'worthlessness': worthlessness_terms,
            'sleep_issues': sleep_terms
        }
        
        # Build the lexicon
        for category, terms in categories.items():
            for term, values in terms.items():
                lexicon[term] = {
                    'weight': values['weight'],
                    'category': category,
                    'clinical_relevance': values['clinical_relevance']
                }
        
        return lexicon
    
    def _load_crisis_keywords(self) -> List[Dict[str, Any]]:
        """Load crisis intervention keywords from database"""
        crisis_keywords = []
        
        try:
            # Delayed import to avoid circular dependency
            from models import CrisisKeywords
            keywords = CrisisKeywords.query.all()
            for keyword_entry in keywords:
                crisis_keywords.append({
                    'keyword': keyword_entry.keyword.lower(),
                    'severity': keyword_entry.severity,
                    'immediate_response': keyword_entry.immediate_response,
                    'category': keyword_entry.category
                })
                
        except Exception as e:
            logging.warning(f"Could not load crisis keywords from database: {e}")
            crisis_keywords = self._create_default_crisis_keywords()
        
        if not crisis_keywords:
            crisis_keywords = self._create_default_crisis_keywords()
            
        return crisis_keywords
    
    def _create_default_crisis_keywords(self) -> List[Dict[str, Any]]:
        """Create comprehensive default crisis intervention keywords"""
        return [
            # CRITICAL SUICIDE INDICATORS
            {'keyword': 'suicide', 'severity': 'critical', 'immediate_response': True, 'category': 'suicide'},
            {'keyword': 'kill myself', 'severity': 'critical', 'immediate_response': True, 'category': 'suicide'},
            {'keyword': 'want to die', 'severity': 'critical', 'immediate_response': True, 'category': 'suicide'},
            {'keyword': 'end it all', 'severity': 'critical', 'immediate_response': True, 'category': 'suicide'},
            {'keyword': 'end everything', 'severity': 'critical', 'immediate_response': True, 'category': 'suicide'},
            {'keyword': 'way out is to end', 'severity': 'critical', 'immediate_response': True, 'category': 'suicide'},
            {'keyword': 'only way out', 'severity': 'critical', 'immediate_response': True, 'category': 'suicide'},
            {'keyword': 'take my own life', 'severity': 'critical', 'immediate_response': True, 'category': 'suicide'},
            {'keyword': 'better off dead', 'severity': 'critical', 'immediate_response': True, 'category': 'suicide'},
            {'keyword': 'not worth living', 'severity': 'critical', 'immediate_response': True, 'category': 'suicide'},
            {'keyword': 'want to disappear', 'severity': 'critical', 'immediate_response': True, 'category': 'suicide'},
            {'keyword': 'give up on life', 'severity': 'critical', 'immediate_response': True, 'category': 'suicide'},
            {'keyword': 'rather be dead', 'severity': 'critical', 'immediate_response': True, 'category': 'suicide'},
            {'keyword': 'finish myself', 'severity': 'critical', 'immediate_response': True, 'category': 'suicide'},
            {'keyword': 'end my life', 'severity': 'critical', 'immediate_response': True, 'category': 'suicide'},
            
            # CRITICAL HOPELESSNESS
            {'keyword': 'no hope', 'severity': 'critical', 'immediate_response': True, 'category': 'hopelessness'},
            {'keyword': 'hopeless', 'severity': 'critical', 'immediate_response': True, 'category': 'hopelessness'},
            {'keyword': 'meaningless', 'severity': 'critical', 'immediate_response': True, 'category': 'hopelessness'},
            {'keyword': 'broken and abandoned', 'severity': 'critical', 'immediate_response': True, 'category': 'hopelessness'},
            {'keyword': 'nobody I can trust', 'severity': 'critical', 'immediate_response': True, 'category': 'hopelessness'},
            
            # SELF-HARM INDICATORS
            {'keyword': 'hurt myself', 'severity': 'critical', 'immediate_response': True, 'category': 'self_harm'},
            {'keyword': 'cut myself', 'severity': 'critical', 'immediate_response': True, 'category': 'self_harm'},
            {'keyword': 'self harm', 'severity': 'critical', 'immediate_response': True, 'category': 'self_harm'},
            
            # HIGH RISK INDICATORS
            {'keyword': 'worthless', 'severity': 'high', 'immediate_response': True, 'category': 'worthlessness'},
            {'keyword': 'alone', 'severity': 'high', 'immediate_response': False, 'category': 'isolation'},
            {'keyword': 'isolated', 'severity': 'high', 'immediate_response': False, 'category': 'isolation'},
            {'keyword': 'abandoned', 'severity': 'high', 'immediate_response': False, 'category': 'isolation'},
            {'keyword': 'broken', 'severity': 'high', 'immediate_response': False, 'category': 'despair'},
            {'keyword': 'torture', 'severity': 'high', 'immediate_response': False, 'category': 'trauma'},
            {'keyword': 'fights', 'severity': 'moderate', 'immediate_response': False, 'category': 'stress'}
        ]
    
    def _initialize_depression_patterns(self) -> Dict[str, List[str]]:
        """Initialize regex patterns for depression detection"""
        return {
            'hopelessness_expressions': [
                r'\b(nothing will get better|things will never change|no hope)\b',
                r'\b(why bother|what\'s the point|no use trying)\b',
                r'\b(always be this way|never going to change)\b'
            ],
            'self_criticism': [
                r'\b(i\'m so stupid|i\'m an idiot|i\'m worthless)\b',
                r'\b(i hate myself|i\'m disgusting|i\'m pathetic)\b',
                r'\b(i can\'t do anything right|i always mess up)\b'
            ],
            'cognitive_distortions': [
                r'\b(always|never|everyone|nobody|everything|nothing)\b',
                r'\b(should have|could have|if only)\b',
                r'\b(all or nothing|black and white)\b'
            ],
            'withdrawal_indicators': [
                r'\b(don\'t want to see anyone|avoiding people|staying in bed)\b',
                r'\b(cancelled plans|didn\'t go|stayed home)\b',
                r'\b(don\'t feel like|can\'t be bothered)\b'
            ],
            'physical_symptoms': [
                r'\b(no appetite|can\'t eat|lost weight)\b',
                r'\b(headaches|stomach aches|body aches)\b',
                r'\b(can\'t concentrate|memory problems|foggy)\b'
            ]
        }
    
    def _initialize_cognitive_patterns(self) -> Dict[str, float]:
        """Initialize cognitive distortion patterns and their weights"""
        return {
            'all_or_nothing': -0.6,  # "always", "never", "everyone", "nobody"
            'catastrophizing': -0.7,  # "terrible", "disaster", "awful"
            'personalization': -0.5,  # "my fault", "because of me"
            'mind_reading': -0.4,  # "they think", "they hate me"
            'fortune_telling': -0.5,  # "will never", "always will"
            'emotional_reasoning': -0.4,  # "feel like", "seems like"
            'should_statements': -0.5,  # "should", "must", "have to"
            'labeling': -0.6  # "i'm stupid", "i'm worthless"
        }
    
    def _initialize_feature_weights(self) -> Dict[str, float]:
        """Initialize weights for different feature categories"""
        return {
            'lexicon_score': 0.35,  # Depression lexicon matching
            'emotion_sadness': 0.15,  # Sadness emotion score
            'emotion_fear': 0.10,  # Fear/anxiety emotion score
            'crisis_keywords': 0.25,  # Crisis intervention keywords
            'cognitive_patterns': 0.10,  # Cognitive distortion patterns
            'linguistic_features': 0.05  # Additional linguistic features
        }
    
    def predict_depression(self, text: str, features: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Comprehensive depression prediction using multiple analytical approaches
        Returns detailed prediction results with confidence scores
        """
        if not text:
            return self._create_empty_prediction()
        
        text_lower = text.lower()
        
        # Initialize prediction components
        prediction_components = {}
        
        # 1. Lexicon-based scoring
        lexicon_result = self._calculate_lexicon_score(text_lower)
        prediction_components['lexicon'] = lexicon_result
        
        # 2. Crisis keyword detection
        crisis_result = self._detect_crisis_indicators(text_lower)
        prediction_components['crisis'] = crisis_result
        
        # 3. Cognitive pattern analysis
        cognitive_result = self._analyze_cognitive_patterns(text_lower)
        prediction_components['cognitive'] = cognitive_result
        
        # 4. Linguistic feature analysis
        if features:
            linguistic_result = self._analyze_linguistic_features(features)
            prediction_components['linguistic'] = linguistic_result
        else:
            prediction_components['linguistic'] = {'score': 0.0, 'indicators': []}
        
        # 5. Emotional profile analysis
        emotion_result = self._analyze_emotional_profile(features if features else {})
        prediction_components['emotional'] = emotion_result
        
        # Calculate weighted final score
        final_score = self._calculate_weighted_score(prediction_components)

        # --- STRICT PRIORITY CLASSIFICATION RULES ---
        # 1: Identify key signals
        strong_negative_phrases = [
            'nothing matters', 'feeling low', 'struggling', 'no motivation',
            'lost interest', 'trouble sleeping', 'emotionally drained',
            'no hope', 'hopeless', 'give up', 'want to die', 'kill myself',
            'sleep issues', "can't sleep", 'cannot sleep'
        ]
        
        has_clear_negative = self._has_clear_negative_signals(text_lower, prediction_components)
        negative_match_count = sum(1 for p in strong_negative_phrases if p in text_lower)
        positive_buffer = self._calculate_positive_buffer(text_lower)
        is_explicitly_neutral = any(phrase in text_lower for phrase in self.neutral_phrases)

        # STEP 1: CONCERNING (Strong Negative Signals)
        # Hard rules: 'nothing matters' always concerning. 2+ negative phrases always concerning. Crisis > 0 always concerning.
        is_concerning = False
        if 'nothing matters' in text_lower:
            is_concerning = True
        elif negative_match_count >= 2:
            is_concerning = True
        elif prediction_components['crisis']['score'] > 0:
            is_concerning = True
            
        if is_concerning:
            final_score = max(0.55, final_score)
            
        # STEP 2: NEUTRAL (No emotion or explicitly neutral)
        elif not has_clear_negative and positive_buffer == 0:
            # Absence of negative != positive. No emotion means NEUTRAL.
            final_score = 0.35
        elif is_explicitly_neutral and not has_clear_negative:
            # Explicit neutral phrases without distress -> NEUTRAL
            final_score = 0.35

        # STEP 3: POSITIVE (Strong Positive Signals)
        elif positive_buffer > 0 and not has_clear_negative:
            # Clear positive emotion exists -> POSITIVE
            final_score = min(0.15, final_score)
        
        # Determine risk level and confidence (based STRICTLY on final_score)
        
        # Determine risk level and confidence
        risk_level, confidence = self._determine_risk_level(final_score, prediction_components)
        
        # Compile indicators
        all_indicators = self._compile_indicators(prediction_components)
        
        # Generate recommendations
        recommendations = self._generate_recommendations(risk_level, all_indicators)
        
        return {
            'score': final_score,
            'risk_level': risk_level,
            'confidence': confidence,
            'indicators': all_indicators,
            'components': prediction_components,
            'recommendations': recommendations,
            'analysis_summary': self._generate_analysis_summary(final_score, risk_level, all_indicators)
        }

    def _compute_distress_floor(self, text_lower: str, components: Dict[str, Dict[str, Any]]) -> float:
        """Compute a minimum depression score floor when clear distress language exists.

        This prevents short-but-concerning inputs from being normalized away.
        Returns a value in [0.0, 1.0].
        """
        floor = 0.0

        # Crisis indicators get the highest floor
        crisis = components.get('crisis', {})
        if crisis.get('immediate_intervention'):
            return 0.85
        if crisis.get('score', 0) > 0:
            floor = max(floor, 0.60 + crisis['score'] * 0.25)

        # Heavy-weight depression lexicon matches
        matched = components.get('lexicon', {}).get('matched_terms', [])
        if matched:
            max_weight = max(abs(t.get('weight', 0)) for t in matched)
            max_clin = max(t.get('clinical_relevance', 0) for t in matched)
            # Scale: a single term with weight 0.9 and relevance 0.9 → floor ~0.56
            floor = max(floor, 0.35 + 0.25 * max_weight * max_clin)

        # Explicit phrase patterns that should always be at least moderate
        severe_phrases = [
            'nothing matters', 'nothing seems to matter',
            'no hope', 'no point', 'give up',
            'going through the motions', 'just existing',
            'hate myself', 'want to die', 'kill myself',
        ]
        mild_concern_phrases = [
            'feel down', 'feeling down', 'felt down',
            'feeling really down', 'really down', 'very down',
            'exhausted', 'no energy', 'no motivation',
            'alone', 'lonely', 'can\'t sleep', 'insomnia',
            'lost interest', 'losing interest', 'no interest',
            'struggling', 'suffering', 'miserable',
            'pointless',
        ]
        for p in severe_phrases:
            if p in text_lower:
                floor = max(floor, 0.50)
        for p in mild_concern_phrases:
            if p in text_lower:
                floor = max(floor, 0.40)

        return min(1.0, floor)

    def _calculate_positive_buffer(self, text_lower: str) -> float:
        """Return 0..1 score for strong positive signals."""
        score = 0.0

        for phrase in self.positive_phrases:
            if phrase in text_lower:
                score += 0.25

        # Light positive-word boost
        positive_words = {
            'great', 'excited', 'happy', 'optimistic', 'energetic', 'energized',
            'motivated', 'wonderful', 'amazing', 'love', 'thrilled', 'joyful'
        }
        score += min(0.5, 0.05 * sum(1 for w in positive_words if re.search(r'\b' + re.escape(w) + r'\b', text_lower)))

        return min(1.0, score)

    def _detect_neutral_text(self, text_lower: str) -> bool:
        """Detect routine/neutral statements to avoid over-triggering.
        
        Only returns True when the text genuinely matches a neutral template
        AND does not contain any explicit distress phrases.
        """
        if not any(phrase in text_lower for phrase in self.neutral_phrases):
            return False
        # If any clear negative signal is present, it is NOT neutral
        if self._text_has_distress_phrases(text_lower):
            return False
        return True

    def _text_has_distress_phrases(self, text_lower: str) -> bool:
        """Check if text contains explicit distress / concerning phrases."""
        # Exact substring matches
        distress_phrases = [
            'nothing matters', 'nothing seems to matter', 'nothing to matter',
            'doesn\'t matter anymore', 'does not matter anymore',
            'don\'t matter', 'do not matter',
            'feel down', 'feeling down', 'felt down',
            'feeling really down', 'really down', 'very down', 'so down',
            'hopeless', 'worthless', 'helpless',
            'lost interest', 'no interest', 'losing interest',
            'cannot sleep', "can't sleep", 'can not sleep', 'insomnia',
            'want to die', 'kill myself', 'end it all', 'suicide',
            'no hope', 'give up', 'no point',
            'hate myself', 'burden', 'alone', 'lonely',
            'depressed', 'miserable', 'suffering', 'struggling',
            'going through the motions', 'just existing',
            'no motivation', 'no energy', 'exhausted',
            'can\'t go on', 'cannot go on',
            'not enjoy', 'do not enjoy', 'don\'t enjoy',
            'used to enjoy', 'no longer enjoy',
            'pointless', 'meaningless',
        ]
        if any(p in text_lower for p in distress_phrases):
            return True
        # Regex patterns for flexible modifier handling
        distress_patterns = [
            r'\bfeel(?:ing|s)?\s+(?:so\s+|really\s+|very\s+|extremely\s+)?(?:down|low|empty|numb|sad|terrible|awful|horrible)\b',
            r'\bstruggl(?:ing|e|ed)\b',
            r'\blost\s+(?:all\s+)?interest\b',
            r'\bno\s+(?:longer\s+)?(?:enjoy|interest|motivation|energy|hope|point)\b',
        ]
        return any(re.search(p, text_lower) for p in distress_patterns)

    def _has_clear_negative_signals(self, text_lower: str, components: Dict[str, Dict[str, Any]]) -> bool:
        """Only treat as concerning if there are clear negative signals."""
        if components.get('crisis', {}).get('score', 0.0) > 0:
            return True

        # Strong lexicon evidence (any matched depression term counts)
        lexicon_data = components.get('lexicon', {})
        if lexicon_data.get('score', 0.0) >= 0.05:
            return True
        if lexicon_data.get('matched_terms', []):
            return True

        # Explicit distress phrases
        return self._text_has_distress_phrases(text_lower)
    
    def _calculate_lexicon_score(self, text: str) -> Dict[str, Any]:
        """Calculate depression score based on lexicon matching"""
        words = re.findall(r'\b\w+\b', text)
        phrases = self._extract_phrases(text)
        
        total_score = 0.0
        matched_terms = []
        category_scores = {}
        
        # Check individual words
        for word in words:
            if word in self.depression_lexicon:
                term_data = self.depression_lexicon[word]
                weight = term_data['weight']
                category = term_data['category']
                clinical_relevance = term_data['clinical_relevance']
                
                adjusted_weight = weight * clinical_relevance
                total_score += adjusted_weight
                
                matched_terms.append({
                    'term': word,
                    'weight': weight,
                    'category': category,
                    'clinical_relevance': clinical_relevance
                })
                
                if category not in category_scores:
                    category_scores[category] = 0.0
                category_scores[category] += adjusted_weight
        
        # Check phrases (2-3 word combinations)
        for phrase in phrases:
            if phrase in self.depression_lexicon:
                term_data = self.depression_lexicon[phrase]
                weight = term_data['weight']
                category = term_data['category']
                clinical_relevance = term_data['clinical_relevance']
                
                # Give phrases higher weight
                adjusted_weight = weight * clinical_relevance * 1.5
                total_score += adjusted_weight
                
                matched_terms.append({
                    'term': phrase,
                    'weight': weight,
                    'category': category,
                    'clinical_relevance': clinical_relevance,
                    'type': 'phrase'
                })
                
                if category not in category_scores:
                    category_scores[category] = 0.0
                category_scores[category] += adjusted_weight
        
        # Normalize score
        # Lexicon weights for depression indicators are negative. We only want to count
        # evidence *toward* depression risk, so convert negative totals into a positive
        # risk magnitude and ignore any positive totals.
        if words:
            depressive_magnitude = max(0.0, -total_score)
            # Use a blended normalization: average over words BUT also consider the
            # max single-term weight.  This prevents short, strongly-negative texts
            # (e.g. "nothing matters") from being diluted to near-zero.
            per_word = depressive_magnitude / len(words)
            max_term_weight = max(
                (abs(t['weight']) * t.get('clinical_relevance', 1.0)
                 for t in matched_terms),
                default=0.0
            )
            # Blend: 50% per-word average, 50% strongest-match magnitude
            normalized_score = 0.5 * per_word + 0.5 * min(1.0, max_term_weight)
        else:
            normalized_score = 0.0
        
        return {
            'score': min(1.0, normalized_score),
            'matched_terms': matched_terms,
            'category_scores': category_scores,
            'raw_score': total_score
        }
    
    def _detect_crisis_indicators(self, text: str) -> Dict[str, Any]:
        """Detect crisis intervention keywords and phrases"""
        crisis_score = 0.0
        detected_keywords = []
        immediate_intervention = False
        
        for keyword_data in self.crisis_keywords:
            keyword = keyword_data['keyword']
            pattern = r'\b' + re.escape(keyword) + r'\b'
            if re.search(pattern, text):
                if keyword_data['immediate_response']:
                    immediate_intervention = True
                    crisis_score += 1.0
                elif keyword_data['severity'] == 'critical':
                    crisis_score += 0.8
                elif keyword_data['severity'] == 'high':
                    crisis_score += 0.6
                else:
                    crisis_score += 0.4
                
                detected_keywords.append(keyword_data)
        
        return {
            'score': min(1.0, crisis_score),
            'keywords': detected_keywords,
            'immediate_intervention': immediate_intervention,
            'crisis_level': 'critical' if immediate_intervention else ('high' if crisis_score > 0.5 else 'none')
        }
    
    def _analyze_cognitive_patterns(self, text: str) -> Dict[str, Any]:
        """Analyze cognitive distortion patterns"""
        pattern_scores = {}
        total_score = 0.0
        detected_patterns = []
        
        # All-or-nothing thinking
        # Avoid over-triggering on neutral phrases like "nothing special" / "nothing much"
        all_nothing_words = re.findall(r'\b(always|never|everyone|nobody|everything|all|none)\b', text)

        nothing_matches = list(re.finditer(r'\bnothing\b', text))
        kept_nothing = 0
        for m in nothing_matches:
            after = text[m.end():m.end() + 25]
            if re.search(r'^\s+(special|much|new|different|out\s+of\s+the\s+ordinary)\b', after):
                continue
            kept_nothing += 1

        all_or_nothing_count = len(all_nothing_words) + kept_nothing
        if all_or_nothing_count:
            pattern_scores['all_or_nothing'] = all_or_nothing_count * 0.1
            detected_patterns.append('all_or_nothing_thinking')
        
        # Catastrophizing
        catastrophe_words = re.findall(r'\b(terrible|disaster|awful|horrible|catastrophe|worst|ruined)\b', text)
        if catastrophe_words:
            pattern_scores['catastrophizing'] = len(catastrophe_words) * 0.15
            detected_patterns.append('catastrophizing')
        
        # Should statements
        should_statements = re.findall(r'\b(should|must|have to|need to|supposed to|ought to)\b', text)
        if should_statements:
            pattern_scores['should_statements'] = len(should_statements) * 0.1
            detected_patterns.append('should_statements')
        
        # Personalization
        personalization = re.findall(r'\b(my fault|because of me|i caused|i\'m responsible)\b', text)
        if personalization:
            pattern_scores['personalization'] = len(personalization) * 0.2
            detected_patterns.append('personalization')
        
        # Calculate total cognitive distortion score
        total_score = sum(pattern_scores.values())
        
        return {
            'score': min(1.0, total_score),
            'patterns': detected_patterns,
            'pattern_scores': pattern_scores
        }
    
    def _analyze_linguistic_features(self, features: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze linguistic features that may indicate depression"""
        linguistic_score = 0.0
        indicators = []
        
        # High personal pronoun usage (self-focus)
        if features.get('personal_pronoun_ratio', 0) > 0.15:
            linguistic_score += 0.2
            indicators.append('high_self_focus')
        
        # Negative word ratio
        negative_ratio = features.get('negative_words', 0) / max(1, features.get('token_count', 1))
        if negative_ratio > 0.1:
            linguistic_score += negative_ratio * 2
            indicators.append('high_negative_language')
        
        # Low positive word usage
        positive_ratio = features.get('positive_words', 0) / max(1, features.get('token_count', 1))
        if positive_ratio < 0.05:
            linguistic_score += 0.1
            indicators.append('low_positive_language')
        
        # Question ratio (uncertainty, rumination)
        if features.get('question_ratio', 0) > 0.1:
            linguistic_score += 0.1
            indicators.append('excessive_questioning')
        
        return {
            'score': min(1.0, linguistic_score),
            'indicators': indicators
        }
    
    def _analyze_emotional_profile(self, features: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze emotional profile for depression indicators"""
        emotional_score = 0.0
        indicators = []
        
        # High sadness indicators
        sadness_count = features.get('sadness_indicators', 0)
        if sadness_count > 2:
            emotional_score += 0.3
            indicators.append('high_sadness_indicators')
        
        # High fear/anxiety indicators
        fear_count = features.get('fear_indicators', 0)
        if fear_count > 1:
            emotional_score += 0.2
            indicators.append('anxiety_indicators')
        
        # Low joy indicators
        joy_count = features.get('joy_indicators', 0)
        if joy_count == 0 and features.get('token_count', 0) > 20:
            emotional_score += 0.1
            indicators.append('absence_of_joy')
        
        return {
            'score': min(1.0, emotional_score),
            'indicators': indicators
        }
    
    def _calculate_weighted_score(self, components: Dict[str, Dict[str, Any]]) -> float:
        """Calculate weighted final depression score"""
        weighted_score = 0.0
        
        # Apply weights to each component
        weighted_score += components['lexicon']['score'] * self.weights['lexicon_score']
        weighted_score += components['crisis']['score'] * self.weights['crisis_keywords']
        weighted_score += components['cognitive']['score'] * self.weights['cognitive_patterns']
        weighted_score += components['linguistic']['score'] * self.weights['linguistic_features']
        weighted_score += components['emotional']['score'] * (self.weights['emotion_sadness'] + self.weights['emotion_fear'])
        
        return min(1.0, weighted_score)
    
    def _determine_risk_level(self, score: float, components: Dict[str, Dict[str, Any]]) -> Tuple[str, float]:
        """Determine risk level and confidence based on depression_score ONLY.

        SINGLE SOURCE OF TRUTH: depression_score
            score <= 0.2  -> 'positive'   (GREEN theme)
            0.2 < score <= 0.5 -> 'neutral'    (YELLOW theme)
            score > 0.5   -> 'concerning' (RED theme / crisis)

        NO overrides from crisis keywords, indicators, or any other source.
        The score already incorporates crisis keyword signals numerically.
        """
        # Determine risk level based on score ONLY — 3-tier system
        if score > 0.5:
            risk_level = 'concerning'
            confidence = 0.75 + (score - 0.5) * 0.5
        elif score > 0.2:
            risk_level = 'neutral'
            confidence = 0.60 + (score - 0.2) * 0.5
        else:
            risk_level = 'positive'
            confidence = 0.50 + score * 2.5
        
        # Adjust confidence based on component agreement
        component_scores = [
            components['lexicon']['score'],
            components['crisis']['score'],
            components['cognitive']['score']
        ]
        
        # If multiple components agree, increase confidence
        high_scores = sum(1 for s in component_scores if s > 0.5)
        if high_scores >= 2:
            confidence = min(1.0, confidence + 0.1)
        
        return risk_level, confidence
    
    def _compile_indicators(self, components: Dict[str, Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Compile all detected indicators from different components"""
        indicators = []
        
        # Lexicon indicators
        for term_data in components['lexicon']['matched_terms']:
            indicators.append({
                'type': 'lexicon',
                'indicator': term_data['term'],
                'category': term_data['category'],
                'severity': abs(term_data['weight']),
                'clinical_relevance': term_data['clinical_relevance']
            })
        
        # Crisis indicators
        for keyword_data in components['crisis']['keywords']:
            indicators.append({
                'type': 'crisis',
                'indicator': keyword_data['keyword'],
                'category': keyword_data['category'],
                'severity': keyword_data['severity'],
                'immediate_response': keyword_data['immediate_response']
            })
        
        # Cognitive pattern indicators
        for pattern in components['cognitive']['patterns']:
            indicators.append({
                'type': 'cognitive_pattern',
                'indicator': pattern,
                'category': 'cognitive_distortion'
            })
        
        # Linguistic indicators
        for indicator in components['linguistic']['indicators']:
            indicators.append({
                'type': 'linguistic',
                'indicator': indicator,
                'category': 'language_pattern'
            })
        
        return indicators
    
    def _generate_recommendations(self, risk_level: str, indicators: List[Dict[str, Any]]) -> List[str]:
        """Generate recommendations based on risk level and detected indicators"""
        recommendations = []
        
        if risk_level == 'concerning':
            recommendations.extend([
                "Immediate professional intervention is recommended",
                "Contact a mental health crisis hotline immediately",
                "Do not leave the person alone if possible",
                "Consider emergency room evaluation",
                "Remove any means of self-harm from environment"
            ])
        elif risk_level == 'neutral':
            recommendations.extend([
                "Schedule appointment with mental health professional",
                "Implement self-care strategies",
                "Increase social activities and support",
                "Monitor symptoms closely",
                "Consider counseling or therapy"
            ])
        elif risk_level == 'positive':
            recommendations.extend([
                "Continue maintaining healthy lifestyle habits",
                "Stay connected with support network",
                "Monitor mood and symptoms",
                "Consider preventive mental health resources"
            ])
        
        # Add specific recommendations based on indicators
        indicator_categories = [ind['category'] for ind in indicators]
        
        if 'self_harm' in indicator_categories:
            recommendations.append("Remove access to means of self-harm")
            recommendations.append("Implement crisis safety plan")
        
        if 'isolation' in indicator_categories:
            recommendations.append("Increase social connections and activities")
            
        if 'sleep_issues' in indicator_categories:
            recommendations.append("Address sleep hygiene and sleep disorders")
        
        if 'hopelessness' in indicator_categories:
            recommendations.append("Focus on hope-building and future-oriented therapies")
        
        return recommendations
    
    def _generate_analysis_summary(self, score: float, risk_level: str, indicators: List[Dict[str, Any]]) -> str:
        """Generate a comprehensive analysis summary"""
        summary_parts = []
        
        # Overall assessment
        summary_parts.append(f"Depression risk assessment indicates {risk_level} risk level with a score of {score:.2f}.")
        
        # Indicator summary
        if indicators:
            indicator_count = len(indicators)
            summary_parts.append(f"Analysis identified {indicator_count} depression-related indicators.")
            
            # Category breakdown
            categories = {}
            for indicator in indicators:
                category = indicator.get('category', 'other')
                categories[category] = categories.get(category, 0) + 1
            
            if categories:
                category_text = ", ".join([f"{count} {category}" for category, count in categories.items()])
                summary_parts.append(f"Indicator categories: {category_text}.")
        
        # Risk-specific summary
        if risk_level == 'concerning':
            summary_parts.append("Immediate professional intervention is strongly recommended.")
        elif risk_level == 'neutral':
            summary_parts.append("Consider scheduling a mental health consultation.")
        
        return " ".join(summary_parts)
    
    def _extract_phrases(self, text: str) -> List[str]:
        """Extract 2-3 word phrases from text"""
        words = re.findall(r'\b\w+\b', text)
        phrases = []
        
        # 2-word phrases
        for i in range(len(words) - 1):
            phrase = f"{words[i]} {words[i+1]}"
            phrases.append(phrase)
        
        # 3-word phrases
        for i in range(len(words) - 2):
            phrase = f"{words[i]} {words[i+1]} {words[i+2]}"
            phrases.append(phrase)
        
        return phrases
    
    def _create_empty_prediction(self) -> Dict[str, Any]:
        """Create empty prediction result"""
        return {
            'score': 0.0,
            'risk_level': 'minimal',
            'confidence': 0.0,
            'indicators': [],
            'components': {},
            'recommendations': [],
            'analysis_summary': "No text provided for analysis."
        }
