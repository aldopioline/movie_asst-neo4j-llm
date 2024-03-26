from langchain_community.llms import Ollama
from langchain_openai import OpenAI

from typing import Any, Optional

class Model:
    def __init__(self) -> None:
        self.defaultModel = "mistral"
        self.curModel = None

    def Ollama(self, modelName=None) -> None:
        if not modelName:
            self.curModel = Ollama(model=self.defaultModel)
        self.curModel= Ollama(model=modelName)

    def OpenAI(self,api_key: str) -> None:
        self.curModel = OpenAI(api_key=api_key)

    def getModel(self) -> Optional[Any]:
        return self.curModel