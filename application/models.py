from dataclasses import dataclass, field
from uuid import uuid4
from typing import Optional

@dataclass
class TodoItem:
    title: str
    completed: bool = False
    id: str = field(default_factory=lambda: str(uuid4()))
    attachment_filename: Optional[str] = None      # e.g. "image.png" or "document.pdf"
    attachment_mimetype: Optional[str] = None        # e.g. "image/png" or "application/pdf"
    attachment_data: Optional[bytes] = None          # Binary file data (BLOB)
