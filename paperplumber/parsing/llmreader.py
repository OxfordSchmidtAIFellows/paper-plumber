"""Functionality to process text for mining."""

import os
from typing import Optional

from langchain import PromptTemplate
from langchain.llms import OpenAI


OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")


class OpenAIReader:
    """Class to parse text using OpenAI's models."""

    PROMPT_TEMPLATE = """
    Can you read the following text from a scientific article, and
    tell me if it contains information about the value of {target}?
    If the value is not quoted in the text, return just 'NA'. If the value
    is quoted in the text, please return the value.

    Text: 'The value of {target} is 10 +/- .5'
    Answer: 10

    Text: 'Chocolate is delicious'
    Answer: NA

    Text: {text}
    Answer:
    """

    def __init__(self, target: str):
        if not OPENAI_API_KEY:
            raise ValueError("OpenAI API key not found. "
                "Please set OPENAI_API_KEY in your local environment.")

        self.target = target
        self.prompt = PromptTemplate(
            input_variables=["target", "text"], template=self.PROMPT_TEMPLATE
        )
        self.model = OpenAI(
            model_name="gpt-3.5-turbo", openai_api_key=OPENAI_API_KEY
        )

    def clean_response(self, response: str):
        """Clean the response from the model."""
        response = response.strip()
        response = response.replace("\n", "")
        return response

    def read(self, text: str) -> Optional[str]:
        """Read text and return the value of the target variable."""
        prompt = self.prompt.format(target=self.target, text=text)
        response = self.model(prompt)
        return self.clean_response(response)
