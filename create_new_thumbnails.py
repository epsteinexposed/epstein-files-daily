#!/usr/bin/env python3
"""Create thumbnails for new articles"""

from PIL import Image, ImageDraw, ImageFont
import os

# Ensure images directory exists
os.makedirs('images', exist_ok=True)

# Thumbnail configuration
WIDTH = 420
HEIGHT = 280
BG_COLOR = (26, 26, 26)  # Dark gray
ACCENT_COLOR = (220, 38, 38)  # Red accent

# Article data
articles = [
    {
        'filename': 'branson-thumb.png',
        'label': 'BRANSON',
        'icon': '🏝️',
    },
    {
        'filename': 'brin-thumb.png',
        'label': 'GOOGLE',
        'icon': '🔍',
    },
    {
        'filename': 'thiel-thumb.png',
        'label': 'THIEL',
        'icon': '💰',
    },
    {
        'filename': 'harris-thumb.png',
        'label': 'HARRIS',
        'icon': '🏈',
    },
    {
        'filename': 'oz-thumb.png',
        'label': 'DR. OZ',
        'icon': '🩺',
    },
]

def create_thumbnail(article):
    """Create a thumbnail image for an article"""
    img = Image.new('RGB', (WIDTH, HEIGHT), BG_COLOR)
    draw = ImageDraw.Draw(img)

    # Draw red accent bar at top
    draw.rectangle([0, 0, WIDTH, 6], fill=ACCENT_COLOR)

    # Draw diagonal pattern
    for i in range(-HEIGHT, WIDTH + HEIGHT, 30):
        draw.line([(i, 0), (i + HEIGHT, HEIGHT)], fill=(35, 35, 35), width=1)

    # Draw central box
    box_margin = 40
    draw.rectangle(
        [box_margin, box_margin, WIDTH - box_margin, HEIGHT - box_margin],
        fill=(40, 40, 40),
        outline=ACCENT_COLOR,
        width=2
    )

    # Try to use a font, fall back to default if not available
    try:
        font_large = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 32)
        font_small = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 14)
    except:
        font_large = ImageFont.load_default()
        font_small = ImageFont.load_default()

    # Draw label
    label = article['label']
    bbox = draw.textbbox((0, 0), label, font=font_large)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    x = (WIDTH - text_width) // 2
    y = (HEIGHT - text_height) // 2
    draw.text((x, y), label, fill='white', font=font_large)

    # Draw "DOJ FILES" subtitle
    subtitle = "DOJ FILES"
    bbox = draw.textbbox((0, 0), subtitle, font=font_small)
    text_width = bbox[2] - bbox[0]
    draw.text(((WIDTH - text_width) // 2, y + text_height + 10), subtitle, fill=ACCENT_COLOR, font=font_small)

    # Save image
    filepath = os.path.join('images', article['filename'])
    img.save(filepath, 'PNG')
    print(f"✓ Created {filepath}")

# Create all thumbnails
for article in articles:
    create_thumbnail(article)

print("\n" + "=" * 50)
print("All thumbnails created successfully!")
