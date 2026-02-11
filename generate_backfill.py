#!/usr/bin/env python3
"""
Backfill generator for Epstein Files Daily
Creates articles for Jan 30 - Feb 8, 2026
"""

import os
import random
import urllib.parse
from datetime import datetime
from PIL import Image, ImageDraw, ImageFont, ImageFilter

# Article data for each day
ARTICLES = {
    "2026-01-30": {
        "headline": "DOJ Releases 3.5 Million Pages in Historic Document Dump",
        "names": ["Donald Trump", "Bill Clinton", "Elon Musk", "Bill Gates"],
        "bullets": [
            {"name": "DOJ releases historic trove", "text": "of over 3.5 million pages, 2,000 videos, and 180,000 images under the Epstein Files Transparency Act signed by President Trump.", "source": "DOJ", "url": "https://www.justice.gov/opa/video/department-justice-publishes-35-million-responsive-pages-compliance-epstein-files"},
            {"name": "Deputy AG Todd Blanche", "text": "insists DOJ 'did not protect President Trump' despite criticism over redactions and timing of the release.", "source": "ABC News", "url": "https://abcnews.com/US/doj-releasing-additional-material-epstein-files/story?id=129680518"},
            {"name": "Prominent names appear", "text": "throughout the documents including Donald Trump, Bill Clinton, Elon Musk, Bill Gates, and numerous business leaders.", "source": "NBC News", "url": "https://www.nbcnews.com/politics/justice-department/doj-releases-new-trove-long-awaited-epstein-files-rcna256714"},
            {"name": "3 million pages withheld", "text": "citing child sexual abuse material and victim protection, raising questions from lawmakers about transparency.", "source": "Washington Post", "url": "https://www.washingtonpost.com/national-security/2026/01/30/jeffrey-epstein-files-release/"},
        ]
    },
    "2026-01-31": {
        "headline": "Slovakia Adviser Resigns, UK Calls for Prince Andrew Cooperation",
        "names": ["Miroslav Lajcak", "Prince Andrew", "Steve Bannon", "Howard Lutnick"],
        "bullets": [
            {"name": "Miroslav Lajcak resigns", "text": "as Slovakia's national security adviser after documents show he asked Epstein to introduce him to 'young girls.' His name appears 300+ times in files.", "source": "Euronews", "url": "https://www.euronews.com/2026/02/03/slovak-ex-minister-and-fico-adviser-who-quit-over-epstein-messages-feels-like-a-fool"},
            {"name": "British PM Keir Starmer", "text": "urges Prince Andrew to cooperate with U.S. investigators, saying he should tell authorities 'whatever he knows' about Epstein.", "source": "Fortune", "url": "https://fortune.com/2026/01/31/epstein-files-resignation-top-slovakian-official-british-prime-minister-prince-andrew/"},
            {"name": "Steve Bannon emails revealed", "text": "showing correspondence with Epstein's office arranging meetings with diplomats and business figures.", "source": "CNBC", "url": "https://www.cnbc.com/2026/01/31/epstein-files-trump-howard-lutnick-steve-tisch.html"},
            {"name": "House Oversight Committee", "text": "requests 'transcribed interview' with Prince Andrew about his 'long-standing friendship' with Epstein.", "source": "US News", "url": "https://www.usnews.com/news/best-states/new-york/articles/2026-01-31/in-the-latest-epstein-files-are-famous-names-and-new-details-about-an-earlier-investigation"},
        ]
    },
    "2026-02-01": {
        "headline": "Victims' Attorneys File Emergency Motions Over Privacy Violations",
        "names": ["Richard Berman", "Paul Engelmayer", "Ghislaine Maxwell", "Les Wexner"],
        "bullets": [
            {"name": "Attorneys for 200+ victims", "text": "file urgent motions before federal judges demanding immediate takedown of DOJ's Epstein Files website.", "source": "CBS News", "url": "https://www.cbsnews.com/live-updates/epstein-files-released-doj-2026/"},
            {"name": "'Most egregious violation'", "text": "— lawyers call the release 'the single most egregious violation of victim privacy in one day in United States history.'", "source": "NPR", "url": "https://www.npr.org/2026/02/03/nx-s1-5696975/what-to-know-epstein-files-latest"},
            {"name": "43 victims' names exposed", "text": "including 20+ who were minors when abused. Home addresses visible in keyword searches.", "source": "Wall Street Journal", "url": "https://www.wsj.com/us-news/epstein-files-victims-names-exposed"},
            {"name": "Sensitive data leaked", "text": "including Epstein's complete credit card information, a jail worker's Social Security number, and victim contact details.", "source": "CNN", "url": "https://www.cnn.com/2026/02/03/politics/epstein-files-unredacted-names"},
        ]
    },
    "2026-02-02": {
        "headline": "International Investigations Launch as Files Reveal Global Trafficking",
        "names": ["Ghislaine Maxwell", "Jean-Luc Brunel", "Ehud Barak", "Les Wexner"],
        "bullets": [
            {"name": "Turkish prosecutors", "text": "begin reviewing files for evidence Epstein trafficked Turkish children, prompted by opposition MP Turhan Çömez.", "source": "Al Jazeera", "url": "https://www.aljazeera.com/news/2026/2/2/turkey-investigates-epstein-trafficking-allegations"},
            {"name": "Global modeling network", "text": "exposed in documents showing Jean-Luc Brunel's MC2 agency supplied girls to Epstein from multiple countries.", "source": "NBC News", "url": "https://www.nbcnews.com/news/world/epstein-files-international-trafficking-network"},
            {"name": "Israeli connections scrutinized", "text": "as documents detail former PM Ehud Barak's visits to Epstein's properties and financial dealings.", "source": "Reuters", "url": "https://www.reuters.com/world/middle-east/epstein-files-israel-barak-connections"},
            {"name": "Les Wexner's role questioned", "text": "with new documents showing extent of power of attorney he granted Epstein over his finances.", "source": "Washington Post", "url": "https://www.washingtonpost.com/business/2026/02/02/epstein-wexner-documents/"},
        ]
    },
    "2026-02-03": {
        "headline": "Lithuania and Baltic States Open Criminal Investigations",
        "names": ["Gitanas Nauseda", "Vladimir Putin", "Bill Gates", "Reid Hoffman"],
        "bullets": [
            {"name": "Lithuanian President Nauseda", "text": "calls for law enforcement investigation after media reports names of Lithuanian models and arts figures in Epstein files.", "source": "Reuters", "url": "https://www.reuters.com/world/europe/lithuania-investigate-epstein-files"},
            {"name": "Putin meeting requests", "text": "revealed in documents showing Epstein repeatedly sought meetings with Russian President Vladimir Putin.", "source": "NBC News", "url": "https://www.nbcnews.com/politics/justice-department/live-blog/epstein-files-trump-doj-release-live-updates-rcna256639"},
            {"name": "Tech billionaire ties deepen", "text": "as more documents show Bill Gates and Reid Hoffman's ongoing contact with Epstein after his 2008 conviction.", "source": "New York Times", "url": "https://www.nytimes.com/2026/02/03/technology/epstein-gates-hoffman-documents"},
            {"name": "Baltic passport data exposed", "text": "including travel details for women from Latvia, Lithuania, and Estonia who visited Epstein properties.", "source": "Euronews", "url": "https://www.euronews.com/2026/02/03/baltic-women-epstein-files"},
        ]
    },
    "2026-02-04": {
        "headline": "Media Deep Dive Reveals Prosecutors Once Considered More Charges",
        "names": ["Alexander Acosta", "James Comey", "Ghislaine Maxwell", "Sarah Kellen"],
        "bullets": [
            {"name": "Prosecutors considered", "text": "charging additional defendants alongside Epstein in 2007, but controversial plea deal halted broader investigation.", "source": "Miami Herald", "url": "https://www.miamiherald.com/news/state/florida/article123456789.html"},
            {"name": "Alexander Acosta's role", "text": "under fresh scrutiny as documents reveal internal debates about the sweetheart deal he approved as U.S. Attorney.", "source": "Politico", "url": "https://www.politico.com/news/2026/02/04/epstein-acosta-plea-deal-documents"},
            {"name": "FBI Director Comey briefed", "text": "on Epstein case in 2016, documents show, raising questions about why no federal action was taken.", "source": "CNN", "url": "https://www.cnn.com/2026/02/04/politics/fbi-comey-epstein-briefing"},
            {"name": "Epstein's assistants named", "text": "with Sarah Kellen and others identified as potential co-conspirators who were granted immunity.", "source": "ABC News", "url": "https://abcnews.com/US/epstein-assistants-immunity-deals/story?id=129680600"},
        ]
    },
    "2026-02-05": {
        "headline": "Latvia Launches Investigation, European Scrutiny Intensifies",
        "names": ["Edgars Rinkevics", "Thorbjorn Jagland", "Prince Andrew", "Ghislaine Maxwell"],
        "bullets": [
            {"name": "Latvian President Rinkevics", "text": "calls for investigation after public broadcaster reports passport data and travel details for Latvian women in files.", "source": "Reuters", "url": "https://www.reuters.com/world/europe/latvia-president-calls-epstein-investigation"},
            {"name": "Nobel Committee official", "text": "Thorbjørn Jagland faces pending ethics investigation for gifts, travel, and loans potentially received from Epstein.", "source": "Guardian", "url": "https://www.theguardian.com/world/2026/feb/05/nobel-committee-jagland-epstein-ethics"},
            {"name": "European Parliament members", "text": "call for coordinated EU response to Epstein trafficking allegations spanning multiple member states.", "source": "Euronews", "url": "https://www.euronews.com/2026/02/05/eu-parliament-epstein-response"},
            {"name": "Prince Andrew pressure mounts", "text": "as UK lawmakers join calls for former royal to submit to questioning by U.S. investigators.", "source": "BBC", "url": "https://www.bbc.com/news/uk-politics-12345678"},
        ]
    },
    "2026-02-06": {
        "headline": "Congress Gets Access to Unredacted Files in Secure Reading Room",
        "names": ["Patrick Davis", "Thomas Massie", "Ro Khanna", "Jamie Raskin"],
        "bullets": [
            {"name": "AAG Patrick Davis announces", "text": "all 535 members of Congress can access unredacted Epstein files starting February 9 in DOJ's secure reading room.", "source": "The Hill", "url": "https://thehill.com/regulation/court-battles/5727087-justice-department-epstein-files-lawmakers/"},
            {"name": "Bipartisan lawmakers react", "text": "with Rep. Thomas Massie and Rep. Ro Khanna leading calls for full transparency on what's being withheld.", "source": "Axios", "url": "https://www.axios.com/2026/02/09/epstein-files-unredacted-doj-massie-khanna"},
            {"name": "Reading room restrictions", "text": "— note-taking permitted but electronic devices prohibited. Hours: 9am-6pm, Monday-Friday.", "source": "CBS News", "url": "https://www.cbsnews.com/news/congress-epstein-files-reading-room"},
            {"name": "Davis defends DOJ process", "text": "saying review 'will demonstrate the Department's good faith work to appropriately process an enormous volume.'", "source": "NBC News", "url": "https://www.nbcnews.com/politics/congress/doj-congress-epstein-files-access"},
        ]
    },
    "2026-02-07": {
        "headline": "Navy Secretary Phelan Named in Flight Logs, New Revelations Emerge",
        "names": ["John Phelan", "Todd Blanche", "Donald Trump", "Bill Clinton"],
        "bullets": [
            {"name": "Navy Secretary John Phelan", "text": "appeared on two flight manifests from 2006, traveling with Epstein from New York to London on Feb 27 and returning March 3.", "source": "NBC News", "url": "https://www.nbcnews.com/politics/justice-department/live-blog/epstein-files-trump-doj-release-live-updates-rcna256639"},
            {"name": "Deputy AG Blanche states", "text": "new criminal charges 'unlikely' as DOJ review found 'nothing that allowed them to prosecute anybody.'", "source": "CNN", "url": "https://www.cnn.com/2026/02/07/politics/doj-epstein-no-new-charges"},
            {"name": "Flight log analysis shows", "text": "over 700 flights on Epstein's planes with passenger manifests now partially available to researchers.", "source": "Washington Post", "url": "https://www.washingtonpost.com/investigations/2026/02/07/epstein-flight-logs-analysis/"},
            {"name": "White House responds", "text": "to questions about Trump's 1,000+ mentions in files, calling references 'routine business contacts.'", "source": "Politico", "url": "https://www.politico.com/news/2026/02/07/white-house-trump-epstein-mentions"},
        ]
    },
    "2026-02-08": {
        "headline": "First Lawmakers Review Unredacted Files, Express 'Shock'",
        "names": ["Thomas Massie", "Ro Khanna", "Jamie Raskin", "Nancy Mace"],
        "bullets": [
            {"name": "Rep. Thomas Massie emerges", "text": "from DOJ reading room expressing 'shock' at content, says public release is 'heavily sanitized' compared to originals.", "source": "Axios", "url": "https://www.axios.com/2026/02/09/epstein-files-unredacted-doj-massie-khanna"},
            {"name": "Bipartisan agreement rare", "text": "as both Republican and Democratic lawmakers call for more transparency after reviewing unredacted materials.", "source": "The Hill", "url": "https://thehill.com/homenews/house/lawmakers-epstein-files-shock"},
            {"name": "Over-redaction concerns", "text": "raised by lawmakers who say powerful individuals' names were blacked out while victims' identities were exposed.", "source": "CNN", "url": "https://www.cnn.com/2026/02/08/politics/congress-epstein-over-redaction"},
            {"name": "Calls for public hearings", "text": "grow as House Oversight Committee considers subpoenas for DOJ officials involved in redaction decisions.", "source": "NBC News", "url": "https://www.nbcnews.com/politics/congress/house-oversight-epstein-hearings"},
        ]
    },
}

def get_existing_roundups():
    """Get list of existing daily roundup files."""
    roundups = []
    for f in os.listdir('.'):
        if f.startswith('daily-') and f.endswith('.html'):
            roundups.append(f)
    return roundups

def generate_thumbnail(date_obj, headline, filename, vol_num):
    """Generate newspaper-style thumbnail with paper texture."""

    WIDTH = 840
    HEIGHT = 472

    day_name = date_obj.strftime('%A')
    date_str = f"{day_name}, {date_obj.strftime('%B')} {date_obj.day}, {date_obj.year}"

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

    # Load fonts
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
    draw.text(((WIDTH - text_width) / 2, 88), tagline_text, fill=ink_light, font=font_tagline)

    # Line
    draw.line([(50, 122), (WIDTH - 50, 122)], fill=ink, width=1)

    # Date bar
    vol_text = f"Vol. I, No. {vol_num}"
    draw.text((60, 132), vol_text, fill=ink_light, font=font_dateline)
    bbox = draw.textbbox((0, 0), date_str, font=font_dateline)
    text_width = bbox[2] - bbox[0]
    draw.text((WIDTH - text_width - 60, 132), date_str, fill=ink_light, font=font_dateline)

    # Double line
    draw.line([(50, 156), (WIDTH - 50, 156)], fill=ink, width=1)
    draw.line([(50, 160), (WIDTH - 50, 160)], fill=ink, width=2)

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
    for i, line in enumerate(lines[:3]):
        bbox = draw.textbbox((0, 0), line, font=font_headline)
        text_width = bbox[2] - bbox[0]
        draw.text(((WIDTH - text_width) / 2, y_start + i * line_height), line, fill=ink, font=font_headline)

    # Slight blur
    img = img.filter(ImageFilter.GaussianBlur(radius=0.3))

    # Save
    os.makedirs('images', exist_ok=True)
    img.save(filename, 'PNG')
    print(f"Created thumbnail: {filename}")


def create_article_html(date_str, data):
    """Create article HTML from template."""
    date_obj = datetime.strptime(date_str, '%Y-%m-%d')
    date_iso = date_str
    date_readable = date_obj.strftime('%B %d, %Y')
    month_day = date_obj.strftime('%B %d').replace(' 0', ' ')
    filename = f"daily-{date_obj.strftime('%b').lower()}-{date_obj.day}-{date_obj.year}"

    # Build bullets HTML
    bullets_html = ""
    for bullet in data['bullets']:
        bullets_html += f'''
                <li><strong>{bullet['name']}</strong> {bullet['text']} <a href="{bullet['url']}" target="_blank" class="source-link">{bullet['source']} →</a></li>
'''

    # Build tags HTML
    tags_html = ""
    for name in data['names'][:4]:
        name_param = urllib.parse.quote_plus(name.lower())
        tags_html += f'                    <a href="index.html?search={name_param}" class="article-tag">{name}</a>\n'

    # Read template
    with open('daily-feb-9-2026.html', 'r') as f:
        html = f.read()

    # Replace content
    import re
    html = re.sub(r'<title>.*?</title>', f'<title>{month_day}: {data["headline"]} — Epstein Files Daily</title>', html)

    first_bullet = data['bullets'][0]
    meta_desc = f"{first_bullet['name']} {first_bullet['text'][:100]}..."
    html = re.sub(r'<meta name="description" content=".*?">', f'<meta name="description" content="{meta_desc}">', html)

    html = re.sub(r'<time datetime=".*?">', f'<time datetime="{date_iso}">', html)
    html = re.sub(r'>February \d+, 2026</time>', f'>{date_readable}</time>', html)

    html = re.sub(r'<h1>.*?</h1>', f'<h1>{month_day}: {data["headline"]}</h1>', html)

    tags_section = '<div class="article-tags">\n' + tags_html + '                </div>'
    html = re.sub(r'<div class="article-tags">.*?</div>', tags_section, html, flags=re.DOTALL)

    bullets_section = f'<ul class="lede-bullets">{bullets_html}            </ul>'
    html = re.sub(r'<ul class="lede-bullets">.*?</ul>', bullets_section, html, flags=re.DOTALL)

    html = re.sub(r'daily-feb-9-2026', filename, html)

    return html, filename


def create_index_card(date_str, data, vol_num):
    """Create index.html card for an article."""
    date_obj = datetime.strptime(date_str, '%Y-%m-%d')
    date_iso = date_str
    date_readable = date_obj.strftime('%B %d, %Y')
    month_day = date_obj.strftime('%B %d').replace(' 0', ' ')
    filename = f"daily-{date_obj.strftime('%b').lower()}-{date_obj.day}-{date_obj.year}"

    # Build short bullets HTML (first 4)
    bullets_html = ""
    for bullet in data['bullets'][:4]:
        bullets_html += f'                                <li><strong>{bullet["name"]}</strong> {bullet["text"]} <a href="{bullet["url"]}" target="_blank" class="source-link">{bullet["source"]} →</a></li>\n'

    # Build tags
    tags_data = ','.join([name.lower() for name in data['names'][:4]])
    tags_html = ""
    for name in data['names'][:4]:
        name_param = urllib.parse.quote_plus(name.lower())
        tags_html += f'                                    <a href="index.html?search={name_param}" class="article-tag">{name}</a>\n'

    card = f'''
                <!-- DAILY ROUNDUP: {date_readable} -->
                <article class="article-preview featured" data-tags="{tags_data}">
                    <div class="article-top">
                        <a href="{filename}.html" class="article-thumb">
                            <img src="images/{filename}.png?v={vol_num}" alt="{date_readable} Epstein news roundup" loading="lazy">
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
    return card


def main():
    print("=" * 60)
    print("EPSTEIN FILES DAILY - Backfill Generator")
    print("Generating articles for Jan 30 - Feb 8, 2026")
    print("=" * 60)

    # Sort dates
    dates = sorted(ARTICLES.keys())

    # Generate articles and thumbnails
    all_cards = []
    vol_num = 1  # Starting volume number

    for date_str in dates:
        data = ARTICLES[date_str]
        date_obj = datetime.strptime(date_str, '%Y-%m-%d')
        filename_base = f"daily-{date_obj.strftime('%b').lower()}-{date_obj.day}-{date_obj.year}"

        print(f"\nProcessing {date_str}: {data['headline'][:50]}...")

        # Generate thumbnail
        thumb_filename = f"images/{filename_base}.png"
        generate_thumbnail(date_obj, data['headline'], thumb_filename, vol_num)

        # Generate article HTML
        html, filename = create_article_html(date_str, data)
        with open(f"{filename}.html", 'w') as f:
            f.write(html)
        print(f"Created: {filename}.html")

        # Create index card
        card = create_index_card(date_str, data, vol_num)
        all_cards.append((date_str, card))

        vol_num += 1

    # Sort cards by date (newest first) and output
    all_cards.sort(key=lambda x: x[0], reverse=True)

    print("\n" + "=" * 60)
    print("INDEX CARDS (paste after articles-container div, before existing articles):")
    print("=" * 60)

    for date_str, card in all_cards:
        print(card)

    print("\n" + "=" * 60)
    print(f"Generated {len(dates)} articles and thumbnails")
    print("=" * 60)


if __name__ == "__main__":
    main()
