from fastapi_users import schemas


class AdministrationUserRead(schemas.BaseUser[int]):
    """Schema for read admin users."""

    pass


class AdminUserCreate(schemas.BaseUserCreate):
    """Schema for create admin users."""

    pass


class AdminUserUpdate(schemas.BaseUserUpdate):
    """Schema for update admin users."""

    pass
