
"""TensorFlow Cross-Encoder Reranker

This module provides a training loop (outline) and an inference function for a TensorFlow-based
cross-encoder reranker. It uses Hugging Face Transformers (TF) to build a model that scores (query, doc) pairs.

Notes:
- Training a real model requires GPUs and a sizable labeled dataset.
- This file provides runnable code structure. To train, install `transformers[sentencepiece]` and `tensorflow`.
"""
from typing import List, Tuple
import numpy as np

try:
    from transformers import TFAutoModel, AutoTokenizer
    import tensorflow as tf
except Exception as e:
    # If transformers/tensorflow are not installed, we still allow the file to be imported for static analysis.
    TFAutoModel = None
    AutoTokenizer = None
    tf = None

class TFReranker:
    def __init__(self, model_name: str = 'distilbert-base-uncased', max_length: int = 128):
        if AutoTokenizer is None or TFAutoModel is None:
            raise ImportError('transformers and tensorflow are required for TFReranker. pip install transformers tensorflow')
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = TFAutoModel.from_pretrained(model_name)

        # Simple head: pool CLS token to a single scalar score via Dense
        inputs = {
            'input_ids': tf.keras.layers.Input(shape=(max_length,), dtype=tf.int32, name='input_ids'),
            'attention_mask': tf.keras.layers.Input(shape=(max_length,), dtype=tf.int32, name='attention_mask')
        }
        outputs = self.model(inputs)[0]  # sequence output
        cls = outputs[:,0,:]  # CLS token
        score = tf.keras.layers.Dense(1, activation=None, name='score')(cls)
        self.cross_model = tf.keras.Model(inputs=inputs, outputs=score)
        self.max_length = max_length
        self.cross_model.compile(optimizer=tf.keras.optimizers.Adam(1e-5), loss='mse')


    def _prepare(self, queries: List[str], docs: List[str]):
        # concatenate [query] [SEP] [doc] or use pair encoding
        pairs = [q + " [SEP] " + d for q, d in zip(queries, docs)]
        enc = self.tokenizer(pairs, truncation=True, padding='max_length', max_length=self.max_length, return_tensors='tf')
        return enc

    def train(self, dataset: List[Tuple[str, str, float]], epochs: int = 1, batch_size: int = 8):
        """Train on a dataset of (query, doc, score) triples."""
        queries = [q for q, d, s in dataset]
        docs = [d for q, d, s in dataset]
        scores = np.array([s for q, d, s in dataset], dtype=np.float32)
        enc = self._prepare(queries, docs)
        self.cross_model.fit(x={'input_ids': enc['input_ids'], 'attention_mask': enc['attention_mask']},
                             y=scores, epochs=epochs, batch_size=batch_size)

    def score(self, query: str, docs: List[str]):
        enc = self._prepare([query]*len(docs), docs)
        preds = self.cross_model.predict({'input_ids': enc['input_ids'], 'attention_mask': enc['attention_mask']})
        return [float(p[0]) for p in preds]

if __name__ == '__main__':
    print('TFReranker module loaded.')
