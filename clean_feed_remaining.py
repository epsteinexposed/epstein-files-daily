#!/usr/bin/env python3
"""Remove remaining fabricated articles from feed.xml"""

import re

with open('feed.xml', 'r', encoding='utf-8') as f:
    content = f.read()

# Articles to remove (partial URL matches)
articles_to_remove = [
    'martha-stewart',
    'kevin-spacey',
    'rupert-murdoch',
    'david-blaine',
    'woody-allen',
    'james-gorman',
    'glenn-dubin',
    'thomas-pritzker',
    'reid-hoffman',
    'ehud-barak',
    'leon-black'
]

for article in articles_to_remove:
    # Pattern to match the entire <item>...</item> block containing this article
    pattern = rf'<item>\s*<title>.*?</title>\s*<link>.*?{article}.*?</link>.*?</item>\s*'

    match = re.search(pattern, content, re.DOTALL)
    if match:
        content = content.replace(match.group(0), '')
        print(f"✓ Removed from feed: {article}")
    else:
        print(f"✗ Not found in feed: {article}")

with open('feed.xml', 'w', encoding='utf-8') as f:
    f.write(content)

print("\n" + "=" * 50)
print("Remaining fabricated articles removed from feed.xml")
