# Scifigraph - Sci-Fi Economic Concepts Extractor

A Python tool that reads text files containing science fiction book reviews or summaries and uses AI to extract relationships between books and the economic concepts they explore. The output is a clean, minimal JSON structure perfect for knowledge graph analysis. Built for Edgeryders and the Sci-Fi economics lab, for use primarily on our discussions of books and authors.

It essentially turns text into this: 

<img width="1275" alt="Screenshot 2025-07-01 at 15 41 17" src="https://github.com/user-attachments/assets/7b8fea44-13b3-4c83-9e6f-e03e19731750" />

The input is a folder containing book reviews, summaries, or academic papers about sci-fi novels (up to 7000-ish words, to be safe)


## Key Features

- **Easy to use**: Stick files in an input folder, run, enjoy the JSON. It's easy.
- **Fuzzy Matching**: Automatically deduplicates similar books and concepts
- **Multiple Formats**: Supports both plain text and HTML input files
- **Robust Processing**: Handles encoding issues and API errors with relative grace
- **Fast Processing**: Uses Claude 3.5 Sonnet for efficient extraction
- **Clean Output**: Simple JSON with just books and concepts - no unnecessary metadata
- **Bidirectional Relationships**: Easy to query books by concepts or concepts by books

## Use Cases

This is largely meant for researchers, academics, and sci-fi enthusiasts who want analyze economic themes in science fiction literature. Broadly:

- **Academic Research**: Analyze economic themes across sci-fi literature
- **Content Discovery**: Find books that explore specific economic concepts
- **Knowledge Graph Analysis**: Build networks of books and concepts
- **Data Visualization**: Create graphs showing relationships between literature and economics
- **Research Projects**: Support studies on economics in speculative fiction

## Installation

### Prerequisites
- Python 3.7 or higher
- An Anthropic API key (get one at [console.anthropic.com](https://console.anthropic.com))

### Setup Steps

1. **Install Python dependencies:**
```bash
pip install anthropic beautifulsoup4 fuzzywuzzy python-levenshtein
```

2. **Set up your API key:**
Create a file named `api_key.txt` in the project directory and add your Anthropic API key:
```
your-anthropic-api-key-here
```

3. **Prepare input files:**
Create an `Input/` folder and add your text files containing sci-fi book reviews/summaries.

## Usage

### Basic Usage
```bash
python graphgen.py
```
Depending on your Python setup, you might have to use instead

```bash
python3 graphgen.py
```
This will:
- Process all files in the `Input/` folder
- Generate `scifi_concepts_clean.json` with the extracted knowledge graph
- Display progress and summary statistics

### Custom Options
```bash
# Use a different input folder
python3 graphgen.py --folder MyFiles

# Specify custom output filename
python3 graphgen.py --output my_concepts

# Both options together
python3 graphgen.py --folder MyFiles --output my_concepts
```

## Input Requirements

### Supported File Types
- **Plain text files** (`.txt`)
- **HTML files** (`.html`, `.htm`)

### Content Types
- Book reviews from websites, blogs, or publications
- Academic papers discussing sci-fi novels
- Wikipedia summaries of science fiction books
- Discussion posts about sci-fi literature and economics
- Any text that mentions sci-fi books and economic concepts

### File Specifications
- **File size**: Up to 50KB each (larger files will be truncated)
- **Encoding**: UTF-8 preferred, but the tool handles most common encodings
- **Location**: All files must be in the specified input folder

## Output Format

The tool generates a clean JSON file with this structure:

```json
{
  "books": [
    {
      "title": "Foundation",
      "author": "Isaac Asimov",
      "concepts": ["Psychohistory", "Economic Modeling", "Social Prediction"]
    }
  ],
  "concepts": [
    {
      "name": "Psychohistory",
      "books": ["Foundation", "Foundation and Empire"]
    }
  ]
}
```

### Real Example Output

Based on processing reviews of "Another Now" and "Market Forces":

```json
{
  "books": [
    {
      "title": "Another Now",
      "author": "Yanis Varoufakis",
      "concepts": [
        "Central Banking",
        "Corporate Democracy",
        "International Trade Balance",
        "Labor Market Reform",
        "Market Socialism",
        "Universal Basic Dividend"
      ]
    },
    {
      "title": "Market Forces",
      "author": "Richard Morgan",
      "concepts": [
        "Corporate Governance",
        "Corporate Monopoly",
        "Economic Exploitation",
        "Economic Imperialism",
        "Economic Inequality",
        "Free Market Capitalism",
        "Global Investment",
        "Gross Domestic Product",
        "Market Competition"
      ]
    }
  ],
  "concepts": [
    {
      "name": "Central Banking",
      "books": ["Another Now"]
    },
    {
      "name": "Corporate Democracy",
      "books": ["Another Now"]
    },
    {
      "name": "Free Market Capitalism",
      "books": ["Market Forces"]
    }
  ]
}
```



## File Structure

```
├── graphgen_simple.py          # Main extraction program
├── README.md                   # This documentation
├── api_key.txt                 # Your Anthropic API key (create this)
├── Input/                      # Input folder (create this)
│   ├── book_review1.txt
│   ├── book_review2.html
│   └── ...
└── scifi_concepts_clean.json   # Generated output
```
## How It Works

### Core Components

#### FileProcessor
- Discovers and reads input files
- Handles multiple file formats and encodings
- Extracts clean text from HTML files

#### ClaudeExtractor
- Interfaces with Anthropic's Claude API
- Sends focused prompts for book and concept extraction
- Handles API rate limiting and error recovery

#### EntityNormalizer
- Deduplicates similar books and concepts using fuzzy string matching
- Creates bidirectional relationships between books and concepts
- Maintains consistent naming across entities

#### SciFiConceptExtractor
- Orchestrates the entire processing pipeline
- Aggregates results from all input files
- Generates the final clean JSON output

### Data Models

```python
# Book entity - represents a science fiction novel
{
    "title": str,           # Book title
    "author": str,          # Author name
    "concepts": [str]       # List of economic concepts
}

# Concept entity - represents an economic concept
{
    "name": str,           # Concept name
    "books": [str]         # List of book titles
}
```

## Troubleshooting

### Common Issues

**"No module named 'anthropic'"**
```bash
pip install anthropic beautifulsoup4 fuzzywuzzy python-levenshtein
```

**"API key not found"**
- Ensure `api_key.txt` exists in the project directory
- Check that the file contains only your API key (no extra spaces/newlines)
- Verify your API key is valid at [console.anthropic.com](https://console.anthropic.com)

**"Folder path does not exist"**
- Create an `Input/` folder in the project directory
- Add your text files to this folder
- Ensure the folder name is exactly `Input` (case-sensitive)

**No extractions found**
- Ensure your text files contain clear references to sci-fi books and economic concepts
- Check that files are not empty or corrupted
- Verify files contain actual book reviews or summaries, not just metadata

**API errors or timeouts**
- Check your internet connection
- Verify your Anthropic API key has sufficient credits
- The tool automatically retries failed requests


## Customization and Extension

- **Larger files**: switch the model to a different version with a larger context window. 
- **Large datasets**: For 500+ files, consider processing in smaller batches
- **Content quality**: Higher quality input text produces better extractions

Scifigraph can be easily modified to extract different types of concepts by editing the Claude prompts in `graphgen_simple.py`. For example:

- **Political concepts** in sci-fi literature
- **Technological themes** across different genres
- **Social issues** in speculative fiction

Scifigraph can be adapted to use other AI services by modifying the `ClaudeExtractor` class. It's not doing anything special enough that it can't be switched to something else - even a local LLM is easy to do.

## Output Analysis

### Using the JSON Output

The generated JSON can be easily imported into:
- **Graph databases** (Neo4j, Amazon Neptune)
- **Visualization tools** (Gephi, Cytoscape, D3.js)
- **Data analysis platforms** (Python pandas, R)
- **Spreadsheet applications** (Excel, Google Sheets)

### Example Analysis Queries

With the JSON output, you can easily answer questions like:
- Which books explore "Universal Basic Income"?
- What economic concepts appear most frequently across sci-fi literature?
- Which authors write most about economic themes?
- How are different economic concepts connected through shared books?

## Contributing

This tool is designed to be simple and focused. When making modifications:

1. Preserve the clean, minimal output format
2. Maintain the bidirectional relationship structure
3. Keep the codebase readable and well-documented
4. Test with sample files to ensure quality extraction

## License

This project is provided as-is for research and educational purposes.

## Support

For issues, questions, or contributions, please refer to the project documentation or create an issue in the project repository.
