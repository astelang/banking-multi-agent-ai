from services.llm_service import LLMService
from memory.fraud_memory import FraudMemory

class FraudAgent:

    def __init__(self):

        self.llm = LLMService()
        self.memory = FraudMemory()

    async def analyze(self, transaction):

        similar_cases = self.memory.search_similar(transaction)

        prompt = f"""
        Analyze this banking transaction for fraud risk.

        Amount: {transaction.amount}
        Country: {transaction.country}
        Account Age: {transaction.account_age}

        Similar past fraud cases:
        {similar_cases}

        Return ONLY a fraud score between 0 and 100.
        """

        result = self.llm.analyze(prompt)

        try:
            score = int(result.strip())
        except:
            score = 50

        if score > 70:
            self.memory.add_transaction(transaction)

        return {
            "fraud_score": score
        }