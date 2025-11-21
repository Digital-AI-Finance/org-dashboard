#!/usr/bin/env python3
"""
Fetch academic data from external sources: arXiv, CrossRef, Google Scholar.
"""

import requests
import time
import json
from typing import Dict, List, Any, Optional
from datetime import datetime
import xml.etree.ElementTree as ET


class AcademicDataFetcher:
    """Fetch metadata from academic databases."""

    def __init__(self, cache_dir='data/academic_cache'):
        self.cache_dir = cache_dir
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'ResearchDashboard/1.0 (mailto:research@example.com)'
        })

    def fetch_arxiv_metadata(self, arxiv_id: str) -> Optional[Dict[str, Any]]:
        """
        Fetch metadata from arXiv API.

        Args:
            arxiv_id: arXiv identifier (e.g., '2024.12345')

        Returns:
            Dictionary with paper metadata or None if not found
        """
        # Clean arXiv ID
        arxiv_id = arxiv_id.replace('arXiv:', '').strip()

        url = f"http://export.arxiv.org/api/query?id_list={arxiv_id}"

        try:
            response = self.session.get(url, timeout=10)
            response.raise_for_status()

            # Parse XML response
            root = ET.fromstring(response.content)
            ns = {'atom': 'http://www.w3.org/2005/Atom'}

            entry = root.find('atom:entry', ns)
            if entry is None:
                return None

            # Extract metadata
            metadata = {
                'arxiv_id': arxiv_id,
                'title': self._get_text(entry, 'atom:title', ns),
                'abstract': self._get_text(entry, 'atom:summary', ns),
                'published': self._get_text(entry, 'atom:published', ns),
                'updated': self._get_text(entry, 'atom:updated', ns),
                'url': f"https://arxiv.org/abs/{arxiv_id}",
                'pdf_url': f"https://arxiv.org/pdf/{arxiv_id}.pdf",
                'authors': [],
                'categories': []
            }

            # Extract authors
            for author in entry.findall('atom:author', ns):
                name = self._get_text(author, 'atom:name', ns)
                if name:
                    metadata['authors'].append({'name': name})

            # Extract categories
            for category in entry.findall('atom:category', ns):
                term = category.get('term')
                if term:
                    metadata['categories'].append(term)

            # Extract year from published date
            if metadata['published']:
                try:
                    metadata['year'] = int(metadata['published'][:4])
                except:
                    pass

            return metadata

        except Exception as e:
            print(f"Error fetching arXiv {arxiv_id}: {e}")
            return None

    def fetch_crossref_metadata(self, doi: str) -> Optional[Dict[str, Any]]:
        """
        Fetch metadata from CrossRef API.

        Args:
            doi: DOI identifier

        Returns:
            Dictionary with paper metadata or None if not found
        """
        url = f"https://api.crossref.org/works/{doi}"

        try:
            response = self.session.get(url, timeout=10)
            response.raise_for_status()

            data = response.json()
            message = data.get('message', {})

            metadata = {
                'doi': doi,
                'title': self._get_first(message.get('title', [])),
                'abstract': message.get('abstract', ''),
                'type': message.get('type', ''),
                'published': self._format_date(message.get('published', {})),
                'year': self._extract_year(message.get('published', {})),
                'url': message.get('URL', f"https://doi.org/{doi}"),
                'authors': [],
                'venue': self._get_first(message.get('container-title', [])),
                'publisher': message.get('publisher', ''),
                'citation_count': message.get('is-referenced-by-count', 0),
                'reference_count': message.get('references-count', 0)
            }

            # Extract authors
            for author in message.get('author', []):
                author_data = {
                    'name': f"{author.get('given', '')} {author.get('family', '')}".strip()
                }
                if author.get('affiliation'):
                    affiliations = [aff.get('name', '') for aff in author['affiliation']]
                    if affiliations:
                        author_data['affiliation'] = affiliations[0]
                metadata['authors'].append(author_data)

            return metadata

        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 404:
                print(f"DOI not found: {doi}")
            else:
                print(f"Error fetching DOI {doi}: {e}")
            return None
        except Exception as e:
            print(f"Error fetching DOI {doi}: {e}")
            return None

    def fetch_ssrn_metadata(self, ssrn_id: str) -> Optional[Dict[str, Any]]:
        """
        Fetch metadata from SSRN (limited, no official API).

        Args:
            ssrn_id: SSRN paper ID

        Returns:
            Dictionary with paper metadata or None
        """
        # SSRN doesn't have a public API, so we construct basic metadata
        return {
            'ssrn_id': ssrn_id,
            'url': f"https://ssrn.com/abstract={ssrn_id}",
            'type': 'working_paper',
            'note': 'Limited metadata available (no SSRN API)'
        }

    def enrich_publications(self, publications: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Enrich publication metadata by fetching from external sources.

        Args:
            publications: List of publications with identifiers

        Returns:
            Enriched publications list
        """
        enriched = []

        for pub in publications:
            enriched_pub = pub.copy()

            # Rate limiting
            time.sleep(0.5)

            # Fetch from arXiv
            if 'arxiv_id' in pub and pub['arxiv_id']:
                print(f"Fetching arXiv: {pub['arxiv_id']}")
                arxiv_data = self.fetch_arxiv_metadata(pub['arxiv_id'])
                if arxiv_data:
                    enriched_pub.update(arxiv_data)

            # Fetch from CrossRef
            elif 'doi' in pub and pub['doi']:
                print(f"Fetching DOI: {pub['doi']}")
                crossref_data = self.fetch_crossref_metadata(pub['doi'])
                if crossref_data:
                    enriched_pub.update(crossref_data)

            # Fetch from SSRN
            elif 'ssrn_id' in pub and pub['ssrn_id']:
                print(f"Fetching SSRN: {pub['ssrn_id']}")
                ssrn_data = self.fetch_ssrn_metadata(pub['ssrn_id'])
                if ssrn_data:
                    enriched_pub.update(ssrn_data)

            enriched.append(enriched_pub)

        return enriched

    @staticmethod
    def _get_text(element, path: str, namespace: Dict) -> str:
        """Helper to get text from XML element."""
        child = element.find(path, namespace)
        return child.text.strip() if child is not None and child.text else ''

    @staticmethod
    def _get_first(items: List) -> str:
        """Get first item from list or empty string."""
        return items[0] if items else ''

    @staticmethod
    def _format_date(date_parts: Dict) -> str:
        """Format CrossRef date parts to ISO string."""
        if not date_parts or 'date-parts' not in date_parts:
            return ''

        parts = date_parts['date-parts'][0] if date_parts['date-parts'] else []
        if not parts:
            return ''

        # Pad with 1s for month/day if missing
        while len(parts) < 3:
            parts.append(1)

        try:
            return f"{parts[0]:04d}-{parts[1]:02d}-{parts[2]:02d}"
        except:
            return ''

    @staticmethod
    def _extract_year(date_parts: Dict) -> Optional[int]:
        """Extract year from CrossRef date parts."""
        if not date_parts or 'date-parts' not in date_parts:
            return None

        parts = date_parts['date-parts'][0] if date_parts['date-parts'] else []
        return parts[0] if parts else None


def main():
    """Test the fetcher."""
    fetcher = AcademicDataFetcher()

    # Test arXiv
    print("Testing arXiv...")
    arxiv_data = fetcher.fetch_arxiv_metadata("2401.00001")
    if arxiv_data:
        print(json.dumps(arxiv_data, indent=2))

    print("\nTesting CrossRef...")
    # Test CrossRef with a known DOI
    crossref_data = fetcher.fetch_crossref_metadata("10.1038/nature12373")
    if crossref_data:
        print(json.dumps(crossref_data, indent=2))


if __name__ == '__main__':
    main()
