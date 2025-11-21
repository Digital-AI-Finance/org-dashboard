#!/usr/bin/env python3
"""
Parse research metadata from GitHub repositories.
Extracts: DOIs, arXiv IDs, authors, citations, datasets, notebooks, etc.
"""

import re
import json
import os
from datetime import datetime
from typing import Dict, List, Any, Optional
from pathlib import Path


class ResearchMetadataParser:
    """Extract research metadata from repository content."""

    # Regular expressions for extracting identifiers
    DOI_PATTERN = r'10\.\d{4,9}/[-._;()/:a-zA-Z0-9]+'
    ARXIV_PATTERN = r'arXiv:\s*(\d{4}\.\d{4,5}(?:v\d+)?)'
    ARXIV_URL_PATTERN = r'arxiv\.org/(?:abs|pdf)/(\d{4}\.\d{4,5}(?:v\d+)?)'
    SSRN_PATTERN = r'(?:ssrn\.com/abstract=|SSRN:\s*)(\d+)'

    # Email pattern for author extraction
    EMAIL_PATTERN = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'

    # BibTeX pattern
    BIBTEX_PATTERN = r'@\w+\{[^}]+,[\s\S]*?\n\}'

    def __init__(self):
        self.metadata = {}

    def parse_readme(self, readme_content: str) -> Dict[str, Any]:
        """Parse README content for research metadata."""
        metadata = {
            "publications": self.extract_publications(readme_content),
            "authors": self.extract_authors(readme_content),
            "citations": self.extract_citations(readme_content),
            "keywords": self.extract_keywords(readme_content),
            "abstract": self.extract_abstract(readme_content)
        }
        return metadata

    def extract_publications(self, content: str) -> List[Dict[str, Any]]:
        """Extract publication information (DOI, arXiv, SSRN)."""
        publications = []

        # Extract DOIs
        dois = re.findall(self.DOI_PATTERN, content)
        for doi in set(dois):
            publications.append({
                "type": "journal",  # Default, may need refinement
                "doi": doi,
                "url": f"https://doi.org/{doi}"
            })

        # Extract arXiv IDs
        arxiv_ids = re.findall(self.ARXIV_PATTERN, content, re.IGNORECASE)
        arxiv_ids += re.findall(self.ARXIV_URL_PATTERN, content, re.IGNORECASE)

        for arxiv_id in set(arxiv_ids):
            publications.append({
                "type": "preprint",
                "arxiv_id": arxiv_id,
                "url": f"https://arxiv.org/abs/{arxiv_id}"
            })

        # Extract SSRN IDs
        ssrn_ids = re.findall(self.SSRN_PATTERN, content, re.IGNORECASE)
        for ssrn_id in set(ssrn_ids):
            publications.append({
                "type": "working_paper",
                "ssrn_id": ssrn_id,
                "url": f"https://ssrn.com/abstract={ssrn_id}"
            })

        return publications

    def extract_authors(self, content: str) -> List[Dict[str, str]]:
        """Extract author information from README."""
        authors = []

        # Look for common author sections
        author_section_patterns = [
            r'##?\s*Authors?\s*\n(.*?)(?:\n##|\Z)',
            r'##?\s*Contributors?\s*\n(.*?)(?:\n##|\Z)',
            r'##?\s*Team\s*\n(.*?)(?:\n##|\Z)',
            r'By\s+(.*?)(?:\n|$)',
        ]

        for pattern in author_section_patterns:
            matches = re.findall(pattern, content, re.IGNORECASE | re.DOTALL)
            for match in matches:
                # Extract names and emails
                lines = match.split('\n')
                for line in lines:
                    line = line.strip('*- ')
                    if line and len(line) > 3:
                        author = {"name": line}

                        # Try to extract email
                        emails = re.findall(self.EMAIL_PATTERN, line)
                        if emails:
                            author["email"] = emails[0]
                            # Remove email from name
                            author["name"] = re.sub(self.EMAIL_PATTERN, '', line).strip(' ()')

                        # Try to extract affiliation (text in parentheses)
                        affiliation_match = re.search(r'\((.*?)\)', author["name"])
                        if affiliation_match:
                            author["affiliation"] = affiliation_match.group(1)
                            author["name"] = re.sub(r'\(.*?\)', '', author["name"]).strip()

                        if author["name"]:
                            authors.append(author)

        return authors[:10]  # Limit to 10 authors

    def extract_citations(self, content: str) -> List[str]:
        """Extract BibTeX citations from README."""
        bibtex_entries = re.findall(self.BIBTEX_PATTERN, content, re.MULTILINE)
        return bibtex_entries

    def extract_keywords(self, content: str) -> List[str]:
        """Extract research keywords and topics."""
        keywords = set()

        # Look for keywords section
        keyword_patterns = [
            r'##?\s*Keywords?\s*\n(.*?)(?:\n##|\Z)',
            r'##?\s*Topics?\s*\n(.*?)(?:\n##|\Z)',
            r'##?\s*Tags?\s*\n(.*?)(?:\n##|\Z)',
        ]

        for pattern in keyword_patterns:
            matches = re.findall(pattern, content, re.IGNORECASE | re.DOTALL)
            for match in matches:
                # Split by common separators
                words = re.split(r'[,;\n\-\*]', match)
                for word in words:
                    word = word.strip().strip('`')
                    if word and len(word) > 2:
                        keywords.add(word)

        return list(keywords)[:20]  # Limit to 20

    def extract_abstract(self, content: str) -> Optional[str]:
        """Extract abstract or summary from README."""
        # Look for abstract section
        abstract_patterns = [
            r'##?\s*Abstract\s*\n(.*?)(?:\n##|\Z)',
            r'##?\s*Summary\s*\n(.*?)(?:\n##|\Z)',
            r'##?\s*Overview\s*\n(.*?)(?:\n##|\Z)',
        ]

        for pattern in abstract_patterns:
            matches = re.findall(pattern, content, re.IGNORECASE | re.DOTALL)
            if matches:
                # Clean up the abstract
                abstract = matches[0].strip()
                # Remove markdown formatting
                abstract = re.sub(r'\[([^\]]+)\]\([^\)]+\)', r'\1', abstract)
                abstract = re.sub(r'[*_`]', '', abstract)
                return abstract[:1000]  # Limit length

        # If no abstract section, use first paragraph after title
        paragraphs = content.split('\n\n')
        for para in paragraphs[1:]:  # Skip first (usually title)
            para = para.strip()
            if len(para) > 100 and not para.startswith('#'):
                return para[:500]

        return None

    def detect_datasets(self, repo_contents: List[Dict]) -> List[Dict[str, Any]]:
        """Detect datasets in repository."""
        datasets = []

        data_extensions = {'.csv', '.xlsx', '.xls', '.json', '.parquet', '.h5', '.hdf5', '.db', '.sqlite'}
        data_folders = {'data', 'datasets', 'input', 'raw_data', 'processed_data'}

        for item in repo_contents:
            path = item.get('path', '')
            name = item.get('name', '')
            size = item.get('size', 0)

            # Check if in data folder or has data extension
            path_parts = Path(path).parts
            is_data_folder = any(folder in path_parts for folder in data_folders)
            has_data_ext = Path(path).suffix.lower() in data_extensions

            if is_data_folder or has_data_ext:
                dataset = {
                    "name": name,
                    "path": path,
                    "format": Path(path).suffix.lower(),
                    "size_bytes": size
                }
                datasets.append(dataset)

        return datasets

    def detect_notebooks(self, repo_contents: List[Dict]) -> List[Dict[str, Any]]:
        """Detect Jupyter and R Markdown notebooks."""
        notebooks = []

        for item in repo_contents:
            path = item.get('path', '')
            name = item.get('name', '')

            if path.endswith('.ipynb'):
                notebooks.append({
                    "path": path,
                    "title": name.replace('.ipynb', ''),
                    "language": "python",
                    "type": "jupyter"
                })
            elif path.endswith('.Rmd'):
                notebooks.append({
                    "path": path,
                    "title": name.replace('.Rmd', ''),
                    "language": "r",
                    "type": "rmarkdown"
                })

        return notebooks

    def parse_requirements(self, requirements_txt: str) -> List[str]:
        """Parse Python requirements.txt file."""
        if not requirements_txt:
            return []

        packages = []
        for line in requirements_txt.split('\n'):
            line = line.strip()
            if line and not line.startswith('#'):
                # Extract package name (before ==, >=, etc.)
                package = re.split(r'[=<>!]', line)[0].strip()
                if package:
                    packages.append(package)

        return packages

    def check_reproducibility(self, repo_contents: List[Dict]) -> Dict[str, Any]:
        """Check for reproducibility indicators."""
        files = {item.get('name', '').lower() for item in repo_contents}

        return {
            "has_requirements": 'requirements.txt' in files,
            "has_dockerfile": 'dockerfile' in files,
            "has_environment_yml": 'environment.yml' in files or 'environment.yaml' in files,
            "has_makefile": 'makefile' in files,
            "replication_status": "not_attempted"
        }


def parse_repository_metadata(repo_data: Dict[str, Any], repo_contents: List[Dict] = None) -> Dict[str, Any]:
    """
    Parse research metadata from repository data.

    Args:
        repo_data: Repository data from GitHub API
        repo_contents: Optional list of repository contents

    Returns:
        Research metadata dictionary
    """
    parser = ResearchMetadataParser()

    readme = repo_data.get('readme', '')

    metadata = {
        "repo_name": repo_data.get('name', ''),
        "research": {
            "title": repo_data.get('description', ''),
            "abstract": parser.extract_abstract(readme),
            "keywords": parser.extract_keywords(readme),
            "authors": parser.extract_authors(readme)
        },
        "publications": parser.extract_publications(readme),
        "code": {
            "languages": [repo_data.get('language', 'Unknown')],
            "notebooks": [],
            "dependencies": {}
        },
        "reproducibility": {},
        "citations": {
            "cited_by": [],
            "cites": parser.extract_citations(readme),
            "citation_count": 0
        },
        "meta": {
            "extracted_at": datetime.now().isoformat(),
            "extraction_version": "1.0",
            "extraction_method": "readme_parse"
        }
    }

    # If repo contents provided, extract additional info
    if repo_contents:
        metadata["datasets"] = parser.detect_datasets(repo_contents)
        metadata["code"]["notebooks"] = parser.detect_notebooks(repo_contents)
        metadata["reproducibility"] = parser.check_reproducibility(repo_contents)

    return metadata


def main():
    """Test the parser with example data."""
    example_readme = """
    # Cryptocurrency Price Prediction using LSTM

    ## Abstract
    This repository contains code for predicting cryptocurrency prices using
    Long Short-Term Memory (LSTM) neural networks. We achieve 72% directional
    accuracy on Bitcoin price movements.

    ## Authors
    - John Doe (MIT) john@example.com
    - Jane Smith (Stanford)

    ## Citation
    If you use this code, please cite:
    arXiv:2024.12345

    DOI: 10.1234/example.2024

    ## Keywords
    cryptocurrency, deep learning, LSTM, time series, forecasting
    """

    parser = ResearchMetadataParser()
    result = parser.parse_readme(example_readme)

    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
