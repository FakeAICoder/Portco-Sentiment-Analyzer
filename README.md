# Portfolio Company Sentiment Analyzer

This project now exposes a small web application that aggregates news from an RSS feed and summarizes sentiment using the OpenAI API. A Django backend provides an `/aggregate` endpoint and a simple Node.js server proxies requests to it.

## Setup

1. Install Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Install Node dependencies:
   ```bash
   npm install
   ```
3. Set environment variables:
   - `OPENAI_API_KEY` – OpenAI API key
   - `TWITTER_BEARER_TOKEN` – bearer token for the X.com API

## Running the servers

Start the Django development server on port 8000:
```bash
python sentiment_project/manage.py runserver 8000
```

In another terminal start the Node.js server:
```bash
node server.js
```

The Node server exposes `/news?feed_url=<rss>` which internally calls the Django endpoint and returns summarized results as JSON.

## Command line usage

The original script is still available and can be run directly:
```bash
python aggregate_and_summarize.py <rss_feed_url>
```
