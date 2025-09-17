#!/usr/bin/env python3
"""
Virtual Advisory Board - Render Deployment
Simple HTTP wrapper for MCP-style advisory board
"""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional
import uvicorn
import os

app = FastAPI(title="Virtual Advisory Board", version="1.0.0")

# Request models
class ToolRequest(BaseModel):
    tool: str
    arguments: dict = {}

# Advisory Board Members Database
ADVISORS = {
    "tim_cook": {
        "name": "Tim Cook",
        "role": "CEO & Technology Strategy Advisor",
        "background": """Tim Cook focuses on operational excellence, long-term value creation, and ethical technology leadership. Known for Apple's privacy-first approach and sustainable business practices."""
    },
    "warren_buffett": {
        "name": "Warren Buffett", 
        "role": "Investment & Business Strategy Advisor",
        "background": """Warren Buffett emphasizes value investing, business fundamentals, and long-term wealth building. Famous for seeking businesses with sustainable competitive advantages ("moats")."""
    },
    "maya_angelou": {
        "name": "Maya Angelou",
        "role": "Leadership & Cultural Wisdom Advisor", 
        "background": """Maya Angelou brings wisdom about authentic leadership, human dignity, and building resilient organizations through understanding people and culture."""
    },
    "jamie_dimon": {
        "name": "Jamie Dimon",
        "role": "Financial Strategy & Risk Management Advisor",
        "background": """Jamie Dimon focuses on rigorous risk management, financial strength, and crisis leadership. Known for JPMorgan's "fortress balance sheet" approach."""
    },
    "charlie_munger": {
        "name": "Charlie Munger", 
        "role": "Mental Models & Decision Architecture Advisor",
        "background": """Charlie Munger applies multidisciplinary thinking and mental models to business decisions. Famous for "inverting" problems and avoiding cognitive biases."""
    },
    "art_gensler": {
        "name": "Art Gensler",
        "role": "Design Thinking & Organizational Culture Advisor",
        "background": """Art Gensler focuses on human-centered design, organizational culture, and creating positive experiences for people and communities."""
    }
}

@app.get("/")
async def root():
    """Server information endpoint"""
    return {
        "name": "Virtual Advisory Board",
        "version": "1.0.0", 
        "description": "Consult with virtual versions of famous business leaders",
        "tools": [
            {"name": "list_advisors", "description": "Get list of advisory board members"},
            {"name": "consult_advisor", "description": "Consult with a specific advisor"},
            {"name": "board_meeting", "description": "Hold virtual board meeting"},
            {"name": "advisor_philosophy", "description": "Learn advisor's background"}
        ]
    }

@app.post("/tools")
async def execute_tool(request: ToolRequest):
    """Execute advisory board tools"""
    try:
        if request.tool == "list_advisors":
            return {"result": list_advisors()}
        
        elif request.tool == "consult_advisor":
            advisor_name = request.arguments.get("advisor_name", "")
            situation = request.arguments.get("situation", "")
            context = request.arguments.get("context", "")
            return {"result": consult_advisor(advisor_name, situation, context)}
        
        elif request.tool == "board_meeting":
            topic = request.arguments.get("topic", "")
            background_info = request.arguments.get("background_info", "")
            return {"result": board_meeting(topic, background_info)}
        
        elif request.tool == "advisor_philosophy":
            advisor_name = request.arguments.get("advisor_name", "")
            return {"result": advisor_philosophy(advisor_name)}
        
        else:
            raise HTTPException(status_code=400, detail=f"Unknown tool: {request.tool}")
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

def list_advisors():
    """Get list of all advisory board members"""
    advisor_list = []
    for advisor_id, advisor in ADVISORS.items():
        advisor_list.append(f"• {advisor['name']} - {advisor['role']}")
    
    return f"""Your Virtual Advisory Board Members:

{chr(10).join(advisor_list)}

Use 'consult_advisor' to get specific advice from any board member."""

def consult_advisor(advisor_name: str, situation: str, context: str = ""):
    """Consult with a specific advisory board member"""
    
    # Find the advisor
    advisor_key = None
    for key, advisor in ADVISORS.items():
        if advisor_name.lower() in advisor['name'].lower():
            advisor_key = key
            break
    
    if not advisor_key:
        available_advisors = [advisor['name'] for advisor in ADVISORS.values()]
        return f"Advisor '{advisor_name}' not found. Available advisors: {', '.join(available_advisors)}"
    
    advisor = ADVISORS[advisor_key]
    
    response = f"""🎯 **Advisory Session with {advisor['name']}**

**Your Situation:** {situation}

**{advisor['name']}'s Perspective:**

{advisor['background']}

**My advice for your situation:**

Based on my experience and philosophy, here's how I'd approach this:

**Key Questions to Consider:**
- What are the fundamental drivers of success here?
- How does this align with your long-term vision and values?
- What are the potential risks and how can you mitigate them?

**Strategic Recommendations:**
1. Focus on the core fundamentals that will drive lasting value
2. Build systems and processes that can scale sustainably  
3. Consider multiple scenarios and prepare for different outcomes
4. Don't neglect the human elements - culture and people matter
5. Measure what matters and track your progress consistently

**Red Flags to Watch:**
Be wary of decisions driven by short-term pressures rather than sound strategic thinking.

**Next Steps:**
- Define clear success metrics
- Identify key assumptions and test them
- Build in regular review and adjustment processes

---
*This advice reflects {advisor['name']}'s known approach and philosophy.*"""

    if context:
        response += f"\n\n**Additional Context Considered:** {context}"
    
    return response

def board_meeting(topic: str, background_info: str = ""):
    """Hold a virtual board meeting"""
    
    return f"""📋 **Virtual Advisory Board Meeting**

**Topic:** {topic}
**Background:** {background_info}

---

**Board Discussion:**

**Tim Cook (Operations):** "We need to think about scalability and operational efficiency. How does this decision impact your core processes and values? What systems will you need to support this long-term?"

**Warren Buffett (Strategy):** "Let's focus on the fundamentals. Does this make your business stronger or weaker? Can you explain the value creation in simple terms? Would you be comfortable with this decision for the next 10 years?"

**Maya Angelou (Leadership):** "What story does this decision tell about your leadership? How will this impact the people who depend on you? Are you making this choice from a place of authenticity and care?"

**Jamie Dimon (Risk Management):** "What could go wrong here? What's your downside scenario and are you prepared for it? Show me your risk management framework and capital requirements."

**Charlie Munger (Decision Framework):** "Let's invert this problem. Why might this fail? What cognitive biases might be affecting your thinking? Are you considering second and third-order effects?"

**Art Gensler (Culture & Design):** "How will this affect the human experience for your customers and employees? What would the ideal outcome look like from a people perspective? How do you design for positive culture and experience?"

---

**Board Consensus:**
1. Ensure strong operational foundations and systems
2. Verify the business fundamentals and value creation story
3. Consider the human and cultural impact
4. Prepare for multiple scenarios including stress cases
5. Build in measurement and feedback mechanisms

**Recommended Next Steps:**
Return with specific implementation details for deeper analysis, or consult individual advisors for specialized expertise."""

def advisor_philosophy(advisor_name: str):
    """Get detailed philosophy of a specific advisor"""
    
    # Find the advisor
    advisor_key = None
    for key, advisor in ADVISORS.items():
        if advisor_name.lower() in advisor['name'].lower():
            advisor_key = key
            break
    
    if not advisor_key:
        available_advisors = [advisor['name'] for advisor in ADVISORS.values()]
        return f"Advisor '{advisor_name}' not found. Available advisors: {', '.join(available_advisors)}"
    
    advisor = ADVISORS[advisor_key]
    return f"""📚 **Philosophy & Background: {advisor['name']}**

**Role:** {advisor['role']}

**Background & Approach:**
{advisor['background']}

**Key Principles:**
- Focus on long-term value creation over short-term gains
- Build sustainable competitive advantages
- Prioritize operational excellence and systematic thinking
- Consider the human impact of all decisions
- Maintain strong ethical foundations

---

Use 'consult_advisor' to get specific advice from {advisor['name']} on your business situations."""

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
