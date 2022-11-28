import abc
import enum
from datetime import datetime
from typing import List, Dict, Optional

from docarray import DocumentArray, Document, dataclass
import numpy as np

from backend.internal import Processor, Model
from docarray.typing import Image, Text, Blob, JSON
import prefect
from prefect import task, flow


class DBDocument:
    pass


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


@flow
def create_data_from_docs(
        model: Model,
        processor: Processor,
        docs: List[DBDocument],
        **kwargs
) -> np.ndarray:
    da = DocumentArray(
        storage='opensearch',
        config=dict(
            n_dim=128,
            hosts=[],
            index_name='monocle_data'
        )
    )
    da.extend([create_docarray_doc(processor, doc) for doc in docs])
    da.embeddings = model.generate_embeddings(da.tensors)


@task
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
