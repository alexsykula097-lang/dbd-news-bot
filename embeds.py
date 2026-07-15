import discord


def stworz_embed(news):

    print("=== DANE EMBEDA ===")
    print(news)

    embed = discord.Embed(
        title=f"📰 {news['tytul']}",
        description=news["opis"],
        color=discord.Color.red()
    )

    if news.get("link"):
        embed.url = news["link"]

    if news.get("obrazek"):
        embed.set_image(url=news["obrazek"])

    embed.set_footer(
        text="DBD NEWS • Oficjalne wiadomości Dead by Daylight"
    )

    return embed