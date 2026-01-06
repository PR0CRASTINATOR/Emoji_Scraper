# Emoji Scraper  
A Python tool that automatically downloads, parses, and merges the complete Unicode emoji set — always using the latest published Unicode Emoji version.

This script fetches all official emoji data files from the Unicode Consortium, extracts every emoji (including fully‑qualified, minimally‑qualified, unqualified, sequences, ZWJ sequences, and variation sequences), and produces a single merged output file.

## ✨ Features
- Automatically detects the latest Unicode Emoji version  
- Downloads all official emoji data files:
  - `emoji-test.txt`
  - `emoji-sequences.txt`
  - `emoji-zwj-sequences.txt`
  - `emoji-variation-sequences.txt`
- Extracts:
  - Fully‑qualified emoji  
  - Minimally‑qualified emoji  
  - Unqualified emoji  
  - Emoji sequences  
  - ZWJ sequences  
  - Variation sequences  
- Produces a unified file: `emoji_merged.txt`
- Future‑proof — works with all upcoming Unicode emoji releases

## 📦 Requirements
- Python 3.7+
- `requests` library

Install dependencies:

```bash
pip install requests
