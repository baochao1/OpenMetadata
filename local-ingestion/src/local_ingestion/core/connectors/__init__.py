"""Core Connectors Module - Source and Sink Connectors for metadata extraction"""

from local_ingestion.core.connectors.base import SourceConnector, SinkConnector
from local_ingestion.core.connectors.mysql import MySQLSourceConnector
from local_ingestion.core.connectors.postgres import PostgresSourceConnector
from local_ingestion.core.connectors.snowflake import SnowflakeSourceConnector
from local_ingestion.core.connectors.file_sink import (
    JSONFileSink,
    NDJSONFileSink,
    ParquetFileSink,
    LocalFileSinkConfig,
    FileSinkConfig,
    FileFormat,
)

__all__ = [
    "SourceConnector",
    "SinkConnector",
    "MySQLSourceConnector",
    "PostgresSourceConnector",
    "SnowflakeSourceConnector",
    "JSONFileSink",
    "NDJSONFileSink",
    "ParquetFileSink",
    "LocalFileSinkConfig",
    "FileSinkConfig",
    "FileFormat",
]
