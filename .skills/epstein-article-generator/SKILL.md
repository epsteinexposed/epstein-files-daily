---
name: epstein-daily-roundup
description: |
  Generate daily news roundups for Epstein Files Daily website.
  TRIGGERS: "daily roundup", "epstein news", "publish daily", "today's roundup"
  Aggregates news from multiple sources, writes brief summaries, creates date thumbnails, updates the site, and pushes to GitHub.
---

# Epstein Daily Roundup Generator

Generate daily news roundups for epsteinfilesdaily.com that aggregate coverage from multiple news sources.

## Content Model

Each "article" is a **daily roundup** containing:
- **Date-based headline** (e.g., "February 9: Silicon Valley's Epstein Problem Gets Worse")
- **3-4 sentence lede** summarizing the biggest revelations of the day
- **5-8 links** to external news sources with brief context
- **Name-only tags** for building name pages (e.g., "Peter Thiel", "Elon Musk")

---

## Workflow

### Step 1: Find Today's News

Search for recent Epstein-related news coverage:

```bash
# Use web search to find recent coverage
```

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

### Step 3: Write the Lede

Write 3-4 sentences summarizing the day's biggest revelations:

```html
<p class="lede">
    Today's DOJ document release reveals new Silicon Valley connections.
    Peter Thiel appears in thousands of pages with lunch meetings spanning 2014-2017.
    Meanwhile, documents show Google co-founder Sergey Brin received outreach from
    Ghislaine Maxwell after meeting at TED in 2003.
</p>
```

**Lede guidelines:**
- Focus on the most newsworthy revelations
- Name specific people and connections
- Be factual and source-based
- Create urgency without sensationalism

### Step 4: Create Link Cards

Each link card includes:
- **Source name** (e.g., "NBC NEWS", "SF CHRONICLE")
- **Headline** (link to original article)
- **Brief context** (1-2 sentences explaining what this story adds)

```html
<div class="link-card">
    <span class="source">NBC NEWS</span>
    <h3><a href="https://..." target="_blank">Jeffrey Epstein files reveal deep tech ties</a></h3>
    <p>First major report on the new DOJ release, detailing connections to Musk, Gates, Thiel, and Brin.</p>
</div>
```

**Aim for 5-8 links per roundup** - enough to be comprehensive without overwhelming.

### Step 5: Generate Date Thumbnail

Use the auto-generation script:

```bash
cd /sessions/dreamy-epic-mccarthy/mnt/AI\ experiment
python generate_daily_thumb.py "Feb 9, 2026" "Silicon Valley Ties"
```

This creates `images/daily-feb-9-2026.png` with:
- Red accent bar at top
- Date prominently displayed
- Theme text below
- "EPSTEIN FILES DAILY" branding
- Document number styling

**Thumbnail filename format:** `daily-[month]-[day]-[year].png` (lowercase)

### Step 6: Create the Roundup HTML

**Use the daily template format:**

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>[Month Day]: [Theme Headline] | Epstein Files Daily</title>
    <!-- ... standard meta tags ... -->
</head>
<body>
    <header><!-- Standard header --></header>

    <main>
        <article class="daily-roundup">
            <div class="article-meta">
                <time datetime="YYYY-MM-DD">[Full Date]</time>
                <div class="tags">
                    <a href="name-[firstname]-[lastname].html">[Full Name]</a>
                    <!-- More name tags -->
                </div>
            </div>

            <h1>[Month Day]: [Theme Headline]</h1>

            <p class="lede">[3-4 sentence summary]</p>

            <section class="links-section">
                <h2>Today's Coverage</h2>

                <div class="link-card">
                    <span class="source">[SOURCE NAME]</span>
                    <h3><a href="[URL]" target="_blank">[Headline]</a></h3>
                    <p>[Brief context]</p>
                </div>

                <!-- More link cards (5-8 total) -->
            </section>
        </article>
    </main>

    <footer><!-- Standard footer --></footer>
</body>
</html>
```

**Filename format:** `daily-[month]-[day]-[year].html` (lowercase)

### Step 7: Update index.html

Add the new roundup card to index.html:

```html
<!-- DAILY ROUNDUP: [DATE] -->
<article class="article-preview featured" data-tags="[name1] [name2] [name3]">
    <div class="article-top">
        <a href="daily-[month]-[day]-[year].html" class="article-thumb">
            <img src="images/daily-[month]-[day]-[year].png?v=1" alt="[Date] Epstein news roundup" loading="lazy">
        </a>
        <div class="article-title-section">
            <div class="article-meta">
                <div class="article-tags">
                    <a href="name-[firstname]-[lastname].html" class="article-tag">[Full Name]</a>
                    <!-- More name tags -->
                </div>
                <time datetime="YYYY-MM-DD" class="article-date">[Month DD, YYYY]</time>
            </div>
            <h2><a href="daily-[month]-[day]-[year].html">[Month Day]: [Theme Headline]</a></h2>
            <p class="lede">[Same 3-4 sentence lede from article]</p>
            <a href="daily-[month]-[day]-[year].html" class="read-more">Read full roundup</a>
        </div>
    </div>
</article>
```

**Tag format in `data-tags`:** lowercase full names with spaces (e.g., `data-tags="peter thiel elon musk sergey brin"`)

### Step 8: Update feed.xml

Add new `<item>` with RFC 822 date format:

```xml
<item>
    <title>[Month Day]: [Theme Headline]</title>
    <link>https://epsteinfilesdaily.com/daily-[month]-[day]-[year].html</link>
    <description>[Lede text]</description>
    <pubDate>[RFC 822 date]</pubDate>
    <guid>https://epsteinfilesdaily.com/daily-[month]-[day]-[year].html</guid>
</item>
```

### Step 9: Verify and Publish

**Run these checks before committing:**

```bash
# 1. Thumbnail exists
ls images/daily-*.png

# 2. Roundup HTML exists
ls daily-*.html

# 3. index.html has the card with thumbnail
grep "daily-[month]-[day]-[year].png" index.html

# 4. Feed has the entry
grep "daily-[month]-[day]-[year]" feed.xml
```

**Commit and push:**

```bash
git add daily-*.html index.html feed.xml images/daily-*.png
git commit -m "Daily roundup: [Month Day] - [Theme]"
git push
```

---

## Name Pages

Name pages aggregate all roundups mentioning a specific person. These are built from the tags.

**Example:** `name-peter-thiel.html` shows:
- Profile header (name, title, stats)
- Key facts from the files
- All coverage mentioning this person (links to roundups + external sources)
- Related names

**Create/update name pages when:**
- A person appears in 3+ roundups
- There's significant new information about them

---

## Key Rules

1. **3+ links minimum**: Don't publish a roundup with fewer than 3 genuinely new stories
2. **5-8 links ideal**: Comprehensive but not overwhelming
3. **Names only for tags**: Build name pages, not category pages
4. **Real sources only**: Link to actual news coverage, not fabricated articles
5. **Brief context**: 1-2 sentences per link, not full summaries
6. **Daily thumbnails**: Auto-generate with date and theme

---

## Quick Reference

**File naming:**
- Roundup: `daily-feb-9-2026.html`
- Thumbnail: `images/daily-feb-9-2026.png`
- Name page: `name-peter-thiel.html`

**Thumbnail generation:**
```bash
python generate_daily_thumb.py "Feb 9, 2026" "Silicon Valley Ties"
```

**Tag format:**
- `data-tags`: lowercase with spaces (`peter thiel elon musk`)
- Visible tags: proper case (`Peter Thiel`)
- Links: to name pages (`name-peter-thiel.html`)

**Don't publish if:**
- Fewer than 3 new links
- No significant new revelations
- Just rehashing old news
