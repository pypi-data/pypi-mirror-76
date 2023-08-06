from sqlalchemy import (
    Column,
    Integer,
    String,
    Text,
    DateTime,
    ForeignKey,
)

from ...database import Base


class PatentRefModel(Base):
    __tablename__ = 'patent_refs'

    id = Column(Integer, primary_key=True)
    patent_id = Column(
        Integer,
        ForeignKey('patents.id'),
    )
    cited_by = Column(String(50), nullable=False)
    ref_title = Column(Text)
    year = Column(String(50), nullable=True)
    updated_at = Column(DateTime, nullable=False)
