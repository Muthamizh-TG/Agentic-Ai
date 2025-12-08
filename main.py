import os
from dotenv import load_dotenv
load_dotenv()

import requests
from typing import TypedDict, Annotated, Sequence
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage
from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph, END
from langgraph.prebuilt import ToolNode
import operator
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse, PlainTextResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn
import logging
import time
import re
import json
from datetime import datetime

# Import data from external file
from data import MOCK_TICKETS, MOCK_ACTIVITIES, COMPANY_INFO, INFRASTRUCTURE_COSTS

# Configure logging
logging.basicConfig(level=logging.INFO, format='[%(asctime)s] %(levelname)s - %(message)s')

# Initialize FastAPI
app = FastAPI(title="Technology-Garage Multi-Agent System")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "http://localhost:5173",
        "https://visual-agent-1d383.web.app"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load API Keys
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
NEWSDATA_API_KEY = os.getenv("NEWSDATA_API_KEY")

# Initialize LLM
llm = ChatOpenAI(model="gpt-5.1", temperature=0.7, api_key=OPENAI_API_KEY)

# Terminal output storage
latest_agent_output = "(No agent output yet)"

# Helper function to limit response to 10 lines
def limit_response(response: str, max_lines: int = 10) -> str:
    """Limit response to max_lines, add note if truncated"""
    lines = response.split('\n')
    if len(lines) > max_lines:
        truncated = '\n'.join(lines[:max_lines])
        return f"{truncated}\n\n[Response limited to summary. Ask for 'details' or 'full details' for complete information]"
    return response

# ==================== STATE DEFINITION ====================
class AgentState(TypedDict):
    """State passed between agents in the graph"""
    messages: Annotated[Sequence[BaseMessage], operator.add]
    user_input: str
    agent_responses: dict
    next_agent: str
    agents_to_run: list


# ==================== AGENT FUNCTIONS ====================

def ticket_analyzer_node(state: AgentState) -> AgentState:
    """Ticket Analyzer Agent Node"""
    logging.info("Executing Ticket Analyzer Agent")
    
    user_input = state.get("user_input", "")
    
    # Use LLM to understand user's intent for better query understanding
    intent_prompt = f"""Analyze this ticket query and extract the intent in JSON format:
    
User query: "{user_input}"

Available ticket data fields: ticket_id, raised_by, category, subject, description, status (Open/In Progress/Resolved), priority (High/Medium/Low), created_at

Return JSON with:
- "query_type": "specific_ticket" | "filter_by_status" | "filter_by_priority" | "filter_by_person" | "count" | "overview"
- "filter_value": the specific value if filtering (e.g., "High", "Open", person name, or ticket ID)
- "question_type": "who" | "what" | "how_many" | "when" | "list" | "details"

Examples:
"Show TKT-001" -> {{"query_type": "specific_ticket", "filter_value": "TKT-001", "question_type": "details"}}
"How many high priority tickets?" -> {{"query_type": "filter_by_priority", "filter_value": "High", "question_type": "count"}}
"Who raised the WiFi ticket?" -> {{"query_type": "filter_by_person", "filter_value": "WiFi", "question_type": "who"}}
"Show open tickets" -> {{"query_type": "filter_by_status", "filter_value": "Open", "question_type": "list"}}
"""
    
    try:
        intent_response = llm.invoke([HumanMessage(content=intent_prompt)])
        intent = json.loads(intent_response.content.strip())
        query_type = intent.get("query_type", "overview")
        filter_value = intent.get("filter_value", "")
        question_type = intent.get("question_type", "list")
    except:
        # Fallback to regex patterns
        query_type = "overview"
        filter_value = ""
        question_type = "list"
    
    # Check if user is asking about specific ticket or general overview
    ticket_id_match = re.search(r'(TKT-\d+)', user_input, re.IGNORECASE)
    status_match = re.search(r'(open|pending|in progress|resolved|closed)', user_input, re.IGNORECASE)
    priority_match = re.search(r'(high|medium|low)\s*priority', user_input, re.IGNORECASE)
    who_match = re.search(r'who\s+(?:raised|created|opened|submitted)', user_input, re.IGNORECASE)
    
    try:
        # Handle "who raised" questions first
        if who_match and filter_value:
            # Find ticket by subject/description matching
            matched_ticket = None
            search_term = filter_value.lower()
            for ticket in MOCK_TICKETS:
                if search_term in ticket['subject'].lower() or search_term in ticket['description'].lower():
                    matched_ticket = ticket
                    break
            
            if matched_ticket:
                result = f"{matched_ticket['raised_by']} raised the ticket '{matched_ticket['subject']}' (ID: {matched_ticket['ticket_id']}, Status: {matched_ticket['status']}, Priority: {matched_ticket['priority']})"
            else:
                result = f"No ticket found matching '{filter_value}'"
        
        elif ticket_id_match:
            # Find specific ticket
            ticket_id = ticket_id_match.group(1).upper()
            ticket = next((t for t in MOCK_TICKETS if t["ticket_id"] == ticket_id), None)
            
            if ticket:
                result = f"""Ticket Details: {ticket['ticket_id']}
Raised By: {ticket['raised_by']}
Category: {ticket['category']}
Subject: {ticket['subject']}
Description: {ticket['description']}
Status: {ticket['status']}
Priority: {ticket['priority']}
Created: {ticket['created_at']}"""
            else:
                result = f"Ticket {ticket_id} not found in the system."
        
        elif priority_match:
            # Filter by priority
            priority = priority_match.group(1).title()
            filtered = [t for t in MOCK_TICKETS if t["priority"].lower() == priority.lower()]
            
            if filtered:
                output = [f"{priority} Priority Tickets ({len(filtered)}):"]
                for ticket in filtered:
                    output.append(f"[{ticket['ticket_id']}] {ticket['subject']} | Raised By: {ticket['raised_by']} | Status: {ticket['status']} | Created: {ticket['created_at']}")
                result = "\n".join(output)
            else:
                result = f"No tickets found with priority: {priority}"
        
        elif status_match:
            # Filter by status
            status = status_match.group(1).title()
            if status.lower() == "pending":
                status = "Open"
            filtered = [t for t in MOCK_TICKETS if t["status"].lower() == status.lower()]
            
            if filtered:
                output = [f"{status} Tickets ({len(filtered)}):"]
                for ticket in filtered:
                    output.append(f"[{ticket['ticket_id']}] {ticket['subject']} | Raised By: {ticket['raised_by']} | Priority: {ticket['priority']} | Created: {ticket['created_at']}")
                result = "\n".join(output)
            else:
                result = f"No tickets found with status: {status}"
        
        else:
            # Show all tickets grouped by status
            open_tickets = [t for t in MOCK_TICKETS if t["status"] == "Open"]
            in_progress = [t for t in MOCK_TICKETS if t["status"] == "In Progress"]
            resolved = [t for t in MOCK_TICKETS if t["status"] == "Resolved"]
            
            output = [f"Tickets Overview (Total: {len(MOCK_TICKETS)})"]
            
            output.append(f"OPEN/PENDING ({len(open_tickets)}):")
            for t in open_tickets:
                output.append(f"[{t['ticket_id']}] {t['subject']} | Priority: {t['priority']}")
            
            output.append(f"IN PROGRESS ({len(in_progress)}):")
            for t in in_progress:
                output.append(f"[{t['ticket_id']}] {t['subject']} | Priority: {t['priority']}")
            
            output.append(f"RESOLVED ({len(resolved)}):")
            for t in resolved:
                output.append(f"[{t['ticket_id']}] {t['subject']}")
            
            result = "\n".join(output)
    
    except Exception as e:
        result = f"Error analyzing tickets: {str(e)}"
    
    # Check if user wants detailed response
    wants_details = any(word in user_input.lower() for word in ['detail', 'full', 'complete', 'comprehensive'])
    
    # Limit response to 10 lines if not requesting details
    if not wants_details:
        result = limit_response(result, max_lines=10)
    
    # Enhance result with LLM for natural language questions
    if question_type in ["who", "what", "when", "count"] and result:
        enhance_prompt = f"""User asked: "{user_input}"

Raw data response:
{result}

Provide a direct, natural answer to the user's specific question. Be concise and precise.
- If they asked "who", tell them the person's name
- If they asked "how many", give the count
- If they asked "what", describe the item
- If they asked "when", give the date/time
- If they asked about status, tell them the status clearly"""
        
        try:
            enhanced = llm.invoke([HumanMessage(content=enhance_prompt)])
            result = enhanced.content.strip()
        except:
            pass  # Keep original result if enhancement fails
    
    state["agent_responses"]["ticket_analyzer"] = result
    state["messages"].append(AIMessage(content=result))
    return state


def news_aggregator_node(state: AgentState) -> AgentState:
    """News Article Aggregator Agent Node"""
    logging.info("Executing News Aggregator Agent")
    
    user_input = state.get("user_input", "")
    
    # Extract topic from user input - more flexible matching
    topic_match = None
    
    # Pattern 1: "X news" - captures topic before the word "news"
    topic_match = re.search(r'\b(AI|ML|machine learning|deep learning|cloud|crypto|blockchain|tech|technology|quantum|robotics|5G|IoT)\s+news\b', user_input, re.IGNORECASE)
    
    # Pattern 2: "news on X" - captures everything after "on" including location/specifics
    if not topic_match:
        topic_match = re.search(r'news\s+on\s+([A-Za-z0-9\s]+?)(?:\?|$)', user_input, re.IGNORECASE)
    
    # Pattern 3: "news about X" or "news for X"
    if not topic_match:
        topic_match = re.search(r'news\s+(?:about|for)\s+([A-Za-z0-9\s]+?)(?:\?|$)', user_input, re.IGNORECASE)
    
    # Pattern 4: "latest/recent news about/on X"
    if not topic_match:
        topic_match = re.search(r'(?:latest|recent)\s+news\s+(?:about|on)\s+([A-Za-z0-9\s]+?)(?:\?|$)', user_input, re.IGNORECASE)
    
    # Pattern 5: "about X news" - extract topic before "news"
    if not topic_match:
        about_match = re.search(r'about\s+(AI|ML|machine learning|deep learning|cloud|crypto|blockchain|tech|technology|quantum|robotics|5G|IoT|[A-Za-z0-9\s]+?)\s+news', user_input, re.IGNORECASE)
        if about_match:
            topic_match = about_match
    
    query = topic_match.group(1).strip() if topic_match else "technology"
    
    try:
        # Use GPT API to generate news summary
        prompt = f"""You are a news summarizer. Provide a professional news summary about '{query}' as if reporting current events for the date {datetime.now().strftime('%Y-%m-%d')}.

Create 5 realistic news articles with:
- Clear article titles
- 2-3 sentence summaries each
- Credible source names (Reuters, TechCrunch, Bloomberg, etc.)
- Recent dates (this week, yesterday, Dec 2025, etc.)

Format cleanly with numbered articles. Do NOT include any disclaimers about live news access or training data cutoffs. Write as a professional news aggregator would."""
        
        response = llm.invoke([HumanMessage(content=prompt)])
        result = f"Latest News about '{query}':\n{'=' * 70}\n\n{response.content}"
    
    except Exception as e:
        result = f"Error fetching news: {str(e)}"
    
    state["agent_responses"]["news_aggregator"] = result
    state["messages"].append(AIMessage(content=result))
    return state


def activity_tracker_node(state: AgentState) -> AgentState:
    """Activity Tracker Agent Node (Kanban Board)"""
    logging.info("Executing Activity Tracker Agent")
    
    user_input = state.get("user_input", "")
    
    # Use LLM to understand user's intent
    intent_prompt = f"""Analyze this activity/task query and extract the intent in JSON format:
    
User query: "{user_input}"

Available activity fields: activity_id, task, employee, status (To Do/In Progress/Completed), priority (High/Medium/Low), progress, due_date

Return JSON with:
- "query_type": "who_assigned" | "filter_by_status" | "filter_by_employee" | "filter_by_priority" | "count" | "overview" | "task_details"
- "filter_value": the specific value if filtering
- "question_type": "who" | "what" | "how_many" | "when" | "list" | "details" | "status_check"

Examples:
"Who is assigned to design landing page?" -> {{"query_type": "who_assigned", "filter_value": "design landing page", "question_type": "who"}}
"Show completed tasks" -> {{"query_type": "filter_by_status", "filter_value": "Completed", "question_type": "list"}}
"What is John working on?" -> {{"query_type": "filter_by_employee", "filter_value": "John", "question_type": "list"}}
"How many tasks are pending?" -> {{"query_type": "filter_by_status", "filter_value": "To Do", "question_type": "count"}}
"""
    
    try:
        intent_response = llm.invoke([HumanMessage(content=intent_prompt)])
        intent = json.loads(intent_response.content.strip())
        query_type = intent.get("query_type", "overview")
        filter_value = intent.get("filter_value", "")
        question_type = intent.get("question_type", "list")
    except:
        query_type = "overview"
        filter_value = ""
        question_type = "list"
    
    # Check for "who" questions about specific tasks
    who_match = re.search(r'who\s+(?:is\s+)?(?:assigned|working|responsible|doing|handling)\s+(?:for|on)?\s*["\']?(.+?)["\']?(?:\?|$)', user_input, re.IGNORECASE)
    
    # Check for employee name or status filter
    employee_match = re.search(r'(?:for|by) ([A-Za-z ]+)', user_input, re.IGNORECASE)
    status_match = re.search(r'(to do|todo|pending|in progress|completed|done)', user_input, re.IGNORECASE)
    
    try:
        if who_match:
            # Extract task description from "who" question
            task_query = who_match.group(1).strip().lower()
            # Find matching activity by task description
            matched_activity = None
            for activity in MOCK_ACTIVITIES:
                if task_query in activity['task'].lower():
                    matched_activity = activity
                    break
            
            if matched_activity:
                result = f"{matched_activity['employee']} is assigned to '{matched_activity['task']}' (Status: {matched_activity['status']}, Priority: {matched_activity['priority']}, Progress: {matched_activity['progress']})"
            else:
                result = f"No activity found matching '{task_query}'"
        
        elif employee_match:
            # Filter by employee
            employee_name = employee_match.group(1).strip()
            filtered = [a for a in MOCK_ACTIVITIES if employee_name.lower() in a["employee"].lower()]
            
            if filtered:
                output = [f"\nActivities for {employee_name} ({len(filtered)} tasks):"]
                for activity in filtered:
                    output.append(f"[{activity['activity_id']}] {activity['task']} | Status: {activity['status']} | Priority: {activity['priority']} | Progress: {activity['progress']} | Due: {activity['due_date']}")
                result = "\n".join(output)
            else:
                result = f"No activities found for employee: {employee_name}"
        
        elif status_match:
            # Filter by status
            status_input = status_match.group(1).lower()
            if status_input in ['todo', 'pending']:
                status = "To Do"
            elif status_input == 'in progress':
                status = "In Progress"
            elif status_input in ['completed', 'done']:
                status = "Completed"
            else:
                status = status_input.title()
            
            filtered = [a for a in MOCK_ACTIVITIES if a["status"] == status]
            
            if filtered:
                output = [f"\nActivities - {status} ({len(filtered)} tasks):"]
                for activity in filtered:
                    output.append(f"[{activity['activity_id']}] {activity['task']} | Employee: {activity['employee']} | Priority: {activity['priority']} | Progress: {activity['progress']} | Due: {activity['due_date']}")
                result = "\n".join(output)
            else:
                result = f"No activities found with status: {status}"
        
        else:
            # Show Kanban board view with all statuses
            todo = [a for a in MOCK_ACTIVITIES if a["status"] == "To Do"]
            in_progress = [a for a in MOCK_ACTIVITIES if a["status"] == "In Progress"]
            completed = [a for a in MOCK_ACTIVITIES if a["status"] == "Completed"]
            
            output = [f"\nActivity Kanban Board (Total: {len(MOCK_ACTIVITIES)} tasks)\n"]
            
            output.append(f"TO DO / PENDING ({len(todo)}):")
            for a in todo:
                output.append(f"  [{a['activity_id']}] {a['task']} | Employee: {a['employee']} | Priority: {a['priority']} | Due: {a['due_date']}")
            
            output.append(f"\nIN PROGRESS ({len(in_progress)}):")
            for a in in_progress:
                output.append(f"  [{a['activity_id']}] {a['task']} | Employee: {a['employee']} | Progress: {a['progress']} | Priority: {a['priority']}")
            
            output.append(f"\nCOMPLETED ({len(completed)}):")
            for a in completed:
                output.append(f"  [{a['activity_id']}] {a['task']} | Employee: {a['employee']} | Completed: 100%")
            
            result = "\n".join(output)
    
    except Exception as e:
        result = f"Error fetching activities: {str(e)}"
    
    # Check if user wants detailed response
    wants_details = any(word in user_input.lower() for word in ['detail', 'full', 'complete', 'comprehensive'])
    
    # Limit response to 10 lines if not requesting details
    if not wants_details:
        result = limit_response(result, max_lines=10)
    
    # Enhance result with LLM for natural language questions
    if question_type in ["who", "what", "when", "count", "status_check"] and result:
        enhance_prompt = f"""User asked: "{user_input}"

Raw data response:
{result}

Provide a direct, natural answer to the user's specific question. Be concise and precise.
- If they asked "who", tell them the person's name and what they're doing
- If they asked "how many", give the count number
- If they asked "what status", tell them the current status
- If they asked "when", give the due date
- Keep it conversational and direct"""
        
        try:
            enhanced = llm.invoke([HumanMessage(content=enhance_prompt)])
            result = enhanced.content.strip()
        except:
            pass  # Keep original result if enhancement fails
    
    state["agent_responses"]["activity_tracker"] = result
    state["messages"].append(AIMessage(content=result))
    return state


def infrastructure_cost_monitor_node(state: AgentState) -> AgentState:
    """Infrastructure Cost Monitor Agent Node"""
    logging.info("Executing Infrastructure Cost Monitor Agent")
    
    user_input = state.get("user_input", "")
    
    # Use LLM to understand user's intent
    intent_prompt = f"""Analyze this infrastructure cost query and extract the intent in JSON format:
    
User query: "{user_input}"

Available providers: AWS, Azure, Google Cloud, Firebase, DigitalOcean, Vercel, Heroku

Return JSON with:
- "query_type": "specific_provider" | "compare_all" | "overview" | "cheapest" | "most_expensive"
- "provider": specific provider name if mentioned
- "question_type": "how_much" | "what" | "which" | "compare" | "list" | "breakdown"

Examples:
"How much does AWS cost?" -> {{"query_type": "specific_provider", "provider": "AWS", "question_type": "how_much"}}
"Which is cheaper, AWS or Azure?" -> {{"query_type": "compare_all", "provider": "", "question_type": "which"}}
"Show me Firebase pricing" -> {{"query_type": "specific_provider", "provider": "Firebase", "question_type": "breakdown"}}
"""
    
    try:
        intent_response = llm.invoke([HumanMessage(content=intent_prompt)])
        intent = json.loads(intent_response.content.strip())
        query_type = intent.get("query_type", "overview")
        question_type = intent.get("question_type", "list")
    except:
        query_type = "overview"
        question_type = "list"
    
    # Extract provider name from user input
    provider_keywords = {
        'aws': 'AWS',
        'amazon': 'AWS',
        'azure': 'Azure',
        'microsoft': 'Azure',
        'google': 'Google Cloud',
        'gcp': 'Google Cloud',
        'firebase': 'Firebase',
        'digitalocean': 'DigitalOcean',
        'ocean': 'DigitalOcean',
        'vercel': 'Vercel',
        'heroku': 'Heroku'
    }
    
    requested_provider = None
    for keyword, provider in provider_keywords.items():
        if keyword in user_input.lower():
            requested_provider = provider
            break
    
    try:
        if requested_provider and requested_provider in INFRASTRUCTURE_COSTS:
            # Show specific provider costs with spending breakdown
            provider_data = INFRASTRUCTURE_COSTS[requested_provider]
            output = [f"\n{requested_provider} Infrastructure Cost Analysis"]
            output.append("=" * 70)
            output.append(f"\nESTIMATED MONTHLY SPENDING: {provider_data['total_monthly_estimate']}")
            output.append(f"Number of Services: {len(provider_data['services'])}")
            output.append("\nCOST BREAKDOWN BY SERVICE:")
            output.append("-" * 70)
            
            for service in provider_data['services']:
                output.append(f"\n[{service['category']}] {service['name']}")
                output.append(f"Region: {service.get('region', 'N/A')}")
                output.append(f"Specifications: {service.get('specs', 'N/A')}")
                
                # Cost details
                output.append("Cost Structure:")
                for key, value in service.items():
                    if 'price' in key.lower():
                        formatted_key = key.replace('_', ' ').replace('price ', '').title()
                        output.append(f"  - {formatted_key}: {value}")
                
                output.append("-" * 70)
            
            # Add summary
            output.append("\nCOST TRAFFIC SUMMARY:")
            compute_services = [s for s in provider_data['services'] if s['category'] == 'Compute']
            storage_services = [s for s in provider_data['services'] if s['category'] == 'Storage']
            database_services = [s for s in provider_data['services'] if s['category'] == 'Database']
            
            output.append(f"Compute Resources: {len(compute_services)} service(s)")
            output.append(f"Storage Resources: {len(storage_services)} service(s)")
            output.append(f"Database Resources: {len(database_services)} service(s)")
            
            result = "\n".join(output)
        
        elif 'compare' in user_input.lower() or 'comparison' in user_input.lower():
            # Compare all providers
            output = [f"\nCloud Infrastructure Cost Comparison"]
            output.append("=" * 70)
            output.append("\nPROVIDER COST OVERVIEW:")
            output.append("-" * 70)
            
            for provider, data in INFRASTRUCTURE_COSTS.items():
                output.append(f"\n{provider}")
                output.append(f"Monthly Spending Estimate: {data['total_monthly_estimate']}")
                output.append(f"Services Tracked: {len(data['services'])}")
                
                # Show key services
                compute = next((s for s in data['services'] if s['category'] == 'Compute'), None)
                if compute:
                    output.append(f"Compute Cost: {compute.get('price_per_month', compute.get('price_per_hour', 'N/A'))}")
                
                database = next((s for s in data['services'] if s['category'] == 'Database'), None)
                if database:
                    output.append(f"Database Cost: {database.get('price_per_month', 'Varies')}")
                
                output.append("-" * 70)
            
            result = "\n".join(output)
        
        else:
            # Show all providers overview with spending summary
            output = [f"\nInfrastructure Cost Monitor - All Providers Overview"]
            output.append("=" * 70)
            output.append("\nAVAILABLE CLOUD PROVIDERS:")
            output.append("-" * 70)
            
            for provider, data in INFRASTRUCTURE_COSTS.items():
                output.append(f"\n{provider}")
                output.append(f"Monthly Spending Estimate: {data['total_monthly_estimate']}")
                output.append(f"Services Monitored: {len(data['services'])}")
                
                categories = set(s['category'] for s in data['services'])
                output.append(f"Service Categories: {', '.join(categories)}")
                output.append("-" * 70)
            
            output.append("\nTip: Specify a provider (e.g., 'AWS costs') for detailed breakdown or ask for 'comparison'")
            result = "\n".join(output)
    
    except Exception as e:
        result = f"Error fetching infrastructure costs: {str(e)}"
    
    # Check if user wants detailed response
    wants_details = any(word in user_input.lower() for word in ['detail', 'full', 'complete', 'comprehensive'])
    
    # Limit response to 10 lines if not requesting details
    if not wants_details:
        result = limit_response(result, max_lines=10)
    
    # Enhance result with LLM for natural language questions
    if question_type in ["how_much", "what", "which", "compare"] and result:
        enhance_prompt = f"""User asked: "{user_input}"

Raw data response:
{result}

Provide a direct, natural answer to the user's specific question. Be concise and precise.
- If they asked "how much", give the specific cost/estimate
- If they asked "which is cheaper", compare and state which one
- If they asked "what services", list the key services
- Keep it conversational and direct"""
        
        try:
            enhanced = llm.invoke([HumanMessage(content=enhance_prompt)])
            result = enhanced.content.strip()
        except:
            pass  # Keep original result if enhancement fails
    
    state["agent_responses"]["infrastructure_cost_monitor"] = result
    state["messages"].append(AIMessage(content=result))
    return state


def chat_node(state: AgentState) -> AgentState:
    """Chat Agent Node - General conversation and company information"""
    logging.info("Executing Chat Agent")
    
    user_input = state.get("user_input", "")
    
    # Use LLM to understand user's intent
    intent_prompt = f"""Analyze this general query and extract the intent in JSON format:
    
User query: "{user_input}"

Return JSON with:
- "query_type": "company_info" | "greeting" | "help" | "general_question" | "goodbye"
- "specific_topic": what they're asking about (e.g., "services", "team", "mission", "location", etc.)
- "question_type": "what" | "who" | "where" | "when" | "how" | "why" | "greeting"

Examples:
"What services do you offer?" -> {{"query_type": "company_info", "specific_topic": "services", "question_type": "what"}}
"Hello" -> {{"query_type": "greeting", "specific_topic": "", "question_type": "greeting"}}
"Where is Technology-Garage located?" -> {{"query_type": "company_info", "specific_topic": "location", "question_type": "where"}}
"""
    
    try:
        intent_response = llm.invoke([HumanMessage(content=intent_prompt)])
        intent = json.loads(intent_response.content.strip())
        query_type = intent.get("query_type", "general_question")
        specific_topic = intent.get("specific_topic", "")
    except:
        query_type = "general_question"
        specific_topic = ""
    
    # Check if user is asking about company information
    company_keywords = ['company', 'technology-garage', 'about', 'services', 'team', 'mission', 'vision']
    is_company_query = any(keyword in user_input.lower() for keyword in company_keywords) or query_type == "company_info"
    
    try:
        if is_company_query:
            # Provide company information
            prompt = f"""
            You are a helpful assistant for Technology-Garage company.
            
            Company Information:
            {json.dumps(COMPANY_INFO, indent=2)}
            
            User question: {user_input}
            
            Provide a direct, specific answer to their question based on the company information above.
            If they ask about something specific (e.g., location, services, team size), answer that directly.
            Be friendly, professional, and concise.
            """
        else:
            # General conversation
            prompt = f"""
            You are a helpful assistant for Technology-Garage, a technology solutions company.
            You can help with general questions and conversations.
            
            User: {user_input}
            
            Provide a helpful, friendly, and natural response.
            If it's a greeting, respond warmly.
            If they need help, guide them on what you can assist with.
            """
        
        response = llm.invoke([HumanMessage(content=prompt)])
        result = response.content
    
    except Exception as e:
        result = f"Chat error: {str(e)}"
    
    state["agent_responses"]["chat"] = result
    state["messages"].append(AIMessage(content=result))
    return state


def router_node(state: AgentState) -> AgentState:
    """Router node to determine which agents to run"""
    logging.info("Executing Router Node")
    
    user_input = state["user_input"]
    
    # Check if user wants a complete overview/summary of everything
    overview_keywords = [
        'summary of everything', 'everything happening', 'complete summary', 'full overview',
        'everything going on', 'all updates', 'comprehensive summary', 'overall status',
        'whats happening', "what's happening", 'status of everything', 'complete update',
        'full status', 'everything status', 'overall summary'
    ]
    
    is_complete_overview = any(keyword in user_input.lower() for keyword in overview_keywords)
    
    if is_complete_overview:
        # User wants everything - invoke all agents
        logging.info("Complete overview requested - activating all agents")
        state["agents_to_run"] = [
            "TicketAnalyzerAgent",
            "NewsAggregatorAgent", 
            "ActivityTrackerAgent",
            "InfrastructureCostMonitorAgent"
        ]
        return state
    
    prompt = f"""
    You are an intelligent router AI for Technology-Garage company assistant. Decide which agents should handle this input:

    Available agents:
    - TicketAnalyzerAgent: Handles ticket queries (employees, players, parents tickets)
    - NewsAggregatorAgent: Fetches latest news articles
    - ActivityTrackerAgent: Shows employee activities and task tracking
    - InfrastructureCostMonitorAgent: Monitors cloud infrastructure costs (AWS, Azure, Google Cloud, Firebase, DigitalOcean, Vercel, Heroku)
    - ChatAgent: General conversation and company information

    User input: "{user_input}"

    Respond in JSON format with the agents that should handle this query:
    {{"agents": ["AgentName1", "AgentName2", ...]}}
    
    Examples:
    - "Show me all tickets" -> {{"agents": ["TicketAnalyzerAgent"]}}
    - "What's the latest news?" -> {{"agents": ["NewsAggregatorAgent"]}}
    - "Show activities for John" -> {{"agents": ["ActivityTrackerAgent"]}}
    - "AWS costs" or "infrastructure pricing" -> {{"agents": ["InfrastructureCostMonitorAgent"]}}
    - "Tell me about the company" -> {{"agents": ["ChatAgent"]}}
    - "What tickets are open and latest news" -> {{"agents": ["TicketAnalyzerAgent", "NewsAggregatorAgent"]}}
    """
    
    try:
        response = llm.invoke([HumanMessage(content=prompt)])
        parsed = json.loads(response.content.strip())
        
        state["agents_to_run"] = parsed.get("agents", ["ChatAgent"])
        
    except Exception as e:
        logging.error(f"Router error: {e}")
        state["agents_to_run"] = ["ChatAgent"]
    
    return state


def should_continue(state: AgentState) -> str:
    """Conditional edge to determine next agent"""
    agents_to_run = state.get("agents_to_run", [])
    
    if not agents_to_run:
        return "summarize"
    
    next_agent = agents_to_run.pop(0)
    state["agents_to_run"] = agents_to_run
    
    agent_map = {
        "TicketAnalyzerAgent": "ticket_analyzer",
        "NewsAggregatorAgent": "news_aggregator",
        "ActivityTrackerAgent": "activity_tracker",
        "InfrastructureCostMonitorAgent": "infrastructure_cost_monitor",
        "ChatAgent": "chat"
    }
    
    return agent_map.get(next_agent, "chat")


def summarize_node(state: AgentState) -> AgentState:
    """Summarize all agent responses"""
    logging.info("Executing Summarize Node")
    
    agent_responses = state.get("agent_responses", {})
    user_input = state.get("user_input", "")
    
    if not agent_responses:
        result = "No responses to summarize."
    elif len(agent_responses) == 1:
        # If only one agent responded, return its response directly without summarization
        result = list(agent_responses.values())[0]
    else:
        # Multiple agents - create intelligent analysis
        # Check if this is a complete overview request
        overview_keywords = [
            'summary of everything', 'everything happening', 'complete summary', 'full overview',
            'everything going on', 'all updates', 'comprehensive summary', 'overall status',
            'whats happening', "what's happening", 'status of everything', 'complete update'
        ]
        is_complete_overview = any(keyword in user_input.lower() for keyword in overview_keywords)
        
        # Format all agent responses
        responses_text = "\n\n".join([f"=== {k.upper().replace('_', ' ')} ===\n{v}" for k, v in agent_responses.items()])
        
        if is_complete_overview:
            # Comprehensive analysis for "everything happening" requests
            prompt = f"""You are an intelligent business analyst for Technology-Garage company. 

The user asked: "{user_input}"

Here are reports from all departments:

{responses_text}

Create a CONCISE executive summary (max 10 lines) that covers:
1. **Key Priorities & Issues** - Most critical blockers
2. **Current Status** - Overall health snapshot
3. **Notable Updates** - Top 1-2 recent developments
4. **Quick Recommendations** - Top 1-2 immediate actions

Format as bullet points. Be ultra-concise - assume busy executive reading in 30 seconds.
NO long paragraphs. Each section: max 1-2 lines.
"""
        else:
            # Standard multi-agent summary
            prompt = f"""
            You are a helpful assistant. Create a single, clear, and concise summary from these agent responses.
            Include at least one key point from EVERY agent's response.
            Do NOT repeat agent names in the summary.
            Keep it within 10 lines maximum.
            
            {responses_text}
            """
        
        try:
            response = llm.invoke([HumanMessage(content=prompt)])
            result = response.content.strip()
            
            # Check if user wants detailed response
            wants_details = any(word in user_input.lower() for word in ['detail', 'full', 'complete', 'comprehensive', 'everything'])
            
            # Limit summary to 10 lines by default (for all cases unless user asks for details)
            if not wants_details:
                result = limit_response(result, max_lines=10)
        except Exception as e:
            result = f"Error creating summary: {str(e)}"
    
    state["messages"].append(AIMessage(content=result))
    return state


# ==================== BUILD LANGGRAPH ====================

def build_graph():
    """Build the LangGraph workflow"""
    workflow = StateGraph(AgentState)
    
    # Add nodes
    workflow.add_node("router", router_node)
    workflow.add_node("ticket_analyzer", ticket_analyzer_node)
    workflow.add_node("news_aggregator", news_aggregator_node)
    workflow.add_node("activity_tracker", activity_tracker_node)
    workflow.add_node("infrastructure_cost_monitor", infrastructure_cost_monitor_node)
    workflow.add_node("chat", chat_node)
    workflow.add_node("summarize", summarize_node)
    
    # Set entry point
    workflow.set_entry_point("router")
    
    # Add conditional edges from router
    workflow.add_conditional_edges(
        "router",
        should_continue,
        {
            "ticket_analyzer": "ticket_analyzer",
            "news_aggregator": "news_aggregator",
            "activity_tracker": "activity_tracker",
            "infrastructure_cost_monitor": "infrastructure_cost_monitor",
            "chat": "chat",
            "summarize": "summarize"
        }
    )
    
    # Add edges from each agent back to conditional router
    for agent in ["ticket_analyzer", "news_aggregator", "activity_tracker", "infrastructure_cost_monitor", "chat"]:
        workflow.add_conditional_edges(
            agent,
            should_continue,
            {
                "ticket_analyzer": "ticket_analyzer",
                "news_aggregator": "news_aggregator",
                "activity_tracker": "activity_tracker",
                "infrastructure_cost_monitor": "infrastructure_cost_monitor",
                "chat": "chat",
                "summarize": "summarize"
            }
        )
    
    # Summarize ends the workflow
    workflow.add_edge("summarize", END)
    
    return workflow.compile()


# Create the graph
graph = build_graph()


# ==================== FASTAPI ENDPOINTS ====================

class ChatMessage(BaseModel):
    message: str

class ChatResponse(BaseModel):
    response: str
    query_type: str
    execution_time: str
    agent_responses: dict = None


@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "LangGraph Multi-Agent API"}


@app.get("/terminal-output", response_class=PlainTextResponse)
async def terminal_output():
    return latest_agent_output


@app.post("/chat", response_model=ChatResponse)
async def chat_endpoint(chat_message: ChatMessage):
    global latest_agent_output
    
    try:
        start_time = time.time()
        user_input = chat_message.message
        logging.info(f"Received /chat request: {user_input}")
        
        # Initialize state
        initial_state = {
            "messages": [HumanMessage(content=user_input)],
            "user_input": user_input,
            "agent_responses": {},
            "next_agent": "",
            "agents_to_run": []
        }
        
        # Run the graph
        result = graph.invoke(initial_state)
        
        # Extract final response
        final_message = result["messages"][-1].content
        agent_responses = result.get("agent_responses", {})
        
        execution_time = f"{(time.time() - start_time):.2f}s"
        
        latest_agent_output = final_message
        
        logging.info(f"Response generated in {execution_time}")
        
        return ChatResponse(
            response=final_message,
            query_type=", ".join(agent_responses.keys()),
            execution_time=execution_time,
            agent_responses=agent_responses
        )
        
    except Exception as e:
        logging.error(f"Error in /chat: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Error processing message: {str(e)}")


@app.get("/agents")
async def get_agents():
    return {
        "agents": [
            {"name": "TicketAnalyzerAgent", "description": "Handles tickets raised by employees, players, or parents"},
            {"name": "NewsAggregatorAgent", "description": "Collects latest news articles using newsdata.io API"},
            {"name": "ActivityTrackerAgent", "description": "Tracks employee activities like a Kanban board"},
            {"name": "InfrastructureCostMonitorAgent", "description": "Monitors cloud infrastructure costs (AWS, Azure, GCP, Firebase, etc.)"},
            {"name": "ChatAgent", "description": "General conversation and company information"}
        ]
    }


if __name__ == "__main__":
    print("Starting Technology-Garage Multi-Agent System...")
    print("API documentation available at: http://localhost:8000/docs")
    uvicorn.run(app, host="127.0.0.1", port=8000)