from typing import Any

from sqlalchemy.orm import Session

class BaseService:
    def __init__(self, session:Session):
        self._db = session

    def _add_registrty(self, new_registry:Any):
        self._db.add(new_registry)
        self._db.commit()
        self._db.refresh(new_registry)

    def _update_registry(self, registry:Any):
        self._db.commit()
        self._db.refresh(registry)

    def _delete_registry(self, registry:Any):
        self._db.delete(registry)
        self._db.commit()
