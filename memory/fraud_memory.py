from openai import OpenAI
import os
from dotenv import load_dotenv
import chromadb

load_dotenv()

class FraudMemory:

    def __init__(self):
        self.openai = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        self.client = chromadb.Client()
        self.collection = self.client.get_or_create_collection(
            name="fraud_transactions"
        )

    def embed_text(self, text: str):
        response = self.openai.embeddings.create(
            model="text-embedding-3-small",
            input=text
        )
        return response.data[0].embedding

    def add_transaction(self, transaction):
        text = f"""
        Amount: {transaction.amount}
        Country: {transaction.country}
        Account Age: {transaction.account_age}
        """

        embedding = self.embed_text(text)

        self.collection.add(
            embeddings=[embedding],
            documents=[text],
            ids=[str(hash(text))]
        )

    def search_similar(self, transaction):
        text = f"""
        Amount: {transaction.amount}
        Country: {transaction.country}
        Account Age: {transaction.account_age}
        """

        embedding = self.embed_text(text)

        results = self.collection.query(
            query_embeddings=[embedding],
            n_results=2
        )

        return results