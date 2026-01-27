# Blog Post Analysis

This repository now includes a comprehensive analysis tool for all blog posts on the website.

## Overview

The blog analysis script (`analyze_blog_posts.py`) automatically scans all markdown files in the `content/posts/` directory and generates detailed statistics about the blog content.

## Analysis Features

The script analyzes:

1. **Overall Statistics**
   - Total number of posts
   - Total word count
   - Total and average reading time
   - Average words per post

2. **Language Distribution**
   - Bilingual posts (Chinese + English)
   - Chinese-only posts
   - English-only posts

3. **Publication Timeline**
   - First and latest posts
   - Posts per year distribution

4. **Tag Analysis**
   - Total unique tags
   - Most common tags
   - Tag frequency distribution

5. **Individual Post Details**
   - Title, date, and filename
   - Tags associated with each post
   - Word count (separate counts for English and Chinese)
   - Estimated reading time

## Usage

Run the analysis script:

```bash
python3 analyze_blog_posts.py
```

## Output Files

The script generates three output files:

1. **`blog_analysis_report.txt`** - Human-readable text report with all statistics
2. **`blog_analysis_data.json`** - Machine-readable JSON data with detailed information about each post
3. Console output showing the full analysis report

## Current Blog Statistics

As of the last analysis:

- **Total Posts**: 5
- **Total Words**: 13,133
- **Total Reading Time**: ~45 minutes (0.7 hours)
- **Average Words per Post**: 2,627
- **Language**: All posts are bilingual (Chinese + English)
- **Date Range**: April 2023 - January 2026
- **Most Common Tags**: conference (2), misc (2)

## Posts Timeline

1. **Goshawk Tutorial for AsiaCCS** (Apr 2023) - bug detection, conference
2. **OSPP 2023: Optimizing LLVM InstCombine Pass** (Sep 2023) - llvm
3. **IntTracer for ICSE SRC** (Jan 2024) - integer overflow, conference
4. **2024 Annual Review** (Dec 2024) - misc
5. **2025 Spring Review** (Jan 2026) - misc

## Requirements

- Python 3.x
- Standard library modules only (no external dependencies)

## Notes

- The script handles both Chinese and English text
- Reading time is calculated based on:
  - 200 words per minute for English
  - 300 characters per minute for Chinese
- The analysis removes markdown syntax before counting words
- Code blocks, inline code, and images are excluded from word counts
