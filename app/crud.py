from typing import Any, Type, TypeVar
from sqlalchemy.orm import Session
from sqlalchemy import inspect

from app.database import Base

ModelType = TypeVar("ModelType", bound=Base)


def get_all(db: Session, model: Type[ModelType], skip: int = 0, limit: int = 100) -> list[ModelType]:
    return db.query(model).offset(skip).limit(limit).all()


def get_by_id(db: Session, model: Type[ModelType], record_id: int) -> ModelType | None:
    return db.query(model).filter(model.id == record_id).first()


def create(db: Session, model: Type[ModelType], data: dict[str, Any]) -> ModelType:
    record = model(**data)
    db.add(record)
    db.commit()
    db.refresh(record)
    return record


def update(db: Session, record: ModelType, data: dict[str, Any]) -> ModelType:
    for key, value in data.items():
        if value is not None:
            setattr(record, key, value)
    db.commit()
    db.refresh(record)
    return record


def delete(db: Session, record: ModelType) -> None:
    db.delete(record)
    db.commit()


def get_model_fields(model: Type[ModelType]) -> list[dict[str, str]]:
    mapper = inspect(model)
    fields = []
    for column in mapper.columns:
        fields.append({
            "name": column.key,
            "type": str(column.type),
            "nullable": column.nullable,
            "primary_key": column.primary_key,
        })
    return fields
