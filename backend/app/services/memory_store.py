from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

from pymongo import MongoClient

from app.config import settings


class MemoryStore:
    def __init__(self) -> None:
        self.client = MongoClient(settings.mongodb_uri)
        self.db = self.client[settings.mongodb_db_name]
        self.sessions = self.db["chat_sessions"]

    def append_message(self, session_id: str, role: str, content: str, metadata: dict[str, Any] | None = None) -> None:
        self.sessions.update_one(
            {"session_id": session_id},
            {
                "$setOnInsert": {"session_id": session_id, "created_at": datetime.now(timezone.utc)},
                "$push": {
                    "history": {
                        "role": role,
                        "content": content,
                        "metadata": metadata or {},
                        "timestamp": datetime.now(timezone.utc),
                    }
                },
                "$set": {"updated_at": datetime.now(timezone.utc)},
            },
            upsert=True,
        )

    def get_history(self, session_id: str, limit: int = 12) -> list[dict[str, Any]]:
        session = self.sessions.find_one({"session_id": session_id})
        if not session:
            return []
        history = session.get("history", [])
        return history[-limit:]
