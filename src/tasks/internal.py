from typing import List

import numpy as np
from docarray import DocumentArray
from prefect import task, flow

from backend.internal import Processor, Model
from search.semantic import MonocleMetadata
from backend.external import SQLDataQuerier, SQLFilter


@flow
def update_internal_data_by_timestamp(model: Model, processor: Processor):
    querier = SQLDataQuerier()
    last_updated_time = _get_last_updated_time()
    docs =
    create_data_from_docs(model, processor, docs)


@flow
def create_data_from_docs(
        model: Model,
        processor: Processor,
        docs: List[ExternalData],
        **kwargs
) -> DocumentArray:
    da = DocumentArray(
        storage='opensearch',
        config=dict(
            n_dim=128,
            hosts=CONFIG.hosts,
            index_name='monocle_data'
        )
    )
    da.extend([create_docarray_doc(processor, doc) for doc in docs])
    da.embeddings = model.generate_embeddings(da.tensors)
    return da


@task
def create_docarray_doc(processor: Processor, doc: ExternalData):
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


def _get_last_updated_time():
