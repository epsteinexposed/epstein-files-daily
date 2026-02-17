---
name: epstein-daily-roundup
description: |
  Generate daily news roundups for Epstein Files Daily website.
  TRIGGERS: "daily roundup", "epstein news", "publish daily", "today's roundup"
  Aggregates news from multiple sources, writes brief summaries, creates newspaper-style thumbnails, updates the site (including name pages, sitemap, SEO tags), and pushes to GitHub.
---

# Epstein Daily Roundup Generator

Generate daily news roundups for epsteinfilesdaily.com that aggregate coverage from multiple news sources.

## Content Model

Each "article" is a **daily roundup** containing:
- **Newspaper-style thumbnail** with a headline that includes at least one specific person's name
- **"[Month Day]: Read Daily Summary →"** as the clickable headline on homepage
- **4-6 bullet points** — SHORT on homepage (one line), LONGER on article page (2-4 sentences)
- **Name-only tags** for building name pages (e.g., "Peter Thiel", "Elon Musk")
- **SEO tags** — canonical URL, Open Graph, Twitter Cards, JSON-LD NewsArticle schema

---

## Workflow

### Step 1: Find Today's News

Search for recent Epstein-related news coverage. **Prioritize stories about specific INDIVIDUALS over generic government process stories.**

**Search queries to use (in order of priority):**
- Specific people: "epstein prince andrew", "epstein bill gates", "epstein les wexner", "epstein jean-luc brunel"
- Victims/survivors: "epstein victim survivor lawsuit"
- Specific evidence: "epstein flight logs names", "epstein island little st james"
- International: "epstein europe investigation", "epstein intelligence FBI CIA"
- Broader: "jeffrey epstein investigation new", "epstein connections revealed billionaire", "epstein documents unsealed names"

**Sources to check:**
- International outlets (Al Jazeera, BBC, CNN International, Reuters) — European investigations often have the most interesting individual stories
- Investigative journalism (ProPublica, The Intercept, local newspapers)
- Legal/court filings and victim advocate organizations
- Major US outlets (NBC, CNBC, NYT, WSJ, PBS) — but look past the DOJ headlines to find the individual stories within

**STORY SELECTION PRIORITIES (in order):**
1. Stories naming specific individuals connected to Epstein (associates, visitors, flight log names, accusers, victims, enablers)
2. Lawsuits, investigations, or legal actions against specific people
3. International angles (European investigations, foreign connections, charges abroad)
4. Victim/survivor stories and advocacy efforts
5. **LAST RESORT:** Government process stories (DOJ releases, AG statements) — include AT MOST ONE of these per roundup

**AVOID:**
- Do NOT lead with Pam Bondi or DOJ release process stories — these have been covered extensively
- Do NOT make "files released" or "documents unsealed" the main theme
- If the only stories available are about DOJ/Bondi, dig deeper into WHO is named in those documents rather than the release process itself

**Minimum requirement:** You need **3+ genuinely new links** to publish a daily roundup. If there aren't enough new stories, don't publish that day.

### Step 2: Identify Names Mentioned

Extract all **person names** mentioned in the coverage. These become your tags.

**Tag rules:**
- ONLY use full person names (e.g., "Peter Thiel", "Elon Musk")
- NO categories (not "Tech", "Silicon Valley", "Politics")
- NO company names (not "Google", "PayPal")
- NO last names only (not "Thiel", "Musk")
- Tags are used to build name-specific pages at `/names/[slug].html`

### Step 3: Write the Theme Headline

The theme headline appears on the thumbnail and article page. It **MUST**:
- Include at least one specific person's name (e.g., "Gates, Musk Linked to Epstein Network")
- Be distinct from recent headlines — **NEVER** use generic headlines like "DOJ Releases Files" or "New Documents Released"
- Lead with the most newsworthy person

Also identify a `featured_name` — the most prominent person from the headline.

### Step 4: Write TWO Versions of Bullets

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

    <li><strong>Elon Musk</strong> was invited to a private dinner at Michelin-starred Baumé in Palo Alto alongside Zuckerberg and Thiel. The restaurant was bought out entirely for the exclusive gathering in August 2015. <a href="https://sfchronicle.com/..." target="_blank" class="source-link">SF Chronicle →</a></li>
</ul>
```

**Bullet guidelines:**
- Homepage: **ONE LINE per bullet** — fits neatly next to thumbnail
- Article page: **2-4 sentences per bullet** — full context
- Lead each bullet with a **bolded name** or subject
- End each bullet with an **inline source link** (format: `SOURCE →`)

### Step 5: Generate Newspaper-Style Thumbnail

Create a newspaper "Morning Edition" style thumbnail (840x472) using Python/Pillow:
- Aged paper background with texture and vignette
- "EPSTEIN FILES DAILY" masthead
- "Comprehensive Coverage of the DOJ Document Releases" tagline
- Date bar with Vol. number
- **Headline that includes at least one person's name** — no generic "DOJ Releases" headlines

**Thumbnail filename format:** `images/daily-[month]-[day]-[year].png` (lowercase)

### Step 6: Create the Article Page HTML

Copy the structure from an existing article (e.g., `daily-feb-9-2026.html`), updating:
- Title, meta description
- **SEO tags:** canonical URL, Open Graph, Twitter Cards, JSON-LD NewsArticle schema
- Tags linking to **name pages** (format: `/names/[name-slug].html`)
- **LONGER bullets** (2-4 sentences each)
- Date, headline, share buttons

**Tag link format (name pages, NOT search):**
```html
<a href="/names/peter-thiel.html" class="article-tag">Peter Thiel</a>
```

### Step 7: Update index.html

Add the new roundup card at the top of `#articles-container`:

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
                    <a href="/names/[name-slug].html" class="article-tag">[Full Name]</a>
                </div>
                <time datetime="YYYY-MM-DD" class="article-date">[Month Day, Year]</time>
            </div>
            <h2><a href="daily-[month]-[day]-[year].html">[Month Day]: Read Daily Summary →</a></h2>
            <ul class="lede-bullets">
                <!-- SHORT bullets (one line each) -->
            </ul>
        </div>
    </div>
</article>
```

**IMPORTANT:**
- Homepage headline: `[Month Day]: Read Daily Summary →` (NOT the theme headline)
- Homepage bullets: **ONE LINE EACH** (fits next to thumbnail)
- Tag links go to `/names/[slug].html` (NOT `index.html?search=`)

### Step 8: Update feed.xml (with full content for newsletters)

Add new `<item>` with both `<description>` and `<content:encoded>`:

```xml
<item>
    <title>[Month Day]: [Theme Headline]</title>
    <link>https://epsteinfilesdaily.com/daily-[month]-[day]-[year].html</link>
    <guid>https://epsteinfilesdaily.com/daily-[month]-[day]-[year].html</guid>
    <pubDate>[RFC 822 date]</pubDate>
    <description>[First bullet summary]</description>
    <content:encoded><![CDATA[
<ul>
<li><strong>[Name]</strong> [Full bullet text]. <a href="[URL]">[Source] →</a></li>
<!-- All bullets with full content -->
</ul>
    ]]></content:encoded>
</item>
```

The `<content:encoded>` section is critical — this is what Mailchimp uses for the newsletter body.

### Step 9: Update sitemap.xml

Add the new article with Google News markup:

```xml
<url>
    <loc>https://epsteinfilesdaily.com/daily-[month]-[day]-[year].html</loc>
    <lastmod>[YYYY-MM-DD]</lastmod>
    <changefreq>never</changefreq>
    <priority>0.9</priority>
    <news:news>
        <news:publication>
            <news:name>Epstein Files Daily</news:name>
            <news:language>en</news:language>
        </news:publication>
        <news:publication_date>[YYYY-MM-DD]</news:publication_date>
        <news:title>[Theme Headline]</news:title>
    </news:news>
</url>
```

Also update the homepage `<lastmod>` to today's date.

### Step 10: Regenerate Name Pages

After adding a new article, regenerate all name pages in `/names/`:
- Each person tagged in any article gets a page at `/names/[name-slug].html`
- The page lists all articles that mention that person
- Sidebar shows all names with article counts
- Name slug format: lowercase, hyphens for spaces, no periods or apostrophes (e.g., `prince-andrew`, `jean-luc-brunel`)

### Step 11: Verify and Publish

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

# 5. Sitemap has the entry
grep "daily-[month]-[day]-[year]" sitemap.xml

# 6. Name pages exist
ls names/
```

**Commit and push:**

```bash
git add daily-*.html index.html feed.xml sitemap.xml images/daily-*.png names/*.html
git commit -m "Daily roundup: [Month Day] - [Theme]

Co-Authored-By: Claude Opus 4.5 <noreply@anthropic.com>"
git push
```

**Search engine pings (automated in workflow, but can be done manually):**
```bash
curl -s "https://www.google.com/ping?sitemap=https://epsteinfilesdaily.com/sitemap.xml"
curl -s "https://www.bing.com/indexnow?url=https://epsteinfilesdaily.com/daily-[month]-[day]-[year].html&key=epsteinfilesdaily"
```

---

## Key Differences: Homepage vs Article Page

| Element | Homepage Card | Article Page |
|---------|--------------|--------------|
| Headline | "[Month Day]: Read Daily Summary →" | "[Month Day]: [Theme Headline]" |
| Bullets | ONE LINE each (fits next to thumbnail) | 2-4 SENTENCES each (full context) |
| Newsletter signup | NO | YES |
| Share buttons | NO | YES (Facebook, Twitter, Bluesky, Email) |

---

## Quick Reference

**File naming:**
- Roundup: `daily-feb-9-2026.html`
- Thumbnail: `images/daily-feb-9-2026.png`
- Name page: `names/peter-thiel.html`

**Tag link format (name pages):**
```html
<a href="/names/peter-thiel.html" class="article-tag">Peter Thiel</a>
```

**Tag format in `data-tags`:** lowercase full names with commas (e.g., `data-tags="peter thiel,elon musk"`)

**Thumbnail headline rules:**
- MUST include at least one specific person's name
- NEVER use generic "DOJ Releases Files", "Bondi Claims...", or "New Documents Released"
- Always lead with the most newsworthy INDIVIDUAL, not a government agency
- Each day's headline should be distinct from recent ones
- Good examples: "Wexner Faces Congress as Jagland Charged in Norway", "Prince Andrew Faces New Pressure in Document Dump"
- Bad examples: "DOJ Releases More Epstein Files", "Bondi Claims All Files Released"

**Content diversity rules:**
- AT MOST ONE bullet about DOJ/Bondi/government process per roundup
- Prioritize lesser-known stories about specific individuals over mainstream DOJ coverage
- Include international angles when available (European investigations, foreign charges)
- Feature victims/survivors and their advocacy efforts

**SEO checklist for each article:**
- `<link rel="canonical">` with full URL
- Open Graph tags (og:title, og:description, og:url, og:image, og:type, article:published_time)
- Twitter Card tags (twitter:card, twitter:title, twitter:description, twitter:image)
- JSON-LD NewsArticle schema
- Entry in sitemap.xml with Google News markup

**Don't publish if:**
- Fewer than 4 distinct stories
- No significant new revelations
- Just rehashing old news
