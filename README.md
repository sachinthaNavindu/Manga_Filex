# 📚 MangaCord Bot

**MangaCord** is a feature-rich Discord bot that provides manga recommendations using the [Jikan API](https://jikan.moe/), which fetches data from MyAnimeList. This bot enhances your server with manga discovery, periodic suggestions, and personalized recommendations.

---

## ✨ Features

- 🎲 `!recom [genre]`: Get a random manga recommendation. If no genre is provided, it sends a top-rated manga.
- ⏰ Auto-posts manga suggestions every 2 hours.
- 🧠 Detects message activity and sends a reading reminder after 80 messages.
- ⏳ Automatically deletes auto-sent recommendations after 25 minutes.
- 📌 Integrated search link to [MangaCord website](https://mangacord.netlify.app/).

---

## 📦 Tech Stack

- **Language:** Python 3
- **Libraries:** 
  - [`discord.py`](https://github.com/Rapptz/discord.py)
  - [`aiohttp`](https://docs.aiohttp.org/en/stable/)
  - [`requests`](https://pypi.org/project/requests/)
  - `dotenv` (for managing secrets)
- **API:** [Jikan API v4](https://docs.api.jikan.moe/)
- **Hosting:** Compatible with both local and cloud platforms (e.g. Replit, Railway, Heroku).

---

## 🚀 Setup & Installation

1. **Clone the Repository**

```bash
git clone https://github.com/sachinthaNavindu/Manga_Filex.git
cd mangacord-bot
