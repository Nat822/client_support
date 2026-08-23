from collections.abc import Callable
from client_support.contracts.tool import ToolDescription, ToolRequest, ToolResult

class ToolRegistry:
    def __init__(self) -> None:
        self._tools: dict[str, tuple[ToolDescription, Callable[[ToolRequest], ToolResult]]] = {}

    def register(self, description: ToolDescription, handler: Callable[[ToolRequest], ToolResult]) -> None:
        if description.name in self._tools:
            raise ValueError(f"Tool already registered: {description.name}")
        self._tools[description.name] = (description, handler)

    def describe(self) -> list[ToolDescription]:
        return [item[0] for item in self._tools.values()]

    def execute(self, request: ToolRequest) -> ToolResult:
        try:
            _, handler = self._tools[request.tool_name]
        except KeyError as exc:
            raise KeyError(f"Unknown tool: {request.tool_name}") from exc
        return handler(request)
