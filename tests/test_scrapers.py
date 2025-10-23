"""
Tests for the DOCX scraper
"""

import unittest
from unittest.mock import patch, MagicMock
from pathlib import Path
import sys

# Add src to path for imports
sys.path.append(str(Path(__file__).parent.parent / "src"))

from educational_search.scrapers.docx_scraper import DocxScraper


class TestDocxScraper(unittest.TestCase):
    """Test cases for DocxScraper class"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.scraper = DocxScraper()
    
    def test_scraper_initialization(self):
        """Test that scraper initializes correctly"""
        self.assertEqual(self.scraper.base_url, "https://asianamericanedu.org")
        self.assertIsNotNone(self.scraper.session)
        self.assertTrue(self.scraper.download_dir.exists())
    
    @patch('educational_search.scrapers.docx_scraper.requests.Session.get')
    def test_extract_docx_from_page(self, mock_get):
        """Test DOCX extraction from a page"""
        # Mock response
        mock_response = MagicMock()
        mock_response.content = b'<html><a href="test.docx">Download</a></html>'
        mock_get.return_value = mock_response
        
        # Test extraction
        result = self.scraper.extract_docx_from_page("http://test.com")
        self.assertIsInstance(result, list)


if __name__ == '__main__':
    unittest.main()