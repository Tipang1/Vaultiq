from dataclasses import dataclass, field
import uuid
from datetime import datetime

@dataclass
class PasswordEntry:
    service: str
    username: str
    password: str
    notes: str = ""
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())
