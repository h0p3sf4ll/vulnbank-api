from __future__ import annotations

import os
from dataclasses import dataclass, field


@dataclass
class Config:
    secret_key: str = field(default_factory=lambda: os.getenv("SECRET_KEY", "vulnbank-2024"))
    token_expiry_hours: int = 8
    debug: bool = True
