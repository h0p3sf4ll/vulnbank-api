# VulnBank API

> **Warning:** This application is intentionally insecure. Run it only in an isolated local environment.

## Setup

```bash
pip install -r requirements.txt
python app.py
```

Server starts on `http://localhost:5001`.

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

*Additional endpoints may exist outside this table.*

---

## Discussion Questions

1. For each vulnerability you found, state the root cause and the minimal code change that fixes it.
2. What distinguishes BOLA from BFLA architecturally? How would you write automated tests to catch each class in a CI pipeline?
3. What properties of this application's JWT implementation would you scrutinize in a real engagement, and what attack would you attempt against it?
4. The `PATCH /api/users/me` endpoint uses a blocklist to prevent modification of certain fields. Is this approach sound? What would you recommend instead, and why?
5. Several resource IDs in this API are sequential integers. A colleague suggests switching to UUIDs as the fix. Is that sufficient? What is the actual control required?
6. Describe a defense-in-depth strategy for this API — beyond patching the individual bugs, what controls at the infrastructure, framework, and SDLC layer would reduce the likelihood of these issues recurring?
7. Write a Semgrep rule (or describe it precisely) that would catch the authorization pattern missing from the transfer endpoint.
