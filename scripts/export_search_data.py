"""Export search index to JSON for web interface."""

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from search_indexer import SearchIndex


def export_search_data(output_file: str = "docs/data/search_data.json"):
    """Export search index and repository data for web interface."""
    print("Exporting search data for web interface...")

    # Load search index
    index = SearchIndex.load_index()

    if not index.documents:
        print("Warning: No documents in search index")
        return

    # Convert documents to JSON-friendly format
    documents = []
    for doc_id, doc in index.documents.items():
        documents.append(
            {
                "id": doc_id,
                "content": doc["content"],
                "preview": doc["content"][:300],
                "metadata": doc["metadata"],
                "added_at": doc["added_at"],
            }
        )

    # Get all facets with counts
    facets = index.get_facets()

    # Convert inverted index to JSON-friendly format (term -> list of doc IDs)
    inverted_index = {term: list(doc_ids) for term, doc_ids in index.inverted_index.items()}

    # Load repos.json for additional metadata
    repos_file = Path("data/repos.json")
    repos_data = []
    if repos_file.exists():
        with open(repos_file, encoding="utf-8") as f:
            repos_data = json.load(f)

    # Build quick lookup for repos
    repos_lookup = {repo["name"]: repo for repo in repos_data}

    # Export data
    export_data = {
        "documents": documents,
        "inverted_index": inverted_index,  # Full index for client-side search
        "facets": facets,
        "repos": repos_lookup,
        "stats": {
            "total_documents": len(documents),
            "total_terms": len(inverted_index),
            "total_repos": len(repos_lookup),
            "document_types": {},
        },
    }

    # Calculate document type distribution
    for doc in documents:
        doc_type = doc["metadata"].get("type", "unknown")
        export_data["stats"]["document_types"][doc_type] = (
            export_data["stats"]["document_types"].get(doc_type, 0) + 1
        )

    # Save to JSON
    output_path = Path(output_file)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(export_data, f, indent=2, ensure_ascii=False)

    print(f"Search data exported to {output_path}")
    print(f"  - {export_data['stats']['total_documents']} documents")
    print(f"  - {export_data['stats']['total_terms']} indexed terms")
    print(f"  - {export_data['stats']['total_repos']} repositories")

    # Also create a minimal version for faster loading (without full inverted index)
    minimal_export = {
        "documents": documents,
        "facets": facets,
        "repos": repos_lookup,
        "stats": export_data["stats"],
    }

    minimal_path = output_path.parent / "search_data_minimal.json"
    with open(minimal_path, "w", encoding="utf-8") as f:
        json.dump(minimal_export, f, indent=2, ensure_ascii=False)

    print(f"Minimal search data exported to {minimal_path}")


if __name__ == "__main__":
    export_search_data()
