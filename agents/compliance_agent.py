class ComplianceAgent:

    async def analyze(self, transaction):

        sanctioned_countries = ["Iran", "North Korea"]

        if transaction.country in sanctioned_countries:
            score = 100
        else:
            score = 0

        return {
            "compliance_score": score
        }