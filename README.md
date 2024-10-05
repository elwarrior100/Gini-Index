## Table of Contents
- [Features](#features)
- [Requirements](#requirements)
- [Installation](#installation)
- [Usage](#usage)
- [Running Tests](#running-tests)

## Features

- Scrapes ZIP files containing census data from the IBGE website.
- Processes the data and extracts Gini index values.
- Stores the extracted data in a SQLite database.
- Supports downloading and handling of files.

## Requirements

This project requires the following Python packages:

- `beautifulsoup4`
- `requests`
- `pandas`
- `openpyxl`
- `coverage`
- `sqlite3` (included with Python)

You can install the required packages using the provided `requirements.txt`.

## Installation

To install the project and its dependencies, follow these steps:

1. **Clone the repository**:

   ```bash
   git clone https://github.com/elwarrior100/Gini-Index.git
   cd Gini-Index


2. **Create a virtual environment (optional but recommended):**:

    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    pip install -r requirements.txt

## Usage

1. **Usage**:
    ```bash
    cd Gini-Index
    python -m src.main

2. **Docker**:
    ```bash
    cd Gini-Index
    docker build -t Gini-Index .
    docker run census-data-scraper


## Testing
1. **For Testing:**
    ```bash
    python -m unittest discover -s test -p "test_*.py"
    python -m coverage run -m unittest discover -s test -p "test_*.py"
    python -m coverage html  


    
