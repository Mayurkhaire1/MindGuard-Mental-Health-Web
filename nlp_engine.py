import re
import string
import json
import os
from collections import Counter
from typing import List, Dict, Tuple
import logging

class NLPEngine:
    """Custom NLP Engine for text preprocessing and feature extraction"""
    
    def __init__(self):
        self.stop_words = self._load_stop_words()
        self.contractions = self._load_contractions()
        self.emotion_patterns = self._load_emotion_patterns()
        self.depression_patterns = self._load_depression_patterns()
        
    def _load_stop_words(self) -> set:
        """Load common English stop words"""
        stop_words = {
            'a', 'an', 'and', 'are', 'as', 'at', 'be', 'by', 'for', 'from',
            'has', 'he', 'in', 'is', 'it', 'its', 'of', 'on', 'that', 'the',
            'to', 'was', 'were', 'will', 'with', 'the', 'this', 'but', 'they',
            'have', 'had', 'what', 'said', 'each', 'which', 'their', 'time',
            'if', 'up', 'out', 'many', 'then', 'them', 'these', 'so', 'some',
            'her', 'would', 'make', 'like', 'into', 'him', 'has', 'two', 'more',
            'very', 'after', 'words', 'long', 'than', 'first', 'been', 'call',
            'who', 'its', 'now', 'find', 'could', 'made', 'may', 'part'
        }
        return stop_words
    
    def _load_contractions(self) -> dict:
        """Load contraction mappings for expansion"""
        return {
            "aren't": "are not", "can't": "cannot", "couldn't": "could not",
            "didn't": "did not", "doesn't": "does not", "don't": "do not",
            "hadn't": "had not", "hasn't": "has not", "haven't": "have not",
            "he'd": "he would", "he'll": "he will", "he's": "he is",
            "i'd": "i would", "i'll": "i will", "i'm": "i am", "i've": "i have",
            "isn't": "is not", "it'd": "it would", "it'll": "it will",
            "it's": "it is", "let's": "let us", "mustn't": "must not",
            "shan't": "shall not", "she'd": "she would", "she'll": "she will",
            "she's": "she is", "shouldn't": "should not", "that's": "that is",
            "there's": "there is", "they'd": "they would", "they'll": "they will",
            "they're": "they are", "they've": "they have", "we'd": "we would",
            "we're": "we are", "we've": "we have", "weren't": "were not",
            "what's": "what is", "where's": "where is", "who's": "who is",
            "won't": "will not", "wouldn't": "would not", "you'd": "you would",
            "you'll": "you will", "you're": "you are", "you've": "you have"
        }
    
    def _load_emotion_patterns(self) -> dict:
        """Load regex patterns for emotion detection"""
        return {
            'sadness': [
                r'\b(sad|depressed|down|blue|melancholy|gloomy|sorrowful)\b',
                r'\b(crying|tears|weeping|sobbing)\b',
                r'\b(grief|mourning|heartbroken|devastated)\b'
            ],
            'anger': [
                r'\b(angry|mad|furious|rage|irritated|annoyed)\b',
                r'\b(hate|hatred|despise|loathe)\b',
                r'\b(frustrated|aggravated|livid|enraged)\b'
            ],
            'fear': [
                r'\b(afraid|scared|terrified|frightened|anxious)\b',
                r'\b(worry|worried|nervous|panic|dread)\b',
                r'\b(phobia|terror|horror|apprehensive)\b'
            ],
            'joy': [
                r'\b(happy|joyful|cheerful|glad|pleased|delighted)\b',
                r'\b(excited|thrilled|elated|euphoric)\b',
                r'\b(love|loving|adore|wonderful|amazing)\b'
            ],
            'disgust': [
                r'\b(disgusting|revolting|nauseating|repulsive)\b',
                r'\b(gross|sick|vomit|repugnant)\b'
            ],
            'surprise': [
                r'\b(surprised|amazed|astonished|shocked|stunned)\b',
                r'\b(unexpected|sudden|startled)\b'
            ]
        }
    
    def _load_depression_patterns(self) -> dict:
        """Load patterns indicating depression symptoms"""
        return {
            'hopelessness': [
                r'\b(hopeless|pointless|meaningless|worthless)\b',
                r'\b(no point|give up|what\'s the use)\b',
                r'\b(nothing matters|don\'t care anymore)\b'
            ],
            'fatigue': [
                r'\b(tired|exhausted|drained|fatigued|weary)\b',
                r'\b(no energy|can\'t move|too tired)\b'
            ],
            'isolation': [
                r'\b(alone|lonely|isolated|abandoned)\b',
                r'\b(no friends|nobody cares|by myself)\b'
            ],
            'self_harm': [
                r'\b(hurt myself|self harm|cut myself|want to die)\b',
                r'\b(suicide|kill myself|end it all|not worth living)\b',
                r'\b(better off dead|wish I was dead)\b'
            ],
            'worthlessness': [
                r'\b(worthless|useless|pathetic|failure|loser)\b',
                r'\b(not good enough|hate myself|disgusted with myself)\b'
            ],
            'sleep_issues': [
                r'\b(can\'t sleep|insomnia|sleep problems|tossing and turning)\b',
                r'\b(sleep too much|always tired|restless sleep)\b'
            ]
        }
    
    def preprocess_text(self, text: str) -> str:
        """Comprehensive text preprocessing"""
        if not text:
            return ""
        
        # Convert to lowercase
        text = text.lower()
        
        # Expand contractions
        for contraction, expansion in self.contractions.items():
            text = text.replace(contraction, expansion)
        
        # Remove URLs
        text = re.sub(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', '', text)
        
        # Remove email addresses
        text = re.sub(r'\S+@\S+', '', text)
        
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text)
        
        # Remove leading/trailing whitespace
        text = text.strip()
        
        return text
    
    def tokenize(self, text: str) -> List[str]:
        """Advanced tokenization with punctuation handling"""
        if not text:
            return []
        
        # Split on whitespace and punctuation, but preserve emotionally significant punctuation
        tokens = re.findall(r'\b\w+\b|[!?]+', text)
        
        # Filter out stop words but keep emotional indicators
        filtered_tokens = []
        for token in tokens:
            if token not in self.stop_words or len(token) <= 2:
                filtered_tokens.append(token)
        
        return filtered_tokens
    
    def split_sentences(self, text: str) -> List[str]:
        """Split text into sentences"""
        # Simple sentence splitting on periods, exclamation marks, and question marks
        sentences = re.split(r'[.!?]+', text)
        return [s.strip() for s in sentences if s.strip()]
    
    def extract_features(self, tokens: List[str]) -> Dict:
        """Extract comprehensive linguistic features"""
        if not tokens:
            return {}
        
        features = {}
        
        # Basic statistics
        features['token_count'] = len(tokens)
        features['unique_tokens'] = len(set(tokens))
        features['avg_word_length'] = sum(len(token) for token in tokens) / len(tokens)
        
        # Punctuation analysis
        exclamation_count = sum(1 for token in tokens if '!' in token)
        question_count = sum(1 for token in tokens if '?' in token)
        features['exclamation_ratio'] = exclamation_count / len(tokens)
        features['question_ratio'] = question_count / len(tokens)
        
        # Emotional intensity indicators
        features['caps_ratio'] = sum(1 for token in tokens if token.isupper()) / len(tokens)
        features['repeated_chars'] = sum(1 for token in tokens if re.search(r'(.)\1{2,}', token)) / len(tokens)
        
        # Pattern matching for emotions and depression indicators
        text_lower = ' '.join(tokens).lower()
        
        # Count emotion patterns
        for emotion, patterns in self.emotion_patterns.items():
            count = 0
            for pattern in patterns:
                count += len(re.findall(pattern, text_lower))
            features[f'{emotion}_indicators'] = count
        
        # Count depression patterns
        for category, patterns in self.depression_patterns.items():
            count = 0
            for pattern in patterns:
                count += len(re.findall(pattern, text_lower))
            features[f'depression_{category}'] = count
        
        # Calculate positive/negative word counts (simplified sentiment)
        positive_words = {'good', 'great', 'wonderful', 'amazing', 'excellent', 'fantastic', 
                         'love', 'happy', 'joy', 'beautiful', 'perfect', 'best', 'awesome'}
        negative_words = {'bad', 'terrible', 'awful', 'horrible', 'hate', 'worst', 'disgusting',
                         'sad', 'angry', 'depressed', 'disappointed', 'frustrated', 'annoying'}
        
        features['positive_words'] = sum(1 for token in tokens if token.lower() in positive_words)
        features['negative_words'] = sum(1 for token in tokens if token.lower() in negative_words)
        
        # Personal pronoun usage (can indicate self-focus in depression)
        personal_pronouns = {'i', 'me', 'my', 'myself', 'mine'}
        features['personal_pronoun_ratio'] = sum(1 for token in tokens if token.lower() in personal_pronouns) / len(tokens)
        
        return features
    
    def calculate_readability(self, text: str) -> Dict[str, float]:
        """Calculate text readability metrics"""
        sentences = self.split_sentences(text)
        words = self.tokenize(text)
        
        if not sentences or not words:
            return {'flesch_score': 0, 'complexity': 0}
        
        # Simplified Flesch Reading Ease approximation
        avg_sentence_length = len(words) / len(sentences)
        avg_syllables = sum(self._count_syllables(word) for word in words) / len(words)
        
        flesch_score = 206.835 - (1.015 * avg_sentence_length) - (84.6 * avg_syllables)
        complexity = avg_sentence_length + avg_syllables
        
        return {
            'flesch_score': max(0, min(100, flesch_score)),
            'complexity': complexity,
            'avg_sentence_length': avg_sentence_length,
            'avg_syllables': avg_syllables
        }
    
    def _count_syllables(self, word: str) -> int:
        """Estimate syllable count in a word"""
        word = word.lower()
        if len(word) <= 3:
            return 1
        
        vowels = 'aeiouy'
        syllables = 0
        prev_was_vowel = False
        
        for i, char in enumerate(word):
            if char in vowels:
                if not prev_was_vowel:
                    syllables += 1
                prev_was_vowel = True
            else:
                prev_was_vowel = False
        
        # Adjust for silent 'e'
        if word.endswith('e'):
            syllables -= 1
        
        return max(1, syllables)
    
    def extract_ngrams(self, tokens: List[str], n: int = 2) -> List[str]:
        """Extract n-grams from tokens"""
        if len(tokens) < n:
            return []
        
        ngrams = []
        for i in range(len(tokens) - n + 1):
            ngram = ' '.join(tokens[i:i+n])
            ngrams.append(ngram)
        
        return ngrams
    
    def get_word_frequency(self, tokens: List[str]) -> Dict[str, int]:
        """Get word frequency distribution"""
        return dict(Counter(tokens))
