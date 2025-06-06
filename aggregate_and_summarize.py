import os
import argparse
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


def main():
    parser = argparse.ArgumentParser(description="Aggregate and summarize news about portfolio companies.")
    parser.add_argument("feed_url", help="RSS feed URL for portfolio company news")
    parser.add_argument("--openai-key", dest="openai_key", default=os.getenv("OPENAI_API_KEY"), help="OpenAI API key")
    parser.add_argument("--twitter-bearer", dest="bearer_token", default=os.getenv("TWITTER_BEARER_TOKEN"), help="Twitter API bearer token")
    args = parser.parse_args()

    if not args.openai_key:
        raise SystemExit("OpenAI API key not provided")
    if not args.bearer_token:
        raise SystemExit("Twitter bearer token not provided")

    entries = fetch_rss_entries(args.feed_url)
    for entry in entries:
        title = entry.get("title", "")
        summary = entry.get("summary", "")
        link = entry.get("link", "")
        print(f"\n=== {title} ===")
        print(f"Source: {link}")

        # Summarize article
        article_summary = summarize_text(summary, args.openai_key)
        print("Summary and Sentiment:\n", article_summary)

        # Fetch tweets related to the title
        tweets = search_tweets(title, args.bearer_token)
        if tweets:
            tweets_text = "\n".join(tweets)
            tweet_summary = summarize_text(tweets_text, args.openai_key)
            print("Twitter Sentiment:\n", tweet_summary)
        else:
            print("No recent tweets found for this topic.")


if __name__ == "__main__":
    main()
