from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import DateTime, func, UUID
from datetime import datetime
import uuid


class BaseModel(DeclarativeBase):
    __abstract__ = True
    __exclude_default_id__ = False
    repr_cols_num = 3
    repr_cols = tuple()

    # def __init_subclass__(cls, **kw: Any) -> None:

    #     if cls.__exclude_default_id__:
    #         if hasattr(cls, "id"):
    #             delattr(cls, "id")
    #     super().__init_subclass__(**kw)

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), default=uuid.uuid4, primary_key=True
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )

    def __repr__(self):
        cols = []
        for idx, col in enumerate(self.__table__.columns.keys()):
            if col in self.repr_cols or idx < self.repr_cols_num:
                cols.append(f"{col}={getattr(self, col)}")
        return f"<{self.__class__.__name__} ({', '.join(cols)})>"
