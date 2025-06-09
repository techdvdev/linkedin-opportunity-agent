# LinkedIn Opportunity Detection Agent

An AI agent that analyzes LinkedIn posts to identify IT service opportunities in:
- Data Integration
- Data Visualization  
- Web Development
- App Development

## Features

- **Smart Detection**: Identifies posts seeking IT services
- **Confidence Scoring**: Rates opportunity likelihood (0-1)
- **Urgency Analysis**: Categorizes timeline urgency
- **Requirement Extraction**: Pulls out technologies, budgets, timelines
- **Response Suggestions**: Provides tailored approach recommendations

## Usage

```python
from linkedin_agent import LinkedInOpportunityAgent

agent = LinkedInOpportunityAgent()
result = agent.analyze_post("Your LinkedIn post text here")

print(f"Opportunity: {result.opportunity_type.value}")
print(f"Confidence: {result.confidence_score:.2f}")
print(f"Urgency: {result.urgency_level.value}")
```

## Deployment Options

- **GitHub Actions**: Automated monitoring with email alerts
- **Railway**: Web interface for manual analysis
- **Google Cloud Run**: Serverless API endpoint
- **Heroku**: Simple web app deployment

## Setup

1. Clone this repository
2. Install dependencies: `pip install -r requirements.txt`
3. Run the agent: `python linkedin_agent.py`

## Legal Note

This tool is for analyzing text content you have permission to access. Respect LinkedIn's terms of service and only analyze posts you have legitimate access to.
