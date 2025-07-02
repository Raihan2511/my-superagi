from datetime import datetime
from typing import Type
from pydantic import BaseModel, Field
from superagi.tools.base_tool import BaseTool

class TimeQuerySchema(BaseModel):
    timezone: str = Field(
        default="UTC",
        description="Timezone like 'UTC', 'Asia/Kolkata', 'America/New_York'",
    )

class CurrentTimeTool(BaseTool):
    name = "CurrentTimeTool"
    description = "Returns the current time in a given timezone"
    args_schema: Type[TimeQuerySchema] = TimeQuerySchema

    def _execute(self, timezone: str = "UTC") -> str:
        try:
            import pytz
            now = datetime.now(pytz.timezone(timezone))
        except Exception:
            now = datetime.utcnow()
            timezone = "UTC"
        return f"The current time in {timezone} is {now.strftime('%Y-%m-%d %H:%M:%S')}"
