import re
import json
from typing import Dict, List, Tuple
from dataclasses import dataclass
from enum import Enum

class OpportunityType(Enum):
    DATA_INTEGRATION = "data_integration"
    DATA_VISUALIZATION = "data_visualization"
    WEB_DEVELOPMENT = "web_development"
    APP_DEVELOPMENT = "app_development"
    MIXED = "mixed"

class UrgencyLevel(Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    URGENT = "urgent"

@dataclass
class OpportunityScore:
    opportunity_type: OpportunityType
    confidence_score: float  # 0-1
    urgency_level: UrgencyLevel
    key_indicators: List[str]
    extracted_requirements: List[str]

class LinkedInOpportunityAgent:
    def __init__(self):
        # Keywords for different opportunity types
        self.keywords = {
            OpportunityType.DATA_INTEGRATION: {
                'primary': [
                    'data integration', 'data pipeline', 'etl', 'data migration',
                    'api integration', 'database sync', 'data warehousing',
                    'data consolidation', 'system integration', 'data flow'
                ],
                'secondary': [
                    'connect systems', 'merge data', 'automate data',
                    'real-time data', 'data sync', 'import data', 'export data'
                ]
            },
            OpportunityType.DATA_VISUALIZATION: {
                'primary': [
                    'data visualization', 'dashboard', 'reporting', 'analytics',
                    'charts', 'graphs', 'business intelligence', 'bi tool',
                    'data analysis', 'metrics', 'kpi dashboard'
                ],
                'secondary': [
                    'visualize data', 'show data', 'data insights',
                    'performance tracking', 'report automation', 'tableau',
                    'power bi', 'looker', 'data studio'
                ]
            },
            OpportunityType.WEB_DEVELOPMENT: {
                'primary': [
                    'website', 'web development', 'web app', 'web application',
                    'frontend', 'backend', 'full stack', 'responsive design',
                    'web portal', 'landing page', 'e-commerce'
                ],
                'secondary': [
                    'build website', 'create site', 'web solution',
                    'online presence', 'web platform', 'cms', 'wordpress',
                    'react', 'angular', 'vue', 'django', 'flask'
                ]
            },
            OpportunityType.APP_DEVELOPMENT: {
                'primary': [
                    'mobile app', 'app development', 'ios app', 'android app',
                    'application development', 'native app', 'cross platform',
                    'flutter', 'react native', 'swift', 'kotlin'
                ],
                'secondary': [
                    'build app', 'create application', 'mobile solution',
                    'app store', 'play store', 'mobile platform'
                ]
            }
        }
        
        # Help-seeking indicators
        self.help_indicators = [
            'looking for', 'need help', 'seeking', 'require', 'want to hire',
            'need assistance', 'help needed', 'recommendations for',
            'anyone know', 'suggestions for', 'advice on', 'expertise in',
            'consultant', 'freelancer', 'agency', 'developer', 'specialist',
            'outsource', 'contract', 'project', 'budget for', 'quote for'
        ]
        
        # Urgency indicators
        self.urgency_indicators = {
            UrgencyLevel.URGENT: ['urgent', 'asap', 'immediately', 'rush', 'emergency'],
            UrgencyLevel.HIGH: ['soon', 'quickly', 'fast', 'priority', 'deadline'],
            UrgencyLevel.MEDIUM: ['next month', 'few weeks', 'planning', 'upcoming'],
            UrgencyLevel.LOW: ['future', 'eventually', 'considering', 'thinking about']
        }

    def preprocess_text(self, text: str) -> str:
        """Clean and normalize text for analysis"""
        # Convert to lowercase
        text = text.lower()
        
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text)
        
        # Remove URLs
        text = re.sub(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', '', text)
        
        # Remove hashtags for cleaner analysis (but keep the text)
        text = re.sub(r'#(\w+)', r'\1', text)
        
        return text.strip()

    def detect_help_seeking(self, text: str) -> Tuple[bool, List[str]]:
        """Detect if the post is seeking help/services"""
        found_indicators = []
        
        for indicator in self.help_indicators:
            if indicator in text:
                found_indicators.append(indicator)
        
        return len(found_indicators) > 0, found_indicators

    def calculate_opportunity_scores(self, text: str) -> Dict[OpportunityType, float]:
        """Calculate confidence scores for each opportunity type"""
        scores = {}
        
        for opp_type, keywords in self.keywords.items():
            primary_matches = sum(1 for keyword in keywords['primary'] if keyword in text)
            secondary_matches = sum(1 for keyword in keywords['secondary'] if keyword in text)
            
            # Weight primary keywords more heavily
            total_score = (primary_matches * 2) + secondary_matches
            max_possible = (len(keywords['primary']) * 2) + len(keywords['secondary'])
            
            scores[opp_type] = min(total_score / max_possible, 1.0) if max_possible > 0 else 0.0
        
        return scores

    def detect_urgency(self, text: str) -> UrgencyLevel:
        """Determine urgency level based on text indicators"""
        for urgency_level, indicators in self.urgency_indicators.items():
            for indicator in indicators:
                if indicator in text:
                    return urgency_level
        
        return UrgencyLevel.MEDIUM  # Default

    def extract_requirements(self, text: str) -> List[str]:
        """Extract specific requirements mentioned in the post"""
        requirements = []
        
        # Look for technology mentions
        tech_patterns = [
            r'(python|java|javascript|react|angular|vue|node\.?js|django|flask|spring)',
            r'(sql|mysql|postgresql|mongodb|oracle|elasticsearch)',
            r'(aws|azure|gcp|google cloud|cloud)',
            r'(tableau|power bi|looker|qlik|grafana)',
            r'(api|rest|graphql|microservices)',
            r'(mobile|ios|android|flutter|react native)'
        ]
        
        for pattern in tech_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            requirements.extend([match.title() for match in matches])
        
        # Look for budget mentions
        budget_pattern = r'\$[\d,]+(?:\.\d{2})?|\d+k?\s*(?:budget|dollar|usd)'
        budget_matches = re.findall(budget_pattern, text, re.IGNORECASE)
        if budget_matches:
            requirements.append(f"Budget mentioned: {', '.join(budget_matches)}")
        
        # Look for timeline mentions
        timeline_pattern = r'\d+\s*(?:days?|weeks?|months?|hours?)'
        timeline_matches = re.findall(timeline_pattern, text, re.IGNORECASE)
        if timeline_matches:
            requirements.append(f"Timeline: {', '.join(timeline_matches)}")
        
        return list(set(requirements))  # Remove duplicates

    def analyze_post(self, post_text: str) -> OpportunityScore:
        """Main method to analyze a LinkedIn post for opportunities"""
        
        # Preprocess text
        cleaned_text = self.preprocess_text(post_text)
        
        # Check if post is seeking help
        is_seeking_help, help_indicators = self.detect_help_seeking(cleaned_text)
        
        if not is_seeking_help:
            return OpportunityScore(
                opportunity_type=OpportunityType.DATA_INTEGRATION,  # Default
                confidence_score=0.0,
                urgency_level=UrgencyLevel.LOW,
                key_indicators=[],
                extracted_requirements=[]
            )
        
        # Calculate opportunity scores
        opportunity_scores = self.calculate_opportunity_scores(cleaned_text)
        
        # Find the highest scoring opportunity type
        best_opportunity = max(opportunity_scores.items(), key=lambda x: x[1])
        opportunity_type, confidence_score = best_opportunity
        
        # Check if it's a mixed opportunity (multiple high scores)
        high_scores = [opp for opp, score in opportunity_scores.items() if score > 0.3]
        if len(high_scores) > 1:
            opportunity_type = OpportunityType.MIXED
        
        # Detect urgency
        urgency = self.detect_urgency(cleaned_text)
        
        # Extract requirements
        requirements = self.extract_requirements(cleaned_text)
        
        # Compile key indicators
        key_indicators = help_indicators.copy()
        for opp_type, keywords in self.keywords.items():
            for keyword in keywords['primary'] + keywords['secondary']:
                if keyword in cleaned_text:
                    key_indicators.append(keyword)
        
        return OpportunityScore(
            opportunity_type=opportunity_type,
            confidence_score=confidence_score,
            urgency_level=urgency,
            key_indicators=list(set(key_indicators))[:10],  # Limit to top 10
            extracted_requirements=requirements
        )

    def generate_response_suggestions(self, opportunity: OpportunityScore) -> List[str]:
        """Generate suggested response approaches based on the opportunity"""
        suggestions = []
        
        if opportunity.confidence_score < 0.2:
            return ["Low confidence opportunity - may not be relevant"]
        
        base_approaches = {
            OpportunityType.DATA_INTEGRATION: [
                "Highlight experience with ETL processes and data pipelines",
                "Mention specific integration tools (Zapier, MuleSoft, custom APIs)",
                "Showcase data warehousing and real-time processing capabilities"
            ],
            OpportunityType.DATA_VISUALIZATION: [
                "Share portfolio of dashboard examples",
                "Mention expertise in Tableau, Power BI, or custom solutions",
                "Highlight ability to translate business needs into visual insights"
            ],
            OpportunityType.WEB_DEVELOPMENT: [
                "Showcase relevant web development portfolio",
                "Mention technology stack expertise (React, Django, etc.)",
                "Emphasize responsive design and user experience"
            ],
            OpportunityType.APP_DEVELOPMENT: [
                "Share mobile app portfolio and app store links",
                "Mention cross-platform vs native development capabilities",
                "Highlight user-centric design approach"
            ],
            OpportunityType.MIXED: [
                "Emphasize full-stack capabilities across multiple domains",
                "Mention integrated solutions experience",
                "Highlight project management for complex requirements"
            ]
        }
        
        suggestions.extend(base_approaches.get(opportunity.opportunity_type, []))
        
        # Add urgency-specific suggestions
        if opportunity.urgency_level in [UrgencyLevel.HIGH, UrgencyLevel.URGENT]:
            suggestions.append("Emphasize quick turnaround and availability")
            suggestions.append("Mention agile development approach")
        
        return suggestions

# Example usage and testing
def main():
    agent = LinkedInOpportunityAgent()
    
    # Test posts
    test_posts = [
        "Looking for a data visualization expert to create interactive dashboards for our sales team. Need someone with Tableau or Power BI experience. Budget around $5k, timeline 3 weeks.",
        
        "Hey everyone! Our startup needs help building a mobile app for iOS and Android. We're looking for a React Native developer who can work with our existing API. Anyone have recommendations?",
        
        "Urgent: Need data integration specialist ASAP! We have multiple databases that need to sync in real-time. Experience with ETL processes required. Please DM if interested.",
        
        "Planning to build a new website for our consulting firm. Need full-stack developer with modern framework experience. Not urgent, just exploring options.",
        
        "Can someone recommend a good restaurant in downtown? Thanks!"
    ]
    
    print("LinkedIn Opportunity Detection Results:")
    print("=" * 50)
    
    for i, post in enumerate(test_posts, 1):
        print(f"\nPost {i}: {post[:100]}...")
        result = agent.analyze_post(post)
        
        print(f"Opportunity Type: {result.opportunity_type.value}")
        print(f"Confidence Score: {result.confidence_score:.2f}")
        print(f"Urgency Level: {result.urgency_level.value}")
        print(f"Key Indicators: {', '.join(result.key_indicators[:5])}")
        print(f"Requirements: {', '.join(result.extracted_requirements)}")
        
        if result.confidence_score > 0.2:
            suggestions = agent.generate_response_suggestions(result)
            print("Response Suggestions:")
            for suggestion in suggestions[:3]:
                print(f"  - {suggestion}")
        
        print("-" * 30)

if __name__ == "__main__":
    main()
