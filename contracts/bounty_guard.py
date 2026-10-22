# { "Depends": "py-genlayer:1jb45aa8ynh2a9c9xn3b7qqh8sm5q93hwfp7jqmwsfhh8jpz09h6" }
from genlayer import *

class BountyGuard(gl.Contract):
    """
    BountyGuard: Autonomous developer bounty and milestone escrow verifier.
    Implements sponsor and worker roles, precommitted terms & reward values,
    and a foolproof strict verdict parser for GenLayer multi-validator consensus.
    """

    total_bounties: u256
    bounty_sponsor: TreeMap[str, str]
    bounty_worker: TreeMap[str, str]
    bounty_criteria: TreeMap[str, str]
    bounty_reward: TreeMap[str, u256]
    bounty_deliverable: TreeMap[str, str]
    bounty_status: TreeMap[str, str]   # OPEN | APPROVED | REJECTED | PAID
    bounty_feedback: TreeMap[str, str]

    def __init__(self):
        self.total_bounties = u256(0)

    @gl.public.write
    def create_bounty(self, bounty_id: str, sponsor: str, acceptance_criteria: str, reward_amount: u256) -> str:
        """
        Sponsor creates a bounty with precommitted terms, criteria, and reward value.
        """
        if self.bounty_status.get(bounty_id, "NOT_FOUND") != "NOT_FOUND":
            raise ValueError("Bounty ID already exists. Choose a unique ID.")
        if len(acceptance_criteria.strip()) < 5:
            raise ValueError("Acceptance criteria is too short.")

        self.bounty_sponsor[bounty_id] = sponsor
        self.bounty_criteria[bounty_id] = acceptance_criteria
        self.bounty_reward[bounty_id] = reward_amount
        self.bounty_status[bounty_id] = "OPEN"
        self.total_bounties = self.total_bounties + u256(1)

        return f"BOUNTY_CREATED: {bounty_id} | Sponsor: {sponsor} | Reward: {reward_amount}"

    @gl.public.write
    def submit_and_verify_delivery(self, bounty_id: str, worker: str, deliverable_url: str) -> str:
        """
        Worker submits delivery URL. Contract runs GenLayer AI consensus with a safe exact verdict parser.
        """
        current_status = self.bounty_status.get(bounty_id, "NOT_FOUND")
        if current_status == "NOT_FOUND":
            raise ValueError("Bounty ID does not exist. Sponsor must create it first.")
        if current_status in ["APPROVED", "PAID"]:
            raise ValueError("Bounty has already been approved and settled.")

        # Robust URL sanitization
        clean_url = deliverable_url.strip()
        if "](" in clean_url:
            clean_url = clean_url.split("](")[-1].rstrip(")")
        elif "[" in clean_url and "]" in clean_url:
            clean_url = clean_url.split("[")[1].split("]")[0]
        clean_url = clean_url.strip("[]()'")

        if len(clean_url) < 5 or not clean_url.startswith("http"):
            raise ValueError("Invalid deliverable URL provided. Must start with http:// or https://")

        criteria = self.bounty_criteria[bounty_id]
        self.bounty_worker[bounty_id] = worker
        self.bounty_deliverable[bounty_id] = clean_url

        def evaluate_delivery() -> str:
            raw_text = gl.nondet.web.render(clean_url, mode="text")
            page_text = " ".join(str(raw_text).split())
            snippet = page_text[:1200].strip()

            prompt = f"""
            You are a strict technical lead evaluating a software bounty delivery.
            Determine whether the provided Web Content / Repository summary strictly satisfies the Acceptance Criteria.

            Acceptance Criteria:
            "{criteria}"

            Web Content Snippet:
            ---
            {snippet}
            ---

            Instructions:
            Evaluate carefully. If the criteria are fully met, output EXACTLY the word APPROVED.
            If the criteria are NOT fully met, or if there is any failure, violation, or missing requirement, output EXACTLY the word REJECTED.
            Do not output anything else, no punctuation, no markdown, no explanation.
            """

            response = gl.nondet.exec_prompt(prompt).strip().upper()
            
            # Safe exact verdict parser logic inside validator execution
            if "APPROVED" in response and "NOT" not in response and "REJECTED" not in response:
                return "APPROVED"
            return "REJECTED"

        # Strict consensus across validator set
        final_verdict = gl.eq_principle.strict_eq(evaluate_delivery)

        # Bulletproof post-consensus parser check
        if final_verdict == "APPROVED":
            status = "APPROVED"
            feedback = "Delivery successfully verified and approved by validator consensus."
        else:
            status = "REJECTED"
            feedback = "Delivery failed to meet precommitted acceptance criteria."

        self.bounty_status[bounty_id] = status
        self.bounty_feedback[bounty_id] = feedback

        return f"DELIVERY_RESULT: {status} | Feedback: {feedback}"

    @gl.public.write
    def release_payout(self, bounty_id: str, caller: str) -> str:
        """
        Releases escrow payout to the worker if approved by sponsor/contract.
        """
        status = self.bounty_status.get(bounty_id, "NOT_FOUND")
        sponsor = self.bounty_sponsor.get(bounty_id, "")
        
        if status != "APPROVED":
            raise ValueError("Payout can only be released for APPROVED bounties.")
        if caller != sponsor:
            raise ValueError("Only the designated sponsor can release the payout.")

        self.bounty_status[bounty_id] = "PAID"
        reward = self.bounty_reward.get(bounty_id, u256(0))
        worker = self.bounty_worker.get(bounty_id, "unknown")

        return f"PAYOUT_RELEASED: {reward} transferred to worker {worker} for bounty {bounty_id}."

    @gl.public.view
    def get_bounty_details(self, bounty_id: str) -> str:
        """Retrieves comprehensive details of a bounty."""
        status = self.bounty_status.get(bounty_id, "NOT_FOUND")
        if status == "NOT_FOUND":
            return "BOUNTY_NOT_FOUND"
        sponsor = self.bounty_sponsor.get(bounty_id, "")
        worker = self.bounty_worker.get(bounty_id, "None")
        reward = str(self.bounty_reward.get(bounty_id, u256(0)))
        return f"Status: {status} | Sponsor: {sponsor} | Worker: {worker} | Reward: {reward}"
