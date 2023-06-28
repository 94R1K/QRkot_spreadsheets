from sqlalchemy import Column, String, Text

from app.core.db import BaseProject


class CharityProject(BaseProject):
    name = Column(String(100), unique=True, nullable=False)
    description = Column(Text, nullable=False)
