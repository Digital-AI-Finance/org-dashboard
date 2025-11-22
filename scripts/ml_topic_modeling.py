#!/usr/bin/env python3
"""
Machine Learning topic modeling for research repositories.
Uses scikit-learn for NMF and LDA topic extraction from README files.
"""

import json
import os
import re
from typing import Dict, List, Any, Tuple
from datetime import datetime
from collections import defaultdict

try:
    from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
    from sklearn.decomposition import NMF, LatentDirichletAllocation
    import numpy as np
    SKLEARN_AVAILABLE = True
except ImportError:
    print("scikit-learn not installed. Install with: pip install scikit-learn")
    SKLEARN_AVAILABLE = False

try:
    import plotly.graph_objects as go
    import plotly.express as px
    PLOTLY_AVAILABLE = True
except ImportError:
    PLOTLY_AVAILABLE = False


class MLTopicModeler:
    """Machine learning-based topic modeling for repository analysis."""

    def __init__(self, n_topics=5, n_top_words=10):
        self.n_topics = n_topics
        self.n_top_words = n_top_words
        self.vectorizer = None
        self.model = None

    def preprocess_text(self, text: str) -> str:
        """Preprocess text for topic modeling."""
        if not text:
            return ""

        # Convert to lowercase
        text = text.lower()

        # Remove URLs
        text = re.sub(r'http\S+|www\S+', '', text)

        # Remove code blocks
        text = re.sub(r'```[\s\S]*?```', '', text)
        text = re.sub(r'`[^`]*`', '', text)

        # Remove special characters but keep spaces
        text = re.sub(r'[^a-z\s]', ' ', text)

        # Remove extra whitespace
        text = ' '.join(text.split())

        return text

    def extract_topics_nmf(self, documents: List[str], repo_names: List[str]) -> Dict[str, Any]:
        """Extract topics using Non-negative Matrix Factorization."""
        if not SKLEARN_AVAILABLE:
            return {}

        # Preprocess documents
        processed_docs = [self.preprocess_text(doc) for doc in documents]

        # Remove empty documents
        valid_docs = [(doc, name) for doc, name in zip(processed_docs, repo_names) if doc]
        if not valid_docs:
            return {'topics': [], 'error': 'No valid documents'}

        processed_docs, repo_names = zip(*valid_docs)

        # TF-IDF vectorization
        self.vectorizer = TfidfVectorizer(
            max_features=1000,
            min_df=1,
            max_df=0.8,
            stop_words='english',
            ngram_range=(1, 2)
        )

        try:
            tfidf_matrix = self.vectorizer.fit_transform(processed_docs)
        except ValueError as e:
            return {'topics': [], 'error': str(e)}

        # NMF topic modeling
        self.model = NMF(
            n_components=min(self.n_topics, len(processed_docs)),
            random_state=42,
            init='nndsvd',
            max_iter=500
        )

        doc_topic_matrix = self.model.fit_transform(tfidf_matrix)

        # Extract topics
        feature_names = self.vectorizer.get_feature_names_out()
        topics = []

        for topic_idx, topic in enumerate(self.model.components_):
            top_indices = topic.argsort()[-self.n_top_words:][::-1]
            top_words = [feature_names[i] for i in top_indices]
            top_weights = [float(topic[i]) for i in top_indices]

            topics.append({
                'topic_id': topic_idx,
                'words': top_words,
                'weights': top_weights,
                'label': self._generate_topic_label(top_words)
            })

        # Assign dominant topics to repositories
        repo_topics = []
        for idx, repo_name in enumerate(repo_names):
            topic_dist = doc_topic_matrix[idx]
            dominant_topic = int(topic_dist.argmax())
            topic_strength = float(topic_dist[dominant_topic])

            repo_topics.append({
                'repository': repo_name,
                'dominant_topic': dominant_topic,
                'topic_strength': topic_strength,
                'topic_distribution': [float(x) for x in topic_dist]
            })

        return {
            'method': 'NMF',
            'n_topics': len(topics),
            'topics': topics,
            'repository_topics': repo_topics,
            'vocabulary_size': len(feature_names)
        }

    def extract_topics_lda(self, documents: List[str], repo_names: List[str]) -> Dict[str, Any]:
        """Extract topics using Latent Dirichlet Allocation."""
        if not SKLEARN_AVAILABLE:
            return {}

        # Preprocess documents
        processed_docs = [self.preprocess_text(doc) for doc in documents]

        # Remove empty documents
        valid_docs = [(doc, name) for doc, name in zip(processed_docs, repo_names) if doc]
        if not valid_docs:
            return {'topics': [], 'error': 'No valid documents'}

        processed_docs, repo_names = zip(*valid_docs)

        # Count vectorization (LDA works better with raw counts)
        self.vectorizer = CountVectorizer(
            max_features=1000,
            min_df=1,
            max_df=0.8,
            stop_words='english',
            ngram_range=(1, 2)
        )

        try:
            count_matrix = self.vectorizer.fit_transform(processed_docs)
        except ValueError as e:
            return {'topics': [], 'error': str(e)}

        # LDA topic modeling
        self.model = LatentDirichletAllocation(
            n_components=min(self.n_topics, len(processed_docs)),
            random_state=42,
            max_iter=50,
            learning_method='online',
            n_jobs=-1
        )

        doc_topic_matrix = self.model.fit_transform(count_matrix)

        # Extract topics
        feature_names = self.vectorizer.get_feature_names_out()
        topics = []

        for topic_idx, topic in enumerate(self.model.components_):
            top_indices = topic.argsort()[-self.n_top_words:][::-1]
            top_words = [feature_names[i] for i in top_indices]
            top_weights = [float(topic[i]) for i in top_indices]

            topics.append({
                'topic_id': topic_idx,
                'words': top_words,
                'weights': top_weights,
                'label': self._generate_topic_label(top_words)
            })

        # Assign dominant topics to repositories
        repo_topics = []
        for idx, repo_name in enumerate(repo_names):
            topic_dist = doc_topic_matrix[idx]
            dominant_topic = int(topic_dist.argmax())
            topic_strength = float(topic_dist[dominant_topic])

            repo_topics.append({
                'repository': repo_name,
                'dominant_topic': dominant_topic,
                'topic_strength': topic_strength,
                'topic_distribution': [float(x) for x in topic_dist]
            })

        return {
            'method': 'LDA',
            'n_topics': len(topics),
            'topics': topics,
            'repository_topics': repo_topics,
            'vocabulary_size': len(feature_names),
            'perplexity': float(self.model.perplexity(count_matrix))
        }

    def _generate_topic_label(self, top_words: List[str]) -> str:
        """Generate human-readable label for topic."""
        # Take top 3 words and create label
        return ' & '.join(top_words[:3])

    def create_topic_distribution_chart(self, topic_results: Dict[str, Any], output_dir: str) -> str:
        """Create interactive visualization of topic distributions."""
        if not PLOTLY_AVAILABLE:
            return ""

        repo_topics = topic_results.get('repository_topics', [])
        topics = topic_results.get('topics', [])

        if not repo_topics or not topics:
            return ""

        # Create heatmap of repository-topic matrix
        repo_names = [rt['repository'] for rt in repo_topics]
        topic_labels = [t['label'] for t in topics]

        # Build matrix
        matrix = []
        for rt in repo_topics:
            matrix.append(rt['topic_distribution'])

        fig = go.Figure(data=go.Heatmap(
            z=matrix,
            x=topic_labels,
            y=repo_names,
            colorscale='Viridis',
            hoverongaps=False,
            hovertemplate='Repository: %{y}<br>Topic: %{x}<br>Strength: %{z:.3f}<extra></extra>'
        ))

        fig.update_layout(
            title=f'Repository-Topic Distribution ({topic_results["method"]})',
            xaxis_title='Topics',
            yaxis_title='Repositories',
            height=max(400, len(repo_names) * 40)
        )

        output_path = os.path.join(output_dir, f'topic_distribution_{topic_results["method"].lower()}.html')
        fig.write_html(output_path)
        return output_path

    def create_topic_wordcloud_chart(self, topic_results: Dict[str, Any], output_dir: str) -> str:
        """Create bar chart visualization of topic words."""
        if not PLOTLY_AVAILABLE:
            return ""

        topics = topic_results.get('topics', [])
        if not topics:
            return ""

        # Create subplot for each topic
        from plotly.subplots import make_subplots

        n_topics = len(topics)
        rows = (n_topics + 1) // 2
        cols = 2 if n_topics > 1 else 1

        fig = make_subplots(
            rows=rows,
            cols=cols,
            subplot_titles=[t['label'] for t in topics],
            vertical_spacing=0.15,
            horizontal_spacing=0.1
        )

        for idx, topic in enumerate(topics):
            row = (idx // 2) + 1
            col = (idx % 2) + 1

            fig.add_trace(
                go.Bar(
                    x=topic['weights'][:8],  # Top 8 words
                    y=topic['words'][:8],
                    orientation='h',
                    marker_color='lightblue',
                    showlegend=False
                ),
                row=row,
                col=col
            )

        fig.update_layout(
            title=f'Topic Word Distributions ({topic_results["method"]})',
            height=300 * rows,
            showlegend=False
        )

        fig.update_xaxes(title_text="Weight")

        output_path = os.path.join(output_dir, f'topic_words_{topic_results["method"].lower()}.html')
        fig.write_html(output_path)
        return output_path


def analyze_repository_topics(repos_data: List[Dict], method='both') -> Dict[str, Any]:
    """Analyze repository topics using machine learning."""
    print("Analyzing repository topics with ML...")

    if not SKLEARN_AVAILABLE:
        print("ERROR: scikit-learn not available")
        return {'error': 'scikit-learn not installed'}

    # Extract documents (README + description)
    documents = []
    repo_names = []

    for repo in repos_data:
        # Combine description and README
        text_parts = []

        if repo.get('description'):
            text_parts.append(repo['description'])

        # Get README content if available
        readme = repo.get('readme_content', '')
        if readme:
            # Limit README to first 5000 chars to avoid overwhelming
            text_parts.append(readme[:5000])

        # Combine
        doc_text = ' '.join(text_parts)

        if doc_text.strip():
            documents.append(doc_text)
            repo_names.append(repo['name'])

    if len(documents) < 2:
        print("ERROR: Need at least 2 repositories with content")
        return {'error': 'Insufficient documents'}

    print(f"Processing {len(documents)} repositories...")

    # Initialize modeler
    modeler = MLTopicModeler(n_topics=min(5, len(documents)), n_top_words=10)

    results = {
        'generated_at': datetime.now().isoformat(),
        'total_repositories': len(repos_data),
        'analyzed_repositories': len(documents),
        'methods': {}
    }

    # NMF analysis
    if method in ['nmf', 'both']:
        print("Running NMF topic modeling...")
        nmf_results = modeler.extract_topics_nmf(documents, repo_names)
        results['methods']['nmf'] = nmf_results

        # Create visualizations
        if PLOTLY_AVAILABLE:
            dist_path = modeler.create_topic_distribution_chart(nmf_results, 'docs/visualizations')
            words_path = modeler.create_topic_wordcloud_chart(nmf_results, 'docs/visualizations')
            nmf_results['visualizations'] = {
                'distribution': dist_path,
                'words': words_path
            }

    # LDA analysis
    if method in ['lda', 'both']:
        print("Running LDA topic modeling...")
        lda_results = modeler.extract_topics_lda(documents, repo_names)
        results['methods']['lda'] = lda_results

        # Create visualizations
        if PLOTLY_AVAILABLE:
            dist_path = modeler.create_topic_distribution_chart(lda_results, 'docs/visualizations')
            words_path = modeler.create_topic_wordcloud_chart(lda_results, 'docs/visualizations')
            lda_results['visualizations'] = {
                'distribution': dist_path,
                'words': words_path
            }

    # Save results
    output_path = 'data/ml_topic_analysis.json'
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)

    print(f"Topic analysis saved to {output_path}")
    return results


def main():
    """Test ML topic modeling."""
    print("ML Topic Modeling System")
    print("=" * 60)

    if not SKLEARN_AVAILABLE:
        print("ERROR: scikit-learn not available")
        print("Install with: pip install scikit-learn")
        return

    if os.path.exists('data/repos.json'):
        with open('data/repos.json', 'r', encoding='utf-8') as f:
            repos_data = json.load(f)

        results = analyze_repository_topics(repos_data, method='both')

        if 'error' not in results:
            print("\nResults:")
            print(f"  Analyzed {results['analyzed_repositories']} repositories")

            for method_name, method_results in results['methods'].items():
                if 'topics' in method_results:
                    print(f"\n{method_name.upper()} Topics:")
                    for topic in method_results['topics']:
                        print(f"    Topic {topic['topic_id']}: {topic['label']}")
                        print(f"      Words: {', '.join(topic['words'][:5])}")

    else:
        print("No repos data found. Run build_research_platform.py first.")


if __name__ == '__main__':
    main()
