import os
import argparse
from sentiment_project.sentiment import aggregator


def main():
    parser = argparse.ArgumentParser(description="Aggregate and summarize news about portfolio companies.")
    parser.add_argument("feed_url", help="RSS feed URL for portfolio company news")
    parser.add_argument("--openai-key", dest="openai_key", default=os.getenv("OPENAI_API_KEY"), help="OpenAI API key")
    parser.add_argument("--twitter-bearer", dest="bearer_token", default=os.getenv("TWITTER_BEARER_TOKEN"), help="Twitter API bearer token")
    args = parser.parse_args()

    results = aggregator.aggregate_feed(args.feed_url, args.openai_key, args.bearer_token)
    for item in results:
        print(f"\n=== {item['title']} ===")
        print(f"Source: {item['link']}")
        print("Summary and Sentiment:\n", item['article_summary'])
        print("Twitter Sentiment:\n", item['twitter_summary'])


if __name__ == "__main__":
    main()
