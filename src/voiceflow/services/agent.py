from langchain_anthropic import ChatAnthropic
from langchain.agents import create_react_agent, AgentExecutor
from langchain.memory import ConversationBufferWindowMemory
from langchain.prompts import PromptTemplate
from voiceflow.config import get_settings
from voiceflow.tools import crm, booking, ticketing

settings = get_settings()


class VoiceAgent:
    def __init__(self) -> None:
        self.llm = ChatAnthropic(
            anthropic_api_key=settings.anthropic_api_key,
            model="claude-sonnet-4-20250514",
            temperature=0.7,
            max_tokens=150
        )
        
        self.memory = ConversationBufferWindowMemory(
            k=5,
            return_messages=True
        )
        
        self.tools = self._setup_tools()
        self.agent = self._create_agent()
    
    def _create_agent(self) -> AgentExecutor:
        prompt = PromptTemplate.from_template("""
You are VoiceFlow AI, a helpful voice assistant.

VOICE RULES (CRITICAL):
- Keep responses under 2-3 sentences
- Use natural, conversational language
- NO emojis, markdown, or special characters
- Be aware STT may have errors
- Be concise - audio has limited attention span

Context: {context}
History: {chat_history}
User: {input}
""")
        
        agent = create_react_agent(self.llm, self.tools, prompt)
        return AgentExecutor(agent=agent, tools=self.tools)
    
    def _setup_tools(self) -> list:
        return [
            crm.get_customer_info,
            crm.update_customer_notes,
            crm.get_account_history,
            booking.check_availability,
            booking.book_appointment,
            booking.cancel_appointment,
            booking.reschedule_appointment,
            ticketing.create_ticket,
            ticketing.get_ticket_status,
            ticketing.escalate_ticket,
        ]
    
    async def process(self, user_input: str, context: dict) -> str:
        response = await self.agent.ainvoke({
            "input": user_input,
            "context": str(context),
            "chat_history": self.memory.load_memory_variables({})
        })
        
        self.memory.save_context(
            {"input": user_input},
            {"output": response["output"]}
        )
        
        return response["output"]
