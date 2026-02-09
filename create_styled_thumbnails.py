#!/usr/bin/env python3
"""Create DOJ-styled document thumbnails for new articles"""

from PIL import Image, ImageDraw, ImageFont
import os

# Thumbnail dimensions (matching originals)
WIDTH = 500
HEIGHT = 280

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
DARK_BLUE = (0, 51, 102)
HIGHLIGHT = (255, 255, 0)
GRAY = (128, 128, 128)
LIGHT_GRAY = (245, 245, 245)

def get_fonts():
    """Load fonts with fallbacks"""
    try:
        font_bold = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 14)
        font_regular = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 14)
        font_small = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 11)
    except:
        font_bold = ImageFont.load_default()
        font_regular = ImageFont.load_default()
        font_small = ImageFont.load_default()
    return font_bold, font_regular, font_small

def create_email_thumbnail(filename, email_data, doc_id):
    """Create a thumbnail that looks like an email document"""
    img = Image.new('RGB', (WIDTH, HEIGHT), WHITE)
    draw = ImageDraw.Draw(img)
    font_bold, font_regular, font_small = get_fonts()

    y = 15

    # Email headers
    headers = [
        ('To:', email_data.get('to', '')),
        ('From:', email_data.get('from', '')),
        ('Sent:', email_data.get('sent', '')),
        ('Subject:', email_data.get('subject', '')),
    ]

    for label, value in headers:
        draw.text((20, y), label, fill=DARK_BLUE, font=font_bold)
        draw.text((85, y), value, fill=BLACK, font=font_regular)
        y += 22

    y += 10

    # Body text
    body_lines = email_data.get('body', [])
    for line in body_lines:
        if isinstance(line, tuple):
            # Highlighted text
            text, is_highlight = line
            if is_highlight:
                bbox = draw.textbbox((20, y), text, font=font_regular)
                draw.rectangle([bbox[0]-2, bbox[1]-2, bbox[2]+2, bbox[3]+2], fill=HIGHLIGHT)
            draw.text((20, y), text, fill=BLACK, font=font_regular)
        else:
            draw.text((20, y), line, fill=BLACK, font=font_regular)
        y += 20

    # Footer bar
    footer_y = HEIGHT - 30
    draw.rectangle([0, footer_y, WIDTH, HEIGHT], fill=DARK_BLUE)
    footer_text = f"U.S. Department of Justice  •  {doc_id}"
    bbox = draw.textbbox((0, 0), footer_text, font=font_small)
    text_width = bbox[2] - bbox[0]
    draw.text(((WIDTH - text_width) // 2, footer_y + 8), footer_text, fill=WHITE, font=font_small)

    # Save
    filepath = os.path.join('images', filename)
    img.save(filepath, 'PNG')
    print(f"✓ Created {filepath}")

# Article thumbnails
thumbnails = [
    {
        'filename': 'branson-thumb.png',
        'doc_id': 'DOJ-EPSTEIN-BRANSON',
        'email': {
            'to': 'Jeffrey Epstein',
            'from': 'Richard Branson',
            'sent': 'Wed 9/11/2013 2:34:12 PM',
            'subject': 'Re: Nice seeing you',
            'body': [
                'Dear Jeffrey,',
                '',
                'It was really nice seeing you yesterday.',
                'The boys in Watersports can\'t stop speaking',
                'about it! Any time you\'re in the area would',
                ('love to see you. As long as you bring your harem!', True),
            ]
        }
    },
    {
        'filename': 'brin-thumb.png',
        'doc_id': 'DOJ-EPSTEIN-GOOGLE',
        'email': {
            'to': 'Sergey Brin',
            'from': 'Ghislaine Maxwell',
            'sent': 'March 2003',
            'subject': 'TED follow-up',
            'body': [
                'Hi Sergey,',
                '',
                ('I was the crazy girl with short dark hair', True),
                ('who flew a Black Hawk in Colombia', True),
                ('and a friend of Jeffrey Epstein.', True),
                '',
                'Let me know if you\'re in NY soon.',
            ]
        }
    },
    {
        'filename': 'thiel-thumb.png',
        'doc_id': 'DOJ-EPSTEIN-THIEL',
        'email': {
            'to': '[Calendar Entry]',
            'from': 'Jeffrey Epstein',
            'sent': 'Fri 4/8/2016',
            'subject': 'Schedule',
            'body': [
                '',
                ('LUNCH w/ Peter Thiel', True),
                '',
                'Location: Thiel Capital, San Francisco',
                '',
                '[Limo service booking confirmed]',
            ]
        }
    },
    {
        'filename': 'harris-thumb.png',
        'doc_id': 'DOJ-EPSTEIN-HARRIS',
        'email': {
            'to': 'Jeffrey Epstein',
            'from': 'Josh Harris',
            'sent': 'December 2014',
            'subject': 'Re: breakfast',
            'body': [
                'Epstein: did you hve fun at breakfast',
                '',
                ('Harris: Yes very much.', True),
                ('Thank you for inviting me.', True),
                '',
                '[Re: Dec 5 breakfast with Bill Gates]',
            ]
        }
    },
    {
        'filename': 'oz-thumb.png',
        'doc_id': 'DOJ-EPSTEIN-OZ',
        'email': {
            'to': '[Transaction Record]',
            'from': 'Epstein Financial Records',
            'sent': '2004',
            'subject': 'Travel Payment',
            'body': [
                '',
                'Vendor: Shoppers Travel, Inc.',
                ('Amount: $1,592.00', True),
                ('Purpose: Travel for Dr. Mehmet Oz', True),
                '',
                '[Financial transaction record]',
            ]
        }
    },
]

# Create all thumbnails
for thumb in thumbnails:
    create_email_thumbnail(thumb['filename'], thumb['email'], thumb['doc_id'])

print("\n" + "=" * 50)
print("All styled thumbnails created!")
