from datetime import datetime

from sqlalchemy import Column, Text, ForeignKey, Integer

from app.models.base import BaseModel


class Donation(BaseModel):
    user_id = Column(Integer, ForeignKey('user.id'))
    comment = Column(Text)
