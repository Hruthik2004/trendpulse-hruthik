# Import required libraries
import requests
import json
import time
import os
from datetime import datetime

# API URLs
TOP_STORIES_URL = "https://hacker-news.firebaseio.com/v0/topstories.json"
ITEM_URL = "https://hacker-news.firebaseio.com/v0/item/{}.json"

# Request header
headers = {"User-Agent": "TrendPulse/1.0"}

# Categories and keywords
categories = {
    "technology": ["ai", "software", "tech", "code", "computer", "data", "cloud", "api", "gpu", "llm"],
    "worldnews": ["war", "government", "country", "president", "election", "climate", "attack", "global"],
    "sports": ["nfl", "nba", "fifa", "sport", "game", "team", "player", "league", "championship"],
    "science": ["research", "study", "space", "physics", "biology", "discovery", "nasa", "genome"],
    "entertainment": ["movie", "film", "music", "netflix", "game", "book", "show", "award", "streaming"]
}

# Function to assign category
def assign_category(title):
    title = title.lower()
    for category, keywords in categories.items():
        for word in keywords:
            if word in title:
                return category
    return None


# Step 1: Fetch top story IDs
try:
    response = requests.get(TOP_STORIES_URL, headers=headers, timeout=5)
    story_ids = response.json()[:400]   # reduced for speed
except Exception as e:
    print("Error fetching top stories:", e)
    story_ids = []


# Storage
c_stories = []
c_items = {cat: 0 for cat in categories}


# Step 2: Fetch each story
for story_id in story_ids:

    # Stop once we reach 100+ stories
    if len(c_stories) >= 100:
        break

    try:
        url = ITEM_URL.format(story_id)
        res = requests.get(url, headers=headers, timeout=10)
        story = res.json()
    except Exception as e:
        print(f"Failed to fetch story {story_id}: {e}")
        time.sleep(1)
        continue

    # Skip invalid data
    if not story or "title" not in story:
        continue

    # Assign category
    category = assign_category(story["title"])

    # Only collect valid categorized stories
    if category:

        story_data = {
            "post_id": story.get("id"),
            "title": story.get("title"),
            "category": category,
            "score": story.get("score", 0),
            "num_comments": story.get("descendants", 0),
            "author": story.get("by"),
            "collected_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }

        c_stories.append(story_data)
        c_items[category] += 1

        # Small delay to avoid API overload
        time.sleep(0.1)

        # Pause after every 25 collected stories
        if len(c_stories) % 25 == 0:
            time.sleep(2)


# Step 3: Save to JSON
if not os.path.exists("data"):
    os.makedirs("data")

filename = f"data/trends_{datetime.now().strftime('%Y%m%d')}.json"

with open(filename, "w") as file:
    json.dump(c_stories, file, indent=4)


# Final output
print(f"Collected {len(c_stories)} stories. Saved to {filename}")