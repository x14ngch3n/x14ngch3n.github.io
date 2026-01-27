#!/usr/bin/env python3
"""
Blog Post Analysis Script
Analyzes all blog posts in the Hugo site and generates statistics.
"""

import os
import re
import json
from pathlib import Path
from datetime import datetime
from collections import Counter, defaultdict
import unicodedata


def is_chinese(char):
    """Check if a character is Chinese."""
    return 'CJK' in unicodedata.name(char, '')


def count_words(text):
    """Count words in text, handling both English and Chinese."""
    # Remove markdown syntax
    text = re.sub(r'```[\s\S]*?```', '', text)  # Remove code blocks
    text = re.sub(r'`[^`]*`', '', text)  # Remove inline code
    text = re.sub(r'!\[.*?\]\(.*?\)', '', text)  # Remove images
    text = re.sub(r'\[.*?\]\(.*?\)', '', text)  # Remove links
    text = re.sub(r'[#*_~\[\]()]', '', text)  # Remove markdown symbols
    
    chinese_chars = sum(1 for char in text if is_chinese(char))
    english_words = len(re.findall(r'\b[a-zA-Z]+\b', text))
    
    return {
        'chinese_chars': chinese_chars,
        'english_words': english_words,
        'total': chinese_chars + english_words
    }


def parse_frontmatter(content):
    """Parse TOML frontmatter from markdown file."""
    match = re.match(r'\+\+\+(.*?)\+\+\+', content, re.DOTALL)
    if not match:
        return {}
    
    frontmatter_text = match.group(1)
    metadata = {}
    
    # Parse date
    date_match = re.search(r"date\s*=\s*['\"]([^'\"]+)['\"]", frontmatter_text)
    if date_match:
        metadata['date'] = date_match.group(1)
    
    # Parse title
    title_match = re.search(r"title\s*=\s*['\"]([^'\"]+)['\"]", frontmatter_text)
    if title_match:
        metadata['title'] = title_match.group(1)
    
    # Parse tags
    tags_match = re.search(r"tags\s*=\s*\[(.*?)\]", frontmatter_text)
    if tags_match:
        tags_str = tags_match.group(1)
        metadata['tags'] = [tag.strip().strip("'\"") for tag in tags_str.split(',')]
    else:
        metadata['tags'] = []
    
    # Parse type
    type_match = re.search(r"type\s*=\s*['\"]([^'\"]+)['\"]", frontmatter_text)
    if type_match:
        metadata['type'] = type_match.group(1)
    
    return metadata


def analyze_post(filepath):
    """Analyze a single blog post."""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    metadata = parse_frontmatter(content)
    
    # Remove frontmatter for content analysis
    content_without_frontmatter = re.sub(r'\+\+\+.*?\+\+\+', '', content, count=1, flags=re.DOTALL)
    
    word_stats = count_words(content_without_frontmatter)
    
    # Calculate reading time (assuming 200 words per minute for English, 300 chars per minute for Chinese)
    reading_time_en = word_stats['english_words'] / 200
    reading_time_zh = word_stats['chinese_chars'] / 300
    reading_time = max(reading_time_en + reading_time_zh, 1)  # At least 1 minute
    
    return {
        'filename': filepath.name,
        'title': metadata.get('title', 'Untitled'),
        'date': metadata.get('date', 'Unknown'),
        'tags': metadata.get('tags', []),
        'type': metadata.get('type', 'post'),
        'word_count': word_stats,
        'reading_time_minutes': round(reading_time, 1),
        'has_chinese': word_stats['chinese_chars'] > 0,
        'has_english': word_stats['english_words'] > 0,
    }


def generate_analysis_report(posts):
    """Generate a comprehensive analysis report."""
    report = []
    report.append("=" * 80)
    report.append("BLOG POST ANALYSIS REPORT")
    report.append("=" * 80)
    report.append("")
    
    # Overall statistics
    report.append("## OVERALL STATISTICS")
    report.append("-" * 80)
    report.append(f"Total number of posts: {len(posts)}")
    
    total_words = sum(p['word_count']['total'] for p in posts)
    total_reading_time = sum(p['reading_time_minutes'] for p in posts)
    
    report.append(f"Total word count: {total_words:,}")
    report.append(f"Total reading time: {total_reading_time:.1f} minutes ({total_reading_time/60:.1f} hours)")
    report.append(f"Average words per post: {total_words/len(posts):.0f}")
    report.append(f"Average reading time per post: {total_reading_time/len(posts):.1f} minutes")
    report.append("")
    
    # Language distribution
    report.append("## LANGUAGE DISTRIBUTION")
    report.append("-" * 80)
    bilingual_posts = sum(1 for p in posts if p['has_chinese'] and p['has_english'])
    chinese_only = sum(1 for p in posts if p['has_chinese'] and not p['has_english'])
    english_only = sum(1 for p in posts if p['has_english'] and not p['has_chinese'])
    
    report.append(f"Bilingual posts (Chinese + English): {bilingual_posts}")
    report.append(f"Chinese-only posts: {chinese_only}")
    report.append(f"English-only posts: {english_only}")
    report.append("")
    
    # Date analysis
    report.append("## PUBLICATION TIMELINE")
    report.append("-" * 80)
    
    # Sort posts by date
    dated_posts = [p for p in posts if p['date'] != 'Unknown']
    dated_posts.sort(key=lambda x: x['date'])
    
    if dated_posts:
        report.append(f"First post: {dated_posts[0]['title']} ({dated_posts[0]['date'][:10]})")
        report.append(f"Latest post: {dated_posts[-1]['title']} ({dated_posts[-1]['date'][:10]})")
        
        # Year distribution
        year_counts = Counter(p['date'][:4] for p in dated_posts)
        report.append("\nPosts per year:")
        for year in sorted(year_counts.keys()):
            report.append(f"  {year}: {year_counts[year]} posts")
    report.append("")
    
    # Tag analysis
    report.append("## TAG ANALYSIS")
    report.append("-" * 80)
    
    all_tags = []
    for post in posts:
        all_tags.extend(post['tags'])
    
    tag_counts = Counter(all_tags)
    report.append(f"Total unique tags: {len(tag_counts)}")
    report.append("\nMost common tags:")
    for tag, count in tag_counts.most_common(10):
        report.append(f"  {tag}: {count} posts")
    report.append("")
    
    # Individual post details
    report.append("## INDIVIDUAL POST DETAILS")
    report.append("-" * 80)
    
    # Sort by date (newest first)
    sorted_posts = sorted(posts, key=lambda x: x['date'], reverse=True)
    
    for i, post in enumerate(sorted_posts, 1):
        report.append(f"\n{i}. {post['title']}")
        report.append(f"   Date: {post['date'][:10]}")
        report.append(f"   File: {post['filename']}")
        report.append(f"   Tags: {', '.join(post['tags']) if post['tags'] else 'None'}")
        report.append(f"   Word count: {post['word_count']['total']:,} " +
                     f"(EN: {post['word_count']['english_words']}, ZH: {post['word_count']['chinese_chars']})")
        report.append(f"   Reading time: {post['reading_time_minutes']} minutes")
    
    report.append("")
    report.append("=" * 80)
    report.append("END OF REPORT")
    report.append("=" * 80)
    
    return "\n".join(report)


def main():
    """Main function to analyze all blog posts."""
    # Find all blog posts
    posts_dir = Path('/home/runner/work/x14ngch3n.github.io/x14ngch3n.github.io/content/posts')
    
    if not posts_dir.exists():
        print(f"Error: Posts directory not found at {posts_dir}")
        return
    
    # Get all markdown files
    post_files = list(posts_dir.glob('*.md'))
    
    if not post_files:
        print("No blog posts found!")
        return
    
    print(f"Found {len(post_files)} blog post(s). Analyzing...\n")
    
    # Analyze each post
    posts_data = []
    for post_file in post_files:
        try:
            post_data = analyze_post(post_file)
            posts_data.append(post_data)
            print(f"✓ Analyzed: {post_data['title']}")
        except Exception as e:
            print(f"✗ Error analyzing {post_file.name}: {e}")
    
    print(f"\nSuccessfully analyzed {len(posts_data)} posts.\n")
    
    # Generate report
    report = generate_analysis_report(posts_data)
    
    # Save report to file
    report_file = Path('/home/runner/work/x14ngch3n.github.io/x14ngch3n.github.io/blog_analysis_report.txt')
    with open(report_file, 'w', encoding='utf-8') as f:
        f.write(report)
    
    print(report)
    print(f"\nReport saved to: {report_file}")
    
    # Also save JSON data for potential further analysis
    json_file = Path('/home/runner/work/x14ngch3n.github.io/x14ngch3n.github.io/blog_analysis_data.json')
    with open(json_file, 'w', encoding='utf-8') as f:
        json.dump(posts_data, f, indent=2, ensure_ascii=False)
    
    print(f"JSON data saved to: {json_file}")


if __name__ == "__main__":
    main()
