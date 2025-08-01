#!/usr/bin/env python3
"""
HTML to Markdown Converter CLI
Converts HTML content from URLs or local files to Markdown format.
"""

import argparse
import os
import sys
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse


def is_url(string):
    """Check if the input string is a valid URL."""
    try:
        result = urlparse(string)
        return all([result.scheme, result.netloc])
    except:
        return False


def fetch_html_from_url(url):
    """Download HTML content from a URL."""
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        response = requests.get(url, headers=headers, timeout=30)
        response.raise_for_status()
        return response.text
    except requests.exceptions.RequestException as e:
        raise Exception(f"Failed to fetch URL: {e}")


def read_html_from_file(file_path):
    """Read HTML content from a local file."""
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read()
    except FileNotFoundError:
        raise Exception(f"File not found: {file_path}")
    except IOError as e:
        raise Exception(f"Error reading file: {e}")


def convert_element_to_markdown(element, depth=0):
    """Convert a BeautifulSoup element to Markdown."""
    if element.name is None:
        return element.string.strip() if element.string else ""
    
    text_content = ""
    
    if element.name in ['h1', 'h2', 'h3', 'h4', 'h5', 'h6']:
        level = int(element.name[1])
        text_content = f"{'#' * level} {element.get_text().strip()}\n\n"
    
    elif element.name == 'p':
        text_content = f"{element.get_text().strip()}\n\n"
    
    elif element.name == 'a':
        href = element.get('href', '')
        link_text = element.get_text().strip()
        if href and link_text:
            text_content = f"[{link_text}]({href})"
        else:
            text_content = link_text
    
    elif element.name == 'strong' or element.name == 'b':
        text_content = f"**{element.get_text().strip()}**"
    
    elif element.name == 'em' or element.name == 'i':
        text_content = f"*{element.get_text().strip()}*"
    
    elif element.name == 'code':
        text_content = f"`{element.get_text().strip()}`"
    
    elif element.name == 'pre':
        code_content = element.get_text().strip()
        text_content = f"```\n{code_content}\n```\n\n"
    
    elif element.name == 'ul':
        text_content = convert_list_to_markdown(element, ordered=False, depth=depth)
    
    elif element.name == 'ol':
        text_content = convert_list_to_markdown(element, ordered=True, depth=depth)
    
    elif element.name == 'li':
        text_content = element.get_text().strip()
    
    elif element.name == 'br':
        text_content = "\n"
    
    elif element.name == 'hr':
        text_content = "---\n\n"
    
    elif element.name in ['blockquote']:
        quote_text = element.get_text().strip()
        lines = quote_text.split('\n')
        quoted_lines = [f"> {line}" for line in lines]
        text_content = '\n'.join(quoted_lines) + "\n\n"
    
    else:
        for child in element.children:
            text_content += convert_element_to_markdown(child, depth)
    
    return text_content


def convert_list_to_markdown(list_element, ordered=False, depth=0):
    """Convert HTML list elements to Markdown."""
    markdown_lines = []
    indent = "  " * depth
    
    for i, li in enumerate(list_element.find_all('li', recursive=False), 1):
        if ordered:
            prefix = f"{indent}{i}. "
        else:
            prefix = f"{indent}- "
        
        li_text = ""
        for child in li.children:
            if child.name == 'ul':
                li_text += "\n" + convert_list_to_markdown(child, ordered=False, depth=depth+1)
            elif child.name == 'ol':
                li_text += "\n" + convert_list_to_markdown(child, ordered=True, depth=depth+1)
            else:
                li_text += convert_element_to_markdown(child, depth)
        
        markdown_lines.append(f"{prefix}{li_text.strip()}")
    
    return '\n'.join(markdown_lines) + "\n\n"


def html_to_markdown(html_content):
    """Convert HTML content to Markdown."""
    soup = BeautifulSoup(html_content, 'html.parser')
    
    for script in soup(["script", "style", "meta", "link"]):
        script.decompose()
    
    body = soup.find('body')
    if body:
        content_element = body
    else:
        content_element = soup
    
    markdown_content = ""
    
    for element in content_element.children:
        markdown_content += convert_element_to_markdown(element)
    
    lines = markdown_content.split('\n')
    cleaned_lines = []
    prev_empty = False
    
    for line in lines:
        line = line.strip()
        if line == "":
            if not prev_empty:
                cleaned_lines.append("")
                prev_empty = True
        else:
            cleaned_lines.append(line)
            prev_empty = False
    
    return '\n'.join(cleaned_lines).strip() + '\n'


def save_markdown_to_file(markdown_content, output_path):
    """Save Markdown content to a file."""
    try:
        output_dir = os.path.dirname(output_path)
        if output_dir:
            os.makedirs(output_dir, exist_ok=True)
        with open(output_path, 'w', encoding='utf-8') as file:
            file.write(markdown_content)
    except IOError as e:
        raise Exception(f"Error writing to file: {e}")


def main():
    """Main function to handle CLI arguments and orchestrate the conversion."""
    parser = argparse.ArgumentParser(
        description="Convert HTML content from URLs or local files to Markdown format.",
        epilog="Examples:\n"
               "  python html_to_md.py --input https://example.com --output output.md\n"
               "  python html_to_md.py --input ./example.html --output output.md",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    parser.add_argument(
        '--input', '-i',
        required=True,
        help='Input source: URL (https://example.com) or local HTML file path (./file.html)'
    )
    
    parser.add_argument(
        '--output', '-o',
        required=True,
        help='Output Markdown file path (e.g., output.md)'
    )
    
    args = parser.parse_args()
    
    try:
        print(f"Processing input: {args.input}")
        
        if is_url(args.input):
            print("Downloading HTML content from URL...")
            html_content = fetch_html_from_url(args.input)
        else:
            print("Reading HTML content from local file...")
            html_content = read_html_from_file(args.input)
        
        print("Converting HTML to Markdown...")
        markdown_content = html_to_markdown(html_content)
        
        print(f"Saving Markdown to: {args.output}")
        save_markdown_to_file(markdown_content, args.output)
        
        print("✓ Conversion completed successfully!")
        
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()