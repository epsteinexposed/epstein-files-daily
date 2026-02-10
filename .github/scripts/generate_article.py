#!/usr/bin/env python3
"""
Daily Roundup Generator for Epstein Files Daily
Fetches real news from Google News RSS, then uses Claude to format the roundup.
"""

import os
import json
import re
import random
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from datetime import datetime, timedelta
from anthropic import Anthropic
from PIL import Image, ImageDraw, ImageFont, ImageFilter

# Initialize Anthropic client
client = Anthropic()

def read_file(path):
    """Read a file and return its contents."""
    with open(path, 'r', encoding='utf-8') as f:
        return f.read()

def write_file(path, content):
    """Write content to a file."""
    os.makedirs(os.path.dirname(path) if os.path.dirname(path) else '.', exist_ok=True)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)

def get_existing_roundups():
    """Get list of existing daily roundup files."""
    roundups = []
    for f in os.listdir('.'):
        if f.startswith('daily-') and f.endswith('.html'):
            roundups.append(f)
    return roundups

def fetch_news_from_rss():
    """Fetch recent Epstein-related news from Google News RSS."""

    # Multiple search queries to get diverse results
    queries = [
        "epstein+documents+release",
        "epstein+files+DOJ",
        "jeffrey+epstein+investigation",
        "epstein+connections+revealed"
    ]

    all_articles = []
    seen_titles = set()

    for query in queries:
        url = f"https://news.google.com/rss/search?q={query}&hl=en-US&gl=US&ceid=US:en"

        try:
            print(f"Fetching: {url}")
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req, timeout=30) as response:
                xml_data = response.read().decode('utf-8')

            root = ET.fromstring(xml_data)

            # Find all items in the RSS feed
            for item in root.findall('.//item'):
                title = item.find('title')
                link = item.find('link')
                pub_date = item.find('pubDate')
                source = item.find('source')

                if title is not None and link is not None:
                    title_text = title.text or ""

                    # Skip if we've seen this title
                    if title_text.lower() in seen_titles:
                        continue
                    seen_titles.add(title_text.lower())

                    article = {
                        'title': title_text,
                        'url': link.text or "",
                        'source': source.text if source is not None else "News",
                        'date': pub_date.text if pub_date is not None else ""
                    }
                    all_articles.append(article)

        except Exception as e:
            print(f"Error fetching {query}: {e}")
            continue

    # Filter for recent articles (last 7 days) and relevance
    recent_articles = []
    cutoff = datetime.now() - timedelta(days=7)

    for article in all_articles:
        # Check if title contains relevant keywords
        title_lower = article['title'].lower()
        if any(kw in title_lower for kw in ['epstein', 'ghislaine', 'maxwell', 'doj', 'documents']):
            recent_articles.append(article)

    print(f"Found {len(recent_articles)} relevant articles")
    return recent_articles[:15]  # Return top 15

def generate_thumbnail(date_str, headline, filename):
    """Generate newspaper-style thumbnail with paper texture."""

    WIDTH = 840
    HEIGHT = 472

    # Create aged paper background
    img = Image.new('RGB', (WIDTH, HEIGHT), '#f4ead5')
    draw = ImageDraw.Draw(img)
    pixels = img.load()

    # Add paper texture - noise
    for y in range(HEIGHT):
        for x in range(WIDTH):
            r, g, b = pixels[x, y]
            noise = random.randint(-8, 8)
            edge_dist = min(x, WIDTH-x, y, HEIGHT-y)
            edge_darken = max(0, 15 - edge_dist // 8)
            r = max(0, min(255, r + noise - edge_darken))
            g = max(0, min(255, g + noise - edge_darken - 3))
            b = max(0, min(255, b + noise - edge_darken - 8))
            pixels[x, y] = (r, g, b)

    # Add vignette
    for y in range(HEIGHT):
        for x in range(WIDTH):
            r, g, b = pixels[x, y]
            cx, cy = WIDTH // 2, HEIGHT // 2
            dist = ((x - cx) ** 2 + (y - cy) ** 2) ** 0.5
            max_dist = ((cx) ** 2 + (cy) ** 2) ** 0.5
            vignette = 1 - (dist / max_dist) * 0.15
            pixels[x, y] = (int(r * vignette), int(g * vignette), int(b * vignette))

    draw = ImageDraw.Draw(img)
    ink = '#1a1816'
    ink_light = '#4a4540'

    # Try to load fonts
    try:
        font_masthead = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf", 52)
        font_tagline = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSerif-Italic.ttf", 15)
        font_dateline = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf", 12)
        font_headline = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf", 52)
    except:
        font_masthead = ImageFont.load_default()
        font_tagline = ImageFont.load_default()
        font_dateline = ImageFont.load_default()
        font_headline = ImageFont.load_default()

    # Border
    draw.rectangle([(8, 8), (WIDTH-9, HEIGHT-9)], outline='#c4b89c', width=1)

    # Masthead
    masthead_text = "EPSTEIN FILES DAILY"
    bbox = draw.textbbox((0, 0), masthead_text, font=font_masthead)
    text_width = bbox[2] - bbox[0]
    draw.text(((WIDTH - text_width) / 2, 28), masthead_text, fill=ink, font=font_masthead)

    # Tagline
    tagline_text = "Comprehensive Coverage of the DOJ Document Releases"
    bbox = draw.textbbox((0, 0), tagline_text, font=font_tagline)
    text_width = bbox[2] - bbox[0]
    draw.text(((WIDTH - text_width) / 2, 90), tagline_text, fill=ink_light, font=font_tagline)

    # Line
    draw.line([(50, 118), (WIDTH - 50, 118)], fill=ink, width=1)

    # Date bar
    vol_num = len(get_existing_roundups()) + 1
    vol_text = f"Vol. I, No. {vol_num}"
    draw.text((60, 128), vol_text, fill=ink_light, font=font_dateline)
    bbox = draw.textbbox((0, 0), date_str, font=font_dateline)
    text_width = bbox[2] - bbox[0]
    draw.text((WIDTH - text_width - 60, 128), date_str, fill=ink_light, font=font_dateline)

    # Double line
    draw.line([(50, 152), (WIDTH - 50, 152)], fill=ink, width=1)
    draw.line([(50, 156), (WIDTH - 50, 156)], fill=ink, width=2)

    # Headline (split into lines)
    words = headline.split()
    lines = []
    current_line = []
    for word in words:
        test_line = ' '.join(current_line + [word])
        bbox = draw.textbbox((0, 0), test_line, font=font_headline)
        if bbox[2] - bbox[0] > WIDTH - 100:
            if current_line:
                lines.append(' '.join(current_line))
                current_line = [word]
            else:
                lines.append(word)
                current_line = []
        else:
            current_line.append(word)
    if current_line:
        lines.append(' '.join(current_line))

    # Draw headline centered
    y_start = 190
    line_height = 70
    for i, line in enumerate(lines[:3]):  # Max 3 lines
        bbox = draw.textbbox((0, 0), line, font=font_headline)
        text_width = bbox[2] - bbox[0]
        draw.text(((WIDTH - text_width) / 2, y_start + i * line_height), line, fill=ink, font=font_headline)

    # Slight blur
    img = img.filter(ImageFilter.GaussianBlur(radius=0.3))

    # Save
    os.makedirs('images', exist_ok=True)
    img.save(filename, 'PNG')
    print(f"Created thumbnail: {filename}")

def generate_roundup(articles):
    """Use Claude to format the fetched news into a roundup."""

    if not articles or len(articles) < 3:
        print("Not enough articles to create a roundup")
        return None

    today = datetime.now()
    day_name = today.strftime('%A')

    # Format articles for Claude
    articles_text = "\n".join([
        f"- Title: {a['title']}\n  Source: {a['source']}\n  URL: {a['url']}"
        for a in articles
    ])

    prompt = f"""You are a news editor for Epstein Files Daily. I have gathered the following recent news articles about the Epstein case:

{articles_text}

TODAY'S DATE: {day_name}, {today.strftime('%B %d, %Y')}

Create a daily news roundup from these articles. Select the 4-6 most significant stories and format them.

OUTPUT FORMAT - Return ONLY a JSON object (no markdown):
{{
    "theme_headline": "Short punchy headline summarizing today's biggest story (max 8 words)",
    "names": ["Full Name 1", "Full Name 2"],
    "bullets_short": [
        {{"name": "Subject/Person", "text": "one line summary of the news.", "source": "Source Name", "url": "actual url from above"}}
    ],
    "bullets_long": [
        {{"name": "Subject/Person", "text": "2-4 sentence detailed summary with context and significance.", "source": "Source Name", "url": "actual url from above"}}
    ]
}}

RULES:
1. bullets_short: ONE sentence each, very concise
2. bullets_long: 2-4 sentences each with full context
3. Use the ACTUAL URLs from the articles I provided
4. names: only full person names mentioned (for tags)
5. Pick 4-6 of the most newsworthy stories
6. theme_headline should be compelling and specific

Return ONLY the JSON, no other text."""

    print("Calling Claude API to format roundup...")

    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=4000,
        messages=[
            {"role": "user", "content": prompt}
        ]
    )

    response_text = response.content[0].text

    # Parse JSON
    json_match = re.search(r'```json\s*(.*?)\s*```', response_text, re.DOTALL)
    if json_match:
        json_str = json_match.group(1)
    else:
        json_match = re.search(r'\{.*\}', response_text, re.DOTALL)
        if json_match:
            json_str = json_match.group(0)
        else:
            print("ERROR: Could not find JSON in response")
            print("Response was:", response_text[:500])
            return None

    try:
        data = json.loads(json_str)
    except json.JSONDecodeError as e:
        print(f"ERROR: Could not parse JSON: {e}")
        print("JSON string was:", json_str[:500])
        return None

    return data

def create_article_html(data, today):
    """Create the full article page HTML."""

    date_iso = today.strftime('%Y-%m-%d')
    date_readable = today.strftime('%B %d, %Y')
    month_day = today.strftime('%B %d').replace(' 0', ' ')
    day_name = today.strftime('%A')
    filename = f"daily-{today.strftime('%b').lower()}-{today.day}-{today.year}"

    # Build bullets HTML for article page (long version)
    bullets_html = ""
    for bullet in data['bullets_long']:
        bullets_html += f'''
                <li><strong>{bullet['name']}</strong> {bullet['text']} <a href="{bullet['url']}" target="_blank" class="source-link">{bullet['source']} →</a></li>
'''

    # Build tags HTML
    tags_html = ""
    for name in data.get('names', [])[:4]:
        name_param = urllib.parse.quote_plus(name.lower())
        tags_html += f'                    <a href="index.html?search={name_param}" class="article-tag">{name}</a>\n'

    # URL encode for share buttons
    url = f"https://epsteinfilesdaily.com/{filename}"
    url_encoded = urllib.parse.quote(url, safe='')
    headline = f"{month_day}: {data['theme_headline']}"
    headline_encoded = urllib.parse.quote(headline, safe='')

    # Read template from existing article
    template = read_file('daily-feb-9-2026.html')

    html = template

    # Update title
    html = re.sub(r'<title>.*?</title>', f'<title>{month_day}: {data["theme_headline"]} — Epstein Files Daily</title>', html)

    # Update meta description
    first_bullet = data['bullets_short'][0]
    meta_desc = f"{first_bullet['name']} {first_bullet['text'][:100]}..."
    html = re.sub(r'<meta name="description" content=".*?">', f'<meta name="description" content="{meta_desc}">', html)

    # Update article content
    html = re.sub(r'<time datetime=".*?">', f'<time datetime="{date_iso}">', html)
    html = re.sub(r'>\w+ \d+, 2026</time>', f'>{date_readable}</time>', html)

    # Update h1
    html = re.sub(r'<h1>.*?</h1>', f'<h1>{month_day}: {data["theme_headline"]}</h1>', html)

    # Update tags
    if tags_html:
        tags_section = '<div class="article-tags">\n' + tags_html + '                </div>'
        html = re.sub(r'<div class="article-tags">.*?</div>', tags_section, html, flags=re.DOTALL)

    # Update bullets
    bullets_section = f'<ul class="lede-bullets">{bullets_html}            </ul>'
    html = re.sub(r'<ul class="lede-bullets">.*?</ul>', bullets_section, html, flags=re.DOTALL)

    # Update share links
    html = re.sub(r'daily-feb-9-2026', filename, html)

    return html

def update_index_html(data, today):
    """Add the new roundup card to index.html."""

    date_iso = today.strftime('%Y-%m-%d')
    date_readable = today.strftime('%B %d, %Y')
    month_day = today.strftime('%B %d').replace(' 0', ' ')
    filename = f"daily-{today.strftime('%b').lower()}-{today.day}-{today.year}"

    # Build short bullets HTML
    bullets_html = ""
    for bullet in data['bullets_short'][:4]:
        bullets_html += f'                                <li><strong>{bullet["name"]}</strong> {bullet["text"]} <a href="{bullet["url"]}" target="_blank" class="source-link">{bullet["source"]} →</a></li>\n'

    # Build tags
    names = data.get('names', [])[:4]
    tags_data = ','.join([name.lower() for name in names])
    tags_html = ""
    for name in names:
        name_param = urllib.parse.quote_plus(name.lower())
        tags_html += f'                                    <a href="index.html?search={name_param}" class="article-tag">{name}</a>\n'

    # Get current thumbnail version
    existing_roundups = get_existing_roundups()
    thumb_version = len(existing_roundups) + 1

    new_card = f'''
                <!-- DAILY ROUNDUP: {date_readable} -->
                <article class="article-preview featured" data-tags="{tags_data}">
                    <div class="article-top">
                        <a href="{filename}.html" class="article-thumb">
                            <img src="images/{filename}.png?v={thumb_version}" alt="{date_readable} Epstein news roundup" loading="lazy">
                        </a>
                        <div class="article-title-section">
                            <div class="article-meta">
                                <div class="article-tags">
{tags_html}                                </div>
                                <time datetime="{date_iso}" class="article-date">{date_readable}</time>
                            </div>
                            <h2><a href="{filename}.html">{month_day}: Read Daily Summary →</a></h2>
                            <ul class="lede-bullets">
{bullets_html}                            </ul>
                        </div>
                    </div>
                </article>
'''

    index_content = read_file('index.html')

    # Insert after articles-container opening
    marker = '<div id="articles-container">'
    if marker in index_content:
        index_content = index_content.replace(marker, marker + new_card)
        write_file('index.html', index_content)
        print("Updated index.html with new roundup card")
    else:
        print("WARNING: Could not find articles-container in index.html")

def update_feed_xml(data, today):
    """Add the new roundup to RSS feed."""

    try:
        feed_content = read_file('feed.xml')
    except FileNotFoundError:
        print("WARNING: feed.xml not found, skipping RSS update")
        return

    month_day = today.strftime('%B %d').replace(' 0', ' ')
    filename = f"daily-{today.strftime('%b').lower()}-{today.day}-{today.year}"
    url = f"https://epsteinfilesdaily.com/{filename}.html"
    pub_date = today.strftime('%a, %d %b %Y %H:%M:%S +0000')
    headline = f"{month_day}: {data['theme_headline']}"

    first_bullet = data['bullets_short'][0]
    description = f"{first_bullet['name']} {first_bullet['text']}"

    new_item = f'''
    <item>
      <title>{headline}</title>
      <link>{url}</link>
      <guid>{url}</guid>
      <pubDate>{pub_date}</pubDate>
      <description>{description}</description>
    </item>'''

    marker = '</language>'
    if marker in feed_content:
        feed_content = feed_content.replace(marker, marker + new_item)
        write_file('feed.xml', feed_content)
        print("Updated feed.xml")
    else:
        print("WARNING: Could not find insertion point in feed.xml")

def main():
    print("=" * 50)
    print("EPSTEIN FILES DAILY - Daily Roundup Generator")
    print("=" * 50)

    today = datetime.now()
    day_name = today.strftime('%A')
    date_str = f"{day_name}, {today.strftime('%B')} {today.day}, {today.year}"
    filename_base = f"daily-{today.strftime('%b').lower()}-{today.day}-{today.year}"

    print(f"\nGenerating roundup for: {date_str}")

    # Check if already generated today
    if f"{filename_base}.html" in get_existing_roundups():
        print(f"Roundup for today already exists: {filename_base}.html")
        return

    # Fetch real news from RSS
    print("\n--- FETCHING NEWS ---")
    articles = fetch_news_from_rss()

    if not articles:
        print("ERROR: Could not fetch any news articles")
        return

    print(f"Fetched {len(articles)} articles")
    for i, a in enumerate(articles[:5]):
        print(f"  {i+1}. {a['title'][:60]}... ({a['source']})")

    # Generate roundup content using Claude
    print("\n--- GENERATING ROUNDUP ---")
    roundup_data = generate_roundup(articles)

    if not roundup_data:
        print("No roundup generated")
        return

    print(f"\nTheme: {roundup_data['theme_headline']}")
    print(f"Names: {', '.join(roundup_data.get('names', []))}")
    print(f"Bullets: {len(roundup_data.get('bullets_short', []))}")

    # Generate thumbnail
    thumb_filename = f"images/{filename_base}.png"
    generate_thumbnail(date_str, roundup_data['theme_headline'], thumb_filename)

    # Create article HTML
    article_html = create_article_html(roundup_data, today)
    write_file(f"{filename_base}.html", article_html)
    print(f"Created: {filename_base}.html")

    # Update index.html
    update_index_html(roundup_data, today)

    # Update RSS feed
    update_feed_xml(roundup_data, today)

    # Save info for workflow
    latest_info = {
        "headline": f"{today.strftime('%B')} {today.day}: {roundup_data['theme_headline']}",
        "slug": filename_base,
        "date": today.strftime('%Y-%m-%d')
    }
    write_file('latest_article.json', json.dumps(latest_info))

    print("\n" + "=" * 50)
    print("✅ ROUNDUP GENERATED SUCCESSFULLY")
    print("=" * 50)

if __name__ == "__main__":
    main()
