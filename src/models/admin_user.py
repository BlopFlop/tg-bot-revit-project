from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTable

from core.db import Base


class AdminUser(SQLAlchemyBaseUserTable[int], Base):
    """Стандартная модель пользователя для админки."""

    __tablename__ = "administration_user"
