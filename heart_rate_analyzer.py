"""
Heart Rate and Physical Symptom Analysis Module for MindGuard
Simulates cardiovascular analysis through questionnaire data
"""

import logging
from typing import Dict, Any

class HeartRateAnalyzer:
    """Analyzes simulated heart rate and physical symptoms from questionnaire responses"""
    
    def __init__(self):
        # Clinical scoring weights based on cardiovascular and anxiety research
        self.frequency_weights = {
            'never': 0.0,
            'rarely': 0.2,
            'sometimes': 0.5,
            'often': 0.8,
            'always': 1.0
        }
        
        self.anxiety_weights = {
            'none': 0.0,
            'mild': 0.2,
            'moderate': 0.5,
            'severe': 0.8,
            'extreme': 1.0
        }
        
        # Normal heart rate ranges by age (simplified)
        self.normal_hr_ranges = {
            'young_adult': (60, 85),   # 18-30
            'adult': (60, 80),         # 31-50  
            'older_adult': (60, 75)    # 50+
        }
    
    def analyze_heart_rate_data(self, hr_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analyze heart rate and physical symptoms from questionnaire responses
        
        Args:
            hr_data: Dictionary containing heart rate questionnaire responses
            
        Returns:
            Dictionary with analysis results and scores
        """
        try:
            # Calculate individual component scores
            resting_hr = hr_data.get('resting_heart_rate', 70)
            hr_score = self._calculate_hr_score(resting_hr)
            
            racing_score = self.frequency_weights.get(hr_data.get('heart_racing_frequency', 'never'), 0.0)
            tightness_score = self.frequency_weights.get(hr_data.get('chest_tightness', 'never'), 0.0)
            breathing_score = self.frequency_weights.get(hr_data.get('breathing_difficulty', 'never'), 0.0)
            anxiety_score = self.anxiety_weights.get(hr_data.get('physical_anxiety', 'none'), 0.0)
            sweating_score = self.frequency_weights.get(hr_data.get('sweating_frequency', 'never'), 0.0)
            
            # Calculate composite scores
            cardiovascular_stress_score = (hr_score + racing_score + tightness_score + breathing_score) / 4.0
            physical_anxiety_score = (anxiety_score + sweating_score + racing_score + tightness_score) / 4.0
            
            # Overall heart rate analysis score (0.0 = healthy, 1.0 = concerning)
            overall_score = (cardiovascular_stress_score + physical_anxiety_score) / 2.0
            
            # Determine risk level
            risk_level = self._determine_hr_risk_level(overall_score)
            
            # Generate insights
            insights = self._generate_hr_insights(hr_data, overall_score)
            
            return {
                'cardiovascular_stress_score': round(cardiovascular_stress_score, 3),
                'physical_anxiety_score': round(physical_anxiety_score, 3),
                'overall_score': round(overall_score, 3),
                'risk_level': risk_level,
                'insights': insights,
                'component_scores': {
                    'resting_hr': hr_score,
                    'heart_racing': racing_score,
                    'chest_tightness': tightness_score,
                    'breathing': breathing_score,
                    'physical_anxiety': anxiety_score,
                    'sweating': sweating_score
                },
                'hr_assessment': self._assess_heart_rate(resting_hr)
            }
            
        except Exception as e:
            logging.error(f"Error in heart rate analysis: {str(e)}")
            return {
                'cardiovascular_stress_score': 0.0,
                'physical_anxiety_score': 0.0,
                'overall_score': 0.0,
                'risk_level': 'unknown',
                'insights': ['Error occurred during heart rate analysis'],
                'component_scores': {},
                'hr_assessment': 'unknown'
            }
    
    def _calculate_hr_score(self, hr: int) -> float:
        """Calculate heart rate score based on deviation from normal range"""
        if hr < 50:
            return 0.8  # Bradycardia - could indicate depression
        elif hr < 60:
            return 0.3  # Low normal
        elif hr <= 85:
            return 0.0  # Normal range
        elif hr <= 100:
            return 0.4  # Elevated - mild concern
        elif hr <= 120:
            return 0.7  # Tachycardia - moderate concern
        else:
            return 1.0  # Severe tachycardia - high concern
    
    def _assess_heart_rate(self, hr: int) -> str:
        """Provide heart rate assessment"""
        if hr < 50:
            return 'significantly_low'
        elif hr < 60:
            return 'low_normal'
        elif hr <= 85:
            return 'normal'
        elif hr <= 100:
            return 'elevated'
        elif hr <= 120:
            return 'high'
        else:
            return 'very_high'
    
    def _determine_hr_risk_level(self, score: float) -> str:
        """Determine risk level based on heart rate analysis score"""
        if score >= 0.8:
            return 'high'
        elif score >= 0.6:
            return 'moderate'
        elif score >= 0.3:
            return 'mild'
        else:
            return 'minimal'
    
    def _generate_hr_insights(self, hr_data: Dict[str, Any], overall_score: float) -> list:
        """Generate human-readable insights from heart rate analysis"""
        insights = []
        
        # Resting heart rate insights
        resting_hr = hr_data.get('resting_heart_rate', 70)
        if resting_hr < 50:
            insights.append("Very low resting heart rate may indicate underlying health issues")
        elif resting_hr > 100:
            insights.append("Elevated resting heart rate could suggest stress, anxiety, or health concerns")
        elif resting_hr > 85:
            insights.append("Slightly elevated resting heart rate may indicate mild stress or fitness level")
        
        # Racing heart insights
        racing = hr_data.get('heart_racing_frequency', 'never')
        if racing in ['often', 'always']:
            insights.append("Frequent heart racing episodes suggest high stress or anxiety levels")
        
        # Chest tightness insights
        tightness = hr_data.get('chest_tightness', 'never')
        if tightness in ['often', 'always']:
            insights.append("Regular chest tightness may indicate anxiety or stress-related symptoms")
        
        # Breathing difficulty insights
        breathing = hr_data.get('breathing_difficulty', 'never')
        if breathing in ['often', 'always']:
            insights.append("Breathing difficulties could suggest anxiety or stress-related issues")
        
        # Physical anxiety insights
        anxiety = hr_data.get('physical_anxiety', 'none')
        if anxiety in ['severe', 'extreme']:
            insights.append("High levels of physical anxiety symptoms require attention")
        
        # Sweating insights
        sweating = hr_data.get('sweating_frequency', 'never')
        if sweating in ['often', 'always']:
            insights.append("Frequent sweating may indicate stress, anxiety, or other health factors")
        
        # Overall assessment
        if overall_score >= 0.7:
            insights.append("Physical symptoms suggest significant stress or anxiety levels")
        elif overall_score >= 0.4:
            insights.append("Physical symptoms show some indicators of stress or anxiety")
        else:
            insights.append("Physical symptoms appear within normal range")
        
        return insights if insights else ["Heart rate and physical symptoms analyzed - no specific concerns identified"]
    
    def get_hr_recommendations(self, analysis_result: Dict[str, Any]) -> list:
        """Get recommendations based on heart rate analysis results"""
        recommendations = []
        
        risk_level = analysis_result.get('risk_level', 'minimal')
        overall_score = analysis_result.get('overall_score', 0.0)
        hr_assessment = analysis_result.get('hr_assessment', 'normal')
        
        if risk_level in ['high', 'moderate']:
            recommendations.extend([
                "Consider consulting with a healthcare provider about your physical symptoms",
                "Practice stress reduction techniques like deep breathing or meditation",
                "Monitor your heart rate and symptoms regularly"
            ])
        
        if hr_assessment in ['very_high', 'high']:
            recommendations.extend([
                "Seek medical evaluation for elevated heart rate",
                "Avoid caffeine and stimulants until consulting a doctor",
                "Consider cardiovascular fitness assessment"
            ])
        elif hr_assessment == 'significantly_low':
            recommendations.append("Consult a healthcare provider about low heart rate")
        
        if overall_score >= 0.5:
            recommendations.extend([
                "Keep a daily log of physical symptoms and triggers",
                "Practice regular relaxation techniques",
                "Ensure adequate sleep and hydration"
            ])
        
        # Component-specific recommendations
        component_scores = analysis_result.get('component_scores', {})
        if component_scores.get('physical_anxiety', 0) >= 0.6:
            recommendations.append("Learn grounding techniques for managing physical anxiety symptoms")
        
        if component_scores.get('breathing', 0) >= 0.6:
            recommendations.append("Practice breathing exercises and consider respiratory therapy")
        
        return recommendations if recommendations else ["Physical symptoms appear healthy - maintain current wellness practices"]