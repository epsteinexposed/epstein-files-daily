---
name: photo-article-generator
description: |
  Generate articles based on photos from the DOJ Epstein file releases.
  TRIGGERS: "write photo article", "photo article", "image article", "process photos"
  User drops images into the doj-photos folder, this skill analyzes them and writes articles.
---

# Photo Article Generator

Generate investigative journalism articles for epsteinfilesdaily.com based on photographs from DOJ releases.

## Workflow Overview

Unlike document articles (which are fully automated), photo articles are semi-manual:
1. **You** drop images into the `doj-photos/` folder
2. **Claude** scans the folder, analyzes the images, and writes articles

## Step 1: Scan for New Images

Check the `doj-photos/` folder for images:
```bash
ls -la doj-photos/
```

Look for common image formats: `.jpg`, `.jpeg`, `.png`, `.webp`

## Step 2: Analyze the Image

For each new image:
1. View the image to understand what it shows
2. Identify any recognizable people, locations, or context
3. Note any text, dates, or identifying information visible
4. Determine the news value and angle

**Key questions to answer:**
- Who is in the photo?
- What is happening?
- Where/when was this likely taken?
- Why is this newsworthy?
- What context is needed?

## Step 3: Research Context

Search for additional context about the people/events in the photo:
- Cross-reference with known Epstein connections
- Check if this person has been covered before in `references/covered-topics.md`
- Find any public statements or responses from the individuals pictured

## Step 4: Write Article

Use template from `references/photo-article-template.html`. Elements:

**Media Badge**: Purple "📷 Photo" badge for photos, Red "🎬 Video" badge for videos

**Headline**: Descriptive, names the key people, indicates it's a photo
- Format: "PHOTO: [Description of what the image shows]"

**Lede**: 1-2 sentences explaining what the photo shows and why it matters

**Body Structure**:
1. Opening context (what the photo shows, when released)
2. **Photo evidence box** with the actual image
3. Context about the individuals pictured
4. Any relevant background/history
5. Response boxes (or note if no response)
6. Source box (DOJ links only)
7. Share buttons

**Important Context Note**: Always include a disclaimer that appearing in a photo doesn't imply wrongdoing.

## Step 5: Copy Image to Website

Copy the image from `doj-photos/` to `images/` with a descriptive filename:
```bash
cp doj-photos/original-name.jpg images/person-name-context.jpg
```

Filename format: `firstname-lastname-description.jpg` (lowercase, hyphens)

## Step 6: Save Article

Save HTML to workspace: `firstname-lastname-photo.html` (lowercase, hyphens)

## Step 7: Update Homepage

Add article card to `index.html` with photo badge:

```html
<article class="article-preview featured" data-tags="firstname lastname">
    <div class="article-top">
        <a href="[article-filename].html" class="article-thumb">
            <img src="images/[photo-filename].jpg?v=1" alt="[descriptive alt text]" loading="lazy">
        </a>
        <div class="article-title-section">
            <div class="article-meta">
                <div class="article-tags">
                    <span class="article-tag" style="background:#7c3aed">📷 Photo</span>
                    <a href="?search=firstname+lastname" class="article-tag">Firstname Lastname</a>
                </div>
                <time datetime="YYYY-MM-DD" class="article-date">Month DD, YYYY</time>
                <span class="reading-time">· X min read</span>
            </div>
            <h2><a href="[article-filename].html">PHOTO: [Headline]</a></h2>
        </div>
    </div>
    <p class="lede">[Lede text]</p>
    <a href="[article-filename].html" class="read-more">Read full article</a>
</article>
```

## Step 8: Update Tracking

Add to `references/covered-topics.md`:
```
- [Person Name] - Photo: [brief description] (YYYY-MM-DD)
```

## Step 9: Publish

```bash
git add [article].html index.html images/[photo].jpg
git commit -m "Add photo article: [headline]"
git push
```

## Styling Reference

**Photo Articles (Purple theme)**:
- Badge: `background:#7c3aed` with "📷 Photo"
- Evidence box border: `border:2px solid #7c3aed`
- Header bar: `background:#7c3aed`
- Accent color: `#7c3aed` (purple)

**Video Articles (Red theme)**:
- Badge: `background:#b91c1c` with "🎬 Video"
- Evidence box border: `border:2px solid #b91c1c`
- Header bar: `background:#b91c1c`
- Accent color: `#b91c1c` (red)

## References

- `references/photo-article-template.html` - HTML template for photo articles
- `references/covered-topics.md` - Previously published topics (shared with document articles)
- `doj-photos/` - Drop folder for new images

## Summary of Key Rules

1. **Sources**: ONLY use DOJ sources (justice.gov/epstein) - NO external news
2. **Images**: Use actual photos from `doj-photos/` folder, copy to `images/`
3. **Tags**: Full names only (Firstname Lastname), NO company/country names
4. **Context disclaimer**: Always note that appearing in photos doesn't imply wrongdoing
5. **Headlines**: Start with "PHOTO:" or "VIDEO:" prefix
6. **Badge**: Purple for photos, red for videos
