import os
import feedparser
import openai
import tweepy


def fetch_rss_entries(feed_url: str):
    """Fetch and parse entries from an RSS feed."""
    feed = feedparser.parse(feed_url)
    return feed.entries


def summarize_text(text: str, openai_api_key: str) -> str:
    """Use OpenAI API to summarize the given text and assess sentiment."""
    openai.api_key = openai_api_key
    prompt = (
        "Summarize the following text in a few sentences and provide a brief"
        " assessment of the sentiment (positive, neutral, or negative).\n\n"
        f"Text:\n{text}"
    )
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=150,
    )
    return response.choices[0].message["content"].strip()


def search_tweets(query: str, bearer_token: str, max_results: int = 10):
    """Search recent tweets using the X.com (Twitter) API."""
    client = tweepy.Client(bearer_token=bearer_token)
    tweets = client.search_recent_tweets(query=query, max_results=max_results)
    if tweets.data:
        return [tweet.text for tweet in tweets.data]
    return []


def aggregate_feed(feed_url: str, openai_key: str, bearer_token: str):
    """Return summaries and Twitter sentiment for each feed entry."""
    if not openai_key:
        raise ValueError("OpenAI API key not provided")
    if not bearer_token:
        raise ValueError("Twitter bearer token not provided")

    results = []
    entries = fetch_rss_entries(feed_url)
    for entry in entries:
        title = entry.get("title", "")
        summary = entry.get("summary", "")
        link = entry.get("link", "")

        article_summary = summarize_text(summary, openai_key)

        tweets = search_tweets(title, bearer_token)
        if tweets:
            tweets_text = "\n".join(tweets)
            tweet_summary = summarize_text(tweets_text, openai_key)
        else:
            tweet_summary = "No recent tweets found for this topic."

        results.append({
            "title": title,
            "link": link,
            "article_summary": article_summary,
            "twitter_summary": tweet_summary,
        })
    return results
