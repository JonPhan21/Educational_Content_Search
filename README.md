# Educational Content Search

A powerful search engine for educational content that helps students and educators find relevant learning materials quickly and efficiently.

## 📋 Table of Contents
- [Overview](#overview)
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [Technologies Used](#technologies-used)
- [Contributing](#contributing)
- [License](#license)

## 🎯 Overview

This project was developed during a hackathon to solve the problem of finding quality educational content across multiple platforms. The search engine uses advanced algorithms to index and retrieve educational materials based on relevance, quality, and user preferences.

## ✨ Features

- **Smart Search**: AI-powered search with natural language processing
- **Content Filtering**: Filter by subject, difficulty level, content type
- **Quality Scoring**: Automatic content quality assessment
- **Multi-platform Support**: Search across various educational platforms
- **User Preferences**: Personalized search results
- **DOCX Scraping**: Automated scraping of educational DOCX files

## 🚀 Installation

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Quick Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/JonPhan21/Educational_Content_Search.git
   cd Educational_Content_Search
   ```

2. **Run the setup script**
   ```bash
   ./scripts/setup_environment.sh
   ```

### Manual Setup

1. **Create virtual environment**
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Environment setup**
   ```bash
   cp .env.example .env
   # Edit .env with your API keys and configuration
   ```

## 💡 Usage

### Running the DOCX Scraper

## 📁 Project Structure

```
Educational_Content_Search/
├── .env.example                    # Environment variables template
├── .gitignore                      # Git ignore rules
├── README.md                       # Project documentation
├── requirements.txt                # Python dependencies
├── setup.py                        # Package setup configuration
├── src/                           # Source code
│   └── educational_search/
│       ├── __init__.py
│       ├── main.py                # Main application entry point
│       ├── scrapers/              # Web scraping modules
│       │   ├── __init__.py
│       │   └── docx_scraper.py    # DOCX file scraper
│       └── utils/                 # Utility functions
│           └── __init__.py
├── data/                          # Data storage
│   ├── raw/                       # Raw scraped data
│   │   ├── .gitkeep
│   │   └── downloaded_docx_files/ # Downloaded DOCX files
│   └── processed/                 # Processed data
│       └── .gitkeep
├── tests/                         # Unit tests
│   ├── __init__.py
│   └── test_scrapers.py          # Scraper tests
├── docs/                          # Documentation
│   └── api.md                     # API documentation
└── scripts/                       # Utility scripts
    └── setup_environment.sh       # Environment setup script
```

## 🛠 Technologies Used

- **Python 3.8+**: Core programming language
- **Requests**: HTTP library for web scraping
- **BeautifulSoup4**: HTML/XML parsing for content extraction
- **python-docx**: DOCX file processing
- **NLTK**: Natural Language Processing toolkit
- **Pandas & NumPy**: Data manipulation and analysis
- **AWS Bedrock**: AI/ML services integration

## 🧪 Testing

Run the test suite:

```bash
# Run all tests
python -m pytest tests/

# Run specific test file
python -m pytest tests/test_scrapers.py

# Run with coverage
python -m pytest tests/ --cov=src/educational_search
```

## 🤝 Contributing

We welcome contributions! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Development Setup

```bash
# Install development dependencies
pip install -r requirements.txt

# Run tests
python -m pytest

# Run linting
flake8 src/
black src/
```

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Hackathon organizers and mentors
- Asian American Education organization for content source
- Open source libraries and tools used

## 📞 Contact

- **Project Team**: Educational Search Team
- **Repository**: https://github.com/JonPhan21/Educational_Content_Search

---

*Built with ❤️ during Hackathon 2025*

### Using the DocxScraper Class

```python
from educational_search.scrapers.docx_scraper import DocxScraper

# Initialize scraper
scraper = DocxScraper()

# Scrape files (downloads to data/raw/downloaded_docx_files/)
count = scraper.scrape_docx_files(max_files=50)
print(f"Downloaded {count} files")
```