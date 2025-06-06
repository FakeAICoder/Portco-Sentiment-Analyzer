const express = require('express');
const axios = require('axios');
const app = express();

app.get('/news', async (req, res) => {
  const feedUrl = req.query.feed_url;
  if (!feedUrl) {
    return res.status(400).json({ error: 'feed_url query parameter required' });
  }
  try {
    const response = await axios.get(`http://localhost:8000/aggregate/?feed_url=${encodeURIComponent(feedUrl)}`);
    res.json(response.data);
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
});

app.listen(3000, () => {
  console.log('Node server running on http://localhost:3000');
});
