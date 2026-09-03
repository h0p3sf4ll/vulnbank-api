# VulnBank API — Secure Code Review Challenge

> **Warning:** This application is intentionally insecure. Run it only in an isolated local environment.

## Setup

```bash
pip install -r requirements.txt
python app.py
```

Server starts on `http://localhost:5001`. Running the app is optional — the challenge is primarily a source-code review.

---

## Brief

You are reviewing the `vulnbank/` package before it ships to production. The developer has implemented a small fintech API; your job is to find security vulnerabilities in the source code, explain why each is dangerous, and write the correct fix.

**For each vulnerability you find, provide:**

1. The file and function where the issue lives
2. The vulnerability class (e.g. BOLA, SQLi, mass assignment)
3. A brief explanation of why it is dangerous
4. The corrected code

**Target time:** 30 minutes. A strong candidate will find 6–7 issues. Bonus findings reward candidates who read beyond the obvious paths.

---

## Codebase Overview

```
vulnbank/
├── config.py        — application configuration
├── models.py        — TypedDicts for User, Account, Transaction, Message
├── data.py          — in-memory repositories (UserRepository, AccountRepository, …)
├── auth.py          — JWT creation, require_auth and require_admin decorators
├── services.py      — TransferService (business logic)
├── database.py      — SQLite setup for search features
└── routes/
    ├── auth.py      — POST /auth/login
    ├── users.py     — GET/PATCH /api/users/…
    ├── accounts.py  — GET /api/accounts/…, /api/transactions/…
    ├── transfers.py — POST /api/transfers
    ├── receipts.py  — POST /api/transfers/<id>/receipt
    ├── messages.py  — GET /api/messages/…
    ├── search.py    — GET /api/search/users, /api/search/accounts
    └── admin.py     — GET /api/admin/…
```

Start your review wherever makes sense. Not all files contain vulnerabilities.

---

## Discussion Questions

**Q1 — Warm-up**
Open `vulnbank/routes/users.py`. The `get_user()` function is missing a security check. What check is missing, and what is the one-line fix?

**Q2**
Review `UserRepository.update()` in `vulnbank/data.py`. The method uses a `PROTECTED_FIELDS` set to guard against unwanted writes. Explain why this pattern is fragile, give an example of how it can be abused, and rewrite the method using the safer pattern.

**Q3**
Read `vulnbank/routes/search.py`. Both query functions have the same class of vulnerability. Identify it, explain the risk, and rewrite both functions so they are no longer vulnerable. Beyond the code fix, what other controls would you recommend at the infrastructure or framework level?

**Q4**
There are two independent paths by which an attacker can gain admin privileges in this application. Identify both — specifying the file and function for each — explain why each works, and describe the fix for each.

**Q5 — Stretch**
`TransferService.execute()` in `vulnbank/services.py` has an authorization flaw that is architecturally different from the ones in `routes/users.py`. Explain the difference, name the vulnerability class, and write the corrected `execute()` signature and the check it needs.

**Q6 — Stretch**
Review `send_receipt()` in `vulnbank/routes/receipts.py`. The function makes an outbound HTTP request based on caller-supplied input. What class of vulnerability does this introduce, and what is the minimal input validation needed to prevent it? What would an attacker target in a cloud-hosted environment?
