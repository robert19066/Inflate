
# Project Overview

Inflate is a Python-based compression and archival utility that supports two compression methods:
- **ACS (Abstract Compression System)**: Local compression using 7z format with .acs extension.
- **CBAC (Cloud-Based Abstract Compression)**: Cloud-enabled compression using Dawnbond(Supabase abstraction layer made by me) for remote storage

The system creates file maps and content files, compresses them using py7zr (7-Zip), and optionally uploads to cloud storage with retrieval codes.

## Architecture

# Inner works

## How ACS Works

ACS(or Abstract Compression System) generates 2 blueprints of the selected folder: filemap.txt(map of all files) and filecntt.txt(file contents). Then the 2 files get packed into an .acs arhive. ACS is 3% faster than ZIP and 53% smaller than ZIP(tested on the latest CURL build)

## How CBAC Works

CBAC(or Cloud Based Abstract Compression) uses ACS to create an arhive,and then it stores it using Dawnbond,an supabase abstraction.You can purge,upload and take down from CBAC.  


### Core Components

- **`inflate.py`**: Main CLI interface and orchestration layer
- **`acsmain.py`**: ACS compression/decompression engine with 7z handling
- **`dawnbond.py`**: Supabase cloud storage interface (DawnbondCloud class)

### Data Flow
1. **Compression**: Files → filemap.txt + filecntt.txt → 7z archive → .acs file → (optional) cloud upload
2. **Decompression**: .acs/.cbac file → extract 7z → parse filemap/filecntt → reconstruct directory structure

### External Dependencies
- **py7zr**: Python 7-Zip library for compression
- **supabase-py**: Cloud database/storage client
- **python-dotenv**: Environment variable management
- **System requirement**: 7z command-line tool must be installed

## Development Environment Setup

```bash
# Activate virtual environment (REQUIRED)
source .venv/bin/activate

# Install system dependency
sudo apt install p7zip-full  # Ubuntu/Debian
# or
brew install p7zip  # macOS

# Environment configuration
# Copy .env.template to .env and configure:
# SUPABASE_URL=your_supabase_url
# SUPABASE_KEY=your_supabase_key
```

## Common Development Commands

### Running the Application
```bash
# Must run from virtual environment
source .venv/bin/activate

# ACS local compression
python inflate.py --method acs --compress /path/to/folder

# ACS local decompression  
python inflate.py --method acs --decompress file.acs [output_folder]

# CBAC cloud compression
python inflate.py --method cbac --compress /path/to/folder

# CBAC cloud decompression
python inflate.py --method cbac --decompress <retrieval_code> [output_folder]

# CBAC cloud cleanup
python inflate.py --method cbac --purge <retrieval_code>
```

### Development Testing
```bash
# Test core dependencies are available
python -c "import py7zr, supabase, dotenv; print('All dependencies OK')"

# Test system 7z availability
7z --help

# Quick functionality test (create test folder first)
mkdir test_data && echo "test content" > test_data/test.txt
python inflate.py --method acs --compress test_data
python inflate.py --method acs --decompress compressed_*.acs test_output
```

### Debugging
```bash
# Check environment variables
python -c "from dotenv import load_dotenv; import os; load_dotenv(); print('SUPABASE_URL:', bool(os.getenv('SUPABASE_URL')))"

# Test Supabase connection
python -c "from dawnbond import DawnbondCloud; cloud = DawnbondCloud(); print('Cloud connection OK')"
```

## Known Issues & Architecture Notes

### Cloud Storage Design
- Uses Supabase with base64 encoding for binary file storage
- Generates 5-digit random retrieval codes with collision checking
- Files stored in `cbac` table with fields: `code`, `filename`, `file`

### File Processing
- Text files are read with `errors="ignore"` encoding handling
- Directory structure is flattened into filemap.txt with relative paths
- File contents concatenated into filecntt.txt with delimiter markers

### Virtual Environment Requirement
The application expects to run in a virtual environment and will show initialization errors if dependencies aren't properly installed in the venv.

## Development Guidelines

### Error Handling Patterns
The codebase uses a logging system with `log()`, `warn()`, and `err()` functions that prefix messages with `[INF]`, `[WRN]`, and `[ERR]` respectively.

### Cloud Operations
All cloud operations require valid Supabase credentials in `.env`. The DawnbondCloud class handles connection initialization and will raise exceptions on configuration problems.

### Archive Format
ACS files are standard 7z archives with .acs extension containing two files:
- `filemap.txt`: Directory structure and file paths
- `filecntt.txt`: Concatenated file contents with path delimiters
