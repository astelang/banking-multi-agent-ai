from config.settings import (
    FRAUD_BLOCK_THRESHOLD,
    TOTAL_BLOCK_THRESHOLD,
    TOTAL_REVIEW_THRESHOLD
)

class DecisionEngine:

    def make_decision(self, fraud_result, risk_result, compliance_result):
        fraud_score = int(fraud_result["fraud_score"])
        risk_score = int(risk_result["risk_score"])
        compliance_score = int(compliance_result["compliance_score"])

        total_score = fraud_score + risk_score + compliance_score

        if compliance_score == 100:
            return "BLOCK"

        if fraud_score >= FRAUD_BLOCK_THRESHOLD:
            return "BLOCK"

        if total_score > TOTAL_BLOCK_THRESHOLD:
            return "BLOCK"

        if total_score > TOTAL_REVIEW_THRESHOLD:
            return "REVIEW"

        return "APPROVE"