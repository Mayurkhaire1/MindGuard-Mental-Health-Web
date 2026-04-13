"""
Facial Expression Analysis Module for MindGuard
Simulates facial expression analysis through questionnaire data
"""

import logging
from typing import Dict, Any

class FacialAnalyzer:
    """Analyzes simulated facial expressions from questionnaire responses"""
    
    def __init__(self):
        # Clinical scoring weights based on facial expression research
        self.frequency_weights = {
            'never': 1.0,      # Concerning when reversed (never smiling)
            'rarely': 0.8,     # Mild concern
            'sometimes': 0.4,  # Moderate
            'often': 0.2,      # Good
            'always': 0.0      # Excellent
        }
        
        self.comfort_weights = {
            'very_comfortable': 0.0,
            'comfortable': 0.1,
            'uncomfortable': 0.6,
            'very_uncomfortable': 0.9
        }
        
        self.tension_weights = {
            'relaxed': 0.0,
            'slightly_tense': 0.3,
            'tense': 0.7,
            'very_tense': 1.0
        }
        
        self.control_weights = {
            'easy': 0.0,
            'normal': 0.2,
            'difficult': 0.7,
            'very_difficult': 1.0
        }
        
        self.tiredness_weights = {
            'never': 0.0,
            'rarely': 0.2,
            'sometimes': 0.5,
            'often': 0.8,
            'always': 1.0
        }
    
    def analyze_facial_expressions(self, facial_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analyze facial expressions from questionnaire responses
        
        Args:
            facial_data: Dictionary containing facial expression questionnaire responses
            
        Returns:
            Dictionary with analysis results and scores
        """
        try:
            # Calculate individual component scores
            smile_score = self.frequency_weights.get(facial_data.get('smile_frequency', 'often'), 0.0)
            tiredness_score = self.tiredness_weights.get(facial_data.get('facial_tiredness', 'never'), 0.0)
            eye_contact_score = self.comfort_weights.get(facial_data.get('eye_contact_comfort', 'comfortable'), 0.0)
            tension_score = self.tension_weights.get(facial_data.get('facial_tension', 'relaxed'), 0.0)
            control_score = self.control_weights.get(facial_data.get('expression_control', 'easy'), 0.0)
            
            # Calculate composite scores
            facial_emotion_score = (smile_score + eye_contact_score + control_score) / 3.0
            expression_wellness_score = (tiredness_score + tension_score + control_score) / 3.0
            
            # Overall facial expression score (0.0 = healthy, 1.0 = concerning)
            overall_score = (facial_emotion_score + expression_wellness_score) / 2.0
            
            # Determine risk level
            risk_level = self._determine_facial_risk_level(overall_score)
            
            # Generate insights
            insights = self._generate_facial_insights(facial_data, overall_score)
            
            return {
                'facial_emotion_score': round(facial_emotion_score, 3),
                'expression_wellness_score': round(expression_wellness_score, 3),
                'overall_score': round(overall_score, 3),
                'risk_level': risk_level,
                'insights': insights,
                'component_scores': {
                    'smile_frequency': smile_score,
                    'facial_tiredness': tiredness_score,
                    'eye_contact': eye_contact_score,
                    'tension': tension_score,
                    'control': control_score
                }
            }
            
        except Exception as e:
            logging.error(f"Error in facial expression analysis: {str(e)}")
            return {
                'facial_emotion_score': 0.0,
                'expression_wellness_score': 0.0,
                'overall_score': 0.0,
                'risk_level': 'unknown',
                'insights': ['Error occurred during facial expression analysis'],
                'component_scores': {}
            }
    
    def _determine_facial_risk_level(self, score: float) -> str:
        """Determine risk level based on facial expression analysis score"""
        if score >= 0.8:
            return 'high'
        elif score >= 0.6:
            return 'moderate'
        elif score >= 0.3:
            return 'mild'
        else:
            return 'minimal'
    
    def _generate_facial_insights(self, facial_data: Dict[str, Any], overall_score: float) -> list:
        """Generate human-readable insights from facial expression analysis"""
        insights = []
        
        # Smile frequency insights
        smile_freq = facial_data.get('smile_frequency', 'often')
        if smile_freq in ['never', 'rarely']:
            insights.append("Reduced smiling frequency may indicate low mood or social withdrawal")
        elif smile_freq == 'always':
            insights.append("Frequent smiling is a positive indicator of emotional well-being")
        
        # Facial tiredness insights
        tiredness = facial_data.get('facial_tiredness', 'never')
        if tiredness in ['often', 'always']:
            insights.append("Facial tiredness may suggest fatigue, stress, or sleep issues")
        
        # Eye contact insights
        eye_contact = facial_data.get('eye_contact_comfort', 'comfortable')
        if eye_contact in ['uncomfortable', 'very_uncomfortable']:
            insights.append("Difficulty with eye contact may indicate social anxiety or low confidence")
        
        # Facial tension insights
        tension = facial_data.get('facial_tension', 'relaxed')
        if tension in ['tense', 'very_tense']:
            insights.append("Facial tension could suggest ongoing stress or anxiety")
        
        # Expression control insights
        control = facial_data.get('expression_control', 'easy')
        if control in ['difficult', 'very_difficult']:
            insights.append("Difficulty controlling expressions may indicate emotional dysregulation")
        
        # Overall assessment
        if overall_score >= 0.7:
            insights.append("Facial expression patterns suggest significant emotional distress")
        elif overall_score >= 0.4:
            insights.append("Facial expression patterns show some indicators of stress or mood changes")
        else:
            insights.append("Facial expression patterns appear within healthy range")
        
        return insights if insights else ["Facial expression patterns analyzed - no specific concerns identified"]
    
    def get_facial_recommendations(self, analysis_result: Dict[str, Any]) -> list:
        """Get recommendations based on facial expression analysis results"""
        recommendations = []
        
        risk_level = analysis_result.get('risk_level', 'minimal')
        overall_score = analysis_result.get('overall_score', 0.0)
        
        if risk_level in ['high', 'moderate']:
            recommendations.extend([
                "Consider discussing emotional well-being with a mental health professional",
                "Practice facial relaxation exercises and gentle massage",
                "Try mirror work to become more aware of your expressions"
            ])
        
        if overall_score >= 0.5:
            recommendations.extend([
                "Monitor your facial expressions and emotional state daily",
                "Practice smiling exercises to improve mood naturally",
                "Ensure adequate sleep and stress management"
            ])
        
        # Component-specific recommendations
        component_scores = analysis_result.get('component_scores', {})
        if component_scores.get('smile_frequency', 0) >= 0.6:
            recommendations.append("Try to consciously smile more - it can help improve mood")
        
        if component_scores.get('tension', 0) >= 0.6:
            recommendations.append("Practice progressive muscle relaxation for facial tension")
        
        if component_scores.get('eye_contact', 0) >= 0.6:
            recommendations.append("Gradually practice comfortable eye contact in safe environments")
        
        return recommendations if recommendations else ["Facial expression patterns appear healthy - continue current wellness practices"]