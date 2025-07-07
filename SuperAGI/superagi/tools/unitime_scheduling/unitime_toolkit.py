from superagi.tools.base_tool import BaseToolkit
from typing import List, Type
from superagi.tools.base_tool import BaseTool

# from .generate_xml_tool import GenerateXMLTool
from superagi.tools.unitime_scheduling.generate_xml_tool import GenerateXMLTool
# from .validate_xml_tool import ValidateXMLTool
from superagi.tools.unitime_scheduling.validate_xml_tool import ValidateXMLTool
# from .import_xml_tool import ImportXMLTool
from superagi.tools.unitime_scheduling.import_xml_tool import ImportXMLTool

class UnitimeToolkit(BaseToolkit):
    name = "UnitimeToolkit"
    description = "Toolkit for generating, validating, and importing UniTime-compatible XML"

    def get_tools(self) -> List[Type[BaseTool]]:
        return [GenerateXMLTool, ValidateXMLTool, ImportXMLTool]

    def get_env_keys(self) -> List[str]:
        return [
            "HF_API_TOKEN",
            "HF_MODEL_ENDPOINT",
            "UNITIME_IMPORT_URL"
        ]
