#!/usr/bin/env python3
"""
Twitter/X bot for Epstein Exposed
Posts tweets for new articles and reshares old ones.
"""

import os
import json
import random
import tweepy
from datetime import datetime

def get_twitter_client():
    """Initialize Twitter API client with OAuth 1.0a."""
    client = tweepy.Client(
        consumer_key=os.environ['TWITTER_API_KEY'],
        consumer_secret=os.environ['TWITTER_API_SECRET'],
        access_token=os.environ['TWITTER_ACCESS_TOKEN'],
        access_token_secret=os.environ['TWITTER_ACCESS_TOKEN_SECRET']
    )
    return client

def tweet_new_article(headline, url, tag=None):
    """Tweet about a newly published article."""
    client = get_twitter_client()

    # Create engaging tweet text (max 280 chars)
    # Leave room for URL (23 chars for t.co)

    templates = [
        "🚨 BREAKING: {headline}\n\n{url}",
        "📄 NEW: {headline}\n\n{url}",
        "🔍 JUST PUBLISHED: {headline}\n\n{url}",
        "⚠️ {headline}\n\nRead more: {url}",
        "NEW from the DOJ Epstein files:\n\n{headline}\n\n{url}",
    ]

    template = random.choice(templates)
    tweet_text = template.format(headline=headline, url=url)

    # Truncate headline if tweet is too long
    if len(tweet_text) > 280:
        max_headline_len = 280 - len(template.format(headline='', url=url)) - 3
        truncated_headline = headline[:max_headline_len] + "..."
        tweet_text = template.format(headline=truncated_headline, url=url)

    response = client.create_tweet(text=tweet_text)
    print(f"Tweeted: {tweet_text}")
    print(f"Tweet ID: {response.data['id']}")
    return response

def tweet_reshare(headline, url, original_date=None):
    """Reshare an older article."""
    client = get_twitter_client()

    templates = [
        "In case you missed it:\n\n{headline}\n\n{url}",
        "📌 From the archives:\n\n{headline}\n\n{url}",
        "Worth another look:\n\n{headline}\n\n{url}",
        "🔁 Icymi: {headline}\n\n{url}",
        "Still relevant:\n\n{headline}\n\n{url}",
    ]

    template = random.choice(templates)
    tweet_text = template.format(headline=headline, url=url)

    if len(tweet_text) > 280:
        max_headline_len = 280 - len(template.format(headline='', url=url)) - 3
        truncated_headline = headline[:max_headline_len] + "..."
        tweet_text = template.format(headline=truncated_headline, url=url)

    response = client.create_tweet(text=tweet_text)
    print(f"Reshared: {tweet_text}")
    print(f"Tweet ID: {response.data['id']}")
    return response

def get_all_articles():
    """Get list of all articles with their metadata."""
    articles = []

    # Hardcoded initial articles
    initial_articles = [
        {
            "slug": "musk-epstein-emails",
            "headline": '"What Day Will Be the Wildest Party?" Elon Musk\'s Desperate Texts to Epstein Exposed',
            "date": "2026-02-02"
        },
        {
            "slug": "bannon-epstein-texts",
            "headline": "Steve Bannon Got a Free Apple Watch, Private Planes, and Hundreds of Texts from Epstein",
            "date": "2026-02-01"
        },
        {
            "slug": "lutnick-yacht-island",
            "headline": "Commerce Secretary Lutnick Brought His Kids to Epstein's Island on a Yacht",
            "date": "2026-01-31"
        },
        {
            "slug": "prince-andrew-dinner",
            "headline": "The Dinner Party: Prince Andrew, Woody Allen, Katie Couric—All at Epstein's House",
            "date": "2026-01-31"
        },
        {
            "slug": "clinton-plane-trips",
            "headline": '"32 Plane Trips": The Clinton-Epstein Connection in Black and White',
            "date": "2026-01-30"
        }
    ]

    articles.extend(initial_articles)

    # Try to load any additional articles from a manifest file
    try:
        with open('articles.json', 'r') as f:
            extra_articles = json.load(f)
            articles.extend(extra_articles)
    except FileNotFoundError:
        pass

    return articles

def pick_random_article_for_reshare():
    """Pick a random article to reshare."""
    articles = get_all_articles()
    if not articles:
        print("No articles found to reshare")
        return None

    article = random.choice(articles)
    return article

def main():
    """Main entry point - handles both new tweets and reshares."""
    import sys

    if len(sys.argv) < 2:
        print("Usage: tweet.py <new|reshare> [headline] [url]")
        sys.exit(1)

    action = sys.argv[1]

    if action == "new":
        if len(sys.argv) < 4:
            print("Usage: tweet.py new <headline> <url>")
            sys.exit(1)
        headline = sys.argv[2]
        url = sys.argv[3]
        tweet_new_article(headline, url)

    elif action == "reshare":
        article = pick_random_article_for_reshare()
        if article:
            url = f"https://epstein-exposed.com/{article['slug']}.html"
            tweet_reshare(article['headline'], url, article.get('date'))
        else:
            print("No articles available for reshare")
            sys.exit(1)

    else:
        print(f"Unknown action: {action}")
        sys.exit(1)

if __name__ == "__main__":
    main()
