# BountyGuard 🛡️🤖

**Autonomous developer bounty and milestone escrow verification powered by GenLayer consensus.**

## 💡 Overview
**BountyGuard** is an autonomous trustless Sponsor & Worker escrow verifier built on GenLayer. It scrapes live web deliverables, evaluates them against precommitted acceptance criteria via multi-validator LLM consensus using a safe exact verdict parser, and records immutable approval and payout states on-chain.

The DApp features **full live GenLayer integration** using `genlayer-js` (`studionet`), executing real write and read transactions directly from the browser frontend.

---

## 🚀 Key Features & UX
* **Live On-Chain Integration:** Completely free of mock or simulated timeouts; every action executes real `client.writeContract()` and `client.readContract()` calls.
* **Instant Out-of-the-Box Testing:** Pre-loaded with a default working contract address (`0x41d730cD715190dE1F57D5B0f214f2FB682B35C5`) so judges and stewards can test immediately.
* **Dynamic Contract Configurator:** Includes a header input bar and floating guidance banner allowing users to instantly switch to custom newly deployed contracts.
* **Sponsor & Worker Roles:** Sponsors precommit terms, criteria, and reward values on-chain; workers submit deliverables for automated AI verification.
* **Autonomous Web Scraping & Auditing:** Uses GenLayer's `gl.nondet.web.render` to inspect live GitHub repositories or deployed web pages.
* **Safe Exact Verdict Parser:** Multi-validator AI consensus (`gl.eq_principle.strict_eq`) evaluates submissions across independent AI models with bulletproof error handling.

---

## 🛠️ Smart Contract Architecture (`bounty_guard.py`)
1. `create_bounty(bounty_id, sponsor, acceptance_criteria, reward_amount)`: Sponsor precommits terms and reward value with duplicate ID protection.
2. `submit_and_verify_delivery(bounty_id, worker, deliverable_url)`: Worker submits a deliverable; contract runs GenLayer AI consensus.
3. `release_payout(bounty_id, caller)`: Authorized sponsor releases escrow funds upon successful approval.
4. `get_bounty_details(bounty_id)`: Public view function to check complete lifecycle status.

---

##  GenStudio Testing 

Test the full lifecycle directly inside GenStudio or via the live Vercel frontend:

### Step 1: Create Bounty (Sponsor Role)
* **Function:** `create_bounty`
* **Arguments:** `bounty_id` = `bounty_002`, `sponsor` = `SponsorDAO`, `acceptance_criteria` = `The page must state that it is for use in illustrative examples in documents.`, `reward_amount` = `100`

### Step 2: Submit & Verify Delivery (Worker Role)
* **Function:** `submit_and_verify_delivery`
* **Arguments:** `bounty_id` = `bounty_002`, `worker` = `DevBuilder`, `deliverable_url` = `https://example.com`

### Step 3: Release Payout
* **Function:** `release_payout`
* **Arguments:** `bounty_id` = `bounty_002`, `caller` = `SponsorDAO`

---
