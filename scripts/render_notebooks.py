#!/usr/bin/env python3
"""
Render Jupyter notebooks to HTML for display in dashboard.
Extract figures, tables, and outputs from notebooks.
"""

import json
import os
import re
import base64
from pathlib import Path
from typing import Dict, List, Any, Optional
from io import StringIO

try:
    import nbformat
    from nbconvert import HTMLExporter
    from nbconvert.preprocessors import ExecutePreprocessor
except ImportError:
    print("ERROR: nbconvert not installed. Run: pip install nbconvert nbformat")
    exit(1)


class NotebookRenderer:
    """Render Jupyter notebooks to HTML and extract outputs."""

    def __init__(self, output_dir='docs/notebooks', execute=False):
        self.output_dir = output_dir
        self.execute_notebooks = execute
        self.html_exporter = HTMLExporter()
        self.html_exporter.template_name = 'classic'

        # Configure exporter
        self.html_exporter.exclude_input_prompt = False
        self.html_exporter.exclude_output_prompt = False

        os.makedirs(output_dir, exist_ok=True)

    def render_notebook(self, notebook_path: str, repo_name: str) -> Optional[Dict[str, Any]]:
        """
        Render a single notebook to HTML.

        Args:
            notebook_path: Path to notebook file (local or URL)
            repo_name: Repository name for organization

        Returns:
            Dictionary with rendering info or None if failed
        """
        try:
            # Read notebook
            with open(notebook_path, 'r', encoding='utf-8') as f:
                nb = nbformat.read(f, as_version=4)

            # Optionally execute notebook (disabled by default for safety)
            if self.execute_notebooks:
                print(f"  Executing notebook: {notebook_path}")
                ep = ExecutePreprocessor(timeout=600, kernel_name='python3')
                ep.preprocess(nb, {'metadata': {'path': os.path.dirname(notebook_path)}})

            # Convert to HTML
            (body, resources) = self.html_exporter.from_notebook_node(nb)

            # Save HTML
            notebook_name = Path(notebook_path).stem
            output_file = os.path.join(self.output_dir, f"{repo_name}_{notebook_name}.html")

            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(body)

            # Extract metadata
            metadata = self.extract_metadata(nb, notebook_path)
            metadata['html_path'] = output_file
            metadata['repo_name'] = repo_name

            # Extract figures
            figures = self.extract_figures(nb, repo_name, notebook_name)
            metadata['figures'] = figures

            # Extract tables
            tables = self.extract_tables(nb)
            metadata['tables'] = tables

            print(f"  Rendered: {output_file}")
            return metadata

        except Exception as e:
            print(f"  Error rendering {notebook_path}: {e}")
            return None

    def extract_metadata(self, nb: nbformat.NotebookNode, path: str) -> Dict[str, Any]:
        """Extract metadata from notebook."""
        metadata = {
            'path': path,
            'title': Path(path).stem,
            'cells': len(nb.cells),
            'code_cells': sum(1 for cell in nb.cells if cell.cell_type == 'code'),
            'markdown_cells': sum(1 for cell in nb.cells if cell.cell_type == 'markdown'),
            'kernel': nb.metadata.get('kernelspec', {}).get('name', 'unknown'),
            'language': nb.metadata.get('kernelspec', {}).get('language', 'unknown')
        }

        # Extract title from first markdown cell if available
        for cell in nb.cells:
            if cell.cell_type == 'markdown':
                lines = cell.source.split('\n')
                for line in lines:
                    if line.startswith('# '):
                        metadata['title'] = line[2:].strip()
                        break
                break

        return metadata

    def extract_figures(self, nb: nbformat.NotebookNode, repo_name: str, notebook_name: str) -> List[Dict]:
        """Extract figures from notebook outputs."""
        figures = []
        figure_count = 0

        for cell_idx, cell in enumerate(nb.cells):
            if cell.cell_type != 'code':
                continue

            outputs = cell.get('outputs', [])
            for output in outputs:
                # Check for image outputs
                if output.output_type in ('display_data', 'execute_result'):
                    data = output.get('data', {})

                    for mime_type in ['image/png', 'image/jpeg', 'image/svg+xml']:
                        if mime_type in data:
                            figure_count += 1

                            # Save image to file
                            ext = mime_type.split('/')[-1]
                            if ext == 'svg+xml':
                                ext = 'svg'

                            figure_filename = f"{repo_name}_{notebook_name}_fig{figure_count}.{ext}"
                            figure_path = os.path.join(self.output_dir, 'figures', figure_filename)
                            os.makedirs(os.path.dirname(figure_path), exist_ok=True)

                            # Write image data
                            if mime_type == 'image/svg+xml':
                                with open(figure_path, 'w', encoding='utf-8') as f:
                                    f.write(data[mime_type])
                            else:
                                image_data = base64.b64decode(data[mime_type])
                                with open(figure_path, 'wb') as f:
                                    f.write(image_data)

                            figures.append({
                                'path': figure_path,
                                'filename': figure_filename,
                                'cell': cell_idx,
                                'type': mime_type
                            })

        return figures

    def extract_tables(self, nb: nbformat.NotebookNode) -> List[Dict]:
        """Extract tables from notebook outputs (pandas dataframes)."""
        tables = []

        for cell_idx, cell in enumerate(nb.cells):
            if cell.cell_type != 'code':
                continue

            outputs = cell.get('outputs', [])
            for output in outputs:
                if output.output_type in ('display_data', 'execute_result'):
                    data = output.get('data', {})

                    # Look for HTML tables (pandas DataFrame representations)
                    if 'text/html' in data:
                        html = data['text/html']
                        if '<table' in html.lower():
                            tables.append({
                                'cell': cell_idx,
                                'html': html
                            })

        return tables

    def create_notebook_index(self, notebooks_metadata: List[Dict], repo_name: str) -> str:
        """Create an index markdown file for all notebooks in a repo."""
        index_md = f"# Notebooks for {repo_name}\n\n"

        if not notebooks_metadata:
            index_md += "No notebooks found.\n"
            return index_md

        index_md += f"Total notebooks: {len(notebooks_metadata)}\n\n"

        for nb_meta in notebooks_metadata:
            index_md += f"## {nb_meta['title']}\n\n"
            index_md += f"- **Cells**: {nb_meta['cells']} ({nb_meta['code_cells']} code, {nb_meta['markdown_cells']} markdown)\n"
            index_md += f"- **Kernel**: {nb_meta['kernel']}\n"
            index_md += f"- **Language**: {nb_meta['language']}\n"

            if nb_meta.get('figures'):
                index_md += f"- **Figures**: {len(nb_meta['figures'])}\n"

            if nb_meta.get('tables'):
                index_md += f"- **Tables**: {len(nb_meta['tables'])}\n"

            index_md += f"- [View Notebook]({nb_meta['html_path']})\n\n"

            # List figures
            if nb_meta.get('figures'):
                index_md += "### Figures\n\n"
                for fig in nb_meta['figures'][:5]:  # Limit to first 5
                    index_md += f"![Figure](figures/{fig['filename']})\n\n"

        return index_md


def render_repository_notebooks(repo_data: Dict[str, Any], notebooks_dir: str = 'notebooks') -> List[Dict]:
    """
    Render all notebooks from a repository.

    Args:
        repo_data: Repository data with research metadata
        notebooks_dir: Directory where notebooks are stored locally

    Returns:
        List of rendered notebook metadata
    """
    renderer = NotebookRenderer()
    repo_name = repo_data['name']

    research_meta = repo_data.get('research_metadata', {})
    notebooks = research_meta.get('code', {}).get('notebooks', [])

    if not notebooks:
        return []

    rendered = []

    for notebook in notebooks:
        notebook_path_in_repo = notebook['path']
        # Assume notebooks have been cloned to local directory
        local_path = os.path.join(notebooks_dir, repo_name, notebook_path_in_repo)

        if not os.path.exists(local_path):
            print(f"  Warning: Notebook not found: {local_path}")
            continue

        rendered_meta = renderer.render_notebook(local_path, repo_name)
        if rendered_meta:
            rendered.append(rendered_meta)

    # Create index
    if rendered:
        index_md = renderer.create_notebook_index(rendered, repo_name)
        index_path = os.path.join(renderer.output_dir, f"{repo_name}_index.md")
        with open(index_path, 'w', encoding='utf-8') as f:
            f.write(index_md)

    return rendered


def main():
    """Test notebook rendering."""
    print("Notebook Renderer Test")
    print("=" * 60)

    # This is a test function - in practice, this would be called
    # by the main data fetching script

    # Example: render a single notebook
    renderer = NotebookRenderer(output_dir='test_output/notebooks')

    # You would need an actual notebook file to test
    # notebook_path = 'path/to/notebook.ipynb'
    # result = renderer.render_notebook(notebook_path, 'test-repo')
    # print(json.dumps(result, indent=2))

    print("Notebook rendering system initialized.")
    print("Use render_repository_notebooks() to process repo notebooks.")


if __name__ == '__main__':
    main()
