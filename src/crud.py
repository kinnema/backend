from typing import List
from sqlmodel import Session, select

from src.models import Serie


def create_serie(*, session: Session, serie: Serie) -> List[Serie]:
    db_obj = Serie.model_validate(
        serie
    )
    session.add(db_obj)
    session.commit()
    session.refresh(db_obj)
    return db_obj


def get_series_by_collection(*, session: Session, collection: str) -> List[Serie]:
    db_obj = select(Serie).where(Serie.collection == collection)
    session_db = session.exec(db_obj).fetchmany()

    return session_db