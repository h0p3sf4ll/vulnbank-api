# VulnBank API

> **Warning:** This application is intentionally insecure. Run it only in an isolated local environment.

## Setup

```bash
pip install -r requirements.txt
python app.py
```

Server starts on `http://localhost:5001`. Setup should take under two minutes.

---

## Engagement Brief

You are conducting an authorized API penetration test against VulnBank, a small fintech platform. The client has issued you a test account and granted full access to the API surface described below.

**Your test credentials:**

| Username | Password     |
|----------|-------------|
| alice    | password123 |

Other users have registered accounts on the platform.

**Objective:** Identify authorization and access-control vulnerabilities. For each finding, document:
- The request (method, path, headers, body)
- The response that demonstrates the issue
- Impact assessment
- Recommended remediation

**Target time:** 30 minutes. A strong candidate will find 5–6 issues within that window. Bonus findings reward candidates who think beyond the expected paths.

---

## API Reference

| Method | Endpoint | Auth | Description |
|--------|----------|------|-------------|
| POST | /auth/login | — | Obtain a Bearer token |
| GET | /api/users/me | ✓ | Your profile |
| PATCH | /api/users/me | ✓ | Update your profile |
| GET | /api/accounts | ✓ | Your bank accounts |
| GET | /api/accounts/:id | ✓ | Account details |
| GET | /api/accounts/:id/transactions | ✓ | Account transaction history |
| GET | /api/transactions/:id | ✓ | Transaction detail |
| POST | /api/transfers | ✓ | Initiate a fund transfer (`from_account`, `to_account`, `amount`) |
| GET | /api/messages | ✓ | Inbox summary |
| GET | /api/messages/:id | ✓ | Message detail |
| GET | /api/search/users | ✓ | Search users by username or email (`?q=`) |
| GET | /api/search/accounts | ✓ | Search your accounts by type (`?type=`) |

*Additional endpoints may exist outside this table.*

---

## Discussion Questions

Answer each question concisely. They increase in difficulty.

**Q1 — Warm-up**
Pick one BOLA vulnerability you found. Show the exact request that exploits it, identify the missing check in the code, and write the one-line fix.

**Q2**
The `PATCH /api/users/me` endpoint uses a field blocklist to prevent mass assignment. Give a payload that exploits this, explain *why* blocklists are fragile as a control, and describe the safer pattern.

**Q3**
You found SQL injection in at least one search endpoint. Write the parameterized version of the vulnerable query. Beyond parameterization, what additional layers of defense would you add in a production system?

**Q4**
There are two distinct paths to admin privilege escalation in this application. Identify both, explain why each works, and for each describe the minimal fix.

**Q5 — Stretch**
BOLA and BFLA are both authorization failures. Explain the architectural difference between them. Then describe how you would detect each class automatically in a CI pipeline — what does the test harness look like, and what are its limits?
