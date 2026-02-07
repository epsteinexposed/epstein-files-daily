#!/usr/bin/env python3
"""
Thumbnail generator for Epstein Files Daily articles.
Creates DOJ document-style thumbnails with cream background and red accent bar.

Usage:
    python create_thumbnail.py

Modify the 'thumbnail' dict at the bottom with article details, then run.
"""

from PIL import Image, ImageDraw, ImageFont
import os

# Output directory (relative to workspace root)
OUTPUT_DIR = "images"
WIDTH = 1200
HEIGHT = 630


def create_thumbnail(filename, doc_id, to_field, from_field, date_field, highlight_text):
    """
    Create a thumbnail styled like a DOJ document excerpt.

    Args:
        filename: Output filename (e.g., "woody-allen-dinners.png")
        doc_id: DOJ document ID (e.g., "EFTA00847392.pdf")
        to_field: Email "To" field
        from_field: Email "From" field
        date_field: Email date
        highlight_text: Key damning quote to highlight in yellow

    Returns:
        Path to the created thumbnail image
    """
    # Create cream/off-white background
    img = Image.new('RGB', (WIDTH, HEIGHT), (250, 250, 247))
    draw = ImageDraw.Draw(img)

    # Load fonts
    try:
        font_header = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 22)
        font_label = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf", 26)
        font_value = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 26)
        font_highlight = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 32)
    except:
        font_header = font_label = font_value = font_highlight = ImageFont.load_default()

    # Dark slate header bar
    draw.rectangle([(0, 0), (WIDTH, 45)], fill=(51, 65, 85))
    header_text = f"📁 DOJ EPSTEIN FILES — {doc_id}"
    draw.text((18, 10), header_text, font=font_header, fill=(255, 255, 255))

    # Red accent bar on left side (below header)
    draw.rectangle([(0, 45), (18, HEIGHT)], fill=(220, 38, 38))

    # Email metadata
    y = 80
    label_color = (120, 120, 120)  # Gray for labels
    value_color = (40, 40, 40)      # Dark for values

    # To field
    draw.text((55, y), "To:", font=font_label, fill=label_color)
    draw.text((145, y), to_field, font=font_value, fill=value_color)
    y += 40

    # From field
    draw.text((55, y), "From:", font=font_label, fill=label_color)
    draw.text((145, y), from_field, font=font_value, fill=value_color)
    y += 40

    # Date field
    draw.text((55, y), "Date:", font=font_label, fill=label_color)
    draw.text((145, y), date_field, font=font_value, fill=value_color)
    y += 60

    # Word wrap the highlight text
    max_width = WIDTH - 120
    words = highlight_text.split()
    lines = []
    current_line = []
    for word in words:
        test_line = ' '.join(current_line + [word])
        test_bbox = draw.textbbox((0, 0), test_line, font=font_highlight)
        if test_bbox[2] - test_bbox[0] > max_width:
            if current_line:
                lines.append(' '.join(current_line))
            current_line = [word]
        else:
            current_line.append(word)
    if current_line:
        lines.append(' '.join(current_line))

    # Draw wrapped highlighted text with yellow background
    for line in lines:
        line_bbox = draw.textbbox((0, 0), line, font=font_highlight)
        line_width = line_bbox[2] - line_bbox[0]
        line_height = line_bbox[3] - line_bbox[1]
        # Yellow highlight background
        draw.rectangle([(50, y - 3), (58 + line_width, y + line_height + 8)], fill=(255, 247, 140))
        draw.text((54, y), line, font=font_highlight, fill=(40, 40, 40))
        y += line_height + 18

    # Ensure output directory exists
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    # Save
    output_path = os.path.join(OUTPUT_DIR, filename)
    img.save(output_path, 'PNG', quality=95)
    print(f"✓ Created thumbnail: {output_path}")
    return output_path


if __name__ == "__main__":
    # ============================================
    # MODIFY THESE VALUES FOR EACH NEW ARTICLE
    # ============================================
    thumbnail = {
        "filename": "firstname-lastname-topic.png",  # e.g., "woody-allen-dinners.png"
        "doc_id": "EFTA00XXXXXX.pdf",                # e.g., "EFTA00847392.pdf"
        "to": "Jeffrey Epstein",                      # Email To field
        "from": "Person Name",                        # Email From field
        "date": "Month DD, YYYY",                     # e.g., "November 18, 2010"
        "highlight": "The key damning quote from the document goes here."
    }

    create_thumbnail(
        thumbnail["filename"],
        thumbnail["doc_id"],
        thumbnail["to"],
        thumbnail["from"],
        thumbnail["date"],
        thumbnail["highlight"]
    )

    print("\n⚠️  Don't forget to:")
    print("   1. Add the thumbnail to git: git add images/" + thumbnail["filename"])
    print("   2. Include <img> tag in the article card in index.html")
    print("   3. Update og:image in the article HTML")
