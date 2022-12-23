import abc
import enum
from dataclasses import dataclass, field
from hashlib import md5
import uuid
from datetime import datetime
from typing import Dict, List, Union

import psycopg2
from psycopg2.extras import DictCursor

from src.backend.config import MonocleConfig


class ExternalData(abc.ABC):
    pass


class SQLData(ExternalData):

    def __init__(
            self,
            name: str,
            uri: str,
            description: str,
            data: Dict,
            updated_at: datetime
    ):
        self.name = name
        self.uri = uri
        self.description = description
        self.data = data
        self.updated_at = updated_at
        self.id = self.update_md5()

    def update_md5(self):
        s = f'{self.uri}'
        return md5(s).hexdigest()


class ExternalDataMapping(abc.ABC):
    pass


class SQLExternalDataMapping(ExternalDataMapping):
    name: str
    uri: str
    description: str
    data: List[str]
    updated_at: str
    table_name: str

    def get_data(self, row):
        return SQLData(
            name=row[self.name],
            uri=row[self.uri],
            description=row[self.description],
            data={k: row[k] for k in self.data},
            updated_at=row[self.updated_at]
        )


class ExternalDataQuerier(abc.ABC):
    pass


class OperatorEnum(enum.Enum):
    eq = 1
    uneq = 2
    lte = 3
    gte = 4
    gt = 5
    lt = 6


@dataclass
class SQLFilter:
    column: str
    operator: OperatorEnum
    value: Union[str, int, float, datetime]


class SQLDataQuerier(ExternalDataQuerier):

    def __init__(self, config: MonocleConfig, mapping: SQLExternalDataMapping):
        self.mapping = mapping
        self._config = config
        self.cursor = self._get_cursor()

    def _get_cursor(self):
        conn = psycopg2.connect(
            dbname=self._config.backend.db,
            user=self._config.backend.user,
            password=self._config.backend.password,
            host=self._config.backend.host,
            port=self._config.backend.port
        )
        return conn.cursor(cursor_factory=DictCursor)

    def filter(self, filters: List[SQLFilter]):
        query = """
            SELECT %(name_col)s,%(uri_col)s,%(description_col)s,%(data_col)s,%(updated_col)s
              FROM %(table_name)s
            WHERE 
        """
        query_params = {
            'table_name': self.mapping.table_name,
            'name_col': self.mapping.name,
            'description_col': self.mapping.description,
            'data_col': ','.join(self.mapping.data),
            'updated_col': self.mapping.updated_at
        }
        for idx, sql_filter in enumerate(filters):
            query += f'%(column{idx})s %(op{idx})s %(value{idx})s'
            query_params[f'column{idx}'] = sql_filter.column
            query_params[f'operator{idx}'] = sql_filter.operator
            query_params[f'value{idx}'] = sql_filter.value
        self.cursor.execute(
            query,
            query_params
        )
        return self._mapping(self.cursor.fetchall())

    def _mapping(self, rows):
        return [self.mapping.get_data(row) for row in rows]


class ExternalDataQuery:

    SOURCES = {
        'sql': SQLDataQuerier
    }
