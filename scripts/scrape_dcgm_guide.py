#!/usr/bin/env python3
"""
NVIDIA DCGM User Guide Web Scraper
===================================
Scrapes the complete NVIDIA DCGM User Guide from the online documentation.
Saves as a consolidated markdown file with proper formatting.

Target URL: https://docs.nvidia.com/datacenter/dcgm/latest/user-guide/index.html
Output: docs/nvidia-manuals/NVIDIA-DCGM-User-Guide.md
"""

import requests
from bs4 import BeautifulSoup
import time
import re
from urllib.parse import urljoin, urlparse
from pathlib import Path
import sys

class DCGMGuideScraper:
    def __init__(self, base_url):
        self.base_url = base_url
        self.visited_urls = set()
        self.pages = []
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        })

    def is_valid_url(self, url):
        """Check if URL belongs to the DCGM user guide"""
        parsed = urlparse(url)
        return '/datacenter/dcgm/latest/user-guide/' in parsed.path

    def get_page_content(self, url):
        """Fetch and parse a single page"""
        try:
            print(f"Fetching: {url}")
            response = self.session.get(url, timeout=30)
            response.raise_for_status()
            return BeautifulSoup(response.content, 'html.parser')
        except Exception as e:
            print(f"Error fetching {url}: {e}")
            return None

    def extract_navigation_links(self, soup, current_url):
        """Extract navigation links from the page"""
        links = []

        # Look for navigation in common NVIDIA doc structures
        nav_selectors = [
            'nav.wy-nav-side a',  # Sphinx Read the Docs theme
            '.toctree-l1 a',
            '.toctree-l2 a',
            'aside nav a',
            '.sidebar nav a',
            'nav[role="navigation"] a'
        ]

        for selector in nav_selectors:
            nav_links = soup.select(selector)
            if nav_links:
                for link in nav_links:
                    href = link.get('href')
                    if href:
                        full_url = urljoin(current_url, href)
                        # Remove anchors for deduplication
                        full_url = full_url.split('#')[0]
                        if self.is_valid_url(full_url) and full_url not in self.visited_urls:
                            links.append(full_url)
                break  # Found navigation, stop looking

        return links

    def extract_content(self, soup, url):
        """Extract main content from the page"""
        content = {
            'url': url,
            'title': '',
            'content': '',
            'code_blocks': [],
            'tables': []
        }

        # Extract title
        title_selectors = ['h1', 'title', '.document h1']
        for selector in title_selectors:
            title_elem = soup.select_one(selector)
            if title_elem:
                content['title'] = title_elem.get_text().strip()
                break

        # Find main content area
        main_selectors = [
            'main',
            'article',
            '[role="main"]',
            '.document',
            '.content',
            '#main-content',
            '.rst-content'
        ]

        main_content = None
        for selector in main_selectors:
            main_content = soup.select_one(selector)
            if main_content:
                break

        if not main_content:
            main_content = soup.body if soup.body else soup

        # Remove navigation, footer, and script elements
        for element in main_content.select('nav, footer, script, style, .headerlink'):
            element.decompose()

        # Extract and process content
        content['content'] = self.process_html_content(main_content)

        return content

    def process_html_content(self, element):
        """Convert HTML content to markdown format"""
        markdown = []

        for child in element.children:
            if child.name is None:
                # Text node
                text = str(child).strip()
                if text:
                    markdown.append(text)
            elif child.name == 'h1':
                markdown.append(f"\n# {child.get_text().strip()}\n")
            elif child.name == 'h2':
                markdown.append(f"\n## {child.get_text().strip()}\n")
            elif child.name == 'h3':
                markdown.append(f"\n### {child.get_text().strip()}\n")
            elif child.name == 'h4':
                markdown.append(f"\n#### {child.get_text().strip()}\n")
            elif child.name == 'h5':
                markdown.append(f"\n##### {child.get_text().strip()}\n")
            elif child.name == 'h6':
                markdown.append(f"\n###### {child.get_text().strip()}\n")
            elif child.name == 'p':
                markdown.append(f"\n{child.get_text().strip()}\n")
            elif child.name in ['ul', 'ol']:
                markdown.append(self.process_list(child))
            elif child.name == 'pre':
                code = child.get_text().strip()
                # Try to detect language
                lang = ''
                if child.find('code'):
                    classes = child.find('code').get('class', [])
                    for cls in classes:
                        if cls.startswith('language-'):
                            lang = cls.replace('language-', '')
                            break
                markdown.append(f"\n```{lang}\n{code}\n```\n")
            elif child.name == 'code' and child.parent.name != 'pre':
                markdown.append(f"`{child.get_text().strip()}`")
            elif child.name == 'table':
                markdown.append(self.process_table(child))
            elif child.name == 'blockquote':
                lines = child.get_text().strip().split('\n')
                markdown.append('\n' + '\n'.join(f"> {line}" for line in lines) + '\n')
            elif child.name == 'a':
                href = child.get('href', '')
                text = child.get_text().strip()
                markdown.append(f"[{text}]({href})")
            elif child.name == 'img':
                alt = child.get('alt', 'Image')
                src = child.get('src', '')
                markdown.append(f"\n![{alt}]({src})\n")
            elif child.name in ['div', 'section', 'article']:
                # Recursively process container elements
                markdown.append(self.process_html_content(child))
            elif child.name == 'dl':
                # Definition list
                markdown.append(self.process_definition_list(child))
            else:
                # Default: extract text
                text = child.get_text().strip()
                if text:
                    markdown.append(text)

        return '\n'.join(str(m) for m in markdown if m)

    def process_list(self, list_elem):
        """Process HTML lists to markdown"""
        items = []
        list_type = list_elem.name

        for i, li in enumerate(list_elem.find_all('li', recursive=False), 1):
            prefix = f"{i}." if list_type == 'ol' else "-"
            text = li.get_text().strip().replace('\n', ' ')
            items.append(f"{prefix} {text}")

        return '\n' + '\n'.join(items) + '\n'

    def process_table(self, table_elem):
        """Process HTML tables to markdown"""
        rows = []

        # Process headers
        headers = []
        thead = table_elem.find('thead')
        if thead:
            header_row = thead.find('tr')
            if header_row:
                headers = [th.get_text().strip() for th in header_row.find_all(['th', 'td'])]

        # If no thead, check first row
        if not headers:
            first_row = table_elem.find('tr')
            if first_row:
                headers = [th.get_text().strip() for th in first_row.find_all('th')]

        if headers:
            rows.append('| ' + ' | '.join(headers) + ' |')
            rows.append('| ' + ' | '.join(['---'] * len(headers)) + ' |')

        # Process body rows
        tbody = table_elem.find('tbody') or table_elem
        for tr in tbody.find_all('tr'):
            cells = [td.get_text().strip().replace('\n', ' ') for td in tr.find_all(['td', 'th'])]
            if cells and not (len(headers) > 0 and cells == headers):
                rows.append('| ' + ' | '.join(cells) + ' |')

        return '\n' + '\n'.join(rows) + '\n'

    def process_definition_list(self, dl_elem):
        """Process HTML definition lists"""
        items = []
        for dt in dl_elem.find_all('dt'):
            term = dt.get_text().strip()
            dd = dt.find_next_sibling('dd')
            definition = dd.get_text().strip() if dd else ''
            items.append(f"**{term}**\n: {definition}\n")
        return '\n' + '\n'.join(items)

    def crawl(self, start_url):
        """Crawl all pages starting from the given URL"""
        to_visit = [start_url]

        while to_visit:
            url = to_visit.pop(0)

            if url in self.visited_urls:
                continue

            self.visited_urls.add(url)

            soup = self.get_page_content(url)
            if not soup:
                continue

            # Extract content
            content = self.extract_content(soup, url)
            self.pages.append(content)

            # Find more pages to visit
            links = self.extract_navigation_links(soup, url)
            to_visit.extend(links)

            # Be polite - rate limit
            time.sleep(1)

        print(f"\nCrawled {len(self.pages)} pages")

    def generate_markdown(self):
        """Generate consolidated markdown document"""
        output = []

        # Header
        output.append("# NVIDIA DCGM User Guide\n")
        output.append("**Source:** https://docs.nvidia.com/datacenter/dcgm/latest/user-guide/\n")
        output.append(f"**Scraped:** {time.strftime('%Y-%m-%d')}\n")
        output.append("**Note:** This is a consolidated version of the online documentation.\n")
        output.append("---\n")

        # Table of Contents
        output.append("\n## Table of Contents\n")
        for i, page in enumerate(self.pages, 1):
            title = page['title'] or f"Section {i}"
            anchor = re.sub(r'[^\w\s-]', '', title.lower()).replace(' ', '-')
            output.append(f"{i}. [{title}](#{anchor})")
        output.append("\n---\n")

        # Content
        for page in self.pages:
            output.append(f"\n\n## {page['title']}\n")
            output.append(f"**Source URL:** {page['url']}\n")
            output.append(page['content'])
            output.append("\n---\n")

        return '\n'.join(output)

    def save_markdown(self, filepath):
        """Save the markdown document"""
        markdown_content = self.generate_markdown()

        Path(filepath).parent.mkdir(parents=True, exist_ok=True)
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(markdown_content)

        print(f"\nSaved to: {filepath}")
        print(f"Total size: {len(markdown_content)} characters")


def main():
    start_url = "https://docs.nvidia.com/datacenter/dcgm/latest/user-guide/index.html"
    output_file = "/srv/projects/og-ai-inference-research/docs/nvidia-manuals/NVIDIA-DCGM-User-Guide.md"

    print("=" * 70)
    print("NVIDIA DCGM User Guide Scraper")
    print("=" * 70)
    print(f"Start URL: {start_url}")
    print(f"Output: {output_file}")
    print("=" * 70)
    print()

    scraper = DCGMGuideScraper(start_url)

    try:
        scraper.crawl(start_url)
        scraper.save_markdown(output_file)
        print("\n✅ Scraping completed successfully!")
        return 0
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
