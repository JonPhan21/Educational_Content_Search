import requests
from bs4 import BeautifulSoup
import os
from urllib.parse import urljoin, urlparse
import time
import re

def scrape_docx_files():
    base_url = "https://asianamericanedu.org"
    session = requests.Session()
    session.headers.update({'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'})
    
    # Create downloads directory
    download_dir = "downloaded_docx_files"
    os.makedirs(download_dir, exist_ok=True)
    
    docx_files = []
    visited_pages = set()
    all_pages = set()
    
    def find_all_pages(url, depth=0, max_depth=10):
        """Recursively find all pages on the site"""
        if depth > max_depth or url in visited_pages:
            return set()
        
        visited_pages.add(url)
        found_pages = set()
        
        try:
            print(f"Scanning: {url}")
            response = session.get(url, timeout=10)
            soup = BeautifulSoup(response.content, 'html.parser')
            
            for link in soup.find_all('a', href=True):
                href = link['href']
                full_url = urljoin(base_url, href)
                
                # Skip external links and unwanted content
                if not full_url.startswith(base_url):
                    continue
                if any(skip in href.lower() for skip in ['#', 'javascript:', 'mailto:', '.pdf', '.docx', '/images/', '/css/', '/js/']):
                    continue
                
                # Add all internal pages (HTML and directory-style URLs)
                if (href.endswith('.html') or 
                    (not '.' in href.split('/')[-1] and href != '/') or
                    href.endswith('/')):
                    found_pages.add(full_url)
                    all_pages.add(full_url)
                    
                    # Recursively scan deeper
                    if depth < max_depth and full_url not in visited_pages:
                        found_pages.update(find_all_pages(full_url, depth + 1, max_depth))
            
            time.sleep(0.3)  # Be respectful
            return found_pages
            
        except Exception as e:
            print(f"Error scanning {url}: {e}")
            return set()
    
    def extract_docx_from_page(url):
        """Extract docx download links from a lesson page"""
        try:
            response = session.get(url, timeout=10)
            soup = BeautifulSoup(response.content, 'html.parser')
            
            docx_links = []
            for link in soup.find_all('a', href=True):
                href = link['href']
                if href.endswith('.docx'):
                    full_url = urljoin(base_url, href)
                    filename = os.path.basename(urlparse(href).path)
                    if filename:  # Make sure filename is not empty
                        docx_links.append((full_url, filename))
                        print(f"  Found docx: {filename}")
            
            return docx_links
        except Exception as e:
            print(f"Error extracting from {url}: {e}")
            return []
    
    def download_file(url, filename):
        """Download a single docx file"""
        try:
            response = session.get(url, stream=True)
            response.raise_for_status()
            
            filepath = os.path.join(download_dir, filename)
            with open(filepath, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
            
            print(f"Downloaded: {filename}")
            return True
        except Exception as e:
            print(f"Failed to download {filename}: {e}")
            return False
    
    # Start scraping
    print("Starting to scrape docx files...")
    print("Finding all pages on the website...")
    
    # Find all pages on the site
    visited_pages.clear()  # Reset for page discovery
    find_all_pages(base_url)
    
    print(f"\nFound {len(all_pages)} total pages to check")
    print("Extracting docx files from all pages...")
    
    # Extract docx links from each page
    for page_url in all_pages:
        if len(docx_files) >= 100:
            break
            
        print(f"\nChecking: {page_url}")
        page_docx = extract_docx_from_page(page_url)
        docx_files.extend(page_docx)
        
        time.sleep(0.3)
    
    # Limit to first 100 files
    docx_files = docx_files[:100]
    
    # Remove duplicates
    unique_docx = list(dict.fromkeys(docx_files))
    docx_files = unique_docx[:100]  # Limit to first 100
    
    print(f"\nFound {len(docx_files)} unique docx files to download")
    
    if not docx_files:
        print("No docx files found. The website structure might have changed.")
        return
    
    # Download files
    successful_downloads = 0
    for i, (url, filename) in enumerate(docx_files, 1):
        print(f"\nDownloading {i}/{len(docx_files)}: {filename}")
        if download_file(url, filename):
            successful_downloads += 1
        time.sleep(0.3)
    
    print(f"\n" + "="*50)
    print(f"DOWNLOAD COMPLETE!")
    print(f"Successfully downloaded {successful_downloads} out of {len(docx_files)} files")
    print(f"Files saved to: {os.path.abspath(download_dir)}")
    print(f"" + "="*50)

if __name__ == "__main__":
    scrape_docx_files()