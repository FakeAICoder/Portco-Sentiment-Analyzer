# Portfolio Company Sentiment Analyzer

This project aggregates an RSS feed of portfolio company news and summarizes sentiment using the OpenAI API. It also queries the X.com (Twitter) API for recent tweets related to each news item and summarizes the overall Twitter sentiment.

## Setup

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Set the following environment variables:
   - `OPENAI_API_KEY` – OpenAI API key.
   - `TWITTER_BEARER_TOKEN` – Bearer token for the X.com API.

## Usage

Run the script with an RSS feed URL:

```bash
python aggregate_and_summarize.py <rss_feed_url>
```

You can also pass API keys directly:

```bash
python aggregate_and_summarize.py <rss_feed_url> --openai-key YOUR_KEY --twitter-bearer YOUR_TOKEN
```

The script prints a summary and sentiment for each news item and analyzes Twitter sentiment for related discussions.
