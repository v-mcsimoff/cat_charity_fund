from sqlalchemy import Column, Text, String

from app.models.base import BaseModel


class CharityProject(BaseModel):
    name = Column(String(100), unique=True, nullable=False)
    description = Column(Text, nullable=False)
