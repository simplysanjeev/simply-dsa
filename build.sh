#!/bin/bash

# Check for Python
if ! command -v python &> /dev/null; then
    echo "❌ Python not found. Please install Python to continue."
    exit 1
fi

# Check for mkdocs
if ! command -v mkdocs &> /dev/null; then
    echo "❌ MkDocs not found. Run: pip install mkdocs mkdocs-material"
    exit 1
fi

echo "▶ Generating Markdown files..."
python generate_markdown.py || { echo "❌ Markdown generation failed."; exit 1; }

echo "🔧 Building static site..."
mkdocs build || { echo "❌ MkDocs build failed."; exit 1; }

echo "🚀 Deploying to GitHub Pages..."
mkdocs gh-deploy --clean
