"""Base connector classes for source and sink connectors"""
from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional, TYPE_CHECKING

import structlog

from local_ingestion.schema.data.database import Database, DatabaseSchema
from local_ingestion.schema.data.table import Table
from local_ingestion.schema.service.connection import (
    DatabaseConnection,
    MySQLConnection,
    PostgresConnection,
    SnowflakeConnection,
    FileSinkConfig,
)

if TYPE_CHECKING:
    from sqlalchemy.orm import Session

logger = structlog.get_logger()


class SourceConnector(ABC):
    """Abstract base class for source connectors that extract metadata from data sources"""

    def __init__(self) -> None:
        self._connection: Optional[Any] = None
        self._session: Optional["Session"] = None
        self._config: Optional[DatabaseConnection] = None
        self._connected: bool = False

    @abstractmethod
    def connect(self, config: DatabaseConnection) -> None:
        """Connect to the source data source

        Args:
            config: Connection configuration for the source
        """
        pass

    @abstractmethod
    def disconnect(self) -> None:
        """Disconnect from the source data source"""
        pass

    @abstractmethod
    def fetch_databases(self) -> List[Database]:
        """Fetch all databases from the source

        Returns:
            List of Database objects
        """
        pass

    @abstractmethod
    def fetch_schemas(self, database: str) -> List[DatabaseSchema]:
        """Fetch all schemas from a database

        Args:
            database: Database name

        Returns:
            List of DatabaseSchema objects
        """
        pass

    @abstractmethod
    def fetch_tables(self, database: str, schema: str) -> List[Table]:
        """Fetch all tables from a schema

        Args:
            database: Database name
            schema: Schema name

        Returns:
            List of Table objects with columns
        """
        pass

    @abstractmethod
    def fetch_columns(self, table: Table) -> List[Any]:
        """Fetch columns for a table

        Args:
            table: Table object

        Returns:
            List of Column objects
        """
        pass

    def is_connected(self) -> bool:
        """Check if connector is connected

        Returns:
            True if connected, False otherwise
        """
        return self._connected

    def _log_connection_error(self, error: Exception) -> None:
        """Log connection errors with structured logging"""
        logger.error(
            "connection_error",
            connector=self.__class__.__name__,
            error_type=type(error).__name__,
            error_message=str(error),
        )


class SinkConnector(ABC):
    """Abstract base class for sink connectors that write metadata to output destinations"""

    def __init__(self) -> None:
        self._config: Optional[FileSinkConfig] = None
        self._connected: bool = False
        self._pending_writes: List[Any] = []

    @abstractmethod
    def connect(self, config: FileSinkConfig) -> None:
        """Connect to the sink destination

        Args:
            config: Configuration for the sink
        """
        pass

    @abstractmethod
    def write_table(self, table: Table) -> None:
        """Write table metadata to the sink

        Args:
            table: Table object to write
        """
        pass

    @abstractmethod
    def write_database(self, database: Database) -> None:
        """Write database metadata to the sink

        Args:
            database: Database object to write
        """
        pass

    @abstractmethod
    def flush(self) -> None:
        """Flush pending writes to the sink"""
        pass

    @abstractmethod
    def close(self) -> None:
        """Close the sink and cleanup resources"""
        pass

    def is_connected(self) -> bool:
        """Check if connector is connected

        Returns:
            True if connected, False otherwise
        """
        return self._connected

    def _log_write_error(self, error: Exception, entity_type: str) -> None:
        """Log write errors with structured logging"""
        logger.error(
            "write_error",
            connector=self.__class__.__name__,
            entity_type=entity_type,
            error_type=type(error).__name__,
            error_message=str(error),
        )
