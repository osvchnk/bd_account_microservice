import enum

from sqlalchemy import Column, Integer, String, ForeignKey, Enum

from ..database import Base


class Role(enum.Enum):
    TOURIST = "tourist"
    OPERATOR = "operator"
    FOND = "fond"


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    first_name = Column(String)
    second_name = Column(String)
    email = Column(String, unique=True, nullable=False)
    user_role = Column(Enum(Role), default=Role.TOURIST, nullable=False)
    # public_key = Column(String)
    # user_hash = Column(String)
