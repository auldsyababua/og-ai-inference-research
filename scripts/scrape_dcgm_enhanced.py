#!/usr/bin/env python3
"""
Enhanced NVIDIA DCGM User Guide Web Scraper
============================================
Scrapes the complete NVIDIA DCGM User Guide using requests and BeautifulSoup.
Handles the Sphinx documentation structure used by NVIDIA.

Target: https://docs.nvidia.com/datacenter/dcgm/latest/user-guide/index.html
Output: docs/nvidia-manuals/NVIDIA-DCGM-User-Guide.md
"""

import requests
from bs4 import BeautifulSoup
import time
import re
from urllib.parse import urljoin, urlparse
from pathlib import Path
import sys
from collections import OrderedDict

class NVIDIADCGMScraper:
    def __init__(self, base_url):
        self.base_url = base_url
        self.base_domain = f"{urlparse(base_url).scheme}://{urlparse(base_url).netloc}"
        self.visited_urls = set()
        self.pages = OrderedDict()  # Maintain order
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
        })

    def is_valid_dcgm_url(self, url):
        """Check if URL is part of DCGM user guide"""
        parsed = urlparse(url)
        # Must be from docs.nvidia.com and contain dcgm user-guide path
        return (parsed.netloc == 'docs.nvidia.com' and
                '/datacenter/dcgm/' in parsed.path and
                '/user-guide/' in parsed.path and
                parsed.path.endswith('.html'))

    def fetch_page(self, url):
        """Fetch a page with error handling"""
        try:
            print(f"  Fetching: {url}")
            response = self.session.get(url, timeout=30)
            response.raise_for_status()
            time.sleep(0.5)  # Be polite
            return response.text
        except requests.RequestException as e:
            print(f"  ❌ Error fetching {url}: {e}")
            return None

    def extract_sidebar_links(self, soup, current_url):
        """Extract all documentation links from Sphinx sidebar"""
        links = []

        # Sphinx typically uses these structures
        nav_selectors = [
            'div.sphinxsidebarwrapper a.reference.internal',
            'nav.wy-nav-side a.reference.internal',
            '.toctree-l1 > a',
            '.toctree-l2 > a',
            'div.sidebar a',
            '.sphinxsidebar a[href$=".html"]'
        ]

        for selector in nav_selectors:
            nav_links = soup.select(selector)
            if nav_links:
                print(f"  Found {len(nav_links)} links using selector: {selector}")
                for link in nav_links:
                    href = link.get('href')
                    if href and not href.startswith('#'):
                        full_url = urljoin(current_url, href)
                        # Remove fragment
                        full_url = full_url.split('#')[0]
                        if self.is_valid_dcgm_url(full_url):
                            links.append(full_url)

        # Also check for 'next' navigation
        next_link = soup.select_one('link[rel="next"]')
        if next_link:
            href = next_link.get('href')
            if href:
                full_url = urljoin(current_url, href)
                if self.is_valid_dcgm_url(full_url):
                    links.append(full_url)

        return list(OrderedDict.fromkeys(links))  # Remove duplicates, preserve order

    def clean_text(self, text):
        """Clean up text content"""
        # Remove excessive whitespace
        text = re.sub(r'\n\s*\n\s*\n+', '\n\n', text)
        text = re.sub(r' +', ' ', text)
        return text.strip()

    def convert_element_to_markdown(self, element, indent_level=0):
        """Recursively convert HTML elements to markdown"""
        if element is None:
            return ""

        if isinstance(element, str):
            return self.clean_text(element)

        result = []
        indent = "  " * indent_level

        tag = element.name

        # Skip certain elements
        if tag in ['script', 'style', 'nav', 'header', 'footer']:
            return ""

        # Handle different tags
        if tag == 'h1':
            text = element.get_text().strip()
            if text:
                result.append(f"\n# {text}\n")
        elif tag == 'h2':
            text = element.get_text().strip()
            if text:
                result.append(f"\n## {text}\n")
        elif tag == 'h3':
            text = element.get_text().strip()
            if text:
                result.append(f"\n### {text}\n")
        elif tag == 'h4':
            text = element.get_text().strip()
            if text:
                result.append(f"\n#### {text}\n")
        elif tag == 'h5':
            text = element.get_text().strip()
            if text:
                result.append(f"\n##### {text}\n")
        elif tag == 'h6':
            text = element.get_text().strip()
            if text:
                result.append(f"\n###### {text}\n")
        elif tag == 'p':
            text = element.get_text().strip()
            if text:
                result.append(f"\n{text}\n")
        elif tag == 'pre':
            code_elem = element.find('code')
            if code_elem:
                code_text = code_elem.get_text()
                # Try to detect language from class
                lang = ''
                classes = code_elem.get('class', [])
                for cls in classes:
                    if cls.startswith('language-'):
                        lang = cls.replace('language-', '')
                    elif cls in ['bash', 'python', 'c', 'cpp', 'json', 'yaml']:
                        lang = cls
                result.append(f"\n```{lang}\n{code_text}\n```\n")
            else:
                result.append(f"\n```\n{element.get_text()}\n```\n")
        elif tag == 'code' and element.parent.name != 'pre':
            result.append(f"`{element.get_text()}`")
        elif tag == 'a':
            href = element.get('href', '')
            text = element.get_text().strip()
            if text and href:
                # Make relative URLs absolute
                if not href.startswith(('http://', 'https://', '#')):
                    href = urljoin(self.base_url, href)
                result.append(f"[{text}]({href})")
            elif text:
                result.append(text)
        elif tag == 'img':
            alt = element.get('alt', 'Image')
            src = element.get('src', '')
            if src:
                # Make relative URLs absolute
                if not src.startswith(('http://', 'https://')):
                    src = urljoin(self.base_url, src)
                result.append(f"\n![{alt}]({src})\n")
        elif tag in ['ul', 'ol']:
            result.append('\n')
            for i, li in enumerate(element.find_all('li', recursive=False), 1):
                prefix = f"{i}." if tag == 'ol' else "-"
                # Process li content recursively
                li_content = []
                for child in li.children:
                    if child.name:
                        li_content.append(self.convert_element_to_markdown(child, indent_level + 1))
                    elif isinstance(child, str) and child.strip():
                        li_content.append(child.strip())
                text = ' '.join(li_content).strip()
                result.append(f"{indent}{prefix} {text}\n")
        elif tag == 'table':
            result.append(self.convert_table_to_markdown(element))
        elif tag == 'blockquote':
            lines = element.get_text().strip().split('\n')
            result.append('\n')
            for line in lines:
                if line.strip():
                    result.append(f"> {line.strip()}\n")
        elif tag == 'dl':
            # Definition list
            result.append('\n')
            for dt in element.find_all('dt', recursive=False):
                term = dt.get_text().strip()
                dd = dt.find_next_sibling('dd')
                if dd:
                    definition = dd.get_text().strip()
                    result.append(f"**{term}**\n: {definition}\n\n")
        elif tag in ['div', 'section', 'article', 'main', 'span']:
            # Container elements - process children
            for child in element.children:
                if child.name:
                    result.append(self.convert_element_to_markdown(child, indent_level))
                elif isinstance(child, str) and child.strip():
                    result.append(child.strip() + ' ')
        elif tag == 'br':
            result.append('\n')
        elif tag in ['strong', 'b']:
            text = element.get_text().strip()
            if text:
                result.append(f"**{text}**")
        elif tag in ['em', 'i']:
            text = element.get_text().strip()
            if text:
                result.append(f"*{text}*")
        else:
            # Default: extract text
            text = element.get_text().strip()
            if text:
                result.append(text)

        return ''.join(result)

    def convert_table_to_markdown(self, table):
        """Convert HTML table to markdown"""
        rows = []

        # Extract headers
        headers = []
        thead = table.find('thead')
        if thead:
            header_cells = thead.find_all(['th', 'td'])
            headers = [cell.get_text().strip() for cell in header_cells]
        else:
            # Try first row
            first_row = table.find('tr')
            if first_row:
                header_cells = first_row.find_all('th')
                if header_cells:
                    headers = [cell.get_text().strip() for cell in header_cells]

        if headers:
            rows.append('| ' + ' | '.join(headers) + ' |')
            rows.append('| ' + ' | '.join(['---'] * len(headers)) + ' |')

        # Extract body rows
        tbody = table.find('tbody') if table.find('tbody') else table
        for tr in tbody.find_all('tr'):
            cells = tr.find_all(['td', 'th'])
            if cells:
                cell_texts = [cell.get_text().strip().replace('\n', ' ') for cell in cells]
                # Skip if it's the header row we already processed
                if not (headers and cell_texts == headers):
                    rows.append('| ' + ' | '.join(cell_texts) + ' |')

        return '\n' + '\n'.join(rows) + '\n'

    def extract_content(self, html, url):
        """Extract main content from HTML"""
        soup = BeautifulSoup(html, 'html.parser')

        content = {
            'url': url,
            'title': '',
            'content': ''
        }

        # Extract title
        title_elem = soup.find('h1')
        if not title_elem:
            title_elem = soup.find('title')
        if title_elem:
            content['title'] = title_elem.get_text().strip()

        # Find main content (Sphinx specific)
        main_selectors = [
            'div[role="main"]',
            'div.body',
            'div.document',
            'article',
            'main',
            'div.content'
        ]

        main_content = None
        for selector in main_selectors:
            main_content = soup.select_one(selector)
            if main_content:
                break

        if not main_content:
            # Fallback to body
            main_content = soup.body if soup.body else soup

        # Remove navigation and other non-content elements
        for unwanted in main_content.select('nav, .sphinxsidebar, .related, .footer, script, style, .headerlink'):
            unwanted.decompose()

        # Convert to markdown
        content['content'] = self.convert_element_to_markdown(main_content)
        content['content'] = self.clean_text(content['content'])

        return content

    def crawl(self):
        """Crawl all pages of the DCGM user guide"""
        print("\n📚 Starting crawl of DCGM User Guide...")
        print(f"   Base URL: {self.base_url}\n")

        to_visit = [self.base_url]

        while to_visit:
            url = to_visit.pop(0)

            if url in self.visited_urls:
                continue

            print(f"\n[{len(self.visited_urls) + 1}] Processing: {url}")
            self.visited_urls.add(url)

            html = self.fetch_page(url)
            if not html:
                continue

            # Parse and extract content
            soup = BeautifulSoup(html, 'html.parser')
            content = self.extract_content(html, url)

            if content['title']:
                self.pages[url] = content
                print(f"  ✓ Extracted: {content['title']}")

            # Find more links
            links = self.extract_sidebar_links(soup, url)
            new_links = [link for link in links if link not in self.visited_urls]
            to_visit.extend(new_links)

            if new_links:
                print(f"  Found {len(new_links)} new pages to visit")

        print(f"\n✅ Crawled {len(self.pages)} pages total\n")

    def generate_markdown_document(self):
        """Generate final markdown document"""
        lines = []

        # Header
        lines.append("# NVIDIA DCGM User Guide")
        lines.append("")
        lines.append(f"**Source:** {self.base_url}")
        lines.append(f"**Scraped:** {time.strftime('%Y-%m-%d %H:%M:%S UTC', time.gmtime())}")
        lines.append("**Status:** Complete documentation scraped from online source")
        lines.append("")
        lines.append("---")
        lines.append("")

        # Table of Contents
        lines.append("## Table of Contents")
        lines.append("")
        for i, (url, page) in enumerate(self.pages.items(), 1):
            title = page['title'] or f"Section {i}"
            # Create anchor
            anchor = re.sub(r'[^\w\s-]', '', title.lower())
            anchor = re.sub(r'[-\s]+', '-', anchor)
            lines.append(f"{i}. [{title}](#{anchor})")
        lines.append("")
        lines.append("---")
        lines.append("")

        # Content
        for i, (url, page) in enumerate(self.pages.items(), 1):
            lines.append(f"\n## {page['title']}")
            lines.append("")
            lines.append(f"*Source: {url}*")
            lines.append("")
            lines.append(page['content'])
            lines.append("")
            lines.append("---")
            lines.append("")

        # Footer
        lines.append("\n## Document Information")
        lines.append("")
        lines.append(f"- **Total Pages:** {len(self.pages)}")
        lines.append(f"- **Scraped:** {time.strftime('%Y-%m-%d %H:%M:%S UTC', time.gmtime())}")
        lines.append(f"- **Source:** {self.base_url}")
        lines.append("")
        lines.append("**Note:** This documentation is property of NVIDIA Corporation. ")
        lines.append("This scraped version is for research and reference purposes.")
        lines.append("")

        return '\n'.join(lines)

    def save(self, output_path):
        """Save the markdown document"""
        print(f"\n💾 Generating markdown document...")

        markdown = self.generate_markdown_document()

        # Ensure directory exists
        output_file = Path(output_path)
        output_file.parent.mkdir(parents=True, exist_ok=True)

        # Write file
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(markdown)

        # Stats
        size_kb = len(markdown) / 1024
        print(f"\n✅ Saved successfully!")
        print(f"   File: {output_path}")
        print(f"   Size: {size_kb:.1f} KB")
        print(f"   Pages: {len(self.pages)}")
        print(f"   Characters: {len(markdown):,}")


def main():
    """Main execution"""
    print("=" * 80)
    print("NVIDIA DCGM User Guide Scraper")
    print("=" * 80)

    base_url = "https://docs.nvidia.com/datacenter/dcgm/latest/user-guide/index.html"
    output_path = "/srv/projects/og-ai-inference-research/docs/nvidia-manuals/NVIDIA-DCGM-User-Guide.md"

    scraper = NVIDIADCGMScraper(base_url)

    try:
        scraper.crawl()
        scraper.save(output_path)
        print("\n" + "=" * 80)
        print("✅ DCGM User Guide scraping completed successfully!")
        print("=" * 80)
        return 0
    except KeyboardInterrupt:
        print("\n\n⚠️  Interrupted by user")
        return 1
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
