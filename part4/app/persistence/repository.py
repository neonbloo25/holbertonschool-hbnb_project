#!/usr/bin/python3
import logging
from abc import ABC, abstractmethod

logger = logging.getLogger(__name__)


def get_db():
    from app import db
    return db


class Repository(ABC):
    @abstractmethod
    def add(self, obj):
        pass

    @abstractmethod
    def get(self, obj_id):
        pass

    @abstractmethod
    def get_all(self):
        pass

    @abstractmethod
    def update(self, obj_id, data):
        pass

    @abstractmethod
    def delete(self, obj_id):
        pass

    @abstractmethod
    def get_by_attribute(self, attr_name, attr_value):
        pass


class InMemoryRepository(Repository):
    def __init__(self):
        logger.debug("🧠 Initializing in-memory repository...")
        self._storage = {}
        logger.debug("✅ In-memory storage ready.")

    def add(self, obj):
        logger.debug(f"📦 Adding object with ID {obj.id} to in-memory storage.")
        self._storage[obj.id] = obj

    def get(self, obj_id):
        logger.debug(f"🔍 Retrieving object with ID {obj_id} from in-memory storage.")
        return self._storage.get(obj_id)

    def get_all(self):
        logger.debug("📋 Retrieving all objects from in-memory storage.")
        return list(self._storage.values())

    def update(self, obj_id, data):
        logger.debug(f"♻️ Updating object {obj_id} in in-memory storage with data: {data}")
        obj = self.get(obj_id)
        if obj:
            for key, value in data.items():
                setattr(obj, key, value)
            logger.debug("✅ Object updated in memory.")

    def delete(self, obj_id):
        logger.debug(f"🗑️ Deleting object {obj_id} from in-memory storage.")
        if obj_id in self._storage:
            del self._storage[obj_id]
            logger.debug("✅ Object deleted from memory.")

    def get_by_attribute(self, attr_name, attr_value):
        logger.debug(f"🔍 Searching for object where {attr_name} == {attr_value} in memory.")
        return next(
            (obj for obj in self._storage.values() if getattr(obj, attr_name, None) == attr_value),
            None
        )


class SQLAlchemyRepository(Repository):
    def __init__(self, model):
        logger.debug(f"🔧 Initializing SQLAlchemyRepository for model: {model.__name__}")
        self.model = model

    def add(self, obj):
        db = get_db()
        try:
            logger.debug(f"📦 Adding object to DB: {obj}")
            db.session.add(obj)
            db.session.commit()
            logger.debug("✅ Object added and committed to DB.")
        except Exception:
            db.session.rollback()
            logger.exception("❌ Failed to add object to DB.")
            raise

    def get(self, obj_id):
        logger.debug(f"🔍 Retrieving object with ID {obj_id} from DB.")
        db = get_db()
        return self.model.query.get(obj_id)

    def get_all(self):
        logger.debug("📋 Retrieving all objects from DB.")
        db = get_db()
        return self.model.query.all()

    def update(self, obj_id, data):
        db = get_db()
        logger.debug(f"♻️ Updating object {obj_id} in DB with data: {data}")
        obj = self.get(obj_id)
        if obj:
            try:
                for key, value in data.items():
                    setattr(obj, key, value)
                db.session.commit()
                logger.debug("✅ Object updated and committed.")
            except Exception:
                db.session.rollback()
                logger.exception("❌ Failed to update object in DB.")
                raise

    def delete(self, obj_id):
        db = get_db()
        logger.debug(f"🗑️ Deleting object {obj_id} from DB.")
        obj = self.get(obj_id)
        if obj:
            try:
                db.session.delete(obj)
                db.session.commit()
                logger.debug("✅ Object deleted and committed.")
            except Exception:
                db.session.rollback()
                logger.exception("❌ Failed to delete object from DB.")
                raise

    def get_by_attribute(self, attr_name, attr_value):
        logger.debug(f"🔍 Querying DB for {self.model.__name__} where {attr_name} == {attr_value}")
        db = get_db()
        return self.model.query.filter_by(**{attr_name: attr_value}).first()
