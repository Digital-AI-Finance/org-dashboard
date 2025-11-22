#!/usr/bin/env python3
"""
Full-text search indexer with faceted navigation.
Indexes READMEs, notebooks, papers for searchability.
"""

import json
import os
import pickle
import re
from collections import defaultdict
from datetime import datetime
from typing import Any


class SearchIndex:
    """Full-text search index with faceted navigation."""

    def __init__(self):
        self.documents = {}  # doc_id -> document data
        self.inverted_index = defaultdict(set)  # term -> set of doc_ids
        self.facets = defaultdict(lambda: defaultdict(set))  # facet_name -> value -> doc_ids
        self.doc_counter = 0

    def add_document(self, content: str, metadata: dict[str, Any]) -> str:
        """Add a document to the search index."""
        doc_id = f"doc_{self.doc_counter}"
        self.doc_counter += 1

        # Store document
        self.documents[doc_id] = {
            "content": content,
            "metadata": metadata,
            "added_at": datetime.now().isoformat(),
        }

        # Tokenize and index
        tokens = self._tokenize(content)
        for token in tokens:
            self.inverted_index[token].add(doc_id)

        # Index metadata fields as facets
        for facet_name, facet_value in metadata.items():
            if isinstance(facet_value, list):
                for value in facet_value:
                    self.facets[facet_name][str(value).lower()].add(doc_id)
            elif facet_value:
                self.facets[facet_name][str(facet_value).lower()].add(doc_id)

        return doc_id

    def search(self, query: str, filters: dict[str, Any] = None, limit: int = 100) -> list[dict]:
        """
        Search the index with optional facet filters.

        Args:
            query: Search query string
            filters: Dictionary of facet filters {facet_name: value}
            limit: Maximum number of results

        Returns:
            List of matching documents with scores
        """
        # Tokenize query
        query_tokens = self._tokenize(query)

        if not query_tokens:
            return []

        # Find documents containing query terms
        result_sets = []
        for token in query_tokens:
            if token in self.inverted_index:
                result_sets.append(self.inverted_index[token])

        # Intersection of results (AND query)
        if not result_sets:
            return []

        matching_docs = result_sets[0]
        for result_set in result_sets[1:]:
            matching_docs = matching_docs & result_set

        # Apply facet filters
        if filters:
            for facet_name, facet_value in filters.items():
                if facet_name in self.facets:
                    filter_value = str(facet_value).lower()
                    if filter_value in self.facets[facet_name]:
                        matching_docs = matching_docs & self.facets[facet_name][filter_value]
                    else:
                        return []  # No matches for this filter

        # Score documents (simple TF-IDF approximation)
        scored_docs = []
        for doc_id in matching_docs:
            score = self._score_document(doc_id, query_tokens)
            doc = self.documents[doc_id]

            scored_docs.append(
                {
                    "doc_id": doc_id,
                    "score": score,
                    "content": doc["content"][:300],  # Preview
                    "metadata": doc["metadata"],
                }
            )

        # Sort by score
        scored_docs.sort(key=lambda x: x["score"], reverse=True)

        return scored_docs[:limit]

    def get_facets(self, query: str = None) -> dict[str, dict[str, int]]:
        """
        Get available facets with counts.

        Args:
            query: Optional query to get facets for specific results

        Returns:
            Dictionary of facets with value counts
        """
        facet_counts = {}

        # If query provided, limit to matching docs
        if query:
            query_tokens = self._tokenize(query)
            result_sets = [
                self.inverted_index[token] for token in query_tokens if token in self.inverted_index
            ]

            if result_sets:
                matching_docs = result_sets[0]
                for result_set in result_sets[1:]:
                    matching_docs = matching_docs & result_set
            else:
                matching_docs = set()
        else:
            matching_docs = set(self.documents.keys())

        # Count facet values
        for facet_name, facet_values in self.facets.items():
            facet_counts[facet_name] = {}

            for value, doc_ids in facet_values.items():
                count = len(doc_ids & matching_docs)
                if count > 0:
                    facet_counts[facet_name][value] = count

        return facet_counts

    def autocomplete(self, prefix: str, limit: int = 10) -> list[str]:
        """Get autocomplete suggestions for a prefix."""
        prefix = prefix.lower()
        suggestions = [term for term in self.inverted_index.keys() if term.startswith(prefix)]
        return sorted(suggestions)[:limit]

    def _tokenize(self, text: str) -> set[str]:
        """Tokenize text into searchable terms."""
        # Convert to lowercase
        text = text.lower()

        # Remove punctuation except hyphens in words
        text = re.sub(r"[^\w\s-]", " ", text)

        # Split into words
        words = text.split()

        # Remove common stop words
        stop_words = {
            "a",
            "an",
            "and",
            "are",
            "as",
            "at",
            "be",
            "by",
            "for",
            "from",
            "has",
            "he",
            "in",
            "is",
            "it",
            "its",
            "of",
            "on",
            "that",
            "the",
            "to",
            "was",
            "will",
            "with",
        }

        # Filter and return
        tokens = {word for word in words if len(word) > 2 and word not in stop_words}

        return tokens

    def _score_document(self, doc_id: str, query_tokens: set[str]) -> float:
        """Score a document for relevance (simple TF-IDF)."""
        doc = self.documents[doc_id]
        content = doc["content"].lower()

        score = 0.0

        for token in query_tokens:
            # Term frequency
            tf = content.count(token)

            # Inverse document frequency
            docs_with_term = len(self.inverted_index.get(token, set()))
            idf = 1.0 / (1 + docs_with_term) if docs_with_term > 0 else 0

            score += tf * idf

        # Boost if term appears in title/metadata
        if "title" in doc["metadata"]:
            title = doc["metadata"]["title"].lower()
            for token in query_tokens:
                if token in title:
                    score *= 2.0

        return score

    def save_index(self, filename: str = "data/search_index.pkl") -> None:
        """Save index to disk."""
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        with open(filename, "wb") as f:
            pickle.dump(
                {
                    "documents": self.documents,
                    "inverted_index": dict(self.inverted_index),
                    "facets": dict(self.facets),
                    "doc_counter": self.doc_counter,
                },
                f,
            )

    @classmethod
    def load_index(cls, filename: str = "data/search_index.pkl") -> "SearchIndex":
        """Load index from disk."""
        index = cls()

        if os.path.exists(filename):
            with open(filename, "rb") as f:
                data = pickle.load(f)
                index.documents = data["documents"]
                index.inverted_index = defaultdict(set, data["inverted_index"])
                index.facets = defaultdict(lambda: defaultdict(set), data["facets"])
                index.doc_counter = data["doc_counter"]

        return index


def build_search_index(repos_data: list[dict]) -> SearchIndex:
    """Build search index from repository data."""
    print("Building search index...")
    index = SearchIndex()

    for repo in repos_data:
        repo_name = repo["name"]
        research_meta = repo.get("research_metadata", {})

        # Index README
        if repo.get("readme") and repo["readme"] != "No README available":
            index.add_document(
                content=repo["readme"],
                metadata={
                    "type": "readme",
                    "repo": repo_name,
                    "title": repo["description"],
                    "language": repo["language"],
                    "topics": repo.get("topics", []),
                },
            )

        # Index publications
        for pub in research_meta.get("publications", []):
            if pub.get("title") or pub.get("abstract"):
                content = f"{pub.get('title', '')} {pub.get('abstract', '')}"
                index.add_document(
                    content=content,
                    metadata={
                        "type": "publication",
                        "repo": repo_name,
                        "title": pub.get("title", "Untitled"),
                        "year": pub.get("year"),
                        "doi": pub.get("doi"),
                        "arxiv_id": pub.get("arxiv_id"),
                    },
                )

        # Index research metadata
        if research_meta.get("research"):
            research = research_meta["research"]
            if research.get("abstract"):
                index.add_document(
                    content=research["abstract"],
                    metadata={
                        "type": "research",
                        "repo": repo_name,
                        "title": research.get("title", repo_name),
                        "keywords": research.get("keywords", []),
                    },
                )

    # Save index
    index.save_index()
    print(f"Index built: {len(index.documents)} documents indexed")

    return index


def generate_search_interface_data() -> dict[str, Any]:
    """Generate data for search interface."""
    # Load index
    index = SearchIndex.load_index()

    if not index.documents:
        return {"error": "No search index found"}

    # Get all available facets
    all_facets = index.get_facets()

    # Get document type distribution
    type_dist = {}
    for doc in index.documents.values():
        doc_type = doc["metadata"].get("type", "unknown")
        type_dist[doc_type] = type_dist.get(doc_type, 0) + 1

    return {
        "total_documents": len(index.documents),
        "document_types": type_dist,
        "available_facets": all_facets,
        "index_size": f"{len(index.inverted_index)} terms",
    }


def main():
    """Test search indexer."""
    print("Search Indexer")
    print("=" * 60)

    # Load repos data
    if os.path.exists("data/repos.json"):
        with open("data/repos.json") as f:
            repos_data = json.load(f)

        # Build index
        index = build_search_index(repos_data)

        # Test search
        print("\nTest search for 'machine learning':")
        results = index.search("machine learning", limit=5)

        for i, result in enumerate(results, 1):
            print(f"\n{i}. {result['metadata'].get('title', 'Untitled')}")
            print(f"   Type: {result['metadata'].get('type')}")
            print(f"   Repo: {result['metadata'].get('repo')}")
            print(f"   Score: {result['score']:.2f}")
            print(f"   Preview: {result['content'][:100]}...")

        # Show facets
        print("\nAvailable facets:")
        facets = index.get_facets()
        for facet_name, values in list(facets.items())[:3]:
            print(f"\n{facet_name}:")
            for value, count in list(values.items())[:5]:
                print(f"  - {value}: {count}")

    else:
        print("No repos data found. Run fetch_org_data_research.py first.")


if __name__ == "__main__":
    main()
