"""Functions used to manage catalogs."""

import logging
import os
import os.path
from functools import lru_cache

import alembic.command
import alembic.config
from alembic.migration import MigrationContext

from sqlalchemy import MetaData, create_engine, event
from sqlalchemy.engine import Engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from sqlalchemy_utils import database_exists

from tchelinux.version import Version


@event.listens_for(Engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    """Configure SQLite to respect case sensitivity in LIKE."""
    cursor = dbapi_connection.cursor()
    cursor.execute('pragma case_sensitive_like=ON')
    cursor.execute('pragma foreign_keys=ON')
    cursor.close()


class UnexpectedDatabaseVersion(Exception):
    """Exception for wrong database version."""

    pass


class Database(object):
    """Implements the abstraction of a DAM Catalog."""

    # Constants required for catalog upgrade.
    __system_dir = os.path.dirname(os.path.realpath(__file__ + "/.."))
    __PATH = os.path.join(__system_dir, "data")
    __migration_config = os.path.join(__PATH, "alembic.ini")
    __migration_scripts = os.path.join(__PATH, "schemas")

    def __init__(self, initstr):
        """Initialize a new catalog."""
        self.__session = None
        self.__init_string = initstr
        self.___engine = create_engine(initstr)
        # configure logging.
        logging.getLogger("alembic").setLevel(logging.CRITICAL)

    def __load_schema(self):
        self.__meta = MetaData()
        self.__meta.reflect(self.__engine)
        self.__Base = declarative_base()
        self.__Base.metadata = self.__meta

    @property
    def revision(self):
        """Query the database revision."""
        if self.__engine is None:
            return ""
        if not database_exists(self.__init_string):
            msg = "Cannot verify revision of inexistent database: {}"
            raise Exception(msg.format(self.__init_string))
        context = MigrationContext.configure(self.__engine.connect())
        rev = context.get_current_revision()
        return rev

    def open(self):
        """Open the database for use."""
        if self.__session is not None:
            return
        if database_exists(self.__init_string):
            self.__engine = create_engine(self.__init_string)
            if not Version.version_match(self.revision):
                msg = "Database needs to be upgraded."
                raise UnexpectedDatabaseVersion(msg)
            self.__session = sessionmaker(bind=self.__engine)()
            self.__load_schema()
        else:
            msg = "Database not found: %s" % (self._catalog_file)
            raise Exception(msg)

    def __check_catalog(self):
        if self.__session is None:
            err = "Catalog '%s' has not been opened."
            raise Exception(err % self._catalog_name)

    def upgrade(self):
        """Upgrade catalog to the latest version."""
        try:
            self.open()
        except UnexpectedDatabaseVersion:
            self.__perform_upgrade()
        except Exception:
            raise
        else:
            msg = "Database do not need to be upgraded."
            raise UnexpectedDatabaseVersion(msg)

    def __perform_upgrade(self):
        alembic_cfg = alembic.config.Config(Database.__migration_config)
        alembic_cfg.set_main_option("sqlalchemy.url", self.__init_string)
        alembic_cfg.set_main_option("script_location",
                                    Database.__migration_scripts)
        alembic.command.upgrade(alembic_cfg, "head")

    @property
    def session(self):
        """Retrieve the database session."""
        self.__check_catalog()
        return self.__session

    def create(self):
        """Create a new catalog."""
        if self.__session is not None:
            raise Exception("Catalog is already created and opened.")
        if database_exists(self.__init_string):
            msg = "Database already exists: {}".format(self.__init_string)
            raise Exception(msg)
        else:
            self.__perform_upgrade()
            self.__engine = create_engine(self.__init_string)
            self.__session = sessionmaker(bind=self.__engine)()
            self.__load_schema()

    @lru_cache(maxsize=20)
    def entity(self, entity):
        """Obtain an entity class for a specific table.

        The use of a cache is not due to performance, but to avoid creating
        multiple instances of the entity types.
        """
        return type(entity, (self.__Base,),
                    {'__table__': self.__meta.tables[entity]})

    def close(self):
        """Close the database."""
        self.__check_catalog()
        self.__engine.dispose()
