---
name: epstein-daily-roundup
description: |
  Generate daily news roundups for Epstein Files Daily website.
  TRIGGERS: "daily roundup", "epstein news", "publish daily", "today's roundup"
  Aggregates news from multiple sources, writes brief summaries, creates newspaper-style thumbnails, updates the site, and pushes to GitHub.
---

# Epstein Daily Roundup Generator

Generate daily news roundups for epsteinfilesdaily.com that aggregate coverage from multiple news sources.

## Content Model

Each "article" is a **daily roundup** containing:
- **Newspaper-style thumbnail** with headline
- **"[Month Day]: Read Daily Summary →"** as the clickable headline on homepage
- **4-6 bullet points** — SHORT on homepage (one line), LONGER on article page (2-4 sentences)
- **Name-only tags** for building name pages (e.g., "Peter Thiel", "Elon Musk")

---

## Workflow

### Step 1: Find Today's News

Search for recent Epstein-related news coverage:

**Sources to check:**
- Major news outlets (NBC, CNBC, NYT, WSJ, PBS, etc.)
- Local newspapers covering specific angles
- Congressional/government releases
- Court document releases

**Minimum requirement:** You need **3+ genuinely new links** to publish a daily roundup. If there aren't enough new stories, don't publish that day.

### Step 2: Identify Names Mentioned

Extract all **person names** mentioned in the coverage. These become your tags.

**Tag rules:**
- ONLY use full person names (e.g., "Peter Thiel", "Elon Musk")
- NO categories (not "Tech", "Silicon Valley", "Politics")
- NO company names (not "Google", "PayPal")
- NO last names only (not "Thiel", "Musk")
- Tags are used to build name-specific pages

### Step 3: Write TWO Versions of Bullets

You need **two versions** of the bullets:

#### Homepage Bullets (SHORT - one line each)
```html
<ul class="lede-bullets">
    <li><strong>Peter Thiel</strong> appears in thousands of documents spanning 2014-2017. <a href="https://cnbc.com/..." target="_blank" class="source-link">CNBC →</a></li>
    <li><strong>20+ tech executives</strong> maintained regular contact — far more than previously known. <a href="https://nbcnews.com/..." target="_blank" class="source-link">NBC News →</a></li>
    <li><strong>Elon Musk</strong> invited to private dinner at Baumé with Zuckerberg and Thiel. <a href="https://sfchronicle.com/..." target="_blank" class="source-link">SF Chronicle →</a></li>
    <li><strong>Sergey Brin</strong> targeted by Maxwell after meeting at TED 2003. <a href="https://pbs.org/..." target="_blank" class="source-link">PBS →</a></li>
</ul>
```

#### Article Page Bullets (LONGER - 2-4 sentences each)
```html
<ul class="lede-bullets">
    <li><strong>Peter Thiel</strong> appears in thousands of documents spanning years of lunch meetings from 2014-2017. Emails show Epstein's team coordinating visits to Thiel's San Francisco office and arranging private dinners at high-end restaurants. <a href="https://cnbc.com/..." target="_blank" class="source-link">CNBC →</a></li>

    <li><strong>20+ tech executives</strong> maintained regular contact with Epstein — far more than previously known. The documents reveal a systematic effort to cultivate Silicon Valley's most powerful figures, with detailed scheduling and follow-up correspondence. <a href="https://nbcnews.com/..." target="_blank" class="source-link">NBC News →</a></li>

    <li><strong>Elon Musk</strong> was invited to a private dinner at Michelin-starred Baumé in Palo Alto alongside Zuckerberg and Thiel. The restaurant was bought out entirely for the exclusive gathering in August 2015. <a href="https://sfchronicle.com/..." target="_blank" class="source-link">SF Chronicle →</a></li>

    <li><strong>Sergey Brin</strong> received outreach from Ghislaine Maxwell after meeting at TED 2003. Maxwell's emails describe the Google co-founder as someone she wanted to "cultivate" for Epstein's network. <a href="https://pbs.org/..." target="_blank" class="source-link">PBS →</a></li>
</ul>
```

**Bullet guidelines:**
- Homepage: **ONE LINE per bullet** — fits neatly next to thumbnail
- Article page: **2-4 sentences per bullet** — full context
- Lead each bullet with a **bolded name** or subject
- End each bullet with an **inline source link** (format: `SOURCE →`)

### Step 4: Generate Newspaper-Style Thumbnail

Create a newspaper "Morning Edition" style thumbnail using Python:

```python
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import random

WIDTH = 840
HEIGHT = 472

# Create aged paper background
img = Image.new('RGB', (WIDTH, HEIGHT), '#f4ead5')
draw = ImageDraw.Draw(img)
pixels = img.load()

# Add paper texture - noise and vignette
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
font_masthead = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf", 52)
font_tagline = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSerif-Italic.ttf", 15)
font_dateline = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf", 12)
font_headline = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf", 52)

# Border
draw.rectangle([(8, 8), (WIDTH-9, HEIGHT-9)], outline='#c4b89c', width=1)

# Masthead: "EPSTEIN FILES DAILY"
masthead_text = "EPSTEIN FILES DAILY"
bbox = draw.textbbox((0, 0), masthead_text, font=font_masthead)
text_width = bbox[2] - bbox[0]
draw.text(((WIDTH - text_width) / 2, 28), masthead_text, fill=ink, font=font_masthead)

# Tagline
tagline_text = "Comprehensive Coverage of the DOJ Document Releases"
bbox = draw.textbbox((0, 0), tagline_text, font=font_tagline)
text_width = bbox[2] - bbox[0]
draw.text(((WIDTH - text_width) / 2, 90), tagline_text, fill=ink_light, font=font_tagline)

# Line under masthead
draw.line([(50, 118), (WIDTH - 50, 118)], fill=ink, width=1)

# Date bar (use actual date - e.g., "Monday, February 9, 2026")
vol_text = "Vol. I, No. XX"  # Increment number for each edition
date_text = "[Day], [Month] [Day], [Year]"
draw.text((60, 128), vol_text, fill=ink_light, font=font_dateline)
bbox = draw.textbbox((0, 0), date_text, font=font_dateline)
text_width = bbox[2] - bbox[0]
draw.text((WIDTH - text_width - 60, 128), date_text, fill=ink_light, font=font_dateline)

# Double line
draw.line([(50, 152), (WIDTH - 50, 152)], fill=ink, width=1)
draw.line([(50, 156), (WIDTH - 50, 156)], fill=ink, width=2)

# Headline (split across 3 lines, centered)
headline_lines = ["Silicon Valley's", "Epstein Problem", "Gets Worse"]
y_start = 190
line_height = 70
for i, line in enumerate(headline_lines):
    bbox = draw.textbbox((0, 0), line, font=font_headline)
    text_width = bbox[2] - bbox[0]
    draw.text(((WIDTH - text_width) / 2, y_start + i * line_height), line, fill=ink, font=font_headline)

# Slight blur for print effect
img = img.filter(ImageFilter.GaussianBlur(radius=0.3))

# Save
img.save("images/daily-[month]-[day]-[year].png", 'PNG')
```

**Thumbnail filename format:** `daily-[month]-[day]-[year].png` (lowercase)

### Step 5: Create the Article Page HTML

Copy the structure from `daily-feb-9-2026.html` exactly, including:
- Full header with logo, search box, email signup, theme toggle
- Back link to homepage
- Tags linking to search
- **Article page headline format:** `[Month Day]: [Theme Headline]` (e.g., "February 9: Silicon Valley's Epstein Problem Gets Worse")
- **LONGER bullets** (2-4 sentences each)
- Newsletter signup box
- Share buttons (Facebook, Twitter/X, Bluesky, Email)

**Article page template structure:**
```html
<!DOCTYPE html>
<html lang="en" class="light-mode">
<head>
    <meta charset="UTF-8">
    <title>[Month Day]: [Theme Headline] — Epstein Files Daily</title>
    <!-- Copy full <head> from daily-feb-9-2026.html -->
</head>
<body>
    <header role="banner">
        <!-- Copy FULL header from daily-feb-9-2026.html including:
             - Logo with icon
             - Search box with dropdown
             - Email signup
             - Theme toggle -->
    </header>

    <main>
        <a href="index.html" class="back-link">← Back to all days</a>

        <article class="article">
            <div class="article-meta">
                <div class="article-tags">
                    <a href="index.html?search=[name]" class="article-tag">[Full Name]</a>
                    <!-- More tags -->
                </div>
                <time datetime="YYYY-MM-DD">[Month Day, Year]</time>
            </div>

            <h1>[Month Day]: [Theme Headline]</h1>

            <ul class="lede-bullets">
                <!-- LONGER bullets (2-4 sentences each) -->
                <li><strong>[Name]</strong> [2-4 sentences with full context]. <a href="[URL]" target="_blank" class="source-link">SOURCE →</a></li>
                <!-- 4-6 bullets total -->
            </ul>

            <section class="newsletter">
                <h3>Get the Top Epstein Stories Delivered Straight to Your Inbox</h3>
                <form class="newsletter-form" action="https://epstein-exposed.us13.list-manage.com/subscribe/post?u=dbf04846cbc14c3a4d734f311&amp;id=a2f4925a23&amp;f_id=00cdace2f0" method="post" target="_blank">
                    <input type="email" name="EMAIL" placeholder="your@email.com" required>
                    <div style="position:absolute;left:-5000px" aria-hidden="true"><input type="text" name="b_dbf04846cbc14c3a4d734f311_a2f4925a23" tabindex="-1" value=""></div>
                    <button type="submit">Subscribe</button>
                </form>
            </section>

            <div class="share-section">
                <div class="share-label">Share today's roundup</div>
                <div class="share-buttons">
                    <a href="https://www.facebook.com/sharer/sharer.php?u=https%3A%2F%2Fepsteinfilesdaily.com%2F[filename]" target="_blank" rel="noopener" class="share-btn facebook">
                        <svg viewBox="0 0 24 24" fill="currentColor"><path d="M24 12.073c0-6.627-5.373-12-12-12s-12 5.373-12 12c0 5.99 4.388 10.954 10.125 11.854v-8.385H7.078v-3.47h3.047V9.43c0-3.007 1.792-4.669 4.533-4.669 1.312 0 2.686.235 2.686.235v2.953H15.83c-1.491 0-1.956.925-1.956 1.874v2.25h3.328l-.532 3.47h-2.796v8.385C19.612 23.027 24 18.062 24 12.073z"/></svg>
                        <span>Facebook</span>
                    </a>
                    <a href="https://twitter.com/intent/tweet?url=https%3A%2F%2Fepsteinfilesdaily.com%2F[filename]&text=[URL-encoded headline]" target="_blank" rel="noopener" class="share-btn twitter">
                        <svg viewBox="0 0 24 24" fill="currentColor"><path d="M18.244 2.25h3.308l-7.227 8.26 8.502 11.24H16.17l-5.214-6.817L4.99 21.75H1.68l7.73-8.835L1.254 2.25H8.08l4.713 6.231zm-1.161 17.52h1.833L7.084 4.126H5.117z"/></svg>
                        <span>X / Twitter</span>
                    </a>
                    <a href="https://bsky.app/intent/compose?text=[URL-encoded headline]%20https%3A%2F%2Fepsteinfilesdaily.com%2F[filename]" target="_blank" rel="noopener" class="share-btn bluesky">
                        <svg viewBox="0 0 24 24" fill="currentColor"><path d="M12 10.8c-1.087-2.114-4.046-6.053-6.798-7.995C2.566.944 1.561 1.266.902 1.565.139 1.908 0 3.08 0 3.768c0 .69.378 5.65.624 6.479.815 2.736 3.713 3.66 6.383 3.364.136-.02.275-.039.415-.056-.138.022-.276.04-.415.056-3.912.58-7.387 2.005-2.83 7.078 5.013 5.19 6.87-1.113 7.823-4.308.953 3.195 2.05 9.271 7.733 4.308 4.267-4.308 1.172-6.498-2.74-7.078a8.741 8.741 0 0 1-.415-.056c.14.017.279.036.415.056 2.67.297 5.568-.628 6.383-3.364.246-.828.624-5.79.624-6.478 0-.69-.139-1.861-.902-2.206-.659-.298-1.664-.62-4.3 1.24C16.046 4.748 13.087 8.687 12 10.8Z"/></svg>
                        <span>Bluesky</span>
                    </a>
                    <a href="mailto:?subject=[Month Day] Epstein Files Roundup&body=https%3A%2F%2Fepsteinfilesdaily.com%2F[filename]" class="share-btn email">
                        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="2" y="4" width="20" height="16" rx="2"/><path d="m22 6-10 7L2 6"/></svg>
                        <span>Email</span>
                    </a>
                </div>
            </div>
        </article>
    </main>

    <footer>
        <p>&copy; 2026 Epstein Files Daily · <a href="archive.html">Archive</a> · <a href="privacy.html">Privacy</a></p>
    </footer>

    <script>
        <!-- Copy full script from daily-feb-9-2026.html -->
    </script>
</body>
</html>
```

**Filename format:** `daily-[month]-[day]-[year].html` (lowercase)

### Step 6: Update index.html

Add the new roundup card to index.html (insert at top of `#articles-container`):

```html
<!-- DAILY ROUNDUP: [DATE] -->
<article class="article-preview featured" data-tags="[name1],[name2],[name3]">
    <div class="article-top">
        <a href="daily-[month]-[day]-[year].html" class="article-thumb">
            <img src="images/daily-[month]-[day]-[year].png?v=1" alt="[Date] Epstein news roundup" loading="lazy">
        </a>
        <div class="article-title-section">
            <div class="article-meta">
                <div class="article-tags">
                    <a href="index.html?search=[name]" class="article-tag">[Full Name]</a>
                    <!-- More tags -->
                </div>
                <time datetime="YYYY-MM-DD" class="article-date">[Month Day, Year]</time>
            </div>
            <h2><a href="daily-[month]-[day]-[year].html">[Month Day]: Read Daily Summary →</a></h2>
            <ul class="lede-bullets">
                <!-- SHORT bullets (one line each) -->
                <li><strong>[Name]</strong> [one line summary]. <a href="[URL]" target="_blank" class="source-link">SOURCE →</a></li>
                <li><strong>[Name]</strong> [one line summary]. <a href="[URL]" target="_blank" class="source-link">SOURCE →</a></li>
                <li><strong>[Name]</strong> [one line summary]. <a href="[URL]" target="_blank" class="source-link">SOURCE →</a></li>
                <li><strong>[Name]</strong> [one line summary]. <a href="[URL]" target="_blank" class="source-link">SOURCE →</a></li>
            </ul>
        </div>
    </div>
</article>
```

**IMPORTANT:**
- Homepage headline: `[Month Day]: Read Daily Summary →` (NOT the theme headline)
- Homepage bullets: **ONE LINE EACH** (fits next to thumbnail)
- NO "Read full roundup" link at bottom
- Text turns RED on hover (CSS already handles this)

**Tag format in `data-tags`:** lowercase full names with commas (e.g., `data-tags="peter thiel,elon musk,sergey brin"`)

### Step 7: Update feed.xml

Add new `<item>` with RFC 822 date format:

```xml
<item>
    <title>[Month Day]: [Theme Headline]</title>
    <link>https://epsteinfilesdaily.com/daily-[month]-[day]-[year].html</link>
    <description>[First bullet summary]</description>
    <pubDate>[RFC 822 date, e.g., Mon, 09 Feb 2026 00:00:00 GMT]</pubDate>
    <guid>https://epsteinfilesdaily.com/daily-[month]-[day]-[year].html</guid>
</item>
```

### Step 8: Verify and Publish

**Run these checks before committing:**

```bash
# 1. Thumbnail exists
ls images/daily-*.png

# 2. Roundup HTML exists
ls daily-*.html

# 3. index.html has the card
grep "daily-[month]-[day]-[year]" index.html

# 4. Feed has the entry
grep "daily-[month]-[day]-[year]" feed.xml
```

**Commit and push:**

```bash
git add daily-*.html index.html feed.xml images/daily-*.png
git commit -m "Daily roundup: [Month Day] - [Theme]

Co-Authored-By: Claude Opus 4.5 <noreply@anthropic.com>"
git push
```

---

## Key Differences: Homepage vs Article Page

| Element | Homepage Card | Article Page |
|---------|--------------|--------------|
| Headline | "[Month Day]: Read Daily Summary →" | "[Month Day]: [Theme Headline]" |
| Bullets | ONE LINE each (fits next to thumbnail) | 2-4 SENTENCES each (full context) |
| "Read full roundup" link | NO | N/A |
| Newsletter signup | NO | YES |
| Share buttons | NO | YES (Facebook, Twitter, Bluesky, Email) |

---

## Quick Reference

**File naming:**
- Roundup: `daily-feb-9-2026.html`
- Thumbnail: `images/daily-feb-9-2026.png`
- Name page: `name-peter-thiel.html`

**Homepage bullet format (SHORT):**
```html
<li><strong>Name</strong> [one line]. <a href="URL" target="_blank" class="source-link">SOURCE →</a></li>
```

**Article bullet format (LONG):**
```html
<li><strong>Name</strong> [2-4 sentences]. <a href="URL" target="_blank" class="source-link">SOURCE →</a></li>
```

**Tag format:**
- `data-tags`: lowercase with commas (`peter thiel,elon musk`)
- Visible tags: proper case (`Peter Thiel`)
- Links: to search (`index.html?search=peter+thiel`)

**CSS Hover Effects (already implemented):**
- Headline "Read Daily Summary →" turns RED on hover
- Source links turn RED on hover

**Don't publish if:**
- Fewer than 4 distinct stories
- No significant new revelations
- Just rehashing old news
