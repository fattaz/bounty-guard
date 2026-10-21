# { "Depends": "py-genlayer:1jb45aa8ynh2a9c9xn3b7qqh8sm5q93hwfp7jqmwsfhh8jpz09h6" }
from genlayer import *

class BountyGuard(gl.Contract):
    """
    BountyGuard: Autonomous developer bounty and delivery verifier.
    Scrapes live repository or deployment pages, evaluates them against bounty criteria via AI consensus,
    and settles approval status on-chain with duplicate prevention.
    """

    total_bounties: u256
    bounty_status: TreeMap[str, str]   # APPROVED | REJECTED
    bounty_feedback: TreeMap[str, str] # Summary of consensus feedback

    def __init__(self):
        self.total_bounties = u256(0)

    @gl.public.write
    def verify_delivery(self, bounty_id: str, deliverable_url: str, acceptance_criteria: str) -> str:
        """
        Fetches live deliverable web page/repo data, audits it against criteria via LLM consensus,
        and records structured approval ratings on-chain after checking for duplicate IDs.
        """
        # Block duplicate bounty submissions
        if self.bounty_status.get(bounty_id, "NOT_FOUND") != "NOT_FOUND":
            raise ValueError("This Bounty ID has already been audited. Please use a unique ID.")

        # Robust URL sanitization
        clean_url = deliverable_url.strip()
        if "](" in clean_url:
            clean_url = clean_url.split("](")[-1].rstrip(")")
        elif "[" in clean_url and "]" in clean_url:
            clean_url = clean_url.split("[")[1].split("]")[0]
        clean_url = clean_url.strip("[]()'")

        if len(clean_url) < 5 or not clean_url.startswith("http"):
            raise ValueError("Invalid deliverable URL provided. Must start with http:// or https://")
        if len(acceptance_criteria.strip()) < 5:
            raise ValueError("Acceptance criteria description is too short")

        def evaluate_bounty() -> str:
            raw_text = gl.nondet.web.render(clean_url, mode="text")
            page_text = " ".join(str(raw_text).split())
            snippet = page_text[:1200].strip()

            prompt = f"""
            You are a strict technical lead evaluating a software bounty submission.
            Determine whether the provided Web Content / Repository summary satisfies the Acceptance Criteria.

            Acceptance Criteria:
            "{acceptance_criteria}"

            Web Content Snippet:
            ---
            {snippet}
            ---

            Instructions:
            You must output ONLY one exact word, with no extra text, no punctuation, and no markdown:
            APPROVED or REJECTED
            """

            response = gl.nondet.exec_prompt(prompt).strip().upper()
            if "APPROVED" in response:
                return "APPROVED"
            return "REJECTED"

        # Strict consensus on a single deterministic token
        status = gl.eq_principle.strict_eq(evaluate_bounty)
        
        feedback = "Submission evaluated successfully by validator consensus." if status == "APPROVED" else "Submission failed to meet acceptance criteria."

        self.bounty_status[bounty_id] = status
        self.bounty_feedback[bounty_id] = feedback
        self.total_bounties = self.total_bounties + u256(1)

        return f"BOUNTY_RESULT: {status} | Feedback: {feedback}"

    @gl.public.view
    def get_bounty_status(self, bounty_id: str) -> str:
        """Retrieves the bounty approval status (APPROVED or REJECTED)."""
        return self.bounty_status.get(bounty_id, "BOUNTY_NOT_FOUND")

    @gl.public.view
    def get_bounty_feedback(self, bounty_id: str) -> str:
        """Retrieves validator feedback justification."""
        return self.bounty_feedback.get(bounty_id, "BOUNTY_NOT_FOUND")

    @gl.public.view
    def get_total_bounties(self) -> u256:
        """Returns total bounties audited on-chain."""
        return self.total_bounties
