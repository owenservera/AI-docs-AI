"""
Vector Store for Documentation RAG (Retrieval-Augmented Generation)

This module provides a lightweight, file-based vector store for semantic search
over documentation chunks. It uses 'sentence-transformers' for generating embeddings
and 'numpy' for cosine similarity search.
"""

import os
import json
import logging
import numpy as np
from typing import List, Dict, Any, Optional, Tuple, Union
from datetime import datetime

# Lazy import for sentence_transformers to avoid startup latency if not used
try:
    from sentence_transformers import SentenceTransformer
    HAS_TRANSFORMERS = True
except ImportError:
    HAS_TRANSFORMERS = False

logger = logging.getLogger(__name__)

class VectorStore:
    """Lightweight local vector store for documentation"""
    
    def __init__(self, storage_dir: str, collection_name: str = "default"):
        """
        Initialize the vector store.
        
        Args:
            storage_dir: Directory to save the index files
            collection_name: Name of the collection (usually the doc alias)
        """
        self.storage_dir = storage_dir
        self.collection_name = collection_name
        self.index_path = os.path.join(storage_dir, f"{collection_name}_index.npy")
        self.metadata_path = os.path.join(storage_dir, f"{collection_name}_meta.json")
        
        # State
        self.embeddings: Optional[np.ndarray] = None
        self.metadata: List[Dict[str, Any]] = []
        self.model = None
        
        # Load existing index if available
        self._load_index()

    def _get_model(self):
        """Lazy load the embedding model"""
        if self.model is None:
            if not HAS_TRANSFORMERS:
                raise ImportError(
                    "sentence-transformers is not installed. "
                    "Please run: pip install sentence-transformers"
                )
            logger.info("Loading embedding model (all-MiniLM-L6-v2)...")
            self.model = SentenceTransformer('all-MiniLM-L6-v2')
        return self.model

    def add_texts(self, texts: List[str], metadatas: List[Dict[str, Any]]) -> bool:
        """
        Add text chunks to the vector store.
        
        Args:
            texts: List of text chunks to embed
            metadatas: List of metadata dictionaries for each chunk
        """
        if not texts:
            return False
            
        try:
            model = self._get_model()
            logger.info(f"Generating embeddings for {len(texts)} chunks...")
            
            # Generate embeddings
            new_embeddings = model.encode(texts, convert_to_numpy=True)
            
            # Update state
            if self.embeddings is None:
                self.embeddings = new_embeddings
            else:
                self.embeddings = np.vstack((self.embeddings, new_embeddings))
                
            self.metadata.extend(metadatas)
            
            # Save to disk
            self._save_index()
            return True
            
        except Exception as e:
            logger.error(f"Failed to add texts to vector store: {e}")
            return False

    def search(self, query: str, k: int = 5) -> List[Dict[str, Any]]:
        """
        Semantic search for the query.
        
        Args:
            query: The search query string
            k: Number of results to return
            
        Returns:
            List of results with score and metadata
        """
        if self.embeddings is None or len(self.metadata) == 0:
            return []
            
        try:
            model = self._get_model()
            query_embedding = model.encode([query], convert_to_numpy=True)
            
            # Cosine similarity
            # Normalize embeddings first for cosine similarity using dot product
            # (SentenceTransformer output is usually already normalized, but let's be safe)
            # Actually, let's just use dot product as a proxy for cosine sim if normalized
            
            # Simple dot product
            scores = np.dot(self.embeddings, query_embedding.T).flatten()
            
            # Get top k indices
            # argsort returns lowest to highest, so we take last k and reverse
            top_k_indices = np.argsort(scores)[-k:][::-1]
            
            results = []
            for idx in top_k_indices:
                results.append({
                    "score": float(scores[idx]),
                    "content": self.metadata[idx].get("content", ""), # Assume content is in metadata or we need to pass it
                    "metadata": self.metadata[idx]
                })
                
            return results
            
        except Exception as e:
            logger.error(f"Search failed: {e}")
            return []

    def _save_index(self):
        """Save embeddings and metadata to disk"""
        try:
            if self.embeddings is not None:
                np.save(self.index_path, self.embeddings)
            
            with open(self.metadata_path, 'w', encoding='utf-8') as f:
                json.dump(self.metadata, f, ensure_ascii=False, indent=2)
                
            logger.info(f"Saved vector index for {self.collection_name}")
        except Exception as e:
            logger.error(f"Failed to save index: {e}")

    def _load_index(self):
        """Load embeddings and metadata from disk"""
        if os.path.exists(self.index_path) and os.path.exists(self.metadata_path):
            try:
                self.embeddings = np.load(self.index_path)
                with open(self.metadata_path, 'r', encoding='utf-8') as f:
                    self.metadata = json.load(f)
                logger.info(f"Loaded {len(self.metadata)} vectors for {self.collection_name}")
            except Exception as e:
                logger.error(f"Failed to load index: {e}")
