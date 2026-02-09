#!/usr/bin/env python3
"""
Generate a thumbnail for a daily roundup.

Usage:
    python generate_daily_thumb.py "Feb 9, 2026" "Silicon Valley Ties"
    python generate_daily_thumb.py "Feb 10, 2026" "Branson Harem Email"
"""

import sys
from PIL import Image, ImageDraw, ImageFont
import os
import re

# Dimensions
WIDTH = 500
HEIGHT = 280

# Colors
BG_COLOR = (26, 26, 26)
ACCENT = (220, 38, 38)
WHITE = (255, 255, 255)
GRAY = (150, 150, 150)

def get_fonts():
    """Load fonts with fallbacks"""
    try:
        font_date = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 28)
        font_theme = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 22)
        font_brand = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 12)
    except:
        font_date = ImageFont.load_default()
        font_theme = ImageFont.load_default()
        font_brand = ImageFont.load_default()
    return font_date, font_theme, font_brand

def generate_thumbnail(date_str, theme, output_filename=None):
    """Generate a daily roundup thumbnail"""

    img = Image.new('RGB', (WIDTH, HEIGHT), BG_COLOR)
    draw = ImageDraw.Draw(img)
    font_date, font_theme, font_brand = get_fonts()

    # Red accent bar at top
    draw.rectangle([0, 0, WIDTH, 6], fill=ACCENT)

    # Subtle diagonal lines for texture
    for i in range(-HEIGHT, WIDTH + HEIGHT, 40):
        draw.line([(i, 0), (i + HEIGHT, HEIGHT)], fill=(35, 35, 35), width=1)

    # Center content area
    center_y = HEIGHT // 2 - 30

    # Date (large, white)
    date_upper = date_str.upper()
    bbox = draw.textbbox((0, 0), date_upper, font=font_date)
    text_width = bbox[2] - bbox[0]
    draw.text(((WIDTH - text_width) // 2, center_y - 20), date_upper, fill=WHITE, font=font_date)

    # Red separator line
    line_y = center_y + 25
    draw.rectangle([WIDTH//2 - 100, line_y, WIDTH//2 + 100, line_y + 3], fill=ACCENT)

    # Theme (smaller, white)
    theme_upper = theme.upper()
    # Split into multiple lines if needed
    words = theme_upper.split()
    if len(words) > 3:
        line1 = ' '.join(words[:len(words)//2])
        line2 = ' '.join(words[len(words)//2:])
        lines = [line1, line2]
    else:
        lines = [theme_upper]

    y_offset = line_y + 20
    for line in lines:
        bbox = draw.textbbox((0, 0), line, font=font_theme)
        text_width = bbox[2] - bbox[0]
        draw.text(((WIDTH - text_width) // 2, y_offset), line, fill=WHITE, font=font_theme)
        y_offset += 28

    # Bottom bar with branding
    draw.rectangle([0, HEIGHT - 35, WIDTH, HEIGHT], fill=(15, 15, 15))
    brand = "EPSTEIN FILES DAILY"
    bbox = draw.textbbox((0, 0), brand, font=font_brand)
    text_width = bbox[2] - bbox[0]
    draw.text(((WIDTH - text_width) // 2, HEIGHT - 25), brand, fill=GRAY, font=font_brand)

    # Generate filename if not provided
    if not output_filename:
        # Convert date to filename format: "Feb 9, 2026" -> "daily-2026-02-09.png"
        date_clean = date_str.lower().replace(',', '').replace(' ', '-')
        output_filename = f"images/daily-{date_clean}.png"

    # Ensure images directory exists
    os.makedirs('images', exist_ok=True)

    # Save
    img.save(output_filename, 'PNG')
    print(f"✓ Created {output_filename}")
    return output_filename

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python generate_daily_thumb.py \"Feb 9, 2026\" \"Theme Here\"")
        print("\nExample:")
        print("  python generate_daily_thumb.py \"Feb 9, 2026\" \"Silicon Valley Ties\"")
        sys.exit(1)

    date_str = sys.argv[1]
    theme = sys.argv[2]
    output = sys.argv[3] if len(sys.argv) > 3 else None

    generate_thumbnail(date_str, theme, output)
