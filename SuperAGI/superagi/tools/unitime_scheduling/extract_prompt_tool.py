# extract_prompt_tool.py
import json
from datetime import datetime
from pydantic import BaseModel, Field
from typing import Type, Optional

from superagi.tools.base_tool import BaseTool
# from superagi.llms.base_llm import BaseLLM
from superagi.llms.base_llm import BaseLlm


# Define the input schema for the tool. It expects the body of a single email.
class ExtractPromptInput(BaseModel):
    email_body: str = Field(
        ..., 
        description="The full text body of a single email to be analyzed for scheduling intent and entities."
    )

class ExtractPromptTool(BaseTool):
    """
    Extracts structured scheduling information from an email's body text.
    It identifies the core intent (e.g., CANCEL_CLASS) and key entities 
    (teacher, course, date, time) and returns them as a JSON object string.
    """
    # This allows SuperAGI to inject the configured Language Model into your tool
    llm: Optional[BaseLlm] = None
    name: str = "ExtractPromptTool"
    args_schema: Type[BaseModel] = ExtractPromptInput
    description: str = (
        "Analyzes an email's body text to extract structured scheduling intent and entities."
    )

    def _execute(self, email_body: str) -> str:
        """
        Executes the prompt extraction tool using an LLM.

        Args:
            email_body: The text content from the body of an email.

        Returns:
            A string containing a JSON object with the extracted intent and entities,
            or an error message.
        """
        if self.llm is None:
            return "Error: Language Model is not configured for this tool."

        if not email_body or not email_body.strip():
            return "Error: Input email_body is empty."

        # Get current date to help the LLM resolve relative dates like "today"
        current_date = datetime.now().strftime("%Y-%m-%d")
        
        # The detailed, zero-shot prompt that instructs the LLM on its task
        prompt = f"""
        You are an intelligent administrative assistant for a university. Your task is to analyze the following email body text and extract key information for scheduling purposes.

        The current date is: {current_date}

        Analyze the email body provided below. Identify the primary 'intent' and the associated 'entities'.

        Possible intents are: 'CANCEL_CLASS', 'RESCHEDULE_CLASS', 'TEACHER_UNAVAILABLE', 'REQUEST_INFO', 'OTHER'.

        Extract the following entities:
        - 'teacher_name': The name of the professor or teacher.
        - 'course_name_or_id': The name or code of the course (e.g., 'CS101', 'Physics').
        - 'date': The specific date of the class. Resolve 'today' or 'tomorrow' to 'YYYY-MM-DD' format.
        - 'time': The specific time of the class in 'HH:MM' (24-hour) format.
        - 'reason': A brief reason for the request, if mentioned.

        Email Body to analyze:
        "{email_body}"

        Your final output MUST be a single, valid JSON object and nothing else. Do not add any explanatory text before or after the JSON. If a value for an entity is not found, use `null`.
        """

        try:
            # Send the detailed prompt to the LLM
            response = self.llm.chat_completion([{'role': 'system', 'content': prompt}], max_tokens=self.max_token_limit)
            if 'content' not in response:
                return f"Error: LLM response did not contain 'content'. Response: {response}"
            
            llm_output = response['content']
            
            # Verify the output is valid JSON and return it as a string
            json_output = json.loads(llm_output)
            return json.dumps(json_output, indent=2)

        except json.JSONDecodeError:
            return f"Error: LLM returned malformed JSON. Response: {llm_output}"
        except Exception as e:
            return f"An unexpected error occurred: {str(e)}"