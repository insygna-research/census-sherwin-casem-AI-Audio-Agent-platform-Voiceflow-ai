from langchain.tools import tool
from datetime import datetime


@tool
async def create_ticket(customer_id: str, issue: str, priority: str = "medium") -> dict:
    """Create a support ticket"""
    return {
        "ticket_id": f"TKT-{datetime.now().strftime('%Y%m%d%H%M')}",
        "customer_id": customer_id,
        "issue": issue,
        "priority": priority,
        "status": "open",
        "created_at": datetime.now().isoformat()
    }


@tool
async def get_ticket_status(ticket_id: str) -> dict:
    """Get the status of a support ticket"""
    return {
        "ticket_id": ticket_id,
        "status": "in_progress",
        "assigned_to": "Support Team"
    }


@tool
async def escalate_ticket(ticket_id: str, reason: str) -> dict:
    """Escalate a support ticket to higher priority"""
    return {
        "ticket_id": ticket_id,
        "escalated": True,
        "reason": reason,
        "new_priority": "high"
    }
