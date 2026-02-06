---
name: epstein-article-generator
description: |
  Generate new articles for Epstein Exposed website based on DOJ document releases.
  TRIGGERS: "write new article", "generate article", "publish article", "daily article", "epstein article"
  Finds interesting DOJ documents, writes SEO-optimized investigative articles, creates thumbnails, updates the site, and pushes to GitHub.
---

# Epstein Article Generator

Generate investigative journalism articles for epstein-exposed.com based on DOJ file releases.

## Workflow

### Step 1: Check Covered Topics

Read `references/covered-topics.md` to see what's already published. Do NOT repeat stories.

### Step 2: Find New Source Material

Search DOJ Epstein files (https://www.justice.gov/epstein) for interesting stories:
- **Documents/Emails**: PDFs with revealing correspondence
- **Images**: Photos from the releases
- **Videos**: Depositions or footage
- **Flight logs**: Lolita Express passenger records
- **Financial records**: Wire transfers, payments

**Prioritize lesser-known names** over repeated coverage of big names. Look for:
- Business executives, foreign dignitaries, entertainment figures
- Academics/scientists, financial industry connections
- Real estate deals, foundation/charity connections

### Step 3: Verify Sources

- **ONLY use DOJ sources** - NO external news sources (PBS, CBS, CNN, etc.)
- Only use real DOJ document IDs (format: EFTAxxxxxxxx.pdf)
- Verify URLs exist at justice.gov
- Quote directly from documents
- All source-box links must point to justice.gov/epstein domains

### Step 4: Write Article

Use template from `references/article-template.html`. Elements:

**Headline**: Attention-grabbing, uses quotes from docs when possible
**Lede**: 1-2 sentence hook summarizing the revelation
**Body**:
1. Opening context (2-3 paragraphs)
2. Document evidence box with DOJ source
3. Additional context/analysis
4. Response box (or note if no response)
5. Source box with DOJ links
6. Share buttons

**SEO**: Title <60 chars, meta description 150-160 chars, full name in title/first paragraph

**Style**: Tabloid tone but factual, short paragraphs, pull quotes for damning evidence

### Step 5: Create Thumbnail Image

**IMPORTANT**: Create a thumbnail image for each article using Python/PIL.

**Thumbnail Specifications:**
- Size: 1200x630 pixels (standard og:image size)
- Background: Cream/off-white color (RGB: 250, 250, 247)
- Header: Dark slate bar (RGB: 51, 65, 85) with "📁 DOJ EPSTEIN FILES — [DOC_ID].pdf"
- Content: Email-style format with To/From/Date fields in monospace font
- Highlight: Key damning quote with yellow background (RGB: 255, 247, 140)
- **NO LOGO** in bottom right corner

**Thumbnail Code Example:**
```python
from PIL import Image, ImageDraw, ImageFont

def create_thumbnail(filename, doc_id, to_field, from_field, date_field, body_text, highlight_text):
    img = Image.new('RGB', (1200, 630), (250, 250, 247))
    draw = ImageDraw.Draw(img)

    # Load fonts
    font_header = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 22)
    font_label = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf", 26)
    font_value = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 26)
    font_highlight = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 34)

    # Dark slate header bar
    draw.rectangle([(0, 0), (1200, 45)], fill=(51, 65, 85))
    draw.text((18, 10), f"📁 DOJ EPSTEIN FILES — {doc_id}", font=font_header, fill=(255, 255, 255))

    # Email fields
    y = 80
    draw.text((55, y), "To:", font=font_label, fill=(120, 120, 120))
    draw.text((145, y), to_field, font=font_value, fill=(40, 40, 40))
    # ... continue with From, Date fields

    # Yellow highlighted quote
    # draw.rectangle for yellow background, then text

    # Save to images/ folder
    img.save(f"images/{filename}", 'PNG')
```

**Save thumbnail to**: `images/[person-name]-[topic].png`

**Update og:image in article**: `<meta property="og:image" content="https://epstein-exposed.com/images/[thumbnail-filename].png">`

### Step 6: Save Article

Save HTML to workspace: `firstname-lastname-topic.html` (lowercase, hyphens)

### Step 7: Update Site

1. **Add article card to `index.html`** with the following format:

```html
<article class="article-preview featured" data-tags="firstname lastname">
    <div class="article-top">
        <a href="[article-filename].html" class="article-thumb">
            <img src="images/[thumbnail-filename].png?v=1" alt="[descriptive alt text]" loading="lazy">
        </a>
        <div class="article-title-section">
            <div class="article-meta">
                <div class="article-tags">
                    <a href="?search=firstname+lastname" class="article-tag">Firstname Lastname</a>
                </div>
                <time datetime="YYYY-MM-DD" class="article-date">Month DD, YYYY</time>
                <span class="reading-time">· X min read</span>
            </div>
            <h2><a href="[article-filename].html">[Headline]</a></h2>
        </div>
    </div>
    <p class="lede">[Lede text]</p>
    <a href="[article-filename].html" class="read-more">Read full article</a>
</article>
```

**TAG RULES:**
- `data-tags` attribute: Use lowercase full name with space (e.g., `data-tags="james gorman"`)
- Visible tag: Use proper capitalization (e.g., `James Gorman`)
- Search href: Use `+` for spaces (e.g., `?search=james+gorman`)
- **ONLY use individual names** - NO company names (Morgan Stanley, Apollo, LinkedIn, etc.)
- **ONLY use individual names** - NO country names (Israel, etc.)

2. Add `<item>` to `feed.xml` (RFC 822 date format)
3. Update `references/covered-topics.md`

### Step 8: Publish

```bash
git add [article].html index.html feed.xml images/[thumbnail].png
git commit -m "Add article: [headline]"
git push
```

## References

- `references/article-template.html` - HTML template
- `references/covered-topics.md` - Previously published topics

## Summary of Key Rules

1. **Sources**: ONLY use DOJ sources (justice.gov/epstein) - NO external news (PBS, CBS, CNN, etc.)
2. **Thumbnails**: Cream background, DOJ document style, NO logo
3. **Tags**: Full names only (Firstname Lastname), NO company/country names
4. **Image path**: `images/[name]-[topic].png` with cache-busting `?v=1`
5. **og:image**: Point to `https://epstein-exposed.com/images/[thumbnail].png`
