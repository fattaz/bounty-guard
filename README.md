# BountyGuard 🛡️🤖

**Autonomous developer bounty and milestone escrow verification powered by GenLayer consensus.**

## 💡 Overview
**BountyGuard** is an autonomous trustless Sponsor & Worker escrow verifier built on GenLayer. It scrapes live web deliverables, evaluates them against precommitted acceptance criteria via multi-validator LLM consensus using a safe exact verdict parser, and records immutable approval and payout states on-chain.

The DApp features **full live GenLayer integration** using `genlayer-js` (`studionet`), executing real write and read transactions directly from the browser frontend.

---

## 🚀 Key Features & UX
* **Live On-Chain Integration:** Completely free of mock or simulated timeouts; every action executes real `client.writeContract()` and `client.readContract()` calls.
* **4-Step Escrow Workflow:**
  1. **Create Bounty:** Precommit custom acceptance criteria and token reward values on-chain.
  2. **Submit Delivery:** Submit deliverable URLs for automated multi-validator AI consensus auditing.
  3. **Query Status:** Check real-time live on-chain status (`OPEN`, `APPROVED`, `REJECTED`, or `PAID`).
  4. **Release Payout:** Authorized sponsors release locked escrow funds upon AI approval.
* **Autonomous Web Scraping & Auditing:** Uses GenLayer's `gl.nondet.web.render` to inspect live GitHub repositories or deployed web pages.
* **Safe Exact Verdict Parser:** Multi-validator AI consensus (`gl.eq_principle.strict_eq`) evaluates submissions across independent AI models with bulletproof error handling.

---

## 🛠️ Smart Contract Architecture (`bounty_guard.py`)
1. `create_bounty(bounty_id, sponsor, acceptance_criteria, reward_amount)`: Sponsor precommits terms and reward value with duplicate ID protection.
2. `submit_and_verify_delivery(bounty_id, worker, deliverable_url)`: Worker submits a deliverable; contract runs GenLayer AI consensus.
3. `release_payout(bounty_id, caller)`: Authorized sponsor releases escrow funds upon successful approval.
4. `get_bounty_details(bounty_id)`: Public view function to check complete lifecycle status.

---

## Testing Instructions

Test the full lifecycle directly via the live frontend:

### Step 1: Create Bounty (Tab 1)
* **Bounty ID:** `bounty_taskguard_03`
* **Sponsor:** `SponsorDAO`
* **Criteria:** `The page must state that it is for use in illustrative examples in documents.`
* **Reward Amount:** `100`

### Step 2: Submit Delivery (Tab 2)
* **Bounty ID:** `bounty_taskguard_03`
* **Worker:** `DevBuilder`
* **Deliverable URL:** `https://example.com`

### Step 3: Query Status (Tab 3)
* **Bounty ID:** `bounty_taskguard_03`
* View live consensus state (`APPROVED` or `REJECTED`).

### Step 4: Release Payout (Tab 4)
* **Bounty ID:** `bounty_taskguard_03`
* **Caller Sponsor Handle:** `SponsorDAO`

---

## 📦 Deployment 

1. **Smart Contract Address (StudioNet):** `0x41d730cD715190dE1F57D5B0f214f2FB682B35C5`
2. **Frontend Deployment:** Hosted on Vercel with source code available on GitHub.
