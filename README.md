# BountyGuard 🛡️🤖

**Autonomous developer bounty and milestone verification powered by GenLayer consensus.**

## 💡 Overview
Web3 hackathons, open-source DAOs, and developer platforms constantly struggle with manual bounty verification. Reviewers spend hours checking pull requests or live demo URLs to see if deliverables meet criteria before releasing escrow funds. 

**BountyGuard** solves this by leveraging GenLayer's intelligent execution environment to autonomously scrape live web deliverables, evaluate them against custom acceptance criteria via multi-validator LLM consensus, prevent duplicate submissions, and record immutable approval or rejection states on-chain.

---

## 🚀 Key Features
* **Autonomous Web Scaping & Auditing:** Uses GenLayer's `gl.nondet.web.render` to inspect live GitHub repositories or deployed web pages.
* **Multi-Validator Consensus:** Evaluates submissions using `gl.eq_principle.strict_eq` across independent AI validator models (Mistral, Sonnet, Gemini).
* **Duplicate Prevention:** Built-in validation checks ensure a single `bounty_id` cannot be audited or submitted twice.
* **Interactive Web3 Frontend:** Built with `genlayer-js` featuring live GenLayer wallet connection/disconnection states, tabbed navigation, and real-time on-chain querying.

---

## 🛠️ Smart Contract Architecture (`bounty_guard.py`)
The intelligent contract manages state across three primary public functions:
1. `verify_delivery(bounty_id, deliverable_url, acceptance_criteria)`: Scrapes the live URL, runs AI consensus, checks for duplicate IDs, and writes the `APPROVED` or `REJECTED` status on-chain.
2. `get_bounty_status(bounty_id)`: Public view function to check approval status.
3. `get_bounty_feedback(bounty_id)`: Public view function to retrieve validator justification.

---

## 🧪 GenStudio Testings

You can test both consensus pathways directly inside GenStudio using these precise examples:

### Test Case 1: Expected to be **APPROVED**
*This tests a deliverable where the web content successfully satisfies the acceptance criteria.*
* **Bounty ID:** `bounty_001`
* **Deliverable URL:** `https://example.com`
* **Acceptance Criteria:** `The page must state that it is for use in illustrative examples in documents.`

### Test Case 2: Expected to be **REJECTED**
*This tests a deliverable where the web content fails to meet strict criteria, proving active validator auditing and rejection.*
* **Bounty ID:** `bounty_002`
* **Deliverable URL:** `https://example.com`
* **Acceptance Criteria:** `The page must contain a live cryptocurrency trading dashboard with order books and wallet connect buttons.`

---

## 📦 Deployment Instructions

1. **Smart Contract (GenStudio):**
   * Paste `bounty_guard.py` into GenStudio.
   * Click **Deploy**
