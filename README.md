# Technology-Garage Multi-Agent System

A LangGraph-based multi-agent system for managing tickets, tracking activities, aggregating news, and providing company information.

## Features

### Five Intelligent Agents with Advanced Natural Language Understanding:

1. **Ticket Analyzer Agent**
   - Handles tickets raised by employees, players, or parents
   - Query tickets by ID, status, priority, or get full overview
   - Smart intent detection for natural questions ("Who raised the WiFi ticket?", "How many high priority tickets?")
   - Provides direct, contextual answers based on question type
   - Mock data source for demonstration

2. **News Aggregator Agent**
   - Uses GPT-5.1 to generate comprehensive news summaries
   - Smart topic extraction from various question formats
   - Provides professional news articles with sources and dates
   - No disclaimers about data access - clean, direct responses
   - Customizable news topics (AI, tech, sports, climate, etc.)

3. **Activity Tracker Agent**
   - Tracks employee activities like a Kanban board
   - Filter by employee, status, or view complete board
   - Smart "who" question detection ("Who is assigned to design landing page?")
   - Intelligent intent understanding for varied query formats
   - Shows task progress, priorities, and deadlines
   - Provides precise answers instead of full board dumps

4. **Infrastructure Cost Monitor Agent**
   - Monitors cloud infrastructure costs for multiple providers
   - Supports AWS, Azure, Google Cloud, Firebase, DigitalOcean, Vercel, Heroku
   - Smart query understanding for cost comparisons and specific provider details
   - Natural language enhancement for pricing questions
   - Detailed service breakdowns and spending summaries

5. **Chat Agent**
   - Advanced conversation capabilities with intent detection
   - Provides Technology-Garage company information
   - Understands specific topics (services, location, team, mission)
   - Friendly and professional responses with contextual awareness
   - Handles greetings, help requests, and general questions

## Prerequisites

- Python 3.8+
- Node.js 16+ (for frontend)
- OpenAI API key
- (Optional) NewsData.io API key

## Installation

### Backend Setup

1. Navigate to the project directory:
```bash
cd "c:\Users\MuthamizhS\Desktop\TG Agent"
```

2. Create a virtual environment (recommended):
```bash
python -m venv venv
venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create a `.env` file from the example:
```bash
copy .env.example .env
```

5. Edit `.env` and add your API keys:
```
OPENAI_API_KEY=your_openai_api_key_here
```

### Frontend Setup

1. Navigate to the frontend directory:
```bash
cd agent-app
```

2. Install dependencies:
```bash
npm install
```

## Running the Application

### Start the Backend

From the project root directory:
```bash
python main.py
```

The backend will start on `http://localhost:8000`

### Start the Frontend

In a separate terminal, from the `agent-app` directory:
```bash
npm run dev
```

The frontend will start on `http://localhost:5173`

## Usage Examples

### Ticket Queries
- "Show me all tickets"
- "What's the status of TKT-001?"
- "Show me open tickets"
- "Show pending tickets"
- "Show me resolved tickets"
- "Show tickets in progress"
- "What tickets are there?"
- "Show high priority tickets"
- "How many open tickets are there?"
- "Who raised the WiFi ticket?"
- "What's the priority of TKT-003?"

### News Queries
- "What's the latest news?"
- "Show me news about technology"
- "Get news about AI"
- "I want to know about AI news"
- "Latest news on climate change"
- "News about artificial intelligence"
- "Show recent news about sports"
- "Tell me about quantum computing news"
- "What's happening with blockchain?"

### Activity Tracking
- "Show all activities"
- "What's Priya working on?"
- "Show completed tasks"
- "Show pending activities for Keethana"
- "Show the Kanban board"
- "Activities in progress"
- "Show tasks for Tamizh"
- "What tasks are to do?"
- "Who is assigned to design new landing page?"
- "Who's working on the authentication module?"
- "How many tasks are pending?"
- "Show me completed activities"

### Infrastructure Cost Monitor
- "Show AWS costs"
- "What are Azure infrastructure costs?"
- "Show me Google Cloud pricing"
- "Compare cloud providers"
- "Show Firebase costs"
- "How much does DigitalOcean cost?"
- "Infrastructure cost comparison"
- "How much does AWS cost per month?"
- "Which cloud provider is cheapest?"
- "What services does Azure offer?"
- "Show me Vercel pricing breakdown"

### Company Information
- "Tell me about Technology-Garage"
- "What services does the company offer?"
- "What's the company mission?"
- "Who is Technology-Garage?"
- "What does your company do?"
- "Where is Technology-Garage located?"
- "How many employees work at Technology-Garage?"
- "What industries do you serve?"

### General Chat
- "Hello"
- "Hi, how are you?"
- "What can you help me with?"
- "Good morning"

### Comprehensive Overview (All Agents)
Get a complete executive summary from all agents at once:
- "Get me a summary of everything that's happening"
- "What's happening overall?"
- "Give me a complete overview"
- "Show me everything going on"
- "Full status update"
- "What's the overall status?"
- "Complete summary of all systems"

This will invoke ALL agents and provide an intelligent analysis with:
-  Key Priorities & Issues
-  Current Status Overview
-  Notable Updates
-  Insights & Recommendations

### Multiple Agents (Combined Queries)
You can query multiple agents at once:
- "Show me open tickets and latest news"
- "What are the activities for John and latest tech news?"
- "Show pending tickets and Kanban board"
- "Latest AI news and show me completed activities"
- "AWS costs and show all tickets"

## Sample Test Prompts

Here are comprehensive test prompts to verify all agent functionalities:

### Comprehensive Overview Test
```
0. "Get me a summary of everything that's happening"
   Expected: Executive summary from ALL agents with:
   - Key priorities from tickets
   - Latest industry news
   - Activity status and progress
   - Infrastructure spending overview
   - Intelligent analysis and recommendations
   
   This is the most powerful query - it runs all 4 agents and synthesizes everything!
```

### Basic Single Agent Tests
```
1. "Show me all tickets"
   Expected: List of all tickets grouped by status (Open, In Progress, Resolved)

2. "Show pending tickets"
   Expected: Only Open/Pending tickets

3. "What's the status of TKT-001?"
   Expected: Detailed information about ticket TKT-001

4. "Latest news about technology"
   Expected: 5 recent technology news articles

5. "Show the Kanban board"
   Expected: Activities organized in TO DO, IN PROGRESS, COMPLETED columns

6. "Show AWS costs"
   Expected: Detailed AWS infrastructure cost breakdown with spending summary

7. "Tell me about Technology-Garage"
   Expected: Company information (founded, services, mission, etc.)
```

### Status Filter Tests
```
8. "Show resolved tickets"
   Expected: Only resolved tickets

9. "Show activities in progress"
   Expected: Only tasks with "In Progress" status

10. "Show completed tasks"
    Expected: Only completed activities
```

### Employee/Resource Filter Tests
```
11. "What's John Smith working on?"
    Expected: All activities assigned to John Smith

12. "Show activities for Emily Davis"
    Expected: Emily Davis's tasks with progress details
```

### Infrastructure Cost Tests
```
13. "Compare cloud providers"
    Expected: Cost comparison of all providers (AWS, Azure, GCP, etc.)

14. "Show Firebase pricing"
    Expected: Firebase service costs and spending breakdown

15. "What are Azure infrastructure costs?"
    Expected: Azure cost analysis with traffic summary
```

### News Topic Tests
```
16. "News about artificial intelligence"
    Expected: Latest AI-related news articles

17. "Show me recent news on climate"
    Expected: Climate-related news

18. "Latest sports news"
    Expected: Sports news articles
```

### Multi-Agent Tests
```
19. "Show me open tickets and latest technology news"
    Expected: Summary combining open tickets and tech news

20. "What are pending activities and AWS costs?"
    Expected: Combined response from activity tracker and cost monitor

21. "Show completed tasks and tell me about the company"
    Expected: Completed activities + company information
```

### Edge Cases
```
22. "Hello"
    Expected: Friendly greeting from chat agent

23. "TKT-999"
    Expected: "Ticket TKT-999 not found in the system"

24. "Activities for Unknown Person"
    Expected: "No activities found for employee: Unknown Person"

25. "Show me everything"
    Expected: Router should invoke multiple agents based on context
```

### Alias/Variation Tests
```
26. "Show todo tasks" (alias for "to do")
    Expected: Tasks with "To Do" status

27. "Show done activities" (alias for "completed")
    Expected: Completed activities

28. "What's the news on AI?" (different phrasing)
    Expected: AI-related news

29. "Google Cloud costs" (instead of "GCP")
    Expected: Google Cloud infrastructure costs

30. "Show DigitalOcean pricing"
    Expected: DigitalOcean cost breakdown
```

## Architecture

The system uses LangGraph to create an intelligent multi-agent workflow:

1. **Router Node**: Uses GPT-5.1 to analyze user queries and determine which agents should handle the request
   - **Special Detection**: Recognizes "everything happening" queries and activates ALL agents automatically
   - Smart routing for single or multi-agent queries
   
2. **Agent Nodes**: Execute specific tasks with intelligent intent detection:
   - Each agent uses LLM to understand user intent and question type
   - Smart filtering and data extraction based on natural language patterns
   - Natural language enhancement for direct, contextual answers
   
3. **Summarize Node**: Combines responses from multiple agents into coherent summaries
   - **Single Agent**: Returns response directly without modification
   - **Multiple Agents**: Creates unified summary with key points from each
   - **Comprehensive Overview**: Provides executive analysis with structured sections when all agents are invoked

### Key Features:
- **Intent Detection**: Every agent analyzes user queries to understand what they're really asking
- **Question Type Recognition**: Identifies "who", "what", "when", "how many" questions for precise answers
- **Natural Language Processing**: Extracts topics, filters, and specific values from varied query formats
- **Smart Response Enhancement**: Transforms raw data into conversational, direct answers
- **Multi-Agent Coordination**: Seamlessly combines responses from multiple agents when needed
- **Comprehensive Analysis**: Special "everything happening" mode for executive-level overviews across all systems

## API Endpoints

- `GET /health` - Health check
- `POST /chat` - Send a message to the agent system
- `GET /agents` - List all available agents
- `GET /terminal-output` - Get terminal output (for debugging)

## Configuration

### Mock Data
Mock data for tickets and activities can be found in `main.py`:
- `MOCK_TICKETS`: Sample ticket data
- `MOCK_ACTIVITIES`: Sample activity data
- `COMPANY_INFO`: Technology-Garage company information

### API Keys
- **OPENAI_API_KEY** (Required): For GPT-5.1 LLM routing, intent detection, and all agent capabilities


## License

This project is for demonstration purposes.

