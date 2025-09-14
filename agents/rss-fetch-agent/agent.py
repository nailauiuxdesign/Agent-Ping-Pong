import feedparser

def fetch_rss_feed(url):
    feed = feedparser.parse(url)
    entries = []
    for entry in feed.entries:
            audio_url = None
            # Revisar si hay enclosure (audio)
            if hasattr(entry, 'enclosures') and entry.enclosures:
                audio_url = entry.enclosures[0].get('href')
            elif hasattr(entry, 'enclosure') and entry.enclosure:
                audio_url = entry.enclosure.get('href')
            entries.append({
                'title': entry.title,
                'link': entry.link,
                'published': entry.published,
                'summary': entry.summary,
                'audio_url': audio_url
            })
    return entries
