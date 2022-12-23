
from docarray import DocumentArray, Document, dataclass
import numpy as np
from docarray.typing import Image, Text, Blob, JSON


@dataclass
class MonocleData:
    id: Text


@dataclass
class GraphNode(MonocleData):
    key: Text
    properties: JSON


@dataclass
class GraphRelationship(MonocleData):
    key: Text
    value: Text
    node: GraphNode
    connections: JSON


@dataclass
class RelationalData(MonocleData):
    data: JSON


@dataclass
class TimeSeriesData(MonocleData):
    data_point: RelationalData
    timestamp: Text


@dataclass
class MonocleMetadata:
    uuid: Text
    name: Text
    description: Blob
    uri: Text
    data: MonocleData
    updated_at: Text
    created_at: Text
