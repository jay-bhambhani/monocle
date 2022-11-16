import abc
import enum
from datetime import datetime
from typing import List, Dict, Optional

from docarray import DocumentArray, Document, dataclass
import numpy as np

from backend.internal import Processor, Model
from docarray.typing import Image, Text, Blob, JSON


@dataclass
class MonocleData:
    id: Text


@dataclass
class GraphNode(MonocleData):
    id: Text
    key: Text
    properties: JSON


@dataclass
class GraphRelationship(MonocleData):
    id: Text
    key: Text
    value: Text
    node: GraphNode
    connections: JSON


@dataclass
class RelationalData(MonocleData):
    id: Text
    data: JSON


@dataclass
class TimeSeriesData(MonocleData):
    id: Text
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


def create_data_from_docs(
        model: Model,
        processor: Processor,
        docs: List[MonocleMetadata],
        **kwargs
) -> np.ndarray:
    da = DocumentArray(
        storage='elasticsearch',
        config={

        }
    )
    da.extend([create_docarray_doc(processor, doc) for doc in docs])
    da.embed(model)


def create_docarray_doc(processor: Processor, doc: DBDocument):
    return MonocleMetadata(
        uuid=doc.uuid,
        name=doc.name,
        uri=doc.uri,
        description=doc.description,
        data=doc.data,
        updated_at=doc.updated_at,
        created_at=doc.created_at,
        tensors=processor.process(doc.data)
    )
