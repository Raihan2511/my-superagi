from typing import List
from superagi.tools.base_tool import BaseToolkit
from superagi.tools.current_time.current_time_tool import CurrentTimeTool

class CurrentTimeToolkit(BaseToolkit):
    name = "Current Time Toolkit"
    description = "Toolkit to get the current time in a specified timezone"

    def get_tools(self) -> List[CurrentTimeTool]:
        return [CurrentTimeTool()]

    def get_env_keys(self):
        return []
