#!/usr/bin/env python3
"""Add new article cards to index.html and update feed.xml"""

import re
from datetime import datetime

# New article data
new_articles = [
    {
        'slug': 'richard-branson-harem',
        'title': '"Bring Your Harem!": Richard Branson\'s Emails to Epstein Exposed',
        'lede': 'Virgin billionaire invited Jeffrey Epstein to his private island with a shocking request—and offered PR advice on how to spin his crimes.',
        'date': '2026-02-03',
        'date_display': 'February 3, 2026',
        'tags': ['Richard Branson', 'Bill Gates'],
        'data_tags': 'richard branson,bill gates',
        'thumb': 'images/branson-thumb.png',
        'alt': 'Richard Branson emails to Epstein',
        'reading_time': '4 min read',
    },
    {
        'slug': 'sergey-brin-google-maxwell',
        'title': 'Google\'s Founders and Ghislaine Maxwell: The Dinner Invitations They Can\'t Explain',
        'lede': 'Sergey Brin offered to bring Eric Schmidt to Epstein\'s townhouse. Maxwell called it "happily casual and relaxed." New documents reveal Google\'s uncomfortable Epstein connection.',
        'date': '2026-02-04',
        'date_display': 'February 4, 2026',
        'tags': ['Sergey Brin', 'Google', 'Ghislaine Maxwell'],
        'data_tags': 'sergey brin,google,ghislaine maxwell',
        'thumb': 'images/brin-thumb.png',
        'alt': 'Google founders Epstein connection',
        'reading_time': '5 min read',
    },
    {
        'slug': 'peter-thiel-thousands-documents',
        'title': 'Peter Thiel Appears in Thousands of Epstein Documents: Lunches, Investments, and a Michelin-Star Buyout',
        'lede': 'The PayPal co-founder\'s name appears thousands of times in the DOJ release. Documents reveal years of lunch meetings, a $40 million investment connection, and an exclusive Palo Alto dinner.',
        'date': '2026-02-05',
        'date_display': 'February 5, 2026',
        'tags': ['Peter Thiel', 'Silicon Valley'],
        'data_tags': 'peter thiel,silicon valley',
        'thumb': 'images/thiel-thumb.png',
        'alt': 'Peter Thiel Epstein documents',
        'reading_time': '4 min read',
    },
    {
        'slug': 'josh-harris-gates-breakfast',
        'title': 'NFL Owner Josh Harris Confirmed at Epstein\'s "Intimate" Bill Gates Breakfast',
        'lede': 'New emails show the billionaire sports owner attended a private breakfast with Bill Gates at Epstein\'s Manhattan home. "Yes very much. Thank you for inviting me."',
        'date': '2026-02-06',
        'date_display': 'February 6, 2026',
        'tags': ['Josh Harris', 'Bill Gates'],
        'data_tags': 'josh harris,bill gates',
        'thumb': 'images/harris-thumb.png',
        'alt': 'Josh Harris Bill Gates Epstein breakfast',
        'reading_time': '4 min read',
    },
    {
        'slug': 'dr-oz-epstein-travel',
        'title': 'Epstein Paid for Dr. Oz\'s Travel in 2004, Files Reveal',
        'lede': 'A transaction report shows Jeffrey Epstein paid $1,592 for the celebrity doctor\'s travel. Oz now runs Medicare and Medicaid Services under the Trump administration.',
        'date': '2026-02-07',
        'date_display': 'February 7, 2026',
        'tags': ['Dr. Oz', 'Trump Admin'],
        'data_tags': 'dr oz,trump',
        'thumb': 'images/oz-thumb.png',
        'alt': 'Dr Oz Epstein travel payment',
        'reading_time': '3 min read',
    },
]

def generate_article_card(article):
    """Generate HTML for an article card"""
    tags_html = '\n                                    '.join([
        f'<a href="?search={tag.lower().replace(" ", "+")}" class="article-tag">{tag}</a>'
        for tag in article['tags']
    ])

    return f'''
                <!-- AUTO-GENERATED ARTICLE: {article['tags'][0].upper()} -->
                <article class="article-preview featured" data-tags="{article['data_tags']}">
                    <div class="article-top">
                        <a href="{article['slug']}.html" class="article-thumb">
                            <img src="{article['thumb']}" alt="{article['alt']}" loading="lazy">
                        </a>
                        <div class="article-title-section">
                            <div class="article-meta">
                                <div class="article-tags">
                                    {tags_html}
                                </div>
                                <time datetime="{article['date']}" class="article-date">{article['date_display']}</time>
                                <span class="reading-time">· {article['reading_time']}</span>
                            </div>
                            <h2><a href="{article['slug']}.html">{article['title']}</a></h2>
                            <p class="lede">{article['lede']}</p>
                            <a href="{article['slug']}.html" class="read-more">Read full article</a>
                        </div>
                    </div>
                </article>
'''

def generate_feed_item(article):
    """Generate RSS item for an article"""
    return f'''
    <item>
      <title>{article['title'].replace("&", "&amp;").replace('"', '&quot;')}</title>
      <link>https://epstein-exposed.com/{article['slug']}</link>
      <guid>https://epstein-exposed.com/{article['slug']}</guid>
      <pubDate>{datetime.strptime(article['date'], '%Y-%m-%d').strftime('%a, %d %b %Y 12:00:00 GMT')}</pubDate>
      <description>{article['lede'].replace("&", "&amp;").replace('"', '&quot;')}</description>
    </item>
'''

# Read index.html
with open('index.html', 'r', encoding='utf-8') as f:
    index_content = f.read()

# Find the position to insert new articles (before </div> that closes #articles-container)
# Look for the Clinton article's closing tag, then insert after it
insert_marker = '''                </article>
            </div>

            <div class="no-results"'''

new_articles_html = ''
for article in new_articles:
    new_articles_html += generate_article_card(article)

# Replace the marker with the marker + new articles
new_index_content = index_content.replace(
    insert_marker,
    f'''                </article>
{new_articles_html}
            </div>

            <div class="no-results"'''
)

# Write updated index.html
with open('index.html', 'w', encoding='utf-8') as f:
    f.write(new_index_content)

print("✓ Updated index.html with new article cards")

# Read feed.xml
with open('feed.xml', 'r', encoding='utf-8') as f:
    feed_content = f.read()

# Generate new feed items
new_feed_items = ''
for article in new_articles:
    new_feed_items += generate_feed_item(article)

# Insert new items after the opening <channel> section, before existing items
# Find the position after <atom:link> line
insert_position = feed_content.find('<item>')
if insert_position != -1:
    new_feed_content = feed_content[:insert_position] + new_feed_items.strip() + '\n\n    ' + feed_content[insert_position:]
else:
    # If no items exist, insert before </channel>
    new_feed_content = feed_content.replace('</channel>', new_feed_items + '\n  </channel>')

# Write updated feed.xml
with open('feed.xml', 'w', encoding='utf-8') as f:
    f.write(new_feed_content)

print("✓ Updated feed.xml with new entries")
print("\n" + "=" * 50)
print(f"Added {len(new_articles)} new articles to the site!")
