from __future__ import annotations
import math
import re
from typing import Dict, List, Any, Optional, Set

from dh_harness.core.contracts import SemanticSearchResult

STOPWORDS: Set[str] = {
    "de", "la", "el", "los", "las", "un", "una", "unos", "unas", "y", "o", "en", "a",
    "con", "para", "por", "sobre", "del", "al", "que", "se", "es", "son", "como",
    "the", "of", "and", "in", "to", "for", "with", "on", "at", "by", "from", "an", "a",
    "is", "are", "as", "how", "what", "which", "using"
}

def _stem_tokens(word: str) -> List[str]:
    w = word.lower()
    variants = [w]
    if len(w) >= 5:
        variants.append(w[:5])
    if len(w) >= 6:
        variants.append(w[:6])
    return variants

def _tokenize(text: str) -> List[str]:
    """Tokenizes text into normalized lowercase words, stems and bigrams."""
    clean = re.sub(r"[^a-zA-Z0-9áéíóúÁÉÍÓÚñÑ_]+", " ", text.lower())
    raw_words = [w.strip() for w in clean.split() if len(w.strip()) > 1 and w.strip() not in STOPWORDS]

    tokens: List[str] = []
    for w in raw_words:
        tokens.extend(_stem_tokens(w))

    # Add bigrams for contextual phrase matching
    for i in range(len(raw_words) - 1):
        tokens.append(f"{raw_words[i]}_{raw_words[i+1]}")

    return tokens

class LocalSemanticSearchEngine:
    """
    Local Semantic Search & Vector Similarity Engine (info.md Section 8 & Wave 3).
    Implements TF-IDF term vectorization and Cosine Similarity ranking in pure Python
    with zero external dependencies and 100% privacy compliance.
    """

    def __init__(self):
        self._documents: List[Dict[str, Any]] = []
        self._doc_vectors: List[Dict[str, float]] = []
        self._doc_norms: List[float] = []
        self._idf: Dict[str, float] = {}

    def index_documents(self, documents: List[Dict[str, Any]]) -> None:
        """Indexes curated knowledge documents or ADRs for semantic retrieval."""
        self._documents = list(documents)
        self._doc_vectors = []
        self._doc_norms = []
        self._idf = {}

        if not documents:
            return

        total_docs = len(documents)
        df_counts: Dict[str, int] = {}
        doc_token_counts: List[Dict[str, int]] = []

        # 1. Compute term counts and document frequencies
        for doc in documents:
            combined_text = f"{doc.get('summary', '')} {doc.get('content', '')} {doc.get('key', '')} {doc.get('category', '')}"
            tokens = _tokenize(combined_text)
            counts: Dict[str, int] = {}
            for t in tokens:
                counts[t] = counts.get(t, 0) + 1
            doc_token_counts.append(counts)

            for unique_token in counts.keys():
                df_counts[unique_token] = df_counts.get(unique_token, 0) + 1

        # 2. Compute IDF for all terms
        for term, df in df_counts.items():
            self._idf[term] = math.log(1.0 + (total_docs / float(df)))

        # 3. Vectorize each document and compute L2 norms
        for counts in doc_token_counts:
            total_tokens = sum(counts.values()) or 1
            vector: Dict[str, float] = {}
            squared_sum = 0.0

            for term, count in counts.items():
                tf = count / float(total_tokens)
                tfidf = tf * self._idf.get(term, 1.0)
                vector[term] = tfidf
                squared_sum += tfidf * tfidf

            self._doc_vectors.append(vector)
            self._doc_norms.append(math.sqrt(squared_sum) or 1.0)

    def search(
        self,
        query: str,
        top_k: int = 5,
        min_score: float = 0.05
    ) -> List[SemanticSearchResult]:
        """Performs cosine similarity ranking on indexed documents against natural language query."""
        if not self._documents or not query.strip():
            return []

        query_tokens = _tokenize(query)
        if not query_tokens:
            return []

        # Vectorize query
        q_counts: Dict[str, int] = {}
        for t in query_tokens:
            q_counts[t] = q_counts.get(t, 0) + 1

        total_q_tokens = len(query_tokens)
        q_vector: Dict[str, float] = {}
        q_squared_sum = 0.0

        for term, count in q_counts.items():
            tf = count / float(total_q_tokens)
            idf = self._idf.get(term, math.log(1.0 + len(self._documents)))
            tfidf = tf * idf
            q_vector[term] = tfidf
            q_squared_sum += tfidf * tfidf

        q_norm = math.sqrt(q_squared_sum) or 1.0

        # Calculate cosine similarity with each document
        scored_results: List[SemanticSearchResult] = []
        for idx, doc in enumerate(self._documents):
            d_vec = self._doc_vectors[idx]
            d_norm = self._doc_norms[idx]

            dot_product = 0.0
            for term, q_val in q_vector.items():
                if term in d_vec:
                    dot_product += q_val * d_vec[term]

            similarity = dot_product / (q_norm * d_norm) if (q_norm * d_norm) > 0 else 0.0

            if similarity >= min_score:
                scored_results.append(SemanticSearchResult(
                    key=doc.get("key", f"doc_{idx}"),
                    category=doc.get("category", "general"),
                    summary=doc.get("summary", ""),
                    content=doc.get("content", ""),
                    similarity_score=round(similarity, 4)
                ))

        # Sort descending by similarity score
        scored_results.sort(key=lambda x: x.similarity_score, reverse=True)
        return scored_results[:top_k]
