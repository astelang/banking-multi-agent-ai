class RiskAgent:

    async def analyze(self, transaction):

        amount = transaction.amount

        if amount > 15000:
            score = 80

        elif amount > 5000:
            score = 50

        else:
            score = 20

        return {
            "risk_score": score
        }