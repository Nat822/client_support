import json
import os
from dataclasses import dataclass
from urllib import request

from client_support.agent.nextstep import AgentContext, AgentPlan, ToolCall, ToolResult


@dataclass(slots=True)
class NeuralDeepPlannerProvider:
    api_key: str
    model: str
    base_url: str

    @classmethod
    def from_environment(cls) -> "NeuralDeepPlannerProvider":
        api_key = os.environ.get("NEURALDEEP_API_KEY")
        if not api_key:
            raise ValueError("NEURALDEEP_API_KEY is required")
        return cls(
            api_key=api_key,
            model=os.environ.get("NEURALDEEP_MODEL", "qwen3.6-35b-a3b"),
            base_url=os.environ.get("NEURALDEEP_BASE_URL", "https://api.neuraldeep.ru/v1/chat/completions"),
        )

    def plan(self, *, context: AgentContext, history: list[ToolResult]) -> AgentPlan:
        system = (
            "You are a customer-support planning agent. Return JSON only. "
            "Choose only from the supplied tools. Never invent tools or arguments. "
            "If the task is complete, return done=true and a customer-safe response."
        )
        tools = [
            {"name": "lookup_order", "description": "Read order status by order_id", "arguments": {"order_id": "string"}},
            {"name": "lookup_ticket", "description": "Read helpdesk ticket data", "arguments": {"ticket_id": "string"}},
        ]
        payload = {
            "model": self.model,
            "temperature": 0,
            "messages": [
                {"role": "system", "content": system},
                {"role": "user", "content": json.dumps({
                    "context": {"ticket_id": context.ticket_id, "category": context.category, "ticket_text": context.ticket_text, "extracted": context.extracted},
                    "history": [{"tool_name": x.tool_name, "success": x.success, "output": x.output, "error": x.error} for x in history],
                    "tools": tools,
                    "schema": {"reason": "string", "done": "boolean", "response": "string|null", "calls": [{"tool_name": "string", "arguments": "object"}]},
                })},
            ],
            "response_format": {"type": "json_object"},
        }
        req = request.Request(self.base_url, data=json.dumps(payload).encode(), headers={
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        })
        with request.urlopen(req, timeout=30) as response:
            body = json.loads(response.read())
        content = body["choices"][0]["message"]["content"]
        data = json.loads(content)
        calls = [ToolCall(item["tool_name"], item.get("arguments", {})) for item in data.get("calls", [])]
        return AgentPlan(data.get("reason", ""), calls, bool(data.get("done", False)), data.get("response"))
