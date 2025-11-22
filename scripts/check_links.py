#!/usr/bin/env python3
"""
Link Checker for Repository Overview
Validates all clickable elements and URLs
"""

import json
import os
import re
import time
from typing import List, Dict, Tuple
from urllib.parse import urljoin, urlparse

try:
    import requests
    REQUESTS_AVAILABLE = True
except ImportError:
    REQUESTS_AVAILABLE = False
    print("Warning: requests not installed. Install with: pip install requests")

try:
    from bs4 import BeautifulSoup
    BS4_AVAILABLE = True
except ImportError:
    BS4_AVAILABLE = False
    print("Warning: beautifulsoup4 not installed. Install with: pip install beautifulsoup4")


def extract_links_from_html(html_file: str) -> Dict[str, List[str]]:
    """
    Extract all links and clickable elements from HTML file.
    """
    if not BS4_AVAILABLE:
        print("ERROR: BeautifulSoup4 is required. Install with: pip install beautifulsoup4")
        return {}

    with open(html_file, 'r', encoding='utf-8') as f:
        content = f.read()

    soup = BeautifulSoup(content, 'html.parser')

    links = {
        'external_urls': [],
        'onclick_urls': [],
        'filter_buttons': [],
        'interactive_elements': []
    }

    # Extract <a> tags
    for a_tag in soup.find_all('a'):
        href = a_tag.get('href')
        if href:
            links['external_urls'].append({
                'url': href,
                'text': a_tag.get_text(strip=True),
                'tag': 'a'
            })

    # Extract onclick attributes
    for element in soup.find_all(onclick=True):
        onclick = element.get('onclick')
        # Extract URLs from onclick="window.open('url', '_blank')"
        url_match = re.search(r"window\.open\(['\"]([^'\"]+)['\"]", onclick)
        if url_match:
            links['onclick_urls'].append({
                'url': url_match.group(1),
                'text': element.get_text(strip=True)[:50],
                'class': element.get('class', []),
                'tag': element.name
            })

    # Extract filter buttons
    for button in soup.find_all('button', class_='filter-button'):
        filter_val = button.get('data-filter')
        links['filter_buttons'].append({
            'filter': filter_val,
            'text': button.get_text(strip=True)
        })

    # Check for search input
    search_input = soup.find('input', id='searchInput')
    if search_input:
        links['interactive_elements'].append({
            'type': 'search',
            'id': 'searchInput',
            'placeholder': search_input.get('placeholder', '')
        })

    return links


def check_url(url: str, timeout: int = 10) -> Tuple[bool, int, str]:
    """
    Check if a URL is accessible.
    Returns: (is_accessible, status_code, message)
    """
    if not REQUESTS_AVAILABLE:
        return (None, 0, "requests library not available")

    try:
        # Handle GitHub URLs
        if 'github.com' in url:
            # For GitHub repos, use API to check
            if '/repos/' not in url:
                # Convert HTML URL to check if repo exists
                parts = urlparse(url)
                path_parts = [p for p in parts.path.split('/') if p]
                if len(path_parts) >= 2:
                    org, repo = path_parts[0], path_parts[1]
                    api_url = f"https://api.github.com/repos/{org}/{repo}"

                    headers = {}
                    token = os.environ.get('GITHUB_TOKEN')
                    if token:
                        headers['Authorization'] = f'token {token}'

                    response = requests.get(api_url, headers=headers, timeout=timeout)

                    if response.status_code == 200:
                        return (True, response.status_code, "Repository accessible")
                    elif response.status_code == 404:
                        return (False, response.status_code, "Repository not found")
                    else:
                        return (False, response.status_code, f"HTTP {response.status_code}")

        # For other URLs, do HEAD request
        response = requests.head(url, timeout=timeout, allow_redirects=True)

        if response.status_code < 400:
            return (True, response.status_code, "OK")
        else:
            return (False, response.status_code, f"HTTP {response.status_code}")

    except requests.exceptions.Timeout:
        return (False, 0, "Timeout")
    except requests.exceptions.ConnectionError:
        return (False, 0, "Connection Error")
    except requests.exceptions.RequestException as e:
        return (False, 0, f"Error: {str(e)[:50]}")
    except Exception as e:
        return (False, 0, f"Unexpected error: {str(e)[:50]}")


def verify_filter_functionality(html_file: str) -> Dict[str, bool]:
    """
    Verify that filter buttons have corresponding data attributes on cards.
    """
    if not BS4_AVAILABLE:
        return {}

    with open(html_file, 'r', encoding='utf-8') as f:
        content = f.read()

    soup = BeautifulSoup(content, 'html.parser')

    results = {}

    # Get all filter values
    filter_buttons = soup.find_all('button', class_='filter-button')
    filter_values = [btn.get('data-filter') for btn in filter_buttons if btn.get('data-filter')]

    # Get all cards
    cards = soup.find_all('div', class_='repo-card')

    # Get categories from cards
    card_categories = set()
    for card in cards:
        category = card.get('data-category')
        if category:
            card_categories.add(category)

    # Verify each filter (except 'all')
    for filter_val in filter_values:
        if filter_val == 'all':
            results[filter_val] = True
        else:
            # Check if there are cards with this category
            has_matching_cards = filter_val in card_categories
            results[filter_val] = has_matching_cards

    return results


def check_javascript_functionality(html_file: str) -> Dict[str, bool]:
    """
    Check if required JavaScript functionality is present.
    """
    with open(html_file, 'r', encoding='utf-8') as f:
        content = f.read()

    checks = {
        'search_handler': 'searchInput' in content and 'addEventListener' in content,
        'filter_handler': 'filter-button' in content and 'data-filter' in content,
        'card_click_handler': 'onclick' in content or 'addEventListener' in content,
        'window_open': 'window.open' in content
    }

    return checks


def main():
    """Main execution."""
    # Set UTF-8 encoding for Windows console
    import sys
    if sys.platform == 'win32':
        import io
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

    print("=" * 70)
    print("REPOSITORY OVERVIEW LINK CHECKER")
    print("=" * 70)
    print()

    html_file = 'docs/visualizations/repository_overview.html'

    if not os.path.exists(html_file):
        print(f"ERROR: File not found: {html_file}")
        return

    print(f"Analyzing: {html_file}")
    print()

    # Extract all links
    print(">> Extracting links and interactive elements...")
    links = extract_links_from_html(html_file)

    # Check onclick URLs (repository links)
    print("\n" + "=" * 70)
    print("REPOSITORY LINKS (onclick)")
    print("=" * 70)

    onclick_urls = links.get('onclick_urls', [])
    print(f"Found {len(onclick_urls)} repository card links")
    print()

    if REQUESTS_AVAILABLE and onclick_urls:
        print("Checking URL accessibility...")
        for i, link_info in enumerate(onclick_urls, 1):
            url = link_info['url']
            text = link_info['text']

            is_accessible, status, message = check_url(url)

            status_symbol = "[OK]" if is_accessible else "[FAIL]"
            print(f"{status_symbol} [{i}] {text}")
            print(f"    URL: {url}")
            print(f"    Status: {message}")
            print()

            # Be nice to GitHub API
            if i < len(onclick_urls):
                time.sleep(0.5)
    else:
        for i, link_info in enumerate(onclick_urls, 1):
            print(f"  [{i}] {link_info['text']}")
            print(f"      URL: {link_info['url']}")
            print()

    # Check filter buttons
    print("=" * 70)
    print("FILTER BUTTONS")
    print("=" * 70)

    filter_buttons = links.get('filter_buttons', [])
    print(f"Found {len(filter_buttons)} filter buttons")
    print()

    filter_results = verify_filter_functionality(html_file)

    for button in filter_buttons:
        filter_val = button['filter']
        text = button['text']

        has_cards = filter_results.get(filter_val, False)
        status_symbol = "[OK]" if has_cards or filter_val == 'all' else "[WARN]"

        print(f"{status_symbol} {text}")
        print(f"    Filter value: {filter_val}")
        if filter_val != 'all':
            print(f"    Has matching cards: {has_cards}")
        print()

    # Check JavaScript functionality
    print("=" * 70)
    print("JAVASCRIPT FUNCTIONALITY")
    print("=" * 70)

    js_checks = check_javascript_functionality(html_file)
    print()

    for check_name, result in js_checks.items():
        status_symbol = "[OK]" if result else "[FAIL]"
        print(f"{status_symbol} {check_name.replace('_', ' ').title()}: {result}")

    print()

    # Check interactive elements
    print("=" * 70)
    print("INTERACTIVE ELEMENTS")
    print("=" * 70)

    interactive = links.get('interactive_elements', [])
    print(f"Found {len(interactive)} interactive elements")
    print()

    for element in interactive:
        print(f"[OK] {element['type'].upper()}: {element.get('id', 'N/A')}")
        if 'placeholder' in element:
            print(f"    Placeholder: {element['placeholder']}")
        print()

    # Summary
    print("=" * 70)
    print("SUMMARY")
    print("=" * 70)
    print()
    print(f"Total repository links: {len(onclick_urls)}")
    print(f"Total filter buttons: {len(filter_buttons)}")
    print(f"Total interactive elements: {len(interactive)}")
    print()

    all_js_working = all(js_checks.values())
    all_filters_working = all(v for k, v in filter_results.items() if k != 'all')

    if all_js_working and all_filters_working:
        print("[SUCCESS] All checks passed!")
    else:
        print("[WARNING] Some issues detected - review output above")

    print()
    print("=" * 70)


if __name__ == '__main__':
    main()
