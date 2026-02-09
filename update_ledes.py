#!/usr/bin/env python3
"""Update ledes in index.html to use the actual first lines from articles."""

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Map of article slugs to their new ledes (first sentences from articles)
updates = [
    {
        'slug': 'william-barr-epstein-recusal-justice-department.html',
        'old_lede': 'DOJ files reveal AG William Barr blocked recusal demands in Epstein case despite his father\'s ties to the financier and conflicts of interest.',
        'new_lede': 'When Jeffrey Epstein was arrested in July 2019, calls for Attorney General William Barr to recuse himself from the case were immediate and loud.'
    },
    {
        'slug': 'tom-barrack-epstein-trump-fundraising.html',
        'old_lede': 'DOJ files reveal Trump ally Tom Barrack leveraged Epstein\'s network for Middle East deals and political fundraising worth millions.',
        'new_lede': 'The man who raised over $100 million for Donald Trump\'s presidency had a secret weapon: Jeffrey Epstein\'s Rolodex of the world\'s most powerful people.'
    },
    {
        'slug': 'naomi-campbell-epstein-charity-modeling.html',
        'old_lede': 'Newly released DOJ files reveal supermodel Naomi Campbell\'s charity connections to Jeffrey Epstein and private modeling events.',
        'new_lede': 'The fashion world\'s glittering facade has been shattered by explosive new revelations from the Department of Justice\'s latest Epstein file release.'
    },
    {
        'slug': 'oprah-winfrey-epstein-media-empire-meetings.html',
        'old_lede': 'Shocking DOJ files reveal Oprah Winfrey held private meetings with Jeffrey Epstein about media strategy and victim narrative control.',
        'new_lede': 'In a bombshell revelation that threatens to destroy one of America\'s most beloved media icons, newly released DOJ documents expose Oprah Winfrey\'s secret meetings with Jeffrey Epstein.'
    },
    {
        'slug': 'george-stephanopoulos-epstein-abc-interviews.html',
        'old_lede': 'DOJ files reveal ABC anchor George Stephanopoulos secretly helped Jeffrey Epstein plan favorable TV appearances and media strategy.',
        'new_lede': 'The trusted face of ABC News was secretly in Epstein\'s pocket, helping craft his public image.'
    },
    {
        'slug': 'leslie-wexner-victorias-secret-epstein-power-attorney.html',
        'old_lede': 'DOJ files reveal Leslie Wexner gave Jeffrey Epstein complete control over his Victoria\'s Secret fortune and personal life decisions worth over $1 billion.',
        'new_lede': 'Victoria\'s Secret founder Leslie Wexner didn\'t just have a business relationship with Jeffrey Epstein—he gave the convicted sex trafficker complete legal authority over his billion-dollar empire.'
    },
    {
        'slug': 'stephen-schwarzman-blackstone-epstein-connections.html',
        'old_lede': 'DOJ files reveal private equity titan Stephen Schwarzman discussed lucrative investments with Jeffrey Epstein in newly released phone records',
        'new_lede': 'Explosive new documents reveal Stephen Schwarzman, the billionaire CEO of Blackstone Group, maintained regular contact with Jeffrey Epstein about investment opportunities.'
    },
    {
        'slug': 'alan-dershowitz-epstein-legal-advice.html',
        'old_lede': 'DOJ files reveal Harvard\'s Alan Dershowitz received $300,000 from Epstein for \'special legal consultation\' in confidential arrangement.',
        'new_lede': 'Harvard Law School\'s most famous professor was secretly receiving hundreds of thousands of dollars from Jeffrey Epstein for \'special legal consultation.\''
    },
    {
        'slug': 'carlos-slim-epstein-telecom-empire.html',
        'old_lede': 'DOJ files reveal Mexican telecom mogul Carlos Slim\'s hidden business relationship with Jeffrey Epstein involving major infrastructure deals.',
        'new_lede': 'Mexican telecom magnate Carlos Slim, worth over $90 billion and once the world\'s richest man, maintained a clandestine business relationship with Jeffrey Epstein.'
    },
    {
        'slug': 'sergey-brin-epstein-google-meetings.html',
        'old_lede': 'Shocking DOJ files reveal Google co-founder Sergey Brin held multiple private meetings with Jeffrey Epstein to discuss AI and search algorithm modifications.',
        'new_lede': 'Google co-founder Sergey Brin engaged in a series of clandestine meetings with Jeffrey Epstein that centered around artificial intelligence and search algorithm modifications.'
    },
]

for update in updates:
    old = f'<p class="lede">{update["old_lede"]}</p>'
    new = f'<p class="lede">{update["new_lede"]}</p>'

    if old in content:
        content = content.replace(old, new)
        print(f"✓ Updated: {update['slug'].split('.')[0]}")
    else:
        print(f"✗ Not found: {update['slug']}")
        # Try to find partial match to debug
        if update['old_lede'][:50] in content:
            print(f"  (partial match found)")

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("\n" + "=" * 50)
print("Lede updates complete!")
