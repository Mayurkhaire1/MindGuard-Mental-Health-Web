from typing import Dict, List, Any, Tuple
import re
import logging
from datetime import datetime

class CrisisInterventionSystem:
    """Comprehensive crisis intervention and suicide prevention system"""
    
    def __init__(self):
        self.crisis_indicators = self._initialize_crisis_indicators()
        self.emergency_contacts = self._initialize_emergency_contacts()
        self.intervention_protocols = self._initialize_intervention_protocols()
        self.safety_planning_resources = self._initialize_safety_planning()
        
    def _initialize_crisis_indicators(self) -> Dict[str, Dict[str, Any]]:
        """Initialize comprehensive crisis indicators with severity levels"""
        return {
            # Immediate danger indicators
            'suicide_plan': {
                'keywords': ['plan to kill', 'going to kill myself', 'plan to die', 'tonight i will', 'tomorrow i will'],
                'severity': 'critical',
                'immediate_response': True,
                'response_time': 'immediate'
            },
            'suicide_method': {
                'keywords': ['pills', 'rope', 'gun', 'bridge', 'overdose', 'hanging', 'cut wrists'],
                'severity': 'critical',
                'immediate_response': True,
                'response_time': 'immediate'
            },
            'imminent_intent': {
                'keywords': ['tonight', 'today', 'right now', 'can\'t wait', 'this is it', 'goodbye'],
                'severity': 'critical',
                'immediate_response': True,
                'response_time': 'immediate'
            },
            
            # High risk indicators
            'suicide_ideation': {
                'keywords': ['want to die', 'kill myself', 'end my life', 'suicide', 'better off dead', 
                           'end everything', 'way out is to end', 'only way out', 'take my own life',
                           'want to disappear', 'give up on life', 'not worth living', 'rather be dead',
                           'finish myself', 'end it all', 'kill me'],
                'severity': 'critical',
                'immediate_response': True,
                'response_time': 'immediate'
            },
            'self_harm': {
                'keywords': ['hurt myself', 'cut myself', 'harm myself', 'self harm', 'cutting'],
                'severity': 'high',
                'immediate_response': False,
                'response_time': 'within_24_hours'
            },
            'hopelessness': {
                'keywords': ['no hope', 'hopeless', 'pointless', 'no way out', 'trapped', 'stuck',
                           'meaningless', 'broken and abandoned', 'nobody I can trust', 'worthless',
                           'alone', 'isolated', 'abandoned', 'broken', 'torture', 'fights'],
                'severity': 'critical',
                'immediate_response': True,
                'response_time': 'immediate'
            },
            
            # Moderate risk indicators
            'isolation': {
                'keywords': ['nobody cares', 'all alone', 'isolated', 'no friends', 'abandoned'],
                'severity': 'moderate',
                'immediate_response': False,
                'response_time': 'within_week'
            },
            'substance_abuse': {
                'keywords': ['drinking too much', 'using drugs', 'getting high', 'numbing pain'],
                'severity': 'moderate',
                'immediate_response': False,
                'response_time': 'within_week'
            }
        }
    
    def _initialize_emergency_contacts(self) -> Dict[str, Dict[str, str]]:
        """Initialize emergency contacts and crisis resources"""
        return {
            'telemanas': {
                'name': 'TeleMANAS',
                'phone': '14416',
                'description': '24/7 mental health support helpline',
                'availability': '24/7'
            },
            'telemanas_toll_free': {
                'name': 'TeleMANAS (Toll-Free)',
                'phone': '1-8008914416',
                'description': '24/7 mental health support helpline',
                'availability': '24/7'
            },
            'jeevan_aastha': {
                'name': 'Jeevan Aastha Helpline',
                'phone': '1800 233 3330',
                'description': '24/7 crisis support helpline',
                'availability': '24/7'
            },
            'emergency_contacts_directory': {
                'name': 'Emergency Contacts Directory',
                'website': 'https://sarkarilist.in/government-helpline-numbers/',
                'description': 'List of government helpline and emergency contact numbers',
                'availability': 'Online'
            },
            'international_association': {
                'name': 'International Association for Suicide Prevention',
                'website': 'https://www.iasp.info/resources/Crisis_Centres/',
                'description': 'International crisis center directory',
                'availability': 'Varies by location'
            },
            'mental_health_america': {
                'name': 'Mental Health America',
                'phone': '1-800-273-8255',
                'website': 'https://www.mhanational.org',
                'description': 'Mental health resources and support',
                'availability': 'Varies'
            }
        }
    
    def _initialize_intervention_protocols(self) -> Dict[str, List[str]]:
        """Initialize intervention protocols based on risk level"""
        return {
            'critical': [
                "Do not leave the person alone",
                "Use the emergency contacts directory to find local emergency services: https://sarkarilist.in/government-helpline-numbers/",
                "Call TeleMANAS (14416 / 1-8008914416)",
                "Remove any means of self-harm from environment",
                "Stay with person until professional help arrives",
                "Listen without judgment and express care",
                "Do not promise to keep suicide plans secret"
            ],
            'high': [
                "Take all threats seriously",
                "Encourage immediate professional help",
                "Call TeleMANAS (14416 / 1-8008914416)",
                "Help create a safety plan",
                "Remove or secure potential means of harm",
                "Increase supervision and support",
                "Schedule mental health appointment within 24 hours",
                "Provide crisis contact information"
            ],
            'moderate': [
                "Express concern and willingness to help",
                "Encourage professional mental health evaluation",
                "Provide crisis hotline numbers",
                "Help identify support network",
                "Discuss healthy coping strategies",
                "Schedule follow-up within 48 hours",
                "Monitor for increasing risk factors"
            ],
            'low': [
                "Continue supportive dialogue",
                "Provide mental health resources",
                "Encourage self-care activities",
                "Help identify protective factors",
                "Maintain regular check-ins",
                "Promote connection with others"
            ]
        }
    
    def _initialize_safety_planning(self) -> Dict[str, List[str]]:
        """Initialize safety planning components"""
        return {
            'warning_signs': [
                "Identify personal warning signs of crisis",
                "Recognize thoughts, feelings, and behaviors that indicate risk",
                "Monitor mood changes and stress levels",
                "Notice isolation or withdrawal patterns"
            ],
            'coping_strategies': [
                "Practice deep breathing and relaxation techniques",
                "Engage in physical exercise or movement",
                "Use creative outlets (art, music, writing)",
                "Practice mindfulness and grounding techniques",
                "Call a trusted friend or family member",
                "Take a warm bath or shower",
                "Listen to calming music",
                "Go for a walk in nature"
            ],
            'support_contacts': [
                "List trusted friends and family members",
                "Include phone numbers and availability",
                "Identify mental health professionals",
                "Include crisis hotline numbers",
                "Add emergency contacts"
            ],
            'environment_safety': [
                "Remove or secure means of self-harm",
                "Clear potentially harmful substances",
                "Identify safe physical spaces",
                "Create calming environment elements"
            ],
            'professional_resources': [
                "Primary care physician contact",
                "Mental health counselor/therapist",
                "Psychiatrist or medication provider",
                "Local emergency room information",
                "Crisis center locations"
            ]
        }
    
    def assess_crisis_risk(self, text: str) -> Dict[str, Any]:
        """Comprehensive crisis risk assessment"""
        if not text:
            return self._create_empty_assessment()
        
        text_lower = text.lower()
        
        # Initialize assessment results
        assessment = {
            'overall_risk': 'low',
            'immediate_intervention': False,
            'detected_indicators': [],
            'keywords': [],
            'risk_factors': {},
            'protective_factors': [],
            'recommendations': [],
            'urgency_level': 'routine'
        }
        
        # Analyze each crisis indicator category
        highest_severity = 'low'
        immediate_response_needed = False
        
        for category, indicator_data in self.crisis_indicators.items():
            keywords_found = []
            
            for keyword in indicator_data['keywords']:
                if keyword.lower() in text_lower:
                    keywords_found.append(keyword)
            
            if keywords_found:
                assessment['detected_indicators'].append({
                    'category': category,
                    'severity': indicator_data['severity'],
                    'keywords': keywords_found,
                    'immediate_response': indicator_data['immediate_response'],
                    'response_time': indicator_data['response_time']
                })
                
                assessment['keywords'].extend(keywords_found)
                
                # Update overall risk level
                if indicator_data['severity'] == 'critical':
                    highest_severity = 'critical'
                    immediate_response_needed = True
                elif indicator_data['severity'] == 'high' and highest_severity not in ['critical']:
                    highest_severity = 'high'
                elif indicator_data['severity'] == 'moderate' and highest_severity not in ['critical', 'high']:
                    highest_severity = 'moderate'
                
                if indicator_data['immediate_response']:
                    immediate_response_needed = True
        
        # Set final assessment values
        assessment['overall_risk'] = highest_severity
        assessment['immediate_intervention'] = immediate_response_needed
        
        # Determine urgency level
        if immediate_response_needed:
            assessment['urgency_level'] = 'emergency'
        elif highest_severity == 'high':
            assessment['urgency_level'] = 'urgent'
        elif highest_severity == 'moderate':
            assessment['urgency_level'] = 'priority'
        else:
            assessment['urgency_level'] = 'routine'
        
        # Analyze additional risk factors
        assessment['risk_factors'] = self._analyze_risk_factors(text_lower)
        
        # Identify protective factors
        assessment['protective_factors'] = self._identify_protective_factors(text_lower)
        
        # Generate recommendations
        assessment['recommendations'] = self._generate_crisis_recommendations(assessment)
        
        return assessment
    
    def _analyze_risk_factors(self, text: str) -> Dict[str, List[str]]:
        """Analyze additional risk factors in the text"""
        risk_factors = {
            'psychological': [],
            'social': [],
            'environmental': [],
            'behavioral': []
        }
        
        # Psychological risk factors
        psychological_indicators = [
            'depressed', 'anxious', 'overwhelmed', 'panic', 'worthless',
            'guilty', 'shame', 'angry', 'rage', 'confused', 'scared'
        ]
        for indicator in psychological_indicators:
            if indicator in text:
                risk_factors['psychological'].append(indicator)
        
        # Social risk factors
        social_indicators = [
            'lonely', 'isolated', 'rejected', 'bullied', 'divorced',
            'broke up', 'fired', 'lost job', 'financial problems'
        ]
        for indicator in social_indicators:
            if indicator in text:
                risk_factors['social'].append(indicator)
        
        # Environmental risk factors
        environmental_indicators = [
            'access to weapons', 'alone', 'unsafe', 'chaotic',
            'stressful', 'traumatic', 'abusive'
        ]
        for indicator in environmental_indicators:
            if indicator in text:
                risk_factors['environmental'].append(indicator)
        
        # Behavioral risk factors
        behavioral_indicators = [
            'drinking', 'drugs', 'reckless', 'impulsive',
            'withdrawn', 'giving away', 'saying goodbye'
        ]
        for indicator in behavioral_indicators:
            if indicator in text:
                risk_factors['behavioral'].append(indicator)
        
        return risk_factors
    
    def _identify_protective_factors(self, text: str) -> List[str]:
        """Identify protective factors mentioned in the text"""
        protective_factors = []
        
        protective_indicators = {
            'family support': ['family', 'parents', 'siblings', 'loved ones'],
            'friend support': ['friends', 'buddy', 'companion', 'support'],
            'professional help': ['therapist', 'counselor', 'doctor', 'treatment'],
            'spiritual/religious': ['faith', 'prayer', 'church', 'spiritual', 'god'],
            'hobbies/interests': ['hobby', 'music', 'art', 'sports', 'reading'],
            'future goals': ['future', 'goals', 'dreams', 'plans', 'hope'],
            'pets': ['dog', 'cat', 'pet', 'animal'],
            'work/school': ['job', 'work', 'school', 'career', 'education']
        }
        
        for factor_name, keywords in protective_indicators.items():
            for keyword in keywords:
                if keyword in text:
                    protective_factors.append(factor_name)
                    break  # Only add each factor once
        
        return list(set(protective_factors))  # Remove duplicates
    
    def _generate_crisis_recommendations(self, assessment: Dict[str, Any]) -> List[str]:
        """Generate specific recommendations based on crisis assessment"""
        recommendations = []
        
        # Get base recommendations for risk level
        risk_level = assessment['overall_risk']
        if risk_level in self.intervention_protocols:
            recommendations.extend(self.intervention_protocols[risk_level])
        
        # Add specific recommendations based on detected indicators
        detected_categories = [indicator['category'] for indicator in assessment['detected_indicators']]
        
        if 'suicide_plan' in detected_categories or 'suicide_method' in detected_categories:
            recommendations.extend([
                "This appears to be a medical emergency - use the emergency contacts directory to find local services: https://sarkarilist.in/government-helpline-numbers/",
                "Do not leave the person alone under any circumstances",
                "Contact TeleMANAS at 14416 / 1-8008914416"
            ])
        
        if 'self_harm' in detected_categories:
            recommendations.extend([
                "Remove all sharp objects and potential self-harm tools",
                "Provide immediate emotional support and validation",
                "Seek professional mental health evaluation today"
            ])
        
        if 'substance_abuse' in detected_categories:
            recommendations.extend([
                "Address substance use as part of crisis intervention",
                "Consider dual diagnosis treatment programs",
                "Remove access to substances if possible"
            ])
        
        if 'isolation' in detected_categories:
            recommendations.extend([
                "Increase social connection and support",
                "Arrange for someone to stay with the person",
                "Connect with family and friends for ongoing support"
            ])
        
        # Add protective factor reinforcement
        if assessment['protective_factors']:
            recommendations.append(f"Reinforce protective factors: {', '.join(assessment['protective_factors'])}")
        
        return list(set(recommendations))  # Remove duplicates
    
    def get_crisis_resources(self) -> Dict[str, Any]:
        """Get comprehensive crisis resources and contacts"""
        return {
            'emergency_contacts': self.emergency_contacts,
            'safety_planning': self.safety_planning_resources,
            'immediate_steps': [
                "Stay calm and take the situation seriously",
                "Do not leave the person alone if they are in immediate danger",
                "Call TeleMANAS (14416 / 1-8008914416) for immediate help",
                "Use the emergency contacts directory to find local emergency services: https://sarkarilist.in/government-helpline-numbers/",
                "Listen without judgment and show you care",
                "Help them connect with professional support",
                "Follow up regularly to show ongoing support"
            ],
            'warning_signs': [
                "Talking about wanting to die or kill themselves",
                "Looking for ways to kill themselves",
                "Talking about feeling hopeless or having no purpose",
                "Talking about feeling trapped or being in unbearable pain",
                "Talking about being a burden to others",
                "Increasing use of alcohol or drugs",
                "Acting anxious, agitated, or reckless",
                "Sleeping too little or too much",
                "Withdrawing or feeling isolated",
                "Showing rage or talking about seeking revenge",
                "Displaying extreme mood swings"
            ]
        }
    
    def get_recommendations(self, crisis_assessment: Dict[str, Any]) -> Dict[str, List[str]]:
        """Get detailed recommendations based on crisis assessment"""
        risk_level = crisis_assessment.get('overall_risk', 'low')
        immediate_intervention = crisis_assessment.get('immediate_intervention', False)
        
        recommendations = {
            'immediate_actions': [],
            'short_term_actions': [],
            'long_term_actions': [],
            'resources_to_contact': []
        }
        
        if immediate_intervention or risk_level == 'critical':
            recommendations['immediate_actions'] = [
                "Use the emergency contacts directory to find local emergency services: https://sarkarilist.in/government-helpline-numbers/",
                "Contact TeleMANAS at 14416 / 1-8008914416",
                "Do not leave the person alone",
                "Remove any means of self-harm from the environment",
                "Stay with the person until professional help arrives"
            ]
            recommendations['resources_to_contact'] = [
                "TeleMANAS (14416 / 1-8008914416)",
                "Jeevan Aastha Helpline (1800 233 3330)",
                "Emergency contacts directory (https://sarkarilist.in/government-helpline-numbers/)",
                "Local emergency room",
                "Crisis intervention team"
            ]
        
        elif risk_level == 'high':
            recommendations['immediate_actions'] = [
                "Contact TeleMANAS at 14416 / 1-8008914416",
                "Arrange for mental health evaluation within 24 hours",
                "Ensure the person is not alone",
                "Create a safety plan together"
            ]
            recommendations['short_term_actions'] = [
                "Schedule appointment with mental health professional",
                "Increase social support and monitoring",
                "Implement crisis safety planning",
                "Remove or secure potential means of harm"
            ]
        
        elif risk_level == 'moderate':
            recommendations['short_term_actions'] = [
                "Schedule mental health consultation",
                "Provide crisis hotline information",
                "Help identify support network",
                "Discuss healthy coping strategies"
            ]
            recommendations['long_term_actions'] = [
                "Regular mental health check-ins",
                "Build strong support network",
                "Develop ongoing coping strategies",
                "Monitor for changes in risk level"
            ]
        
        # Add general long-term recommendations
        recommendations['long_term_actions'].extend([
            "Maintain regular mental health care",
            "Build and maintain social connections",
            "Develop healthy lifestyle habits",
            "Practice stress management techniques",
            "Stay connected with support systems"
        ])
        
        return recommendations
    
    def create_safety_plan(self, assessment: Dict[str, Any], user_input: Dict[str, Any] = None) -> Dict[str, Any]:
        """Create a personalized safety plan based on assessment"""
        safety_plan = {
            'warning_signs': self.safety_planning_resources['warning_signs'].copy(),
            'coping_strategies': self.safety_planning_resources['coping_strategies'].copy(),
            'support_contacts': [],
            'professional_contacts': [],
            'environment_safety': self.safety_planning_resources['environment_safety'].copy(),
            'emergency_contacts': self.emergency_contacts
        }
        
        # Customize based on assessment
        detected_indicators = assessment.get('detected_indicators', [])
        risk_factors = assessment.get('risk_factors', {})
        protective_factors = assessment.get('protective_factors', [])
        
        # Add specific coping strategies based on detected issues
        if any('isolation' in ind['category'] for ind in detected_indicators):
            safety_plan['coping_strategies'].insert(0, "Reach out to a trusted friend or family member immediately")
        
        if any('substance_abuse' in ind['category'] for ind in detected_indicators):
            safety_plan['coping_strategies'].insert(0, "Avoid alcohol and drugs, especially when feeling low")
        
        # Incorporate protective factors
        for factor in protective_factors:
            if factor not in str(safety_plan['coping_strategies']):
                safety_plan['coping_strategies'].append(f"Engage with {factor} for support and distraction")
        
        return safety_plan
    
    def _create_empty_assessment(self) -> Dict[str, Any]:
        """Create empty crisis assessment"""
        return {
            'overall_risk': 'low',
            'immediate_intervention': False,
            'detected_indicators': [],
            'keywords': [],
            'risk_factors': {},
            'protective_factors': [],
            'recommendations': [],
            'urgency_level': 'routine'
        }
