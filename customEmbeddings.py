from transformers import AutoTokenizer, AutoModel
from langchain_core.embeddings import Embeddings
from typing import List

class HuggingFaceEmbeddings(Embeddings):
    def __init__(self, model_name:str )-> None:
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModel.from_pretrained(model_name)

    def embed_query(self, text:str) -> List:
        inputs = self.tokenizer(text, return_tensors='pt')
        outputs = self.model(**inputs)
        return outputs.last_hidden_state[0].detach().numpy().tolist()