
# HTML to Markdown CLI Converter

A Python command-line application that converts HTML content from URLs or local files to Markdown format.

## Features

- Convert HTML from URLs or local files to Markdown
- Support for common HTML elements:
  - Headings (h1-h6)
  - Paragraphs
  - Lists (ordered and unordered)
  - Links
  - Bold and italic text
  - Code blocks and inline code
  - Blockquotes
- Comprehensive error handling for network and file issues
- Clean, readable Markdown output

## About `uv`

[`uv`](https://github.com/astral-sh/uv) is an extremely fast Python package manager and virtual environment tool, acting as a drop-in replacement for `pip`, `pip-tools`, and `virtualenv`. It's written in Rust and designed for performance and reliability.

### Install `uv`

You can install `uv` using the official installation script:

```bash
curl -Ls https://astral.sh/uv/install.sh | sh
````

Or with Homebrew (macOS/Linux):

```bash
brew install astral-sh/uv/uv
```

Make sure the `uv` binary is in your system `PATH`.

## Installation

1. Clone or download this repository

2. Navigate to the project directory:

   ```bash
   cd html_to_markdown_cli
   ```

3. Create a virtual environment using `uv`:

   ```bash
   uv venv
   ```

4. Activate the virtual environment:

   ```bash
   source .venv/bin/activate  # On Windows: .venv\\Scripts\\activate
   ```

5. Install dependencies:

   ```bash
   uv pip install -r requirements.txt
   ```

## Usage

### Basic Usage

Convert HTML from a URL:

```bash
uv run -m html_to_md --input https://example.com --output output/output.md
```

Convert HTML from a local file:

```bash
uv run -m html_to_md --input ./example.html --output output/output.md
```

### Command Line Options

* `--input, -i`: Input source (URL or local HTML file path) - **Required**
* `--output, -o`: Output Markdown file path - **Required**
* `--help, -h`: Show help message

### Examples

```bash
# Convert a webpage to Markdown
uv run -m html_to_md --input https://httpbin.org/html --output output/webpage.md

# Convert a local HTML file to Markdown
uv run -m html_to_md --input ./test.html --output output/test.md

# Show help
uv run -m html_to_md --help
```

## Dependencies

* `requests==2.31.0` - For downloading HTML content from URLs
* `beautifulsoup4==4.12.2` - For parsing HTML content

## Error Handling

The application handles various error scenarios:

* Invalid URLs or connection issues
* File not found errors
* Permission errors when reading/writing files
* Invalid HTML content
* Network timeouts

## Output Format

The tool converts HTML elements to their Markdown equivalents:

| HTML Element      | Markdown Output        |
| ----------------- | ---------------------- |
| `<h1>` to `<h6>`  | `#` to `######`        |
| `<p>`             | Plain text with breaks |
| `<strong>`, `<b>` | `**bold text**`        |
| `<em>`, `<i>`     | `*italic text*`        |
| `<a href="url">`  | `[text](url)`          |
| `<ul>`, `<li>`    | `- item`               |
| `<ol>`, `<li>`    | `1. item`              |
| `<code>`          | `` `code` ``           |
| `<pre>`           | `code block`           |
| `<blockquote>`    | `> quoted text`        |

## License

This project is open source and available under the MIT License.
