from langchain.tools import tool


@tool
async def get_customer_info(phone_number: str) -> dict:
    """Retrieve customer information from CRM by phone number"""
    return {
        "name": "Customer",
        "account_id": "12345",
        "status": "active"
    }


@tool
async def update_customer_notes(account_id: str, notes: str) -> dict:
    """Update customer notes in CRM"""
    return {
        "account_id": account_id,
        "notes_updated": True
    }


@tool
async def get_account_history(account_id: str) -> dict:
    """Get customer account history"""
    return {
        "account_id": account_id,
        "recent_interactions": [],
        "total_calls": 0
    }
