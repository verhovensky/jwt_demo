from sqlalchemy import INTEGER, Column, DateTime
from sqlalchemy.orm import declarative_base
from sqlalchemy.sql import func

Base = declarative_base()


class BaseModel(Base):

    __abstract__ = True

    id = Column(INTEGER(),
                primary_key=True)
    created_date = Column(DateTime(timezone=True),
                          server_default=func.now())
    updated_at = Column(DateTime(timezone=True),
                        onupdate=func.now(),
                        nullable=True)

    def __eq__(self, other):
        return type(self) is type(other) and self.id == other.id

    def __ne__(self, other):
        return not self.__eq__(other)
