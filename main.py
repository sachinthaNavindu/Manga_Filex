import discord
from discord.ext import commands, tasks
from dotenv import load_dotenv
import os
import requests
import random

load_dotenv()

TOKEN = os.getenv("DISCORD_TOKEN")
CHANNEL_ID = 1350117296949166193
MESSAGE_SENT = 80
FIXED_MESSAGE = "📚 ** Don't forget to read your favourite manga & manhwas through our [MangaCord website](https://mangacord.netlify.app/)! **"


intents = discord.Intents.default()
intents.messages = True
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)
message_count = 0

genre_map = {
    "action": 1,
    "adventure": 2,
    "comedy": 4,
    "drama": 8,
    "fantasy": 10,
    "horror": 14,
    "romance": 22,
    "sliceoflife": 36,
    "supernatural": 37
}

def get_random_top_manga_embed():
    try:
        response = requests.get("https://api.jikan.moe/v4/top/manga")
        data = response.json()
        manga_list = data["data"]
        manga = random.choice(manga_list)

        return build_manga_embed(manga)
    except Exception as e:
        print(f"Error fetching top Manga: {e}")
        return None

def get_random_genre_manga_embed(genre_id, genre_name):
    try:
        response = requests.get(f"https://api.jikan.moe/v4/manga?genres={genre_id}&order_by=score&sort=desc")
        data = response.json()
        manga_list = data.get("data", [])

        if not manga_list:
            return None

        manga = random.choice(manga_list)
        return build_manga_embed(manga, genre_name)
    except Exception as e:
        print(f"Error fetching genre Manga: {e}")
        return None

def build_manga_embed(manga, genre_name=None):
    title_default = manga.get("title", "No title")
    title_english = manga.get("title_english", None)
    title_japanese = manga.get("title_japanese", None)
    synopsis = manga.get("synopsis", "No description available.")
    image_url = manga["images"]["jpg"]["image_url"]
    search_url = f'https://mangacord.netlify.app/?q={title_default.replace(" ", "+")}'

    title_section = f"📖 **Titles:**\n```"
    if title_english:
        title_section += f"English: {title_english}\n"
    if title_japanese:
        title_section += f"Japanese: {title_japanese}\n"
    title_section += "```"

    if synopsis and len(synopsis) > 300:
        synopsis = synopsis[:297] + "..."

    embed = discord.Embed(
        title=f"📚 {'Top' if not genre_name else genre_name.capitalize()} Manga Recommendation",
        description=(
            f"{title_section}\n"
            f"⚠️ If your manga doesn't appear on the site, try using the Japanese or English name.\n\n"
            f"{synopsis}\n\n"
            f"🔍 [Search on MangaCord]({search_url})"
        )
    )
    embed.set_image(url=image_url)
    embed.set_footer(text="Brought to you by MangaCord Bot")

    return embed

@bot.event
async def on_ready():
    print(f"{bot.user} has connected to Discord!")
    auto_anime_suggestion.start()

@bot.event
async def on_message(message):
    global message_count

    if message.author.bot:
        return

    message_count += 1

    if message_count >= MESSAGE_SENT:
        channel = bot.get_channel(CHANNEL_ID)
        if channel:
            await channel.send(FIXED_MESSAGE)
        message_count = 0

    await bot.process_commands(message)


@bot.command(name="recom")
async def recommend_by_genre(ctx, genre: str = None):
    if genre is None:
        embed = get_random_top_manga_embed()
        if embed:
            await ctx.send("🎲 No genre given, here's a random top manga:", embed=embed)
        else:
            await ctx.send("⚠️ Couldn't fetch a manga recommendation right now.")
        return

    genre_key = genre.lower().replace(" ", "")
    genre_id = genre_map.get(genre_key)

    if not genre_id:
        await ctx.send("⚠️ Genre not found. Try one of these:\n" + ", ".join(genre_map.keys()))
        return

    embed = get_random_genre_manga_embed(genre_id, genre_key)
    if embed:
        await ctx.send(embed=embed)
    else:
        await ctx.send(f"⚠️ Could not fetch manga for genre: {genre_key}")


@tasks.loop(hours=2)
async def auto_anime_suggestion():
    channel = bot.get_channel(CHANNEL_ID)
    if channel:
        embed = get_random_top_manga_embed()
        if embed:
            await channel.send(embed=embed,delete_after=1500)

bot.run(TOKEN)
