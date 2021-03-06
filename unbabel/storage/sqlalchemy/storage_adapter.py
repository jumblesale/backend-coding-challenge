from typing import List, Any

import attr
from flask_sqlalchemy import SQLAlchemy

from unbabel.storage.sqlalchemy.models.translation import Translation
from unbabel.types import SupportsStoringUids, Uid


@attr.s(auto_attribs=True, frozen=True)
class SqlAlchemyStorageAdapter(SupportsStoringUids):
    db: SQLAlchemy

    def store_uid(self, uid: Uid) -> None:
        return store_uid(self.db, uid)

    def retrieve_all_uids(self) -> List[Uid]:
        return retrieve_all_uids(self.db)


def store_uid(db: SQLAlchemy, uid: Uid) -> None:
    model = Translation(uid=uid)
    db.session.add(model)
    db.session.commit()


def retrieve_all_uids(db: SQLAlchemy) -> List[Uid]:
    uids = db.session.query(Translation).all()
    return [Uid(uid.uid) for uid in uids]
