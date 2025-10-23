# API Documentation

## Educational Content Search Engine

### DocxScraper Class

The `DocxScraper` class is responsible for scraping educational DOCX files from websites.

#### Methods

- `__init__(base_url, download_dir)`: Initialize the scraper
- `scrape_docx_files(max_files)`: Main method to scrape DOCX files
- `find_all_pages(url, depth, max_depth)`: Recursively find all pages on a site
- `extract_docx_from_page(url)`: Extract DOCX links from a specific page
- `download_file(url, filename)`: Download a single DOCX file

#### Usage Example

```python
from educational_search.scrapers.docx_scraper import DocxScraper

# Initialize scraper
scraper = DocxScraper()

# Scrape files (downloads to data/raw/downloaded_docx_files/)
count = scraper.scrape_docx_files(max_files=50)
print(f"Downloaded {count} files")
```

### Configuration

The application uses environment variables for configuration:

- `AWS_ACCESS_KEY_ID`: AWS access key
- `AWS_SECRET_ACCESS_KEY`: AWS secret key
- `KNOWLEDGE_BASE_ID`: Knowledge base identifier
- `AWS_DEFAULT_REGION`: AWS region (default: us-west-2)
- `BEDROCK_MODEL_ID`: Bedrock model identifier