# Split big/long PDF files by page numbers

Actually, this script is not splitting the PDF file, but it is creating a new PDF file for every **``n``** pages of the original PDF file.

You can specify the number of pages per file in the script, lines 44-45:

```python
# split pdfs every n pages
PAGES_PER_PDF = 2
```

There is no log file written. But the script will print out the progress in the console.

## Usage

Install script:

```bash
git clone git@github.com:haenno/pdf-split.git
cd pdf-split
conda create --name pdf-split python=3.11
conda activate pdf-split
pip install -r requirements.txt
```

Important: Keep folder structure as is:

```bash
pdf-split.py
data/
  - input/
  - output/
  - error/
  - finished/
```

## First setup process

```bash
conda create --name pdf-split python=3.11
conda activate pdf-split
pip install pypdf
conda list -e > requirements.txt
```
