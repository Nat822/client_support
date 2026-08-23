from enum import StrEnum
from typing import Any
from pydantic import BaseModel

class ToolRisk(StrEnum):
    READ_ONLY = "read_only"
    SIDE_EFFECT = "side_effect"

class ToolDescription(BaseModel):
    name: str
    description: str
    risk: ToolRisk
    input_fields: list[str]
    output_fields: list[str]

class ToolRequest(BaseModel):
    tool_name: str
    arguments: dict[str, Any] = {}
    run_id: str

class ToolResult(BaseModel):
    tool_name: str
    success: bool
    data: dict[str, Any] = {}
    error: str | None = None
