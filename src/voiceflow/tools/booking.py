from langchain.tools import tool
from datetime import datetime, timedelta


@tool
async def check_availability(date: str, time_slot: str) -> dict:
    """Check appointment availability for a given date and time"""
    return {
        "available": True,
        "date": date,
        "time_slot": time_slot
    }


@tool
async def book_appointment(customer_id: str, date: str, time: str, service: str) -> dict:
    """Book an appointment for a customer"""
    return {
        "appointment_id": f"APT-{datetime.now().strftime('%Y%m%d%H%M')}",
        "customer_id": customer_id,
        "date": date,
        "time": time,
        "service": service,
        "confirmed": True
    }


@tool
async def cancel_appointment(appointment_id: str) -> dict:
    """Cancel an existing appointment"""
    return {
        "appointment_id": appointment_id,
        "cancelled": True
    }


@tool
async def reschedule_appointment(appointment_id: str, new_date: str, new_time: str) -> dict:
    """Reschedule an existing appointment"""
    return {
        "appointment_id": appointment_id,
        "new_date": new_date,
        "new_time": new_time,
        "rescheduled": True
    }
