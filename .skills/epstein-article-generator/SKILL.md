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

**DEFAULT STYLE: Authentic Leaked Email**

All thumbnails should look like actual leaked DOJ email screenshots with:
- Plain white background
- Email headers (To/From/Sent/Subject) with full email addresses
- Yellow highlight on incriminating text
- "Sent from my BlackBerry®" signature
- Dark navy DOJ bar at bottom with document number

**Thumbnail filename format**: `firstname-lastname-topic.png` (lowercase, hyphens)

---

#### 📧 AUTHENTIC EMAIL THUMBNAIL (Use for ALL articles)

```python
from PIL import Image, ImageDraw, ImageFont

def get_font(size, bold=False):
    if bold:
        path = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
    else:
        path = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
    try:
        return ImageFont.truetype(path, size)
    except:
        return ImageFont.load_default()

def create_authentic_email(output_path, to_email, from_email, sent_date, subject, body_lines, highlight_text=None, doc_number="DOJ-EPSTEIN-004521"):
    """Create authentic-looking leaked email with yellow highlight and navy DOJ bar"""

    width, height = 500, 300
    img = Image.new('RGB', (width, height), '#ffffff')
    draw = ImageDraw.Draw(img)

    label_font = get_font(13, bold=True)
    value_font = get_font(13)
    body_font = get_font(13)
    sig_font = get_font(12)
    caption_font = get_font(10)

    y = 20
    left = 25
    label_width = 70

    # To field
    draw.text((left, y), "To:", fill='#000', font=label_font)
    draw.text((left + label_width, y), to_email, fill='#000', font=value_font)
    y += 24

    # From field
    draw.text((left, y), "From:", fill='#000', font=label_font)
    draw.text((left + label_width, y), from_email, fill='#000', font=value_font)
    y += 24

    # Sent field
    draw.text((left, y), "Sent:", fill='#000', font=label_font)
    draw.text((left + label_width, y), sent_date, fill='#000', font=value_font)
    y += 24

    # Subject field
    draw.text((left, y), "Subject:", fill='#000', font=label_font)
    draw.text((left + label_width + 15, y), subject, fill='#000', font=value_font)
    y += 38

    # Body text with yellow highlight
    for line in body_lines:
        if line == "":
            y += 14
            continue

        if highlight_text and highlight_text.lower() in line.lower():
            idx = line.lower().find(highlight_text.lower())
            before = line[:idx]
            word = line[idx:idx+len(highlight_text)]
            after = line[idx+len(highlight_text):]

            x = left
            if before:
                draw.text((x, y), before, fill='#000', font=body_font)
                x += draw.textlength(before, font=body_font)

            # Yellow highlight background
            word_w = draw.textlength(word, font=body_font)
            draw.rectangle([x - 2, y - 2, x + word_w + 2, y + 18], fill='#ffff00')
            draw.text((x, y), word, fill='#000', font=body_font)

            x += word_w
            if after:
                draw.text((x, y), after, fill='#000', font=body_font)
        else:
            draw.text((left, y), line, fill='#000', font=body_font)

        y += 22

    # BlackBerry signature
    y += 12
    draw.text((left, y), "Sent from my BlackBerry® wireless device", fill='#000', font=sig_font)

    # Dark navy bar at bottom with DOJ document number
    bar_height = 28
    draw.rectangle([0, height - bar_height, width, height], fill='#1a2744')
    draw.text((15, height - bar_height + 8), f"U.S. Department of Justice  •  {doc_number}", fill='#ffffff', font=caption_font)

    img.save(output_path, quality=95)
    print(f"Created: {output_path}")

# Usage:
create_authentic_email(
    "images/person-topic.png",
    to_email="Jeffrey Epstein[jeevacation@gmail.com]",
    from_email="Person Name[person@email.com]",
    sent_date="Thur 3/15/2005 2:30:15 PM",
    subject="Re: Meeting Request",
    body_lines=[
        "Looking forward to our meeting",
        "at the island next week.",
        "",
        "Keep this between us."
    ],
    highlight_text="between us",
    doc_number="DOJ-EPSTEIN-004521"
)
```

---

#### ✈️ AUTHENTIC FLIGHT LOG (Use for travel/flight articles)

```python
from PIL import Image, ImageDraw, ImageFont

def get_font(size, bold=False):
    if bold:
        path = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
    else:
        path = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
    try:
        return ImageFont.truetype(path, size)
    except:
        return ImageFont.load_default()

def get_mono(size):
    try:
        return ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf", size)
    except:
        return ImageFont.load_default()

def create_authentic_flight_log(output_path, flight_date, origin, destination, tail_number,
                                 passengers, highlight_passenger, doc_number="DOJ-EPSTEIN-FL-00847"):
    """Create authentic flight manifest like actual leaked documents"""

    width, height = 500, 300
    img = Image.new('RGB', (width, height), '#ffffff')
    draw = ImageDraw.Draw(img)

    header_font = get_font(11, bold=True)
    label_font = get_font(11)
    mono_font = get_mono(11)
    caption_font = get_font(10)

    y = 15
    left = 25

    # Document header
    draw.text((left, y), "FLIGHT MANIFEST - CONFIDENTIAL", fill='#000', font=header_font)
    y += 25

    # Flight details
    draw.text((left, y), "Date:", fill='#000', font=label_font)
    draw.text((left + 80, y), flight_date, fill='#000', font=mono_font)
    y += 20

    draw.text((left, y), "Origin:", fill='#000', font=label_font)
    draw.text((left + 80, y), origin, fill='#000', font=mono_font)
    y += 20

    draw.text((left, y), "Destination:", fill='#000', font=label_font)
    draw.text((left + 80, y), destination, fill='#000', font=mono_font)
    y += 20

    draw.text((left, y), "Aircraft:", fill='#000', font=label_font)
    draw.text((left + 80, y), f"{tail_number} (Gulfstream IV)", fill='#000', font=mono_font)
    y += 28

    # Passengers header
    draw.text((left, y), "PASSENGERS:", fill='#000', font=header_font)
    y += 22

    # List passengers with highlight
    for i, passenger in enumerate(passengers):
        text = f"{i+1}. {passenger}"
        if highlight_passenger and highlight_passenger.lower() in passenger.lower():
            text_w = draw.textlength(text, font=mono_font)
            draw.rectangle([left - 2, y - 2, left + text_w + 4, y + 16], fill='#ffff00')
        draw.text((left, y), text, fill='#000', font=mono_font)
        y += 18

    # Dark navy DOJ bar at bottom
    bar_height = 28
    draw.rectangle([0, height - bar_height, width, height], fill='#1a2744')
    draw.text((15, height - bar_height + 8), f"U.S. Department of Justice  •  {doc_number}", fill='#ffffff', font=caption_font)

    img.save(output_path, quality=95)
    print(f"Created: {output_path}")

# Usage:
create_authentic_flight_log(
    "images/person-flight.png",
    flight_date="March 15, 2002",
    origin="Teterboro, NJ (TEB)",
    destination="St. Thomas, USVI (STT)",
    tail_number="N908JE",
    passengers=["Jeffrey Epstein", "Ghislaine Maxwell", "Person Name", "Guest 1"],
    highlight_passenger="Person Name",
    doc_number="DOJ-EPSTEIN-FL-00923"
)
```

---

#### 💰 AUTHENTIC WIRE TRANSFER (Use for financial/payment articles)

```python
from PIL import Image, ImageDraw, ImageFont

def get_font(size, bold=False):
    if bold:
        path = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
    else:
        path = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
    try:
        return ImageFont.truetype(path, size)
    except:
        return ImageFont.load_default()

def create_authentic_wire_transfer(output_path, date, sender, sender_account, recipient,
                                    recipient_account, amount, memo, highlight_text=None,
                                    doc_number="DOJ-EPSTEIN-FIN-01284"):
    """Create authentic wire transfer like actual bank documents"""

    width, height = 500, 300
    img = Image.new('RGB', (width, height), '#ffffff')
    draw = ImageDraw.Draw(img)

    header_font = get_font(11, bold=True)
    label_font = get_font(11)
    value_font = get_font(11)
    amount_font = get_font(14, bold=True)
    caption_font = get_font(10)

    y = 15
    left = 25
    label_w = 120

    # Document header
    draw.text((left, y), "WIRE TRANSFER CONFIRMATION", fill='#000', font=header_font)
    y += 25

    # Transfer details
    fields = [
        ("Date:", date),
        ("Originator:", sender),
        ("Account:", sender_account),
        ("Beneficiary:", recipient),
        ("Beneficiary Acct:", recipient_account),
    ]

    for label, value in fields:
        draw.text((left, y), label, fill='#000', font=label_font)
        draw.text((left + label_w, y), value, fill='#000', font=value_font)
        y += 20

    y += 5

    # Amount with highlight
    draw.text((left, y), "Amount:", fill='#000', font=label_font)
    amount_x = left + label_w
    amount_w = draw.textlength(amount, font=amount_font)
    draw.rectangle([amount_x - 3, y - 3, amount_x + amount_w + 5, y + 20], fill='#ffff00')
    draw.text((amount_x, y), amount, fill='#000', font=amount_font)
    y += 28

    # Memo
    draw.text((left, y), "Memo:", fill='#000', font=label_font)
    memo_text = f'"{memo}"'
    if highlight_text and highlight_text.lower() in memo.lower():
        memo_w = draw.textlength(memo_text, font=value_font)
        draw.rectangle([left + label_w - 2, y - 2, left + label_w + memo_w + 4, y + 16], fill='#ffff00')
    draw.text((left + label_w, y), memo_text, fill='#000', font=value_font)

    # Dark navy DOJ bar at bottom
    bar_height = 28
    draw.rectangle([0, height - bar_height, width, height], fill='#1a2744')
    draw.text((15, height - bar_height + 8), f"U.S. Department of Justice  •  {doc_number}", fill='#ffffff', font=caption_font)

    img.save(output_path, quality=95)
    print(f"Created: {output_path}")

# Usage:
create_authentic_wire_transfer(
    "images/person-payment.png",
    date="September 14, 2008",
    sender="Gratitude America Ltd",
    sender_account="****4521",
    recipient="Person Name",
    recipient_account="****8834",
    amount="$2,500,000.00",
    memo="Consulting services",
    highlight_text="Consulting",
    doc_number="DOJ-EPSTEIN-FIN-01284"
)
```

---

#### 📅 AUTHENTIC CALENDAR (Use for meeting/dinner/event articles)

```python
from PIL import Image, ImageDraw, ImageFont

def get_font(size, bold=False):
    if bold:
        path = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
    else:
        path = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
    try:
        return ImageFont.truetype(path, size)
    except:
        return ImageFont.load_default()

def create_authentic_calendar(output_path, month, day, year, day_of_week, appointments,
                               highlight_text=None, doc_number="DOJ-EPSTEIN-CAL-00384"):
    """Create authentic calendar page with visual calendar element"""

    width, height = 500, 300
    img = Image.new('RGB', (width, height), '#ffffff')
    draw = ImageDraw.Draw(img)

    header_font = get_font(10, bold=True)
    month_font = get_font(12, bold=True)
    day_font = get_font(42, bold=True)
    weekday_font = get_font(10)
    time_font = get_font(11, bold=True)
    event_font = get_font(11)
    caption_font = get_font(10)

    # Document header
    draw.text((25, 12), "PERSONAL CALENDAR - CONFIDENTIAL", fill='#000', font=header_font)

    # Calendar day box on the left
    box_x, box_y = 25, 38
    box_w, box_h = 100, 95

    # Red header bar for month
    draw.rectangle([box_x, box_y, box_x + box_w, box_y + 25], fill='#cc0000')
    draw.text((box_x + 25, box_y + 5), month.upper(), fill='#fff', font=month_font)

    # White box for day number
    draw.rectangle([box_x, box_y + 25, box_x + box_w, box_y + box_h], fill='#fff', outline='#ccc', width=1)

    # Day number centered
    day_text = str(day)
    day_w = draw.textlength(day_text, font=day_font)
    draw.text((box_x + (box_w - day_w) / 2, box_y + 35), day_text, fill='#000', font=day_font)

    # Day of week below
    weekday_w = draw.textlength(day_of_week, font=weekday_font)
    draw.text((box_x + (box_w - weekday_w) / 2, box_y + 78), day_of_week, fill='#666', font=weekday_font)

    # Year below box
    year_text = str(year)
    year_w = draw.textlength(year_text, font=weekday_font)
    draw.text((box_x + (box_w - year_w) / 2, box_y + box_h + 5), year_text, fill='#666', font=weekday_font)

    # Appointments on the right side
    appt_x = 145
    appt_y = 45

    draw.text((appt_x, appt_y), "APPOINTMENTS:", fill='#000', font=header_font)
    appt_y += 22

    for time, event in appointments:
        should_highlight = highlight_text and highlight_text.lower() in event.lower()

        draw.text((appt_x, appt_y), time, fill='#cc0000', font=time_font)

        event_x = appt_x + 70
        if should_highlight:
            event_w = draw.textlength(event, font=event_font)
            draw.rectangle([event_x - 2, appt_y - 2, event_x + event_w + 4, appt_y + 16], fill='#ffff00')
        draw.text((event_x, appt_y), event, fill='#000', font=event_font)
        appt_y += 22

    # Dark navy DOJ bar at bottom
    bar_height = 28
    draw.rectangle([0, height - bar_height, width, height], fill='#1a2744')
    draw.text((15, height - bar_height + 8), f"U.S. Department of Justice  •  {doc_number}", fill='#ffffff', font=caption_font)

    img.save(output_path, quality=95)
    print(f"Created: {output_path}")

# Usage:
create_authentic_calendar(
    "images/person-dinner.png",
    month="MAR",
    day=14,
    year=2010,
    day_of_week="Sunday",
    appointments=[
        ("2:00 PM", "Tea with Person Name"),
        ("5:00 PM", "Call Ghislaine re: arrangements"),
        ("8:00 PM", "Dinner: Person, Maxwell, guests"),
    ],
    highlight_text="Person Name",
    doc_number="DOJ-EPSTEIN-CAL-00384"
)
```

---

#### 💬 AUTHENTIC TEXT MESSAGE (Use for text/chat articles)

```python
from PIL import Image, ImageDraw, ImageFont

def get_font(size, bold=False):
    if bold:
        path = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
    else:
        path = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
    try:
        return ImageFont.truetype(path, size)
    except:
        return ImageFont.load_default()

def create_authentic_text_message(output_path, contact_name, phone_number, messages,
                                   highlight_text=None, doc_number="DOJ-EPSTEIN-DIG-02847"):
    """Create authentic text message screenshot like actual forensic extraction"""

    width, height = 500, 300
    img = Image.new('RGB', (width, height), '#f5f5f5')
    draw = ImageDraw.Draw(img)

    header_font = get_font(11, bold=True)
    contact_font = get_font(12, bold=True)
    msg_font = get_font(11)
    time_font = get_font(9)
    caption_font = get_font(10)

    y = 15
    left = 25

    # Document header
    draw.text((left, y), "TEXT MESSAGE EXTRACTION - FORENSIC COPY", fill='#000', font=header_font)
    y += 22

    draw.text((left, y), f"Contact: {contact_name}", fill='#000', font=contact_font)
    y += 18
    draw.text((left, y), f"Phone: {phone_number}", fill='#666', font=msg_font)
    y += 25

    # Messages (sender, text, timestamp)
    for sender, text, timestamp in messages:
        is_epstein = sender.lower() == "epstein"

        bubble_x = left if not is_epstein else left + 150
        bubble_color = '#e5e5ea' if not is_epstein else '#007aff'
        text_color = '#000' if not is_epstein else '#fff'

        should_highlight = highlight_text and highlight_text.lower() in text.lower()

        text_w = min(draw.textlength(text, font=msg_font), 280)
        bubble_w = text_w + 20

        if should_highlight:
            draw.rectangle([bubble_x - 3, y - 3, bubble_x + bubble_w + 5, y + 40], outline='#ffff00', width=3)

        draw.rounded_rectangle([bubble_x, y, bubble_x + bubble_w, y + 35], radius=10, fill=bubble_color)
        draw.text((bubble_x + 10, y + 8), text[:40], fill=text_color, font=msg_font)
        draw.text((bubble_x + 10, y + 38), timestamp, fill='#888', font=time_font)
        y += 55

    # Dark navy DOJ bar at bottom
    bar_height = 28
    draw.rectangle([0, height - bar_height, width, height], fill='#1a2744')
    draw.text((15, height - bar_height + 8), f"U.S. Department of Justice  •  {doc_number}", fill='#ffffff', font=caption_font)

    img.save(output_path, quality=95)
    print(f"Created: {output_path}")

# Usage (messages format: sender, text, timestamp):
create_authentic_text_message(
    "images/person-texts.png",
    contact_name="Person Name",
    phone_number="+1 (212) 555-0142",
    messages=[
        ("Person", "Got the girls for the trip", "Mar 12, 3:42 PM"),
        ("Epstein", "Perfect. Same as before", "Mar 12, 3:45 PM"),
        ("Person", "Confirmed for Saturday", "Mar 12, 4:12 PM"),
    ],
    highlight_text="girls",
    doc_number="DOJ-EPSTEIN-DIG-02847"
)
```

---

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
4. **Thumbnails**: MANDATORY - Choose appropriate authentic style based on content:
   - 📧 **Email**: correspondence, memos (default)
   - ✈️ **Flight Log**: travel records, Lolita Express
   - 💰 **Wire Transfer**: financial records, payments
   - 📅 **Calendar**: meetings, dinners, appointments
   - 💬 **Text Message**: text conversations, chats
   All styles have: yellow highlights, dark navy DOJ bar at bottom
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
