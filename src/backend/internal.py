import abc
from typing import List

from docarray import DocumentArray
import numpy as np
import tensorflow as tf


class Processor(abc.ABC):
    """Base class for creating numpy ndarrays """
    def __init__(self, for_model):
        self.model_versions = for_model

    def process(self, input_data: DocumentArray, **kwargs) -> np.ndarray:
        raise NotImplementedError

    # def convert(self, output_data: np.ndarray) -> DocumentArray:
    #     raise NotImplementedError


class Model(abc.ABC):
    """Base class to measure similarity"""
    def __init__(self, version: str, task: str):
        self.version = version
        self.task = task

    def generate_embeddings(self, inputs: np.ndarray) -> np.ndarray:
        raise NotImplementedError()

    def __str__(self):
        return f'Model<task: {self.task}, version: {self.version}'
