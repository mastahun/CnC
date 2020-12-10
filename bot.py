import main
import PIL
import discord
from discord.ext import commands

from urllib.request import Request, urlopen


TOKEN = "NzY2MjYyMzU3NjU1MDI3NzEy.X4gzbg.tm8t3L3UMVsTPpoDt6nGfJPICNk"


bot = commands.Bot(command_prefix='!', description="Welcome to the Arena! Meet Craxus the Undefeated!",
                   case_insensitive=True)


TYPES = ["Unit", "Building", "Spell"]
RARITIES = ["Common", "Rare", "Epic", "Legendary"]
FRACTIONS = ["Neutral", "Crusader", "Pirate", "Viking", "Ninja", "Warlock", "Druid", "Hentai"]
WEAPONS = ["Melee", "Ranged"]




@bot.command(pass_context=True)
async def greetings(ctx):
    await ctx.send("GREETINGS, MORTAL!")


@bot.command(pass_context=True)
async def silly(ctx):
    await ctx.send("You face ultimate power! Only one of us leaves here alive!")




@bot.command(pass_context=True)
async def save(ctx, text):
    try:
        link = ctx.message.attachments[0].url
        request = Request(link, headers={"User-Agent": "Mozilla/5.0"})
        pic = urlopen(request)
        file = open("archive/" + str(text) + ".png", 'wb+')
        file.write(pic.read())
        file.close()

        await ctx.send("Tremendous success! You can access this card by typing !require \"{}\"".format(text))


    except:
        await ctx.send("Fail! I don't know why though, don't blame yourself.")



@bot.command(pass_context=True)
async def require(ctx, name):
    await ctx.send("BEHOLD THE KNOWLEDGE!", file=discord.File("archive/" + str(name) + ".png"))

@bot.command(pass_context=True)
async def fail(ctx):
    await ctx.send("YOU FAILED!", file=discord.File("rick.png"))


@bot.command(pass_context=True)
async def card(ctx, name):
    def prs(s):
        x = s
        print(s)
        if len(s) > 0:
            while x[-1] == ' ':
                print(s[:-1])
                x = s[:-1]
            while x[0] == ' ':
                x = s[1:]
            print(x)
            return x
        else:
            return x



    def dis(s):
        x = []
        ignore = False
        t = ""

        for it in s:
            if it == '"':
                if not ignore:
                    x.append(t)
                    t = ""

                else:
                    t += it
                    ignore = False
            elif it == '\\':
                ignore = True
            else:
                t += it
                ignore = False
        if t != "":
            x.append(t)

        return x
    stats = {}
    try:
        text = ctx.message.content

        link = ctx.message.attachments[0].url
        request = Request(link, headers={"User-Agent": "Mozilla/5.0"})

        pic = urlopen(request)
        file = open("pic.png", 'wb+')

        file.write(pic.read())
        file.close()
        stats["picture"] = 'pic.png'
    except:
        text = ctx.message.content
        stats["picture"] = 'default.png'
        await ctx.send("Mah man, u forgot the picture")

    red = dis(text)
    if len(red) > 3:
        race = red[3]
    else:
        race = None
    if len(red) > 5:
        card_text = red[5]
    else:
        card_text = None

    red = red[2].split("\n")[1:]
    name = name

    der = []

    for each in red:
        der.append(prs(each))

    for each in der:
        if each.capitalize() in TYPES:
            stats["type"] = each
        elif each.capitalize() in RARITIES:
            stats["rarity"] = each
        elif each.capitalize() in FRACTIONS:
            stats["fraction"] = each
        elif '/' in each:
            if stats["type"] != "Spell":
                stats["attack"] = each.split('/')[0]
                stats["hp"] = each.split('/')[1]
        elif each.capitalize() in WEAPONS:
            if stats["type"] != "Spell":
                stats["weapon"] = each

        if each.capitalize() == "Shiny":
            stats["shiny"] = True

    try:
        if stats["shiny"]:
            pass
    except:
        stats["shiny"] = False

    stats["race"] = race
    stats["name"] = name
    stats["card_text"] = card_text
    stats["cost"] = der[1][:-1]


    if stats["type"] != "Spell":
        img = main.composite(fraction=stats["fraction"].lower(), shiny=stats["shiny"], picture=stats["picture"],
                             rarity=stats["rarity"].lower(), weapon=stats["weapon"], cost=stats["cost"],
                             attack=stats["attack"], hp=stats["hp"], name=stats["name"], race=stats["race"],
                             text=stats["card_text"], type=stats["type"])
    else:
        img = main.composite(fraction=stats["fraction"].lower(), shiny=stats["shiny"], picture=stats["picture"],
                             rarity=stats["rarity"].lower(), cost=stats["cost"], name=stats["name"], race=stats["race"],
                             text=stats["card_text"], type=stats["type"])
    img.save("card.png")
    await ctx.send("BEHOLD THE POWER", file=discord.File("card.png"))


if __name__ == "__main__":
    print("CRAXUS HAS ARRIVED!")
    bot.run(TOKEN)