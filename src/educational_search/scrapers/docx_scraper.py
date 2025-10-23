"""
DOCX Scraper for Educational Content
Scrapes educational DOCX files from asianamericanedu.org
"""

import requests
from bs4 import BeautifulSoup
import os
from urllib.parse import urljoin, urlparse
import time
import re
from pathlib import Path


class DocxScraper:
    """Web scraper for educational DOCX files"""
    
    def __init__(self, base_url="https://asianamericanedu.org", download_dir=None):
        """
        Initialize the DOCX scraper
        
        Args:
            base_url (str): Base URL to scrape
            download_dir (str): Directory to save downloaded files
        """
        self.base_url = base_url
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
        
        # Set download directory
        if download_dir is None:
            self.download_dir = Path(__file__).parent.parent.parent.parent / "data" / "raw" / "downloaded_docx_files"
        else:
            self.download_dir = Path(download_dir)
        
        self.download_dir.mkdir(parents=True, exist_ok=True)
        
        self.docx_files = []
        self.visited_pages = set()
        self.all_pages = set()
    
    def find_all_pages(self, url, depth=0, max_depth=10):
        """
        Recursively find all pages on the site
        
        Args:
            url (str): URL to start scanning from
            depth (int): Current recursion depth
            max_depth (int): Maximum recursion depth
            
        Returns:
            set: Set of found page URLs
        """
        if depth > max_depth or url in self.visited_pages:
            return set()
        
        self.visited_pages.add(url)
        found_pages = set()
        
        try:
            print(f"Scanning: {url}")
            response = self.session.get(url, timeout=10)
            soup = BeautifulSoup(response.content, 'html.parser')
            
            for link in soup.find_all('a', href=True):
                href = link['href']
                full_url = urljoin(self.base_url, href)
                
                # Skip external links and unwanted content
                if not full_url.startswith(self.base_url):
                    continue
                if any(skip in href.lower() for skip in ['#', 'javascript:', 'mailto:', '.pdf', '.docx', '/images/', '/css/', '/js/']):
                    continue
                
                # Add all internal pages (HTML and directory-style URLs)
                if (href.endswith('.html') or 
                    (not '.' in href.split('/')[-1] and href != '/') or
                    href.endswith('/')):
                    found_pages.add(full_url)
                    self.all_pages.add(full_url)
                    
                    # Recursively scan deeper
                    if depth < max_depth and full_url not in self.visited_pages:
                        found_pages.update(self.find_all_pages(full_url, depth + 1, max_depth))
            
            time.sleep(0.3)  # Be respectful
            return found_pages
            
        except Exception as e:
            print(f"Error scanning {url}: {e}")
            return set()
    
    def extract_docx_from_page(self, url):
        """
        Extract docx download links from a lesson page
        
        Args:
            url (str): URL to extract DOCX links from
            
        Returns:
            list: List of tuples (url, filename) for DOCX files
        """
        try:
            response = self.session.get(url, timeout=10)
            soup = BeautifulSoup(response.content, 'html.parser')
            
            docx_links = []
            for link in soup.find_all('a', href=True):
                href = link['href']
                if href.endswith('.docx'):
                    full_url = urljoin(self.base_url, href)
                    filename = os.path.basename(urlparse(href).path)
                    if filename:  # Make sure filename is not empty
                        docx_links.append((full_url, filename))
                        print(f"  Found docx: {filename}")
            
            return docx_links
        except Exception as e:
            print(f"Error extracting from {url}: {e}")
            return []
    
    def download_file(self, url, filename):
        """
        Download a single docx file
        
        Args:
            url (str): URL to download from
            filename (str): Name to save the file as
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            response = self.session.get(url, stream=True)
            response.raise_for_status()
            
            filepath = self.download_dir / filename
            with open(filepath, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
            
            print(f"Downloaded: {filename}")
            return True
        except Exception as e:
            print(f"Failed to download {filename}: {e}")
            return False
    
    def scrape_docx_files(self, max_files=100):
        """
        Main method to scrape DOCX files
        
        Args:
            max_files (int): Maximum number of files to download
            
        Returns:
            int: Number of successfully downloaded files
        """
        print("Starting to scrape docx files...")
        print("Finding all pages on the website...")
        
        # Find all pages on the site
        self.visited_pages.clear()  # Reset for page discovery
        self.find_all_pages(self.base_url)
        
        print(f"\nFound {len(self.all_pages)} total pages to check")
        print("Extracting docx files from all pages...")
        
        # Extract docx links from each page
        for page_url in self.all_pages:
            if len(self.docx_files) >= max_files:
                break
                
            print(f"\nChecking: {page_url}")
            page_docx = self.extract_docx_from_page(page_url)
            self.docx_files.extend(page_docx)
            
            time.sleep(0.3)
        
        # Limit to first max_files
        self.docx_files = self.docx_files[:max_files]
        
        # Remove duplicates
        unique_docx = list(dict.fromkeys(self.docx_files))
        self.docx_files = unique_docx[:max_files]  # Limit to first max_files
        
        print(f"\nFound {len(self.docx_files)} unique docx files to download")
        
        if not self.docx_files:
            print("No docx files found. The website structure might have changed.")
            return 0
        
        # Download files
        successful_downloads = 0
        for i, (url, filename) in enumerate(self.docx_files, 1):
            print(f"\nDownloading {i}/{len(self.docx_files)}: {filename}")
            if self.download_file(url, filename):
                successful_downloads += 1
            time.sleep(0.3)
        
        print(f"\n" + "="*50)
        print(f"DOWNLOAD COMPLETE!")
        print(f"Successfully downloaded {successful_downloads} out of {len(self.docx_files)} files")
        print(f"Files saved to: {self.download_dir.absolute()}")
        print(f"" + "="*50)
        
        return successful_downloads


def main():
    """Main function to run the scraper"""
    scraper = DocxScraper()
    scraper.scrape_docx_files()


if __name__ == "__main__":
    main()