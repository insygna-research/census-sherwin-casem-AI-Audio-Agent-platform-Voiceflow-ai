from pydantic import BaseModel
from typing import Optional
from enum import Enum


class Intent(Enum):
    BILLING_INQUIRY = "billing"
    TECHNICAL_SUPPORT = "support"
    APPOINTMENT_BOOKING = "appointment"
    GENERAL_INFO = "info"
    ESCALATION_REQUEST = "escalate"
    ORDER_STATUS = "order"


class ConversationMessage(BaseModel):
    role: str
    content: str
    timestamp: str


class ConversationContext(BaseModel):
    phone_number: str
    customer_name: Optional[str] = None
    account_id: Optional[str] = None
    intent: Optional[Intent] = None
    metadata: dict = {}
