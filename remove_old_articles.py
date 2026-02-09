#!/usr/bin/env python3
"""Remove old 5 articles from the site"""

import os
import re

# Old articles to remove
old_articles = [
    {
        'slug': 'musk-epstein-emails',
        'thumb': 'images/musk-email.png',
        'data_tag': 'elon musk',
    },
    {
        'slug': 'bannon-epstein-texts',
        'thumb': 'images/bannon-texts.png',
        'data_tag': 'steve bannon',
    },
    {
        'slug': 'lutnick-yacht-island',
        'thumb': 'images/lutnick-email.png',
        'data_tag': 'howard lutnick',
    },
    {
        'slug': 'prince-andrew-dinner',
        'thumb': 'images/andrew-dinner.png',
        'data_tag': 'prince andrew',
    },
    {
        'slug': 'clinton-plane-trips',
        'thumb': 'images/clinton-flights.png',
        'data_tag': 'bill clinton',
    },
]

# 1. Delete HTML files
print("Deleting article HTML files...")
for article in old_articles:
    filepath = f"{article['slug']}.html"
    if os.path.exists(filepath):
        os.remove(filepath)
        print(f"  ✓ Deleted {filepath}")
    else:
        print(f"  - {filepath} not found")

# 2. Delete thumbnail images
print("\nDeleting thumbnail images...")
for article in old_articles:
    if os.path.exists(article['thumb']):
        os.remove(article['thumb'])
        print(f"  ✓ Deleted {article['thumb']}")
    else:
        print(f"  - {article['thumb']} not found")

# 3. Remove from index.html
print("\nUpdating index.html...")
with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Remove article blocks - they start with <!-- ARTICLE PREVIEW and end with </article>
for article in old_articles:
    # Pattern to match the article block
    pattern = rf'<!-- ARTICLE PREVIEW \d+:.*?data-tags="{article["data_tag"]}[^"]*".*?</article>\s*'
    content = re.sub(pattern, '', content, flags=re.DOTALL)

# Also update trending buttons to remove old names
content = re.sub(r'<button class="trending-name" data-name="elon musk">MUSK</button>\s*', '', content)
content = re.sub(r'<button class="trending-name" data-name="bill clinton">CLINTON</button>\s*', '', content)
content = re.sub(r'<button class="trending-name" data-name="prince andrew">PRINCE ANDREW</button>\s*', '', content)
content = re.sub(r'<button class="trending-name" data-name="steve bannon">BANNON</button>\s*', '', content)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)
print("  ✓ Removed old article cards from index.html")

# 4. Remove from feed.xml
print("\nUpdating feed.xml...")
with open('feed.xml', 'r', encoding='utf-8') as f:
    feed_content = f.read()

for article in old_articles:
    # Pattern to match the feed item
    pattern = rf'<item>\s*<title>.*?</title>\s*<link>https://epstein-exposed\.com/{article["slug"]}</link>.*?</item>\s*'
    feed_content = re.sub(pattern, '', feed_content, flags=re.DOTALL)

with open('feed.xml', 'w', encoding='utf-8') as f:
    f.write(feed_content)
print("  ✓ Removed old entries from feed.xml")

print("\n" + "=" * 50)
print("Old articles removed successfully!")
print(f"Removed {len(old_articles)} articles from the site.")
