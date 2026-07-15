import os
import discord
from discord.ext import commands, tasks

from news import pobierz_najnowszy_news
from embeds import stworz_embed

import os
import discord
from discord.ext import commands

TOKEN = os.getenv("TOKEN")

NEWS_DBD_ID = 966810002788597780

PLIK_OSTATNI_LINK = "ostatni_link.txt"

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)


def wczytaj_ostatni_link():
    if os.path.exists(PLIK_OSTATNI_LINK):
        with open(PLIK_OSTATNI_LINK, "r", encoding="utf-8") as f:
            return f.read().strip()
    return None


def zapisz_ostatni_link(link):
    with open(PLIK_OSTATNI_LINK, "w", encoding="utf-8") as f:
        f.write(link)


ostatni_link = wczytaj_ostatni_link()


@bot.event
async def on_ready():
    print(f"{bot.user} jest online!")

    if not sprawdz_news.is_running():
        sprawdz_news.start()


@bot.command()
async def news(ctx):

    news = pobierz_najnowszy_news()

    if news is None:
        await ctx.send("❌ Nie udało się pobrać newsa.")
        return

    embed = stworz_embed(news)

    await ctx.send(embed=embed)


@tasks.loop(minutes=60)
async def sprawdz_news():

    global ostatni_link

    kanal = bot.get_channel(NEWS_DBD_ID)

    if kanal is None:
        print("Nie znaleziono kanału news-dbd")
        return

    news = pobierz_najnowszy_news()

    if news is None:
        print("Nie udało się pobrać newsów.")
        return

    if news["link"] != ostatni_link:

        print("NOWY NEWS!")
        print(news["tytul"])

        embed = stworz_embed(news)

        await kanal.send(embed=embed)

        print("EMBED WYSŁANY")

        ostatni_link = news["link"]
        zapisz_ostatni_link(ostatni_link)

    else:
        print("Brak nowych newsów.")

    print("Sprawdzono newsy DBD")


bot.run(TOKEN)
