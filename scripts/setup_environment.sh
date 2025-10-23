#!/bin/bash
# Setup script for Educational Content Search Engine

echo "Setting up Educational Content Search Engine..."

# Create virtual environment if it doesn't exist
if [ ! -d ".venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv .venv
fi

# Activate virtual environment
echo "Activating virtual environment..."
source .venv/bin/activate

# Upgrade pip
echo "Upgrading pip..."
pip install --upgrade pip

# Install requirements
echo "Installing requirements..."
pip install -r requirements.txt

# Create .env file if it doesn't exist
if [ ! -f ".env" ]; then
    echo "Creating .env file from template..."
    cp .env.example .env
    echo "Please edit .env file with your actual values"
fi

# Create data directories
echo "Creating data directories..."
mkdir -p data/raw/downloaded_docx_files
mkdir -p data/processed

echo "Setup complete!"
echo "Don't forget to edit .env with your actual configuration values"
echo "To run the application: python src/educational_search/main.py"