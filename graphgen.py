#!/usr/bin/env python3
"""
Sci-Fi Economic Concepts Extractor

Requirements:
- pip install anthropic beautifulsoup4 fuzzywuzzy python-levenshtein
- Create an 'api_key.txt' file with your Anthropic API key
- Create an 'Input' folder with your text files
"""

import os
import json
import time
import logging
from pathlib import Path
from typing import Dict, List, Optional, Set
from dataclasses import dataclass
import re

import anthropic
from bs4 import BeautifulSoup
from fuzzywuzzy import fuzz, process

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

@dataclass
class Book:
    """Simplified book representation"""
    title: str
    author: str = ""
    concepts: Set[str] = None
    
    def __post_init__(self):
        if self.concepts is None:
            self.concepts = set()
    
    def __hash__(self):
        return hash((self.title.lower(), self.author.lower()))

@dataclass 
class EconomicConcept:
    """Simplified economic concept representation"""
    name: str
    books: Set[str] = None
    
    def __post_init__(self):
        if self.books is None:
            self.books = set()
    
    def __hash__(self):
        return hash(self.name.lower())

class FileProcessor:
    """Handles file discovery and content extraction"""
    
    def __init__(self, folder_path: str):
        self.folder_path = Path(folder_path)
        self.supported_extensions = {'.txt', '.html', '.htm'}
    
    def discover_files(self) -> List[Path]:
        """Find all supported text files"""
        files = []
        for ext in self.supported_extensions:
            files.extend(self.folder_path.rglob(f'*{ext}'))
        logger.info(f"Found {len(files)} files to process")
        return files
    
    def extract_content(self, file_path: Path) -> str:
        """Extract clean text content from file"""
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
            
            if file_path.suffix.lower() in {'.html', '.htm'}:
                soup = BeautifulSoup(content, 'html.parser')
                for script in soup(["script", "style"]):
                    script.extract()
                content = soup.get_text()
            
            # Clean up whitespace
            content = re.sub(r'\s+', ' ', content).strip()
            return content
            
        except Exception as e:
            logger.error(f"Error processing file {file_path}: {e}")
            return ""

class ClaudeExtractor:
    """Handles Claude API interactions for concept extraction"""
    
    def __init__(self, api_key: str):
        self.client = anthropic.Anthropic(api_key=api_key)
        self.rate_limit_delay = 1.0
        
    def extract_book_concepts(self, text: str, filename: str = "") -> Dict:
        """Extract books and their economic concepts from text"""
        
        prompt = f"""
Analyze the following text about science fiction novels and extract ONLY the essential information.

Return a JSON object with this exact structure:
{{
    "extractions": [
        {{
            "book_title": "Exact Book Title",
            "author": "Author Name", 
            "economic_concepts": ["Concept 1", "Concept 2", "Concept 3"]
        }}
    ]
}}

Rules:
1. Extract all books in the Input folder
2. Only include legitimate concepts from economics (not general business terms)
3. Include both specific economic concepts (e.g. "environmental subsidies") and terms that refer to broader concepts and theories (e.g. "fiscal policy" or "mechanism design") of subdisciplines of economics (e.g. "economic anthropology", "game theory", or "public microeconomics"). When including a specific economics concept, also include the broader concept or subdiscipline in which the specific economics concept is nested (e.g. both "prisoner's dilemma" and "game theory").
4. Use standard economic concept names (e.g., "Universal Basic Income" not "UBI")
5. If no clear sci-fi books are found, return empty extractions array
6. Normalize book titles and author names consistently
7. Focus on core economic concepts, not peripheral mentions
8. Only use the word "economics" for subdisciplines, such as "labour economics" or "environmental economics", or models, such as "neoclassical economics". Do not attach the word "economics" to nouns otherwise. For example, if you encounter the expression "the economics of open data", return "open data". 

Text to analyze:
{text[:15000]}
"""

        try:
            response = self.client.messages.create(
                model="claude-3-5-haiku-20241022",
                max_tokens=8000,
                messages=[{"role": "user", "content": prompt}]
            )
            
            content = response.content[0].text
            json_start = content.find('{')
            json_end = content.rfind('}') + 1
            
            if json_start >= 0 and json_end > json_start:
                json_str = content[json_start:json_end]
                result = json.loads(json_str)
                extractions = result.get('extractions', [])
                logger.info(f"Extracted {len(extractions)} book-concept mappings from {filename}")
                return result
            else:
                logger.warning(f"No valid JSON found in Claude response for {filename}")
                return {"extractions": []}
                
        except json.JSONDecodeError as e:
            logger.error(f"JSON decode error for {filename}: {e}")
            return {"extractions": []}
        except Exception as e:
            logger.error(f"Claude API error for {filename}: {e}")
            time.sleep(5)
            return {"extractions": []}
        finally:
            time.sleep(self.rate_limit_delay)

class EntityNormalizer:
    """Handles deduplication and normalization of books and concepts"""
    
    def __init__(self, similarity_threshold: int = 75):
        self.similarity_threshold = similarity_threshold
        self.books: Dict[str, Book] = {}
        self.concepts: Dict[str, EconomicConcept] = {}
    
    def add_extraction(self, book_title: str, author: str, concept_names: List[str]):
        """Add a book-concepts extraction to the normalized collection"""
        if not book_title.strip():
            return
            
        # Normalize book
        book_key = self._normalize_book(book_title, author)
        
        # Normalize concepts and create bidirectional relationships
        for concept_name in concept_names:
            if not concept_name.strip():
                continue
                
            concept_key = self._normalize_concept(concept_name)
            
            # Add concept to book
            self.books[book_key].concepts.add(self.concepts[concept_key].name)
            
            # Add book to concept
            self.concepts[concept_key].books.add(self.books[book_key].title)
    
    def _normalize_book(self, title: str, author: str) -> str:
        """Normalize book and return its key"""
        title = title.strip()
        author = author.strip()
        
        # Check for similar existing books
        for existing_key, existing_book in self.books.items():
            title_similarity = fuzz.ratio(title.lower(), existing_book.title.lower())
            if title_similarity >= self.similarity_threshold:
                # Merge author info if missing
                if not existing_book.author and author:
                    existing_book.author = author
                return existing_key
        
        # Create new book
        book_key = title.lower()
        self.books[book_key] = Book(title=title, author=author)
        return book_key
    
    def _normalize_concept(self, name: str) -> str:
        """Normalize concept and return its key"""
        name = name.strip()
        
        # Check for similar existing concepts
        for existing_key, existing_concept in self.concepts.items():
            name_similarity = fuzz.ratio(name.lower(), existing_concept.name.lower())
            if name_similarity >= self.similarity_threshold:
                return existing_key
        
        # Create new concept
        concept_key = name.lower()
        self.concepts[concept_key] = EconomicConcept(name=name)
        return concept_key

class SciFiConceptExtractor:
    """Main orchestrator for the simplified extraction pipeline"""
    
    def __init__(self, folder_path: str, api_key: str):
        self.folder_path = folder_path
        self.file_processor = FileProcessor(folder_path)
        self.claude_extractor = ClaudeExtractor(api_key)
        self.entity_normalizer = EntityNormalizer()
    
    def process_files(self) -> None:
        """Process all files and extract book-concept relationships"""
        files = self.file_processor.discover_files()
        
        for i, file_path in enumerate(files, 1):
            logger.info(f"Processing file {i}/{len(files)}: {file_path.name}")
            
            content = self.file_processor.extract_content(file_path)
            if not content:
                continue
            
            # Extract using Claude
            result = self.claude_extractor.extract_book_concepts(content, str(file_path))
            
            # Process extractions
            for extraction in result.get('extractions', []):
                book_title = extraction.get('book_title', '')
                author = extraction.get('author', '')
                concepts = extraction.get('economic_concepts', [])
                
                if book_title and concepts:
                    self.entity_normalizer.add_extraction(book_title, author, concepts)
        
        logger.info(f"Processing complete. Found {len(self.entity_normalizer.books)} unique books "
                   f"and {len(self.entity_normalizer.concepts)} unique concepts.")
    
    def save_results(self, output_path: str) -> None:
        """Save the clean, simplified results"""
        
        # Convert to clean output format
        books_output = []
        for book in self.entity_normalizer.books.values():
            books_output.append({
                "title": book.title,
                "author": book.author,
                "concepts": sorted(list(book.concepts))
            })
        
        concepts_output = []
        for concept in self.entity_normalizer.concepts.values():
            concepts_output.append({
                "name": concept.name,
                "books": sorted(list(concept.books))
            })
        
        # Sort outputs
        books_output.sort(key=lambda x: x['title'])
        concepts_output.sort(key=lambda x: x['name'])
        
        # Create final output
        output_data = {
            "books": books_output,
            "concepts": concepts_output
        }
        
        # Save to file
        output_file = f"{output_path}.json"
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(output_data, f, indent=2, ensure_ascii=False)
        
        logger.info(f"Clean results saved to {output_file}")
        
        # Print summary
        print(f"\nResults saved to: {output_file}")
        print(f"\nKnowledge Graph Summary:")
        print(f"- Books: {len(books_output)}")
        print(f"- Economic Concepts: {len(concepts_output)}")
        print(f"- Total Relationships: {sum(len(book['concepts']) for book in books_output)}")
    
    def run(self, output_path: str = "scifi_concepts_clean") -> None:
        """Run the complete simplified pipeline"""
        logger.info("Starting Simplified Sci-Fi Economic Concepts Extractor")
        
        try:
            self.process_files()
            self.save_results(output_path)
            logger.info("Pipeline completed successfully!")
            
        except Exception as e:
            logger.error(f"Pipeline failed: {e}")
            raise

def load_api_key() -> Optional[str]:
    """Load API key from file or environment variable"""
    script_dir = Path(__file__).parent
    api_key_file = script_dir / "api_key.txt"
    
    if api_key_file.exists():
        try:
            with open(api_key_file, 'r', encoding='utf-8') as f:
                api_key = f.read().strip()
                if api_key:
                    logger.info("API key loaded from api_key.txt")
                    return api_key
        except Exception as e:
            logger.warning(f"Failed to read API key from file: {e}")
    
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if api_key:
        logger.info("API key loaded from environment variable")
        return api_key
    
    return None

def main():
    """Main entry point"""
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Extract a clean knowledge graph of sci-fi books and economic concepts"
    )
    parser.add_argument(
        "--folder",
        default="Input",
        help="Path to folder containing text files (default: Input)"
    )
    parser.add_argument(
        "--output", 
        default="scifi_concepts_clean",
        help="Output JSON file name (without extension) (default: scifi_concepts_clean)"
    )
    
    args = parser.parse_args()
    
    # Get API key
    api_key = load_api_key()
    if not api_key:
        print("Error: Anthropic API key not found!")
        print("Please either:")
        print("1. Create an 'api_key.txt' file in the same directory as this script")
        print("2. Set the ANTHROPIC_API_KEY environment variable")
        return 1
    
    # Validate folder path
    if not os.path.isdir(args.folder):
        print(f"Error: Folder path '{args.folder}' does not exist")
        print("Please create an 'Input' folder or specify a different folder with --folder")
        return 1
    
    try:
        extractor = SciFiConceptExtractor(args.folder, api_key)
        extractor.run(args.output)
        return 0
    except KeyboardInterrupt:
        print("\nOperation cancelled by user")
        return 1
    except Exception as e:
        print(f"Error: {e}")
        return 1

if __name__ == "__main__":
    exit(main())
