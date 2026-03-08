import asyncio
from agents.fraud_agent import FraudAgent
from agents.risk_agent import RiskAgent
from agents.compliance_agent import ComplianceAgent
from decision_engine.decision_engine import DecisionEngine
from utils.logger import logger


class AgentController:

    def __init__(self):
        self.fraud_agent = FraudAgent()
        self.risk_agent = RiskAgent()
        self.compliance_agent = ComplianceAgent()
        self.decision_engine = DecisionEngine()

    async def process(self, transaction):

        logger.info(f"Processing transaction: {transaction.__dict__}")

        fraud_task = self.fraud_agent.analyze(transaction)
        risk_task = self.risk_agent.analyze(transaction)
        compliance_task = self.compliance_agent.analyze(transaction)

        fraud_result, risk_result, compliance_result = await asyncio.gather(
            fraud_task,
            risk_task,
            compliance_task
        )

        logger.info(f"Fraud Result: {fraud_result}")
        logger.info(f"Risk Result: {risk_result}")
        logger.info(f"Compliance Result: {compliance_result}")

        decision = self.decision_engine.make_decision(
            fraud_result,
            risk_result,
            compliance_result
        )

        return {
            "fraud": fraud_result,
            "risk": risk_result,
            "compliance": compliance_result,
            "decision": decision
        }