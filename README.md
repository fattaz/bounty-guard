# BountyGuard 🛡️🤖

**Autonomous developer bounty and milestone escrow verification powered by GenLayer consensus.**

## 💡 Overview
Web3 hackathons, open-source DAOs, and developer platforms constantly struggle with manual bounty verification and escrow payouts. **BountyGuard** solves this by leveraging GenLayer's intelligent execution environment to create a trustless Sponsor & Worker escrow workflow. 

It autonomously scrapes live web deliverables, evaluates them against precommitted acceptance criteria via multi-validator LLM consensus using a safe exact verdict parser, and records immutable approval and payout states on-chain.

---

## 🚀 Key Features
* **Sponsor & Worker Roles:** Sponsors precommit terms, criteria, and reward values on-chain; workers submit deliverables for automated verification.
* **Autonomous Web Scraping & Auditing:** Uses GenLayer's `gl.nondet.web.render` to inspect live GitHub repositories or deployed web pages.
* **Safe Exact Verdict Parser:** Multi-validator AI consensus (`gl.eq_principle.strict_eq`) evaluates submissions across independent AI models with bulletproof error handling.
* **Interactive Web3 Frontend:** Built with `genlayer-js` featuring wallet connection states, tabbed navigation (`Create Bounty`, `Submit Delivery`, `Release Payout`), and real-time on-chain querying.

---

## 🛠️ Smart Contract Architecture (`bounty_guard.py`)
1. `create_bounty(bounty_id, sponsor, acceptance_criteria, reward_amount)`: Sponsor precommits terms and reward value.
2. `submit_and_verify_delivery(bounty_id, worker, deliverable_url)`: Worker submits a deliverable; contract runs GenLayer AI consensus.
3. `release_payout(bounty_id, caller)`: Authorized sponsor releases escrow funds upon successful approval.
4. `get_bounty_details(bounty_id)`: Public view function to check complete lifecycle status.

---

## GenStudio Testing 

Test the full lifecycle directly inside GenStudio:

### Step 1: Create Bounty (Sponsor Role)
* **Function:** `create_bounty`
* **Arguments:** `bounty_id` = `bounty_001`, `sponsor` = `SponsorDAO`, `acceptance_criteria` = `The page must state that it is for use in illustrative examples in documents.`, `reward_amount` = `500`

### Step 2: Submit & Verify Delivery (Worker Role)
* **Function:** `submit_and_verify_delivery`
* **Arguments:** `bounty_id` = `bounty_001`, `worker` = `DevBuilder`, `deliverable_url` = `https://example.com`

### Step 3: Release Payout
* **Function:** `release_payout`
* **Arguments:** `bounty_id` = `bounty_001`, `caller` = `SponsorDAO`

---

## 📦 Deployment Instructions

1. **Smart Contract (GenStudio):**
   * Paste `bounty_guard.py` into GenStudio, click **Deploy**,
