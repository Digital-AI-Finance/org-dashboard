"""ML-based topic modeling for repositories."""

import logging
from typing import Any

from ..models.repository import Repository
from .base import BaseAnalyzer


class TopicModelingAnalyzer(BaseAnalyzer):
    """Extract research topics using machine learning."""

    def __init__(
        self,
        n_topics: int = 5,
        logger: logging.Logger | None = None,
    ):
        self.n_topics = n_topics
        self.logger = logger or logging.getLogger(__name__)

    async def analyze(self, repositories: list[Repository]) -> dict[str, Any]:
        """
        Perform topic modeling on repository descriptions.

        Args:
            repositories: List of repositories

        Returns:
            Topic analysis results
        """
        # Import ML libraries here (lazy import)

        # Prepare documents
        documents = [
            f"{repo.name} {repo.description} {' '.join(repo.topics)}" for repo in repositories
        ]

        # NMF topic extraction
        nmf_results = await self._extract_nmf_topics(documents)

        # LDA topic extraction
        lda_results = await self._extract_lda_topics(documents)

        return {"methods": {"nmf": nmf_results, "lda": lda_results}}

    async def _extract_nmf_topics(self, documents: list[str]) -> dict[str, Any]:
        """Extract topics using NMF."""
        from sklearn.decomposition import NMF
        from sklearn.feature_extraction.text import TfidfVectorizer

        vectorizer = TfidfVectorizer(max_features=1000, min_df=1, max_df=0.8, ngram_range=(1, 2))

        tfidf = vectorizer.fit_transform(documents)
        model = NMF(n_components=min(self.n_topics, len(documents)), random_state=42)
        model.fit(tfidf)

        # Extract topic keywords
        feature_names = vectorizer.get_feature_names_out()
        topics = []

        for topic_idx, topic in enumerate(model.components_):
            top_indices = topic.argsort()[-10:][::-1]
            keywords = [feature_names[i] for i in top_indices]
            weights = [float(topic[i]) for i in top_indices]

            topics.append(
                {
                    "topic_id": topic_idx,
                    "words": keywords,
                    "weights": weights,
                    "label": " & ".join(keywords[:3]),
                }
            )

        return {"method": "NMF", "n_topics": self.n_topics, "topics": topics}

    async def _extract_lda_topics(self, documents: list[str]) -> dict[str, Any]:
        """Extract topics using LDA."""
        from sklearn.decomposition import LatentDirichletAllocation
        from sklearn.feature_extraction.text import CountVectorizer

        vectorizer = CountVectorizer(max_features=1000, min_df=1, max_df=0.8)

        counts = vectorizer.fit_transform(documents)
        model = LatentDirichletAllocation(
            n_components=min(self.n_topics, len(documents)), random_state=42
        )
        model.fit(counts)

        # Extract topic keywords
        feature_names = vectorizer.get_feature_names_out()
        topics = []

        for topic_idx, topic in enumerate(model.components_):
            top_indices = topic.argsort()[-10:][::-1]
            keywords = [feature_names[i] for i in top_indices]
            weights = [float(topic[i]) for i in top_indices]

            topics.append(
                {
                    "topic_id": topic_idx,
                    "words": keywords,
                    "weights": weights,
                    "label": " & ".join(keywords[:3]),
                }
            )

        return {"method": "LDA", "n_topics": self.n_topics, "topics": topics}

    async def validate_results(self, results: dict[str, Any]) -> bool:
        """Validate topic modeling results."""
        return "methods" in results and len(results["methods"]) > 0
