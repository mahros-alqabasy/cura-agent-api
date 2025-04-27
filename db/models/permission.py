from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from db.base_class import Base

class Permission(Base):
    __tablename__ = "permissions"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, nullable=False)

    roles = relationship("RolePermission", back_populates="permission")
