---
name: epstein-article-generator
description: |
  Generate new articles for Epstein Files Daily website based on DOJ document releases.
  TRIGGERS: "write new article", "generate article", "publish article", "daily article", "epstein article"
  Finds interesting DOJ documents, writes SEO-optimized investigative articles, creates thumbnails, updates the site, and pushes to GitHub.
---

# Epstein Article Generator

Generate investigative journalism articles for epsteinfilesdaily.com based on DOJ file releases.

## ⚠️ CRITICAL CHECKLIST - VERIFY BEFORE PUBLISHING

Before pushing ANY article, confirm ALL of these are complete:

- [ ] **Article created FROM TEMPLATE** - MUST copy `references/article-template.html` as base
- [ ] **Article has theme-toggle** - Verify with: `grep -c "theme-toggle" article.html` (should return 6)
- [ ] **Thumbnail image created** in `images/` folder
- [ ] **index.html updated** with article card INCLUDING thumbnail `<img>` tag
- [ ] **feed.xml updated** with new `<item>`
- [ ] **covered-topics.md updated** with new topic
- [ ] **Tags use FULL NAMES** (e.g., "woody allen" not "allen")

**DO NOT SKIP THE THUMBNAIL** - Articles without thumbnails look broken on the site.

## 🚨 MANDATORY: USE THE TEMPLATE FILE

**NEVER write article HTML from scratch.** ALWAYS:
1. Read `references/article-template.html` first
2. Copy it as the base for your new article
3. Only replace the placeholder content ({{HEADLINE}}, {{SLUG}}, etc.)

The template includes critical features that MUST be present:
- Dark theme CSS with CSS variables
- Light/dark mode toggle in header
- Search bar in header
- Sticky header with red accent
- Theme persistence JavaScript
- Correct "Epstein Files Daily" branding
- EF favicon (not EE)

**If your article is missing any of these, it will look broken on the site.**

---

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

### Step 4: Write Article (MUST USE TEMPLATE)

**⚠️ CRITICAL: You MUST use the template file. DO NOT write HTML from scratch.**

**Step 4a: Read the template first**
```bash
cat references/article-template.html
```

**Step 4b: Copy template and replace placeholders**

The template uses these placeholders - replace ALL of them:
- `{{HEADLINE}}` - Article headline
- `{{META_DESCRIPTION}}` - SEO description (150-160 chars)
- `{{SLUG}}` - URL slug (e.g., `martha-stewart-epstein-parties`)
- `{{THUMBNAIL_FILENAME}}` - Thumbnail filename without extension
- `{{PERSON_TAG}}` - Person's full name for tag
- `{{DATE}}` - Publication date
- `{{ARTICLE_CONTENT}}` - The actual article body

**Step 4c: Verify article has required features**
```bash
# Must return 6 (theme toggle elements)
grep -c "theme-toggle" your-article.html

# Must return matches (dark theme CSS)
grep "var(--bg)" your-article.html | head -1
```

**Article Elements:**
- **Headline**: Attention-grabbing, uses quotes from docs when possible
- **Lede**: 1-2 sentence hook summarizing the revelation
- **Body**: Opening context, document evidence box, analysis, response box, source box, share buttons

**SEO**: Title <60 chars, meta description 150-160 chars, full name in title/first paragraph

**Style**: Tabloid tone but factual, short paragraphs, pull quotes for damning evidence

### Step 5: Create Thumbnail Image (MANDATORY)

**⚠️ THIS STEP IS REQUIRED - DO NOT SKIP**

**DEFAULT STYLE: Realistic Email Screenshot (Times New Roman)**

All thumbnails should use this clean, news-style format that looks like actual DOJ document screenshots.

**Thumbnail filename format**: `firstname-lastname-topic.png` (lowercase, hyphens)

---

#### 📧 REALISTIC EMAIL THUMBNAIL (Default - Use for ALL articles)

This creates a clean, realistic email screenshot using Times New Roman font with yellow highlights and a red DOJ caption bar.

```python
from PIL import Image, ImageDraw, ImageFont
import os

def get_serif_font(size, bold=False):
    """Get Times New Roman equivalent (Liberation Serif)"""
    if bold:
        path = "/usr/share/fonts/truetype/liberation/LiberationSerif-Bold.ttf"
    else:
        path = "/usr/share/fonts/truetype/liberation/LiberationSerif-Regular.ttf"
    try:
        return ImageFont.truetype(path, size)
    except:
        return ImageFont.load_default()

def get_sans_font(size, bold=False):
    """Get sans-serif font for caption"""
    if bold:
        path = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
    else:
        path = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
    try:
        return ImageFont.truetype(path, size)
    except:
        return ImageFont.load_default()

def create_realistic_email_thumbnail(
    output_path,
    from_name,
    to_name,
    date,
    subject,
    body_lines,
    highlights=[],
    doc_number="4521"
):
    """Create realistic email thumbnail with Times New Roman"""

    width, height = 380, 280
    img = Image.new('RGB', (width, height), '#ffffff')
    draw = ImageDraw.Draw(img)

    # Fonts
    label_font = get_serif_font(11)
    value_font = get_serif_font(11, bold=True)
    body_font = get_serif_font(12)
    caption_font = get_sans_font(10, bold=True)
    caption_font_small = get_sans_font(9)

    y = 18
    left_margin = 20
    label_width = 45

    # Header fields
    fields = [
        ("From:", from_name),
        ("To:", to_name),
        ("Date:", date),
        ("Re:", subject)
    ]

    for label, value in fields:
        draw.text((left_margin, y), label, fill='#666666', font=label_font)
        draw.text((left_margin + label_width, y), value, fill='#333333', font=value_font)
        y += 18

    # Divider line
    y += 5
    draw.line([left_margin, y, width - left_margin, y], fill='#e0e0e0', width=1)
    y += 12

    # Body text with highlights
    for line in body_lines:
        if line == "":
            y += 8
            continue

        # Check if this line contains highlighted text
        line_has_highlight = False
        for hl in highlights:
            if hl.lower() in line.lower():
                line_has_highlight = True
                idx = line.lower().find(hl.lower())
                before = line[:idx]
                highlight_text = line[idx:idx+len(hl)]
                after = line[idx+len(hl):]

                x = left_margin
                if before:
                    draw.text((x, y), before, fill='#333333', font=body_font)
                    x += draw.textlength(before, font=body_font)

                # Draw highlight background
                hl_width = draw.textlength(highlight_text, font=body_font)
                draw.rectangle([x-2, y-1, x + hl_width + 2, y + 15], fill='#fff59d')
                draw.text((x, y), highlight_text, fill='#333333', font=body_font)
                x += hl_width

                if after:
                    draw.text((x, y), after, fill='#333333', font=body_font)
                break

        if not line_has_highlight:
            draw.text((left_margin, y), line, fill='#333333', font=body_font)

        y += 18

    # Red caption bar at bottom
    caption_height = 32
    draw.rectangle([0, height - caption_height, width, height], fill='#dc2626')
    draw.text((left_margin, height - caption_height + 9), "DOJ Document Release", fill='#ffffff', font=caption_font)
    draw.text((width - 60, height - caption_height + 10), f"#{doc_number}", fill='#ffcccc', font=caption_font_small)

    os.makedirs(os.path.dirname(output_path) if os.path.dirname(output_path) else "images", exist_ok=True)
    img.save(output_path, quality=95)
    print(f"Created: {output_path}")

# Usage:
create_realistic_email_thumbnail(
    "images/person-topic.png",
    from_name="Jeffrey Epstein",
    to_name="Person Name",
    date="March 15, 2005",
    subject="Meeting Request",
    body_lines=[
        "Dear Person,",
        "",
        "Looking forward to our meeting",
        "at the island next week.",
        "",
        "Keep this between us."
    ],
    highlights=["the island", "between us"],
    doc_number="4521"
)
```

**After creating thumbnail, verify it exists:**
```bash
ls -la images/firstname-lastname-topic.png
```

### Step 6: Save Article

Save HTML to workspace: `firstname-lastname-topic.html` (lowercase, hyphens)

### Step 7: Update Site

#### 7a. Add article card to `index.html`

**IMPORTANT**: The article card MUST include the thumbnail image. Use this exact format:

```html
<!-- AUTO-GENERATED ARTICLE: FIRSTNAME LASTNAME -->
<article class="article-preview featured" data-tags="firstname lastname">
    <div class="article-top">
        <a href="firstname-lastname-topic.html" class="article-thumb">
            <img src="images/firstname-lastname-topic.png?v=1" alt="DOJ files reveal [description]" loading="lazy">
        </a>
        <div class="article-title-section">
            <div class="article-meta">
                <div class="article-tags">
                    <a href="?search=firstname+lastname" class="article-tag">Firstname Lastname</a>
                </div>
                <time datetime="YYYY-MM-DD" class="article-date">Month DD, YYYY</time>
                <span class="reading-time">· X min read</span>
            </div>
            <h2><a href="firstname-lastname-topic.html">[Headline]</a></h2>
            <p class="lede">[Lede text - 1-2 sentences]</p>
            <a href="firstname-lastname-topic.html" class="read-more">Read full article</a>
        </div>
    </div>
</article>
```

**TAG RULES:**
- `data-tags` attribute: Use lowercase full name with space (e.g., `data-tags="woody allen"`)
- Visible tag: Use proper capitalization (e.g., `Woody Allen`)
- Search href: Use `+` for spaces (e.g., `?search=woody+allen`)
- **ONLY use individual FULL names** - NO last names only, NO company names, NO country names

#### 7b. Add to feed.xml

Add new `<item>` with RFC 822 date format.

#### 7c. Update covered-topics.md

Add the new topic to prevent duplicates.

### Step 8: Verify and Publish

**Before committing, run ALL these verification checks:**

```bash
# 1. Thumbnail exists
ls images/firstname-lastname-topic.png

# 2. Article exists
ls firstname-lastname-topic.html

# 3. Article has theme toggle (MUST return 6)
grep -c "theme-toggle" firstname-lastname-topic.html

# 4. Article has dark theme CSS
grep -c "var(--bg)" firstname-lastname-topic.html

# 5. Article has correct branding (should show "Epstein Files Daily")
grep "Epstein Files Daily" firstname-lastname-topic.html | head -1

# 6. index.html has the article card with <img> tag
grep "firstname-lastname-topic.png" index.html
```

**If any check fails, DO NOT commit. Fix the issue first.**

**Commit with ALL files:**
```bash
git add firstname-lastname-topic.html index.html feed.xml images/firstname-lastname-topic.png .skills/epstein-article-generator/references/covered-topics.md
git commit -m "Add article: [headline]"
git push
```

---

## References

- `references/article-template.html` - HTML template (dark theme with light/dark toggle)
- `references/covered-topics.md` - Previously published topics
- `references/create_thumbnail.py` - Thumbnail generator script

## Summary of Key Rules

1. **TEMPLATE IS MANDATORY**: ALWAYS copy `references/article-template.html` - NEVER write HTML from scratch
2. **Verify before publishing**: Article must have theme-toggle (grep returns 6), dark theme CSS, correct branding
3. **Sources**: ONLY use DOJ sources (justice.gov/epstein) - NO external news
4. **Thumbnails**: MANDATORY - Use the realistic email screenshot style (Times New Roman, yellow highlights, red DOJ caption bar)
5. **Tags**: FULL names only (e.g., "woody allen" not "allen"), NO company/country names
6. **Article cards**: MUST include `<img>` thumbnail tag
7. **og:image**: Point to `https://epsteinfilesdaily.com/images/[thumbnail].png`

## Quick Verification Commands

```bash
# Run these BEFORE every commit:
grep -c "theme-toggle" article.html        # Must return 6
grep -c "var(--bg)" article.html           # Must return >0
grep "Epstein Files Daily" article.html    # Must show matches
ls images/thumbnail.png                     # Must exist
```
