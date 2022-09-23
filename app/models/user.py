from sqlalchemy import Column, String, Text
from models.base import BaseModel
from datetime import datetime


def timestamp_to_repr(date: datetime) -> str:
    if isinstance(date, datetime):
        return date.isoformat()
    return ''


class User(BaseModel):
    __tablename__ = "user"

    name = Column(String(200))
    token = Column(Text)

    def to_json(self) -> dict:
        created = timestamp_to_repr(self.created_date)
        updated = timestamp_to_repr(self.updated_at)
        return dict(id=self.id,
                    name=self.id,
                    created=created,
                    last_updated=updated)

    def to_dict(self) -> dict:
        created = timestamp_to_repr(self.created_date)
        updated = timestamp_to_repr(self.updated_at)
        return {'id': self.id,
                'name': self.name,
                'created': created,
                'updated': updated}

    def __repr__(self):
        return f"User: {self.id}, {self.name}"
