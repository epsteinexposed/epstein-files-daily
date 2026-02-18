#!/usr/bin/env python3
"""
Daily Roundup Generator for Epstein Files Daily

CRITICAL: The Claude API CANNOT search the web.
This script MUST fetch news from Google News RSS first,
then pass the articles to Claude for formatting.

DO NOT change this to ask Claude to "search for news" - it will fail.
"""

import os
import json
import re
import random
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from datetime import datetime, timedelta
from email.utils import parsedate_to_datetime
from anthropic import Anthropic
from PIL import Image, ImageDraw, ImageFont, ImageFilter

client = Anthropic()

def read_file(path):
    with open(path, 'r', encoding='utf-8') as f:
        return f.read()

def write_file(path, content):
    os.makedirs(os.path.dirname(path) if os.path.dirname(path) else '.', exist_ok=True)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)

def get_existing_roundups():
    roundups = []
    for f in os.listdir('.'):
        if f.startswith('daily-') and f.endswith('.html'):
            roundups.append(f)
    return roundups

def fetch_news_from_rss():
    """Fetch news from Google News RSS - Claude API cannot search the web."""
    queries = [
        # Specific individuals - cast a wide net for lesser-known stories
        "epstein+prince+andrew",
        "epstein+bill+gates",
        "epstein+ghislaine+maxwell+trial",
        "epstein+les+wexner",
        "epstein+jean-luc+brunel",
        "epstein+victim+survivor+lawsuit",
        "epstein+flight+logs+names",
        "epstein+island+little+st+james",
        # Broader but still distinct from DOJ headlines
        "jeffrey+epstein+investigation+new",
        "epstein+connections+revealed+billionaire",
        "epstein+documents+unsealed+names",
        # International angles
        "epstein+europe+investigation",
        "epstein+intelligence+FBI+CIA",
    ]

    all_articles = []
    seen_titles = set()

    for query in queries:
        url = f"https://news.google.com/rss/search?q={query}&hl=en-US&gl=US&ceid=US:en"
        try:
            print(f"Fetching: {url}")
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (compatible; EpsteinFilesDaily/1.0)'})
            with urllib.request.urlopen(req, timeout=30) as response:
                xml_data = response.read().decode('utf-8')

            root = ET.fromstring(xml_data)
            for item in root.findall('.//item'):
                title = item.find('title')
                link = item.find('link')
                source = item.find('source')
                pub_date = item.find('pubDate')

                if title is not None and link is not None:
                    title_text = title.text or ""
                    if title_text.lower() not in seen_titles:
                        seen_titles.add(title_text.lower())
                        all_articles.append({
                            'title': title_text,
                            'url': link.text or "",
                            'source': source.text if source is not None else "News",
                            'date': pub_date.text if pub_date is not None else ""
                        })
        except Exception as e:
            print(f"Error fetching {query}: {e}")

    # Filter by date - only articles from the last 48 hours
    cutoff = datetime.now().astimezone() - timedelta(hours=48)
    recent = []
    undated = []
    for a in all_articles:
        if a['date']:
            try:
                pub_dt = parsedate_to_datetime(a['date'])
                if pub_dt >= cutoff:
                    recent.append(a)
                else:
                    print(f"  Skipping old article ({a['date']}): {a['title'][:60]}")
            except Exception:
                undated.append(a)  # Keep articles with unparseable dates
        else:
            undated.append(a)

    print(f"Found {len(recent)} articles from last 48 hours, {len(undated)} undated")

    # Use recent articles first, fall back to undated if needed
    filtered = recent + undated

    # Filter for relevance - broad keywords to capture diverse stories
    keywords = ['epstein', 'ghislaine', 'maxwell', 'prince andrew', 'wexner', 'brunel',
                'trafficking', 'victim', 'survivor', 'unsealed', 'flight log',
                'little st james', 'pedophile island']
    relevant = [a for a in filtered if any(kw in a['title'].lower() for kw in keywords)]
    print(f"Found {len(relevant)} relevant recent articles from RSS")
    return relevant[:20]

def generate_thumbnail(date_str, headline, filename, featured_name=""):
    """Generate newspaper-style thumbnail with paper texture."""

    WIDTH = 840
    HEIGHT = 472

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
        font_tagline = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSerif-Italic.ttf", 24)
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

    # Headline starts below double line
    headline_y_start = 190

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
    line_height = 70
    for i, line in enumerate(lines[:3]):
        bbox = draw.textbbox((0, 0), line, font=font_headline)
        text_width = bbox[2] - bbox[0]
        draw.text(((WIDTH - text_width) / 2, headline_y_start + i * line_height), line, fill=ink, font=font_headline)

    # Slight blur
    img = img.filter(ImageFilter.GaussianBlur(radius=0.3))

    # Save
    os.makedirs('images', exist_ok=True)
    img.save(filename, 'PNG')
    print(f"Created thumbnail: {filename}")

def generate_roundup(articles):
    """Use Claude to format the fetched articles into a roundup."""

    if not articles:
        print("No articles to format")
        return None

    existing = get_existing_roundups()
    today = datetime.now()

    # Format articles for Claude — include publish date so it can verify recency
    articles_text = "\n".join([
        f"- {a['title']} (Source: {a['source']}, Published: {a['date'] or 'Unknown'}, URL: {a['url']})"
        for a in articles
    ])

    prompt = f"""You are formatting a news roundup for Epstein Files Daily.

TODAY'S DATE: {today.strftime('%A, %B %d, %Y')}

EXISTING ROUNDUPS (avoid repeating old headlines): {existing}

HERE ARE THE NEWS ARTICLES FETCHED FROM RSS (these are REAL articles with REAL URLs):
{articles_text}

YOUR TASK:
1. Select 4-6 of the most newsworthy and distinct stories
2. PRIORITIZE stories about specific INDIVIDUALS (victims, associates, enablers, investigators) over generic DOJ/government process stories
3. Format them for the website
4. Extract names of notable people mentioned

STORY SELECTION PRIORITIES (in order):
- Stories naming specific individuals connected to Epstein (associates, visitors, flight log names, accusers, victims, enablers)
- Lawsuits, investigations, or legal actions against specific people
- International angles (European investigations, foreign connections)
- Victim/survivor stories and advocacy efforts
- LAST RESORT: Government process stories (DOJ releases, AG statements, congressional hearings) — include AT MOST ONE of these per roundup

CRITICAL DATE RULE:
- Today's date is {today.strftime('%B %d, %Y')}
- ONLY use articles published TODAY or YESTERDAY. Check the "Published:" date on each article.
- If an article's publish date is more than 2 days old, DO NOT include it.
- If you cannot verify the date, skip the article.

AVOID:
- Do NOT lead with Pam Bondi or DOJ release process stories — these have been covered extensively
- Do NOT make "files released" or "documents unsealed" the main theme
- If the only stories available are about DOJ/Bondi, dig deeper into WHO is named in those documents rather than the release process itself
- Do NOT include articles older than 2 days — this is a daily news roundup, not a recap

OUTPUT FORMAT - Return a JSON object:
{{
    "theme_headline": "Short punchy headline that MUST include at least one specific person's name (e.g., 'Prince Andrew Named in New Flight Logs', 'Les Wexner Faces New Lawsuit', 'Victims Push for Accountability Against Maxwell Associates'). NEVER use generic headlines like 'DOJ Releases Files' or 'Bondi Claims All Files Released'. Always lead with the most newsworthy INDIVIDUAL, not a government agency.",
    "featured_name": "The most prominent person's name from the headline (e.g., 'Prince Andrew')",
    "names": ["Full Name 1", "Full Name 2", "Full Name 3"],
    "bullets_short": [
        {{"name": "Key Subject", "text": "one-line summary.", "source": "Source Name", "url": "actual URL from article"}},
        ...
    ],
    "bullets_long": [
        {{"name": "Key Subject", "text": "2-4 sentence detailed summary with context.", "source": "Source Name", "url": "actual URL from article"}},
        ...
    ]
}}

RULES:
1. bullets_short: ONE LINE each (for homepage card)
2. bullets_long: 2-4 SENTENCES each (for article page)
3. 4-6 bullets total
4. Lead each bullet with a bolded name or subject
5. Use the ACTUAL URLs from the articles above - do not make up URLs
6. Names array should only contain full person names (for tags)
7. If fewer than 4 distinct newsworthy stories, return {{"no_news": true}}
8. AT MOST ONE bullet about DOJ/Bondi/government process per roundup — focus on the PEOPLE in the files
"""

    print("Calling Claude API to format roundup...")

    max_retries = 3
    for attempt in range(1, max_retries + 1):
        print(f"API attempt {attempt}/{max_retries}...")

        response = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=4000,
            messages=[{"role": "user", "content": prompt}]
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
                print(f"Attempt {attempt}: Could not find JSON in response")
                if attempt < max_retries:
                    continue
                print("ERROR: No JSON found after all retries")
                return None

        try:
            data = json.loads(json_str)
            break  # Success
        except json.JSONDecodeError as e:
            print(f"Attempt {attempt}: JSON parse error: {e}")
            # Try to repair common JSON issues
            try:
                # Fix trailing commas before } or ]
                repaired = re.sub(r',\s*([}\]])', r'\1', json_str)
                # Fix missing commas between objects/strings
                repaired = re.sub(r'"\s*\n\s*"', '",\n"', repaired)
                repaired = re.sub(r'}\s*\n\s*{', '},\n{', repaired)
                data = json.loads(repaired)
                print("JSON repaired successfully")
                break
            except json.JSONDecodeError:
                if attempt < max_retries:
                    print("JSON repair failed, retrying API call...")
                    continue
                print("ERROR: Could not parse JSON after all retries")
                print(f"Raw response (first 500 chars): {response_text[:500]}")
                return None

    if data.get('no_news'):
        print("No significant news found today")
        return None

    return data

def create_article_html(data, today):
    """Create the full article page HTML."""

    date_iso = today.strftime('%Y-%m-%d')
    date_readable = today.strftime('%B %d, %Y')
    month_day = today.strftime('%B %d').replace(' 0', ' ')
    filename = f"daily-{today.strftime('%b').lower()}-{today.day}-{today.year}"

    # Build bullets HTML for article page (long version)
    bullets_html = ""
    for bullet in data['bullets_long']:
        bullets_html += f'''
                <li><strong>{bullet['name']}</strong> {bullet['text']} <a href="{bullet['url']}" target="_blank" class="source-link">{bullet['source']} →</a></li>
'''

    # Build tags HTML - link to name pages
    tags_html = ""
    for name in data['names'][:4]:
        name_slug = name.lower().replace(' ', '-').replace('.', '').replace("'", '')
        tags_html += f'                    <a href="/names/{name_slug}.html" class="article-tag">{name}</a>\n'

    # URL encode for share buttons
    url = f"https://epsteinfilesdaily.com/{filename}"
    headline = f"{month_day}: {data['theme_headline']}"

    # Read template from existing article
    template = read_file('daily-feb-9-2026.html')

    html = template

    # Update title
    html = re.sub(r'<title>.*?</title>', f'<title>{month_day}: {data["theme_headline"]} — Epstein Files Daily</title>', html)

    # Update meta description
    first_bullet = data['bullets_short'][0]
    meta_desc = f"{first_bullet['name']} {first_bullet['text'][:100]}..."
    html = re.sub(r'<meta name="description" content=".*?">', f'<meta name="description" content="{meta_desc}">', html)

    # Update SEO tags (canonical, OG, Twitter, JSON-LD)
    full_url = f"https://epsteinfilesdaily.com/{filename}.html"
    image_url = f"https://epsteinfilesdaily.com/images/{filename}.png"
    full_headline = f"{month_day}: {data['theme_headline']}"

    # Canonical
    html = re.sub(r'<link rel="canonical" href=".*?">', f'<link rel="canonical" href="{full_url}">', html)

    # Open Graph
    html = re.sub(r'<meta property="og:url" content=".*?">', f'<meta property="og:url" content="{full_url}">', html)
    html = re.sub(r'<meta property="og:title" content=".*?">', f'<meta property="og:title" content="{full_headline} — Epstein Files Daily">', html)
    html = re.sub(r'<meta property="og:description" content=".*?">', f'<meta property="og:description" content="{meta_desc}">', html)
    html = re.sub(r'<meta property="og:image" content=".*?">', f'<meta property="og:image" content="{image_url}">', html)
    html = re.sub(r'<meta property="article:published_time" content=".*?">', f'<meta property="article:published_time" content="{date_iso}">', html)

    # Twitter Card
    html = re.sub(r'<meta name="twitter:url" content=".*?">', f'<meta name="twitter:url" content="{full_url}">', html)
    html = re.sub(r'<meta name="twitter:title" content=".*?">', f'<meta name="twitter:title" content="{full_headline}">', html)
    html = re.sub(r'<meta name="twitter:description" content=".*?">', f'<meta name="twitter:description" content="{meta_desc}">', html)
    html = re.sub(r'<meta name="twitter:image" content=".*?">', f'<meta name="twitter:image" content="{image_url}">', html)

    # JSON-LD (update the entire script block)
    json_ld = f'''<script type="application/ld+json">
    {{
        "@context": "https://schema.org",
        "@type": "NewsArticle",
        "headline": "{full_headline}",
        "image": "{image_url}",
        "datePublished": "{date_iso}",
        "dateModified": "{date_iso}",
        "author": {{
            "@type": "Organization",
            "name": "Epstein Files Daily"
        }},
        "publisher": {{
            "@type": "Organization",
            "name": "Epstein Files Daily",
            "logo": {{
                "@type": "ImageObject",
                "url": "https://epsteinfilesdaily.com/og-image.jpg"
            }}
        }},
        "description": "{meta_desc}",
        "mainEntityOfPage": {{
            "@type": "WebPage",
            "@id": "{full_url}"
        }}
    }}
    </script>'''
    html = re.sub(r'<script type="application/ld\+json">.*?</script>', json_ld, html, flags=re.DOTALL)

    # Update article content
    html = re.sub(r'<time datetime=".*?">', f'<time datetime="{date_iso}">', html)
    html = re.sub(r'>February \d+, 2026</time>', f'>{date_readable}</time>', html)

    # Update h1
    html = re.sub(r'<h1>.*?</h1>', f'<h1>{month_day}: {data["theme_headline"]}</h1>', html)

    # Update tags
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

    # Build tags - link to name pages
    tags_data = ','.join([name.lower() for name in data['names'][:4]])
    tags_html = ""
    for name in data['names'][:4]:
        name_slug = name.lower().replace(' ', '-').replace('.', '').replace("'", '')
        tags_html += f'                                    <a href="/names/{name_slug}.html" class="article-tag">{name}</a>\n'

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
    """Add the new roundup to RSS feed with full content for newsletters."""

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

    # Build full content HTML for newsletters (content:encoded)
    content_bullets = ""
    for bullet in data['bullets_long']:
        content_bullets += f'<li><strong>{bullet["name"]}</strong> {bullet["text"]} <a href="{bullet["url"]}">{bullet["source"]} →</a></li>\n\n'

    new_item = f'''
    <item>
      <title>{headline}</title>
      <link>{url}</link>
      <guid>{url}</guid>
      <pubDate>{pub_date}</pubDate>
      <description>{description}</description>
      <content:encoded><![CDATA[
<ul>
{content_bullets}</ul>
      ]]></content:encoded>
    </item>'''

    # Insert after the atom:link element (proper position in feed)
    marker = '<atom:link href="https://epsteinfilesdaily.com/feed.xml" rel="self" type="application/rss+xml"/>'
    if marker in feed_content:
        feed_content = feed_content.replace(marker, marker + new_item)
        write_file('feed.xml', feed_content)
        print("Updated feed.xml with full content")
    else:
        # Fallback to old marker
        marker = '</language>'
        if marker in feed_content:
            feed_content = feed_content.replace(marker, marker + new_item)
            write_file('feed.xml', feed_content)
            print("Updated feed.xml with full content (fallback)")
        else:
            print("WARNING: Could not find insertion point in feed.xml")

def regenerate_name_pages():
    """Regenerate all name pages after adding a new article."""
    from collections import defaultdict

    def slugify(name):
        return name.lower().replace(' ', '-').replace('.', '').replace("'", '')

    # Extract articles and tags
    articles = []
    for filename in os.listdir('.'):
        if filename.startswith('daily-') and filename.endswith('.html'):
            content = read_file(filename)

            # Extract title
            title_match = re.search(r'<h1[^>]*>([^<]+)</h1>', content)
            title = title_match.group(1) if title_match else filename

            # Extract date
            date_match = re.search(r'<time datetime="([^"]+)"', content)
            date_str = date_match.group(1) if date_match else ''

            # Extract tags
            tags = re.findall(r'class="article-tag">([^<]+)</a>', content)

            # Extract thumbnail
            thumb_match = re.search(r'property="og:image" content="([^"]+)"', content)
            thumbnail = thumb_match.group(1) if thumb_match else ''
            if thumbnail.startswith('https://epsteinfilesdaily.com/'):
                thumbnail = thumbnail.replace('https://epsteinfilesdaily.com/', '')

            # Extract description
            desc_match = re.search(r'<p class="lead">([^<]+)</p>', content)
            description = desc_match.group(1) if desc_match else ''

            if tags:
                articles.append({
                    'filename': filename,
                    'title': title,
                    'date': date_str,
                    'tags': tags,
                    'thumbnail': thumbnail,
                    'description': description
                })

    # Sort by date descending
    articles.sort(key=lambda x: x['date'], reverse=True)

    # Build tag index
    tag_index = defaultdict(list)
    for article in articles:
        for tag in article['tags']:
            tag_index[tag].append(article)

    # Create names directory
    os.makedirs('names', exist_ok=True)

    # Load existing bios
    bios_file = 'name-bios.json'
    try:
        bios = json.loads(read_file(bios_file))
    except:
        bios = {}

    # Generate bios for any new names via Claude
    new_names = [n for n in tag_index.keys() if slugify(n) not in bios]
    if new_names:
        print(f"Generating bios for {len(new_names)} new names: {new_names}")
        for new_name in new_names:
            try:
                bio_response = client.messages.create(
                    model="claude-sonnet-4-20250514",
                    max_tokens=300,
                    messages=[{
                        "role": "user",
                        "content": f"""Write a 2-4 sentence factual bio about {new_name}'s documented connection to Jeffrey Epstein for a news aggregation website.
Only include publicly verified information from court documents, flight logs, or credible news reporting.
Use hedging language where appropriate ("according to documents," "has denied," "allegedly").
Do NOT speculate. If the connection is minimal or unclear, say so.
Return ONLY the bio text, no quotes or labels."""
                    }]
                )
                bio_text = bio_response.content[0].text.strip()
                bios[slugify(new_name)] = bio_text
                print(f"  Generated bio for {new_name}")
            except Exception as e:
                print(f"  Failed to generate bio for {new_name}: {e}")
                bios[slugify(new_name)] = f"{new_name} has been referenced in documents related to the Jeffrey Epstein case. Their name appears in the Epstein Files Daily coverage."

        # Save updated bios
        write_file(bios_file, json.dumps(bios, indent=2))
        print(f"Saved {len(bios)} bios to {bios_file}")

    # Generate each name page
    for name, name_articles in tag_index.items():
        slug = slugify(name)

        # Build article cards
        article_cards = []
        for article in name_articles:
            tags_html = ''.join([
                f'<a href="/names/{slugify(t)}.html" class="article-tag">{t}</a>'
                for t in article['tags']
            ])

            try:
                from datetime import datetime as dt
                date_obj = dt.strptime(article['date'], '%Y-%m-%d')
                formatted_date = date_obj.strftime('%B %d, %Y')
            except:
                formatted_date = article['date']

            card = f'''
            <article class="article-preview" data-tags="{' '.join(t.lower() for t in article['tags'])}">
                <a href="/{article['filename']}" class="article-thumb">
                    <img src="/{article['thumbnail']}" alt="{article['title']}" loading="lazy">
                </a>
                <div class="article-content">
                    <div class="article-tags">{tags_html}</div>
                    <time datetime="{article['date']}">{formatted_date}</time>
                    <h2 class="article-title"><a href="/{article['filename']}">{article['title']}</a></h2>
                    <p class="article-excerpt">{article['description'][:200] if article['description'] else ''}...</p>
                </div>
            </article>'''
            article_cards.append(card)

        # Build sidebar
        sorted_tags = sorted(tag_index.items(), key=lambda x: (-len(x[1]), x[0]))
        tag_filters_html = '\n'.join([
            f'<a href="/names/{slugify(tag)}.html" class="tag-filter{" active" if tag == name else ""}"><span>{tag}</span><span class="count">{len(tag_articles)}</span></a>'
            for tag, tag_articles in sorted_tags[:50]
        ])

        # Get bio for this person
        person_bio = bios.get(slug, '')
        if person_bio:
            meta_desc = person_bio[:155].rsplit(' ', 1)[0] + '...'
            bio_section = f'''
            <div class="person-bio">
                <p>{person_bio}</p>
            </div>
'''
        else:
            meta_desc = f'All articles mentioning {name} in the Epstein Files.'
            bio_section = ''

        html = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <!-- Google tag (gtag.js) -->
    <script async src="https://www.googletagmanager.com/gtag/js?id=G-1NBDE2SB5X"></script>
    <script>
      window.dataLayer = window.dataLayer || [];
      function gtag(){{dataLayer.push(arguments);}}
      gtag('js', new Date());
      gtag('config', 'G-1NBDE2SB5X');
    </script>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width,initial-scale=1">
    <title>{name} - Epstein Files Daily</title>
    <meta name="description" content="{meta_desc}">
    <link rel="canonical" href="https://epsteinfilesdaily.com/names/{slug}.html">
    <meta property="og:title" content="{name} - Epstein Files Daily">
    <meta property="og:description" content="{meta_desc}">
    <meta property="og:type" content="website">
    <meta property="og:url" content="https://epsteinfilesdaily.com/names/{slug}.html">
    <meta property="og:image" content="https://epsteinfilesdaily.com/og-image.jpg">
    <meta name="twitter:card" content="summary_large_image">
    <meta name="twitter:title" content="{name} - Epstein Files Daily">
    <meta name="twitter:description" content="{meta_desc}">
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Oswald:wght@500;600;700&display=swap" rel="stylesheet">
    <link rel="icon" type="image/svg+xml" href="/epstein-unsealed-logo.svg">
    <style>
        :root{{--bg:#1f1f1f;--bg-card:#252525;--text:#fff;--text-muted:#b0b0b0;--text-light:#777;--border:#333;--search-bg:#292929;--sidebar-bg:#181818;--accent:#b91c1c}}
        *{{margin:0;padding:0;box-sizing:border-box}}
        body{{font-family:'Inter',sans-serif;background:var(--bg);color:var(--text);line-height:1.6}}
        a{{color:inherit;text-decoration:none}}

        /* BOLD HEADER */
        header[role="banner"]{{background:#000;border-bottom:4px solid var(--accent);position:sticky;top:0;z-index:100}}
        .header-inner{{display:flex;align-items:center;justify-content:space-between;padding:0}}
        .header-controls{{display:flex;gap:12px;align-items:center;padding-right:20px}}
        .theme-toggle{{background:#333;color:#fff;border:none;padding:10px 14px;font-family:'Inter',sans-serif;font-weight:600;font-size:12px;cursor:pointer;display:flex;align-items:center;gap:6px;transition:background 0.2s}}
        .theme-toggle:hover{{background:var(--accent)}}
        .theme-toggle svg{{width:16px;height:16px}}

        /* LOGO */
        .logo{{display:flex;align-items:center;gap:0;text-decoration:none;background:var(--accent);padding:12px 24px;transition:background 0.2s;flex-shrink:0}}
        .logo:hover{{background:#b91c1c}}
        .logo-icon{{width:56px;height:56px;display:flex;align-items:center;justify-content:center}}
        .logo-icon svg{{width:56px;height:56px}}
        .logo-text{{font-family:'Oswald',sans-serif;font-size:32px;font-weight:700;color:#fff;display:flex;flex-direction:column;line-height:1;text-transform:uppercase;letter-spacing:1px}}
        .logo-text .daily{{font-size:14px;font-weight:600;letter-spacing:3px;opacity:0.9;margin-top:2px}}

        /* HEADER CENTER */
        .header-center{{flex:1;display:flex;align-items:center;gap:24px;padding:0 24px}}
        .header-search-wrapper{{position:relative;flex:1;max-width:400px}}
        .header-search{{display:flex;gap:0}}
        .header-search input{{flex:1;padding:10px 14px;border:none;background:var(--search-bg);color:var(--text);font-size:14px;font-family:'Inter',sans-serif;width:100%}}
        .header-search input:focus{{outline:none;background:var(--bg-card)}}
        .header-search input::placeholder{{color:var(--text-light)}}
        .header-search button{{background:#333;color:#fff;border:none;padding:10px 16px;font-family:'Inter',sans-serif;font-weight:700;font-size:12px;cursor:pointer;text-transform:uppercase;letter-spacing:1px}}
        .header-search button:hover{{background:var(--accent)}}
        .search-dropdown{{display:none;position:absolute;top:100%;left:0;right:0;background:#252525;border:1px solid var(--border);border-top:none;padding:12px;z-index:200}}
        .search-dropdown.visible{{display:block}}
        .search-dropdown-label{{font-size:10px;font-weight:700;color:#666;text-transform:uppercase;letter-spacing:1px;margin-bottom:8px}}
        .search-dropdown-names{{display:flex;gap:6px;flex-wrap:wrap}}
        .trending-name{{background:#333;color:#fff;padding:5px 10px;font-size:11px;font-weight:600;cursor:pointer;transition:all 0.15s;border:none;font-family:'Inter',sans-serif}}
        .trending-name:hover{{background:var(--accent)}}
        .header-email{{display:flex;align-items:center;gap:12px}}
        .header-email-label{{font-size:12px;color:#999;font-weight:500;white-space:nowrap}}
        .header-email-form{{display:flex;gap:0}}
        .header-email-form input{{padding:10px 14px;border:none;background:var(--search-bg);color:var(--text);font-size:14px;font-family:'Inter',sans-serif;width:280px}}
        .header-email-form input:focus{{outline:none;background:var(--bg-card)}}
        .header-email-form input::placeholder{{color:var(--text-light)}}
        .header-email-form button{{background:var(--accent);color:#fff;border:none;padding:10px 16px;font-family:'Inter',sans-serif;font-weight:700;font-size:12px;cursor:pointer;text-transform:uppercase;letter-spacing:1px}}

        .page-wrapper{{display:grid;grid-template-columns:260px 1fr;min-height:calc(100vh - 80px)}}
        .sidebar{{background:var(--sidebar-bg);border-right:1px solid var(--border);padding:0;overflow-y:auto;max-height:calc(100vh - 80px);position:sticky;top:0}}
        .sidebar-section{{padding:16px 20px;border-bottom:1px solid var(--border)}}
        .sidebar-section h3{{font-size:11px;font-weight:700;text-transform:uppercase;letter-spacing:2px;color:var(--accent);margin-bottom:12px}}
        .tag-filters{{display:flex;flex-direction:column;gap:2px;max-height:400px;overflow-y:auto}}
        .tag-filter{{display:flex;justify-content:space-between;align-items:center;padding:8px 10px;font-size:13px;font-weight:500;color:var(--text-muted);transition:all 0.15s;border-left:3px solid transparent}}
        .tag-filter:hover{{background:#252525;color:#fff;border-left-color:var(--accent)}}
        .tag-filter.active{{background:var(--accent);color:#fff;border-left-color:var(--accent)}}
        .tag-filter .count{{font-size:11px;color:#666;background:#252525;padding:2px 6px}}
        .tag-filter.active .count{{background:rgba(0,0,0,0.3);color:#fff}}
        .back-link{{display:block;padding:16px 20px;color:var(--text-muted);font-size:13px;border-bottom:1px solid var(--border)}}
        .back-link:hover{{color:var(--accent)}}
        main{{padding:32px}}
        .page-header{{margin-bottom:32px}}
        .page-header h1{{font-family:'Oswald',sans-serif;font-size:42px;font-weight:700;text-transform:uppercase;letter-spacing:1px;margin-bottom:8px}}
        .page-header p{{color:var(--text-muted)}}
        .person-bio{{background:var(--bg-card);border-left:3px solid var(--accent);padding:16px 20px;margin-bottom:32px;font-size:16px;line-height:1.7;color:var(--text-muted)}}
        .person-bio p{{margin:0}}
        .articles-grid{{display:flex;flex-direction:column;gap:24px}}
        .article-preview{{display:grid;grid-template-columns:200px 1fr;gap:20px;padding-bottom:24px;border-bottom:1px solid var(--border)}}
        .article-thumb{{aspect-ratio:16/9;overflow:hidden;background:#333}}
        .article-thumb img{{width:100%;height:100%;object-fit:cover}}
        .article-content{{display:flex;flex-direction:column;gap:8px}}
        .article-tags{{display:flex;flex-wrap:wrap;gap:6px}}
        .article-tag{{background:var(--accent);color:#fff;padding:4px 10px;font-weight:700;font-size:10px;text-transform:uppercase;letter-spacing:0.5px}}
        .article-tag:hover{{background:#991b1b}}
        .article-content time{{font-size:12px;color:var(--text-light);text-transform:uppercase}}
        .article-title{{font-family:'Oswald',sans-serif;font-size:22px;font-weight:600;line-height:1.2;text-transform:uppercase}}
        .article-title a:hover{{color:var(--accent)}}
        .article-excerpt{{font-size:14px;color:var(--text-muted);line-height:1.5}}

        /* Light mode */
        html.light-mode{{--bg:#f5f5f5;--bg-card:#fff;--text:#1a1a1a;--text-muted:#555;--text-light:#777;--border:#ddd;--search-bg:#fff;--sidebar-bg:#eee}}
        html.light-mode header[role="banner"]{{background:#fff;border-bottom-color:var(--accent)}}
        html.light-mode .logo{{background:var(--accent)}}
        html.light-mode .header-search input{{background:#f0f0f0;color:#1a1a1a}}
        html.light-mode .header-search input:focus{{background:#fff}}
        html.light-mode .header-search input::placeholder{{color:#888}}
        html.light-mode .header-email-form input{{background:#f0f0f0;color:#1a1a1a}}
        html.light-mode .header-email-form input:focus{{background:#fff}}
        html.light-mode .header-email-form input::placeholder{{color:#888}}
        html.light-mode .trending-name{{background:#e0e0e0;color:#1a1a1a}}
        html.light-mode .sidebar{{background:#eee;border-right-color:#ddd}}
        html.light-mode .sidebar-section{{border-bottom-color:#ddd}}
        html.light-mode .tag-filter{{color:#555}}
        html.light-mode .tag-filter:hover{{background:#ddd;color:#1a1a1a}}
        html.light-mode .tag-filter .count{{background:#ddd;color:#555}}
        html.light-mode .back-link{{border-bottom-color:#ddd}}
        html.light-mode .article-preview{{border-bottom-color:#ddd}}
        html.light-mode .article-thumb{{background:#ddd}}
        html.light-mode .person-bio{{background:#fff}}
        html.light-mode .theme-toggle{{background:#e0e0e0;color:#1a1a1a}}

        @media(max-width:900px){{.page-wrapper{{grid-template-columns:1fr}}.sidebar{{display:none}}.article-preview{{grid-template-columns:1fr}}.header-center{{display:none}}.header-inner{{padding:0}}.theme-toggle{{display:none}}}}
    </style>
</head>
<body>
    <header role="banner">
        <div class="header-inner">
            <a href="/" class="logo" aria-label="Epstein Files Daily - Home">
                <div class="logo-icon" aria-hidden="true">
                    <svg viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg">
                        <circle cx="42" cy="42" r="32" fill="#1a1a1a" stroke="white" stroke-width="3"/>
                        <text x="42" y="48" font-size="28" font-family="Arial,sans-serif" font-weight="bold" fill="white" text-anchor="middle">EF</text>
                        <rect x="18" y="52" width="48" height="6" fill="#fff"/>
                        <line x1="66" y1="66" x2="88" y2="88" stroke="white" stroke-width="6" stroke-linecap="round"/>
                    </svg>
                </div>
                <span class="logo-text">EPSTEIN FILES<span class="daily">DAILY</span></span>
            </a>
            <div class="header-center">
                <div class="header-search-wrapper">
                    <div class="header-search">
                        <input type="text" id="header-search-input" placeholder="Search names..." aria-label="Search articles">
                        <button type="button" id="header-search-btn">GO</button>
                    </div>
                    <div class="search-dropdown" id="search-dropdown">
                        <div class="search-dropdown-label">Trending Names</div>
                        <div class="search-dropdown-names">
                            <button class="trending-name" data-name="peter thiel">THIEL</button>
                            <button class="trending-name" data-name="elon musk">MUSK</button>
                            <button class="trending-name" data-name="sergey brin">BRIN</button>
                            <button class="trending-name" data-name="bill gates">GATES</button>
                        </div>
                    </div>
                </div>
                <div class="header-email">
                    <span class="header-email-label">Get updates:</span>
                    <form class="header-email-form" action="https://epstein-exposed.us13.list-manage.com/subscribe/post?u=dbf04846cbc14c3a4d734f311&amp;id=a2f4925a23&amp;f_id=00cdace2f0" method="post" target="_blank">
                        <input type="email" name="EMAIL" placeholder="your@email.com" required>
                        <div style="position:absolute;left:-5000px" aria-hidden="true"><input type="text" name="b_dbf04846cbc14c3a4d734f311_a2f4925a23" tabindex="-1" value=""></div>
                        <button type="submit">GO</button>
                    </form>
                </div>
            </div>
            <div class="header-controls">
                <button type="button" id="theme-toggle" class="theme-toggle" aria-label="Toggle light/dark mode">
                    <svg id="theme-icon-dark" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 3v1m0 16v1m9-9h-1M4 12H3m15.364 6.364l-.707-.707M6.343 6.343l-.707-.707m12.728 0l-.707.707M6.343 17.657l-.707.707M16 12a4 4 0 11-8 0 4 4 0 018 0z"/></svg>
                    <svg id="theme-icon-light" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor" style="display:none"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M20.354 15.354A9 9 0 018.646 3.646 9.003 9.003 0 0012 21a9.003 9.003 0 008.354-5.646z"/></svg>
                    <span id="theme-text">LIGHT</span>
                </button>
            </div>
        </div>
    </header>
    <div class="page-wrapper">
        <aside class="sidebar">
            <a href="/" class="back-link">← Back to Home</a>
            <div class="sidebar-section">
                <h3>Names in the Files</h3>
                <div class="tag-filters">{tag_filters_html}</div>
            </div>
        </aside>
        <main>
            <div class="page-header">
                <h1>{name}</h1>
                <p>{len(name_articles)} article{'' if len(name_articles) == 1 else 's'} mentioning this name</p>
            </div>
{bio_section}            <div class="articles-grid">{''.join(article_cards)}</div>
        </main>
    </div>
    <script>
        const html = document.documentElement;

        // Header search
        const searchInput = document.getElementById('header-search-input');
        const searchBtn = document.getElementById('header-search-btn');
        const searchDropdown = document.getElementById('search-dropdown');
        function slugify(name) {{ return name.toLowerCase().replace(/[^a-z0-9]+/g, '-').replace(/(^-|-$)/g, ''); }}
        function doSearch() {{ const q = searchInput.value.trim(); if (q) window.location.href = '/names/' + slugify(q) + '.html'; }}
        searchBtn.addEventListener('click', doSearch);
        searchInput.addEventListener('keydown', (e) => {{ if (e.key === 'Enter') doSearch(); }});
        searchInput.addEventListener('focus', () => {{ searchDropdown.classList.add('visible'); }});
        document.addEventListener('click', (e) => {{ if (!e.target.closest('.header-search-wrapper')) searchDropdown.classList.remove('visible'); }});
        document.querySelectorAll('.trending-name').forEach(btn => {{ btn.addEventListener('click', () => {{ window.location.href = '/names/' + slugify(btn.dataset.name) + '.html'; }}); }});

        // Theme toggle
        const themeToggle = document.getElementById('theme-toggle');
        const themeText = document.getElementById('theme-text');
        const themeIconDark = document.getElementById('theme-icon-dark');
        const themeIconLight = document.getElementById('theme-icon-light');
        const savedTheme = localStorage.getItem('theme');
        if (savedTheme === 'light') {{
            html.classList.add('light-mode');
            themeText.textContent = 'DARK';
            themeIconDark.style.display = 'none';
            themeIconLight.style.display = 'block';
        }}
        themeToggle.addEventListener('click', () => {{
            html.classList.toggle('light-mode');
            const isLight = html.classList.contains('light-mode');
            themeText.textContent = isLight ? 'DARK' : 'LIGHT';
            themeIconDark.style.display = isLight ? 'none' : 'block';
            themeIconLight.style.display = isLight ? 'block' : 'none';
            localStorage.setItem('theme', isLight ? 'light' : 'dark');
        }});
    </script>
</body>
</html>'''

        write_file(f'names/{slug}.html', html)

    print(f"Regenerated {len(tag_index)} name pages")

def update_sitemap(data, today):
    """Add the new article to sitemap.xml."""

    try:
        sitemap_content = read_file('sitemap.xml')
    except FileNotFoundError:
        print("WARNING: sitemap.xml not found, skipping sitemap update")
        return

    date_iso = today.strftime('%Y-%m-%d')
    month_day = today.strftime('%B %d').replace(' 0', ' ')
    filename = f"daily-{today.strftime('%b').lower()}-{today.day}-{today.year}"
    headline = data['theme_headline']

    new_entry = f'''
  <url>
    <loc>https://epsteinfilesdaily.com/{filename}.html</loc>
    <lastmod>{date_iso}</lastmod>
    <changefreq>never</changefreq>
    <priority>0.9</priority>
    <news:news>
      <news:publication>
        <news:name>Epstein Files Daily</news:name>
        <news:language>en</news:language>
      </news:publication>
      <news:publication_date>{date_iso}</news:publication_date>
      <news:title>{headline}</news:title>
    </news:news>
  </url>
'''

    # Insert after Archive entry
    marker = '<!-- Daily Articles -->'
    if marker in sitemap_content:
        sitemap_content = sitemap_content.replace(marker, marker + new_entry)
        # Update homepage lastmod
        sitemap_content = re.sub(
            r'(<loc>https://epsteinfilesdaily.com/</loc>\s*<lastmod>)\d{4}-\d{2}-\d{2}(</lastmod>)',
            f'\\g<1>{date_iso}\\g<2>',
            sitemap_content
        )
        write_file('sitemap.xml', sitemap_content)
        print("Updated sitemap.xml")
    else:
        print("WARNING: Could not find insertion point in sitemap.xml")

def generate_substack_post(data, today):
    """Generate a Substack-ready version of the daily roundup.

    This is a shorter, rewritten version that links back to the full article
    on epsteinfilesdaily.com to avoid duplicate content issues with Google.
    """
    month_day = today.strftime('%B %d').replace(' 0', ' ')
    filename = f"daily-{today.strftime('%b').lower()}-{today.day}-{today.year}"
    full_url = f"https://epsteinfilesdaily.com/{filename}.html"

    subject = f"{month_day}: {data['theme_headline']}"

    # Build styled bullets matching website design
    bullets_html = ""
    for bullet in data['bullets_short'][:5]:
        name_slug = bullet['name'].lower().replace(' ', '-').replace('.', '').replace("'", '')
        source_url = bullet.get('url', full_url)
        source_name = bullet.get('source', 'Source')
        bullets_html += f'''            <li>
                <strong>{bullet["name"]}</strong> &mdash; {bullet["text"]}
                <br><a href="{source_url}" class="source-link">{source_name} &rarr;</a>
            </li>
'''

    # Build name tags
    name_tags_html = ""
    for name in data['names'][:6]:
        name_slug = name.lower().replace(' ', '-').replace('.', '').replace("'", '')
        name_tags_html += f'                <a href="https://epsteinfilesdaily.com/names/{name_slug}.html" class="name-tag">{name}</a>\n'

    html = f"""<div class="header">
        <h1>Epstein Files</h1>
        <div class="subtitle">Daily</div>
    </div>
    <div class="container">
        <div class="date-bar">
            <span>Daily Roundup</span>
            <span>{month_day}, {today.year}</span>
        </div>
        <div class="intro">
            This is a summary of today's Epstein Files Daily roundup. <a href="{full_url}">Read the full article with all sources &rarr;</a>
        </div>
        <div class="headline">{data['theme_headline']}</div>
        <h2>Today's Key Developments</h2>
        <ul class="bullets">
{bullets_html}        </ul>
        <div class="names-section">
            <h2>Names in Today's Report</h2>
            <div class="name-tags">
{name_tags_html}            </div>
        </div>
        <div class="cta">
            <a href="{full_url}" class="cta-btn">Read the Full Roundup &rarr;</a>
            <p>Visit <a href="https://epsteinfilesdaily.com">epsteinfilesdaily.com</a> for daily coverage tracking every name, every document, and every development.</p>
        </div>
        <div class="footer">
            <p><a href="https://epsteinfilesdaily.com">Epstein Files Daily</a> &mdash; Every name. Every document. Every day.</p>
        </div>
    </div>"""

    return {
        'subject': subject,
        'html': html
    }


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

    # Step 1: Fetch news from RSS (Claude API cannot search the web!)
    print("\nStep 1: Fetching news from Google News RSS...")
    articles = fetch_news_from_rss()

    if not articles:
        print("ERROR: Could not fetch any articles from RSS")
        return

    # Step 2: Use Claude to format the articles
    print("\nStep 2: Using Claude to format articles...")
    roundup_data = generate_roundup(articles)

    if not roundup_data:
        print("No roundup generated")
        return

    print(f"\nTheme: {roundup_data['theme_headline']}")
    print(f"Names: {', '.join(roundup_data['names'])}")
    print(f"Bullets: {len(roundup_data['bullets_short'])}")

    # Generate thumbnail
    thumb_filename = f"images/{filename_base}.png"
    featured_name = roundup_data.get('featured_name', roundup_data['names'][0] if roundup_data['names'] else '')
    generate_thumbnail(date_str, roundup_data['theme_headline'], thumb_filename, featured_name)

    # Create article HTML
    article_html = create_article_html(roundup_data, today)
    write_file(f"{filename_base}.html", article_html)
    print(f"Created: {filename_base}.html")

    # Update index.html
    update_index_html(roundup_data, today)

    # Update RSS feed
    update_feed_xml(roundup_data, today)

    # Update sitemap
    update_sitemap(roundup_data, today)

    # Regenerate name pages
    regenerate_name_pages()

    # Generate Substack cross-post content
    substack_content = generate_substack_post(roundup_data, today)

    # Save info for workflow
    latest_info = {
        "headline": f"{today.strftime('%B')} {today.day}: {roundup_data['theme_headline']}",
        "slug": filename_base,
        "date": today.strftime('%Y-%m-%d'),
        "substack_subject": substack_content['subject'],
        "substack_html": substack_content['html']
    }
    write_file('latest_article.json', json.dumps(latest_info))

    print("\n" + "=" * 50)
    print("ROUNDUP GENERATED SUCCESSFULLY")
    print("=" * 50)

if __name__ == "__main__":
    main()
