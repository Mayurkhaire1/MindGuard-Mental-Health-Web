"""
Voice Analysis Module for MindGuard
Simulates voice pattern analysis through questionnaire data
"""

import logging
from typing import Dict, Any

class VoiceAnalyzer:
    """Analyzes simulated voice patterns from questionnaire responses"""
    
    def __init__(self):
        # Clinical scoring weights based on depression research
        self.pace_weights = {
            'much_slower': 0.9,    # Highly indicative of depression
            'slower': 0.7,         # Moderately indicative 
            'normal': 0.0,         # Baseline
            'faster': 0.3,         # Mild anxiety indicator
            'much_faster': 0.6     # Anxiety/mania indicator
        }
        
        self.volume_weights = {
            'much_quieter': 0.8,   # Depression indicator
            'quieter': 0.5,        # Mild depression
            'normal': 0.0,         # Baseline
            'louder': 0.2,         # Mild indicator
            'much_louder': 0.4     # Possible mania
        }
        
        self.frequency_weights = {
            'never': 0.0,
            'rarely': 0.2,
            'sometimes': 0.5,
            'often': 0.7,
            'always': 1.0
        }
        
        self.clarity_weights = {
            'very_clear': 0.0,
            'clear': 0.1,
            'unclear': 0.6,
            'very_unclear': 0.8,
            'mumbling': 0.9
        }
    
    def analyze_voice_patterns(self, voice_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analyze voice patterns from questionnaire responses
        
        Args:
            voice_data: Dictionary containing voice questionnaire responses
            
        Returns:
            Dictionary with analysis results and scores
        """
        try:
            # Calculate individual component scores
            pace_score = self.pace_weights.get(voice_data.get('speaking_pace_change', 'normal'), 0.0)
            volume_score = self.volume_weights.get(voice_data.get('voice_volume_change', 'normal'), 0.0)
            hesitation_score = self.frequency_weights.get(voice_data.get('speech_hesitation', 'never'), 0.0)
            trembling_score = self.frequency_weights.get(voice_data.get('voice_trembling', 'never'), 0.0)
            clarity_score = self.clarity_weights.get(voice_data.get('speech_clarity', 'very_clear'), 0.0)
            
            # Calculate composite scores
            voice_stress_score = (hesitation_score + trembling_score + clarity_score) / 3.0
            speech_pattern_score = (pace_score + volume_score + clarity_score) / 3.0
            
            # Overall voice analysis score (0.0 = healthy, 1.0 = concerning)
            overall_score = (voice_stress_score + speech_pattern_score) / 2.0
            
            # Determine risk level
            risk_level = self._determine_voice_risk_level(overall_score)
            
            # Generate insights
            insights = self._generate_voice_insights(voice_data, overall_score)
            
            return {
                'voice_stress_score': round(voice_stress_score, 3),
                'speech_pattern_score': round(speech_pattern_score, 3),
                'overall_score': round(overall_score, 3),
                'risk_level': risk_level,
                'insights': insights,
                'component_scores': {
                    'pace': pace_score,
                    'volume': volume_score,
                    'hesitation': hesitation_score,
                    'trembling': trembling_score,
                    'clarity': clarity_score
                }
            }
            
        except Exception as e:
            logging.error(f"Error in voice pattern analysis: {str(e)}")
            return {
                'voice_stress_score': 0.0,
                'speech_pattern_score': 0.0,
                'overall_score': 0.0,
                'risk_level': 'unknown',
                'insights': ['Error occurred during voice analysis'],
                'component_scores': {}
            }
    
    def _determine_voice_risk_level(self, score: float) -> str:
        """Determine risk level based on voice analysis score"""
        if score >= 0.8:
            return 'high'
        elif score >= 0.6:
            return 'moderate'
        elif score >= 0.3:
            return 'mild'
        else:
            return 'minimal'
    
    def _generate_voice_insights(self, voice_data: Dict[str, Any], overall_score: float) -> list:
        """Generate human-readable insights from voice analysis"""
        insights = []
        
        # Speaking pace insights
        pace = voice_data.get('speaking_pace_change', 'normal')
        if pace in ['much_slower', 'slower']:
            insights.append("Slower speaking pace may indicate low energy or depressed mood")
        elif pace in ['much_faster', 'faster']:
            insights.append("Faster speaking pace could suggest anxiety or elevated mood")
        
        # Voice volume insights
        volume = voice_data.get('voice_volume_change', 'normal')
        if volume in ['much_quieter', 'quieter']:
            insights.append("Quieter voice volume may reflect low confidence or withdrawal")
        
        # Speech quality insights
        hesitation = voice_data.get('speech_hesitation', 'never')
        if hesitation in ['often', 'always']:
            insights.append("Frequent speech hesitation may indicate anxiety or uncertainty")
        
        trembling = voice_data.get('voice_trembling', 'never')
        if trembling in ['often', 'always']:
            insights.append("Voice trembling could suggest high stress or anxiety levels")
        
        clarity = voice_data.get('speech_clarity', 'very_clear')
        if clarity in ['unclear', 'very_unclear', 'mumbling']:
            insights.append("Unclear speech may indicate fatigue or concentration difficulties")
        
        # Overall assessment
        if overall_score >= 0.7:
            insights.append("Voice patterns suggest significant stress or mood changes")
        elif overall_score >= 0.4:
            insights.append("Voice patterns show some indicators of stress or mood changes")
        else:
            insights.append("Voice patterns appear within normal range")
        
        return insights if insights else ["Voice patterns analyzed - no specific concerns identified"]
    
    def get_voice_recommendations(self, analysis_result: Dict[str, Any]) -> list:
        """Get recommendations based on voice analysis results"""
        recommendations = []
        
        risk_level = analysis_result.get('risk_level', 'minimal')
        overall_score = analysis_result.get('overall_score', 0.0)
        
        if risk_level in ['high', 'moderate']:
            recommendations.extend([
                "Consider speaking with a mental health professional about your recent experiences",
                "Practice relaxation techniques like deep breathing before speaking",
                "Try vocal warm-up exercises to reduce speech tension"
            ])
        
        if overall_score >= 0.5:
            recommendations.extend([
                "Monitor your voice patterns over the next few days",
                "Consider keeping a daily mood and voice journal",
                "Ensure you're getting adequate rest and hydration"
            ])
        
        # Component-specific recommendations
        component_scores = analysis_result.get('component_scores', {})
        if component_scores.get('hesitation', 0) >= 0.6:
            recommendations.append("Practice mindfulness to reduce speech anxiety")
        
        if component_scores.get('clarity', 0) >= 0.6:
            recommendations.append("Ensure adequate rest - fatigue can affect speech clarity")
        
        return recommendations if recommendations else ["Voice patterns appear healthy - continue current wellness practices"]