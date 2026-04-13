import json
import os
import re
from typing import Dict, List, Tuple
import logging

class EmotionDetector:
    """Custom emotion detection system using lexicon-based and pattern-based approaches"""
    
    def __init__(self):
        self.emotion_lexicon = self._load_emotion_lexicon()
        self.emotion_patterns = self._initialize_emotion_patterns()
        self.intensity_modifiers = self._load_intensity_modifiers()
        self.negation_words = {'not', 'no', 'never', 'nothing', 'nobody', 'nowhere', 
                              'neither', 'nor', 'hardly', 'barely', 'scarcely'}
        
    def _load_emotion_lexicon(self) -> Dict[str, Dict[str, float]]:
        """Load emotion lexicon from database or create default"""
        lexicon = {}
        
        try:
            # Try to load from database (delayed import to avoid circular dependency)
            from app import db
            from models import EmotionLexicon
            emotion_words = EmotionLexicon.query.all()
            
            for word_entry in emotion_words:
                word = word_entry.word.lower()
                emotion = word_entry.emotion
                intensity = word_entry.intensity
                
                if word not in lexicon:
                    lexicon[word] = {}
                lexicon[word][emotion] = intensity
                
        except Exception as e:
            logging.warning(f"Could not load emotion lexicon from database: {e}")
            # Use default lexicon
            lexicon = self._create_default_lexicon()
        
        if not lexicon:
            lexicon = self._create_default_lexicon()
            
        return lexicon
    
    def _create_default_lexicon(self) -> Dict[str, Dict[str, float]]:
        """Create a comprehensive default emotion lexicon"""
        lexicon = {}
        
        # Joy/Happiness words
        joy_words = {
            'happy': 0.8, 'joy': 0.9, 'joyful': 0.8, 'cheerful': 0.7, 'glad': 0.6,
            'pleased': 0.6, 'delighted': 0.8, 'excited': 0.7, 'thrilled': 0.9,
            'elated': 0.9, 'euphoric': 1.0, 'ecstatic': 1.0, 'wonderful': 0.8,
            'amazing': 0.8, 'fantastic': 0.8, 'great': 0.7, 'excellent': 0.7,
            'perfect': 0.8, 'beautiful': 0.7, 'love': 0.9, 'adore': 0.8,
            'blissful': 0.9, 'content': 0.6, 'satisfied': 0.6, 'peaceful': 0.6
        }
        
        # Sadness words
        sadness_words = {
            'sad': 0.8, 'sadness': 0.8, 'depressed': 0.9, 'depression': 0.9,
            'down': 0.7, 'blue': 0.6, 'melancholy': 0.8, 'gloomy': 0.7,
            'sorrowful': 0.8, 'grief': 0.9, 'mourning': 0.8, 'heartbroken': 0.9,
            'devastated': 0.9, 'crying': 0.7, 'tears': 0.6, 'weeping': 0.8,
            'sobbing': 0.8, 'miserable': 0.9, 'hopeless': 0.9, 'despair': 1.0,
            'anguish': 0.9, 'suffering': 0.8, 'pain': 0.7, 'hurt': 0.7,
            'lonely': 0.8, 'isolated': 0.8, 'abandoned': 0.8, 'worthless': 0.9
        }
        
        # Anger words
        anger_words = {
            'angry': 0.8, 'anger': 0.8, 'mad': 0.7, 'furious': 0.9, 'rage': 1.0,
            'irritated': 0.6, 'annoyed': 0.5, 'frustrated': 0.7, 'aggravated': 0.7,
            'livid': 0.9, 'enraged': 0.9, 'hate': 0.9, 'hatred': 0.9,
            'despise': 0.8, 'loathe': 0.8, 'detest': 0.8, 'abhor': 0.8,
            'hostile': 0.8, 'resentful': 0.7, 'bitter': 0.7, 'outraged': 0.9,
            'indignant': 0.7, 'wrathful': 0.9, 'incensed': 0.8
        }
        
        # Fear words
        fear_words = {
            'afraid': 0.7, 'scared': 0.7, 'fear': 0.8, 'terrified': 0.9,
            'frightened': 0.8, 'anxious': 0.7, 'anxiety': 0.7, 'worry': 0.6,
            'worried': 0.6, 'nervous': 0.6, 'panic': 0.9, 'panicked': 0.9,
            'dread': 0.8, 'terror': 1.0, 'horror': 0.9, 'apprehensive': 0.6,
            'uneasy': 0.5, 'disturbed': 0.6, 'alarmed': 0.7, 'startled': 0.6,
            'shocked': 0.7, 'overwhelmed': 0.7, 'threatened': 0.7, 'vulnerable': 0.6
        }
        
        # Disgust words
        disgust_words = {
            'disgusting': 0.8, 'disgust': 0.8, 'revolting': 0.9, 'nauseating': 0.8,
            'repulsive': 0.8, 'gross': 0.7, 'sick': 0.6, 'vomit': 0.7,
            'repugnant': 0.8, 'abhorrent': 0.8, 'loathsome': 0.8, 'vile': 0.8,
            'offensive': 0.6, 'distasteful': 0.6, 'unpleasant': 0.5, 'awful': 0.7
        }
        
        # Surprise words
        surprise_words = {
            'surprised': 0.7, 'surprise': 0.7, 'amazed': 0.8, 'astonished': 0.8,
            'shocked': 0.8, 'stunned': 0.8, 'bewildered': 0.7, 'confused': 0.6,
            'unexpected': 0.6, 'sudden': 0.5, 'startled': 0.7, 'baffled': 0.6,
            'perplexed': 0.6, 'mystified': 0.6, 'flabbergasted': 0.9
        }
        
        # Build the lexicon
        emotion_mappings = {
            'joy': joy_words,
            'sadness': sadness_words,
            'anger': anger_words,
            'fear': fear_words,
            'disgust': disgust_words,
            'surprise': surprise_words
        }
        
        for emotion, words in emotion_mappings.items():
            for word, intensity in words.items():
                if word not in lexicon:
                    lexicon[word] = {}
                lexicon[word][emotion] = intensity
        
        return lexicon
    
    def _initialize_emotion_patterns(self) -> Dict[str, List[str]]:
        """Initialize regex patterns for emotion detection"""
        return {
            'joy': [
                r'\b(so happy|really happy|very happy|extremely happy)\b',
                r'\b(feel great|feeling great|felt great)\b',
                r'\b(love it|love this|love that)\b',
                r'\b(best day|amazing day|wonderful day)\b',
                r'[!]{2,}',  # Multiple exclamation marks often indicate excitement
            ],
            'sadness': [
                r'\b(feel sad|feeling sad|felt sad)\b',
                r'\b(so sad|really sad|very sad|extremely sad)\b',
                r'\b(want to cry|going to cry|started crying)\b',
                r'\b(worst day|terrible day|awful day)\b',
                r'\b(can\'t take|can\'t handle|too much)\b',
            ],
            'anger': [
                r'\b(so angry|really angry|very angry|extremely angry)\b',
                r'\b(pissed off|ticked off|fed up)\b',
                r'\b(makes me mad|making me angry)\b',
                r'\b(hate this|hate that|hate it)\b',
                r'[A-Z]{3,}',  # ALL CAPS often indicates anger
            ],
            'fear': [
                r'\b(so scared|really scared|very scared|terrified)\b',
                r'\b(afraid of|scared of|fear of)\b',
                r'\b(panic attack|having panic|panicking)\b',
                r'\b(what if|worried about|anxiety about)\b',
            ],
            'disgust': [
                r'\b(so gross|really gross|very gross|disgusting)\b',
                r'\b(makes me sick|feel sick|feeling sick)\b',
                r'\b(can\'t stand|cannot stand)\b',
            ],
            'surprise': [
                r'\b(so surprised|really surprised|very surprised)\b',
                r'\b(can\'t believe|cannot believe|hard to believe)\b',
                r'\b(what the|what is|how is)\b',
                r'\b(never expected|didn\'t expect)\b',
            ]
        }
    
    def _load_intensity_modifiers(self) -> Dict[str, float]:
        """Load words that modify emotional intensity"""
        return {
            # Intensifiers
            'very': 1.3, 'really': 1.3, 'extremely': 1.5, 'incredibly': 1.4,
            'absolutely': 1.4, 'completely': 1.3, 'totally': 1.3, 'utterly': 1.4,
            'quite': 1.2, 'rather': 1.2, 'pretty': 1.1, 'fairly': 1.1,
            'super': 1.3, 'mega': 1.4, 'ultra': 1.4, 'so': 1.2,
            
            # Diminishers
            'slightly': 0.7, 'somewhat': 0.8, 'a bit': 0.7, 'a little': 0.7,
            'kind of': 0.8, 'sort of': 0.8, 'barely': 0.5, 'hardly': 0.5,
            'scarcely': 0.5, 'mildly': 0.7, 'moderately': 0.8
        }
    
    def detect_emotions(self, text: str) -> Dict[str, float]:
        """
        Detect emotions in text using lexicon-based approach with context analysis
        Returns emotion scores normalized between 0 and 1
        """
        if not text:
            return {emotion: 0.0 for emotion in ['joy', 'sadness', 'anger', 'fear', 'disgust', 'surprise']}
        
        text = text.lower()
        words = re.findall(r'\b\w+\b', text)
        
        # Initialize emotion scores
        emotion_scores = {emotion: 0.0 for emotion in ['joy', 'sadness', 'anger', 'fear', 'disgust', 'surprise']}
        
        # Track context for negation and intensity
        for i, word in enumerate(words):
            if word in self.emotion_lexicon:
                # Check for negation in the previous 2 words
                negated = False
                intensity_modifier = 1.0
                
                # Look for negation
                for j in range(max(0, i-2), i):
                    if words[j] in self.negation_words:
                        negated = True
                        break
                
                # Look for intensity modifiers
                for j in range(max(0, i-2), i):
                    if words[j] in self.intensity_modifiers:
                        intensity_modifier = self.intensity_modifiers[words[j]]
                        break
                
                # Add emotion scores
                for emotion, base_score in self.emotion_lexicon[word].items():
                    adjusted_score = base_score * intensity_modifier
                    
                    if negated:
                        # Negation can flip certain emotions or reduce intensity
                        if emotion in ['joy', 'surprise']:
                            adjusted_score *= 0.2  # Significantly reduce positive emotions
                        elif emotion in ['sadness', 'anger', 'fear', 'disgust']:
                            adjusted_score *= 0.3  # Moderately reduce negative emotions
                    
                    emotion_scores[emotion] += adjusted_score
        
        # Apply pattern-based detection
        pattern_scores = self._detect_emotion_patterns(text)
        for emotion, pattern_score in pattern_scores.items():
            emotion_scores[emotion] += pattern_score
        
        # Normalize scores
        if words:
            max_possible_score = len(words) * 2  # Rough normalization factor
            for emotion in emotion_scores:
                emotion_scores[emotion] = min(1.0, emotion_scores[emotion] / max_possible_score)
        
        return emotion_scores
    
    def _detect_emotion_patterns(self, text: str) -> Dict[str, float]:
        """Detect emotions using regex patterns"""
        pattern_scores = {emotion: 0.0 for emotion in ['joy', 'sadness', 'anger', 'fear', 'disgust', 'surprise']}
        
        for emotion, patterns in self.emotion_patterns.items():
            for pattern in patterns:
                matches = re.findall(pattern, text, re.IGNORECASE)
                pattern_scores[emotion] += len(matches) * 0.3  # Each pattern match adds 0.3
        
        return pattern_scores
    
    def get_dominant_emotion(self, emotion_scores: Dict[str, float]) -> Tuple[str, float]:
        """Get the dominant emotion and its score"""
        if not emotion_scores:
            return 'neutral', 0.0
        
        dominant_emotion = max(emotion_scores.items(), key=lambda x: x[1])
        
        # If the highest score is very low, consider it neutral
        if dominant_emotion[1] < 0.1:
            return 'neutral', dominant_emotion[1]
        
        return dominant_emotion
    
    def analyze_emotional_progression(self, texts: List[str]) -> Dict[str, List[float]]:
        """Analyze emotional progression across multiple texts"""
        progression = {emotion: [] for emotion in ['joy', 'sadness', 'anger', 'fear', 'disgust', 'surprise']}
        
        for text in texts:
            emotions = self.detect_emotions(text)
            for emotion, score in emotions.items():
                progression[emotion].append(score)
        
        return progression
    
    def get_emotion_summary(self, emotion_scores: Dict[str, float]) -> Dict[str, str]:
        """Generate a human-readable emotion summary"""
        dominant_emotion, max_score = self.get_dominant_emotion(emotion_scores)
        
        # Calculate overall emotional intensity
        total_intensity = sum(emotion_scores.values())
        
        # Determine intensity level
        if total_intensity < 0.2:
            intensity_level = "low"
        elif total_intensity < 0.5:
            intensity_level = "moderate"
        elif total_intensity < 0.8:
            intensity_level = "high"
        else:
            intensity_level = "very high"
        
        # Create summary
        summary = {
            'dominant_emotion': dominant_emotion,
            'intensity_level': intensity_level,
            'emotional_complexity': len([score for score in emotion_scores.values() if score > 0.1]),
            'description': self._generate_emotion_description(dominant_emotion, max_score, total_intensity)
        }
        
        return summary
    
    def _generate_emotion_description(self, dominant_emotion: str, max_score: float, total_intensity: float) -> str:
        """Generate a descriptive text about the emotional state"""
        if dominant_emotion == 'neutral' or max_score < 0.1:
            return "The text shows neutral emotional tone with minimal emotional indicators."
        
        emotion_descriptions = {
            'joy': "positive and uplifting emotional state",
            'sadness': "melancholic and sorrowful emotional state",
            'anger': "frustrated and hostile emotional state",
            'fear': "anxious and apprehensive emotional state",
            'disgust': "disgusted and repulsed emotional state",
            'surprise': "surprised and astonished emotional state"
        }
        
        base_description = emotion_descriptions.get(dominant_emotion, "mixed emotional state")
        
        if max_score > 0.7:
            intensity_word = "strongly"
        elif max_score > 0.4:
            intensity_word = "moderately"
        else:
            intensity_word = "mildly"
        
        if total_intensity > 0.6:
            complexity_note = " with significant emotional complexity"
        elif total_intensity > 0.3:
            complexity_note = " with some emotional variety"
        else:
            complexity_note = ""
        
        return f"The text indicates a {intensity_word} {base_description}{complexity_note}."
