"""
Educational Content Search Engine
Main application entry point
"""

import os
import sys
from pathlib import Path

# Add src to Python path for imports
sys.path.append(str(Path(__file__).parent.parent))

from educational_search.scrapers.docx_scraper import DocxScraper


def main():
    """Main application function"""
    print("Educational Content Search Engine")
    print("=" * 50)
    
    # Initialize the DOCX scraper
    scraper = DocxScraper()
    
    # Start scraping
    try:
        downloaded_count = scraper.scrape_docx_files(max_files=100)
        print(f"\nSuccessfully downloaded {downloaded_count} files")
    except Exception as e:
        print(f"Error during scraping: {e}")
    

if __name__ == "__main__":
    main()