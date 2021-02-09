import main
import PIL
import discord
from discord.ext import commands
import random

from urllib.request import Request, urlopen


TOKEN = open("token.txt", "r").read()


bot = commands.Bot(command_prefix='!', description="Welcome to the Arena! Meet Craxus the Undefeated!",
                   case_insensitive=True)


TYPES = ["Unit", "Building", "Spell"]
RARITIES = ["Common", "Rare", "Epic", "Legendary"]
FRACTIONS = ["Neutral", "Crusader", "Pirate", "Viking", "Ninja", "Warlock", "Druid", "Hentai", "Candy", "Template",
             "Robot"]
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


quotes = ["Want something to be done good? Do it yourself!",
          "Sometimes you have to do what you have to do.",
          "I only know that I don't know anything.",
          "The night is darkest before dawn.",
          "It takes a dragon to kill a rat.",
          "No matter what wind cannot bow a Mountain.",
          "A stiff branch cannot dance in the wind, for it would snap.",
          "A fire is of anger, it dances with beauty, but will burn you the closer you get.",
          "Harden your hearts, as there are yet goals to reach and difficulties to overcome.",
          "Show must go on!"]


@bot.command(pass_context=True)
async def quote(ctx):

    await ctx.send(quotes[random.randint(0, len(quotes) - 1)])


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
            if it == '"' or it == '”' or it == '“':
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

    print(red)

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

    sts = ["name", "race", "card_text", "cost", "weapon", "hp", "attack", "type", "fraction", "rarity"]
    stsp = ["name", "race", "card_text", "cost", "type", "fraction", "rarity"]
    stss = {"name": "Name", "race": "Race", "card_text": "Card text", "cost": "Cost", "weapon": "Attack type",
            "hp": "Health", "attack": "Attack", "type": "Card type", "fraction": "Faction", "rarity": "Card rarity"}

    try:
        typ = stats["type"]
        if typ == "Spell":
            for each in stsp:
                try:
                    x = stats[each]
                except:
                    await ctx.send("Attribute \"" + stss[each] + "\" is missing")
        else:
            for each in sts:
                try:
                    x = stats[each]
                except:
                    await ctx.send("Attribute \"" + stss[each] + "\" is missing")
    except:
        await ctx.send("Attribute \"" + "Card type" + "\" is missing")


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

    if len(stats["card_text"]) > 78:
        await ctx.send("You might want to make your card text smaller.")

@bot.command(pass_context=True)
async def dualcard(ctx, name):
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
            if it == '"' or it == '”' or it == '“':
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

    print(red)

    red = red[2].split("\n")[1:]
    name = name

    der = []

    for each in red:
        seach = each.split(" ")
        for d in seach:
            der.append(prs(d))

    stats["fraction"] = []
    for each in der:
        if each.capitalize() in TYPES:
            stats["type"] = each
        elif each.capitalize() in RARITIES:
            stats["rarity"] = each
        elif each.capitalize() in FRACTIONS:
            stats["fraction"].append(each)
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

    sts = ["name", "race", "card_text", "cost", "weapon", "hp", "attack", "type", "fraction", "rarity"]
    stsp = ["name", "race", "card_text", "cost", "type", "fraction", "rarity"]
    stss = {"name": "Name", "race": "Race", "card_text": "Card text", "cost": "Cost", "weapon": "Attack type",
            "hp": "Health", "attack": "Attack", "type": "Card type", "fraction": "Faction", "rarity": "Card rarity"}

    try:
        typ = stats["type"]
        if typ == "Spell":
            for each in stsp:
                try:
                    x = stats[each]
                except:
                    await ctx.send("Attribute \"" + stss[each] + "\" is missing")
        else:
            for each in sts:
                try:
                    x = stats[each]
                except:
                    await ctx.send("Attribute \"" + stss[each] + "\" is missing")
    except:
        await ctx.send("Attribute \"" + "Card type" + "\" is missing")


    if stats["type"] != "Spell":
        img = main.dual_gradient(fraction=stats["fraction"][0].lower(), faction=stats["fraction"][1].lower(),
                                  shiny=stats["shiny"], picture=stats["picture"],
                                  rarity=stats["rarity"].lower(), weapon=stats["weapon"], cost=stats["cost"],
                                  attack=stats["attack"], hp=stats["hp"], name=stats["name"], race=stats["race"],
                                  text=stats["card_text"], type=stats["type"])
    else:
        img = main.dual_gradient(fraction=stats["fraction"][0].lower(), faction=stats["fraction"][1].lower(),
                                  shiny=stats["shiny"], picture=stats["picture"],
                                  rarity=stats["rarity"].lower(), cost=stats["cost"], name=stats["name"],
                                  race=stats["race"], text=stats["card_text"], type=stats["type"])
    img.save("card.png")
    await ctx.send("BEHOLD THE POWER", file=discord.File("card.png"))

    if len(stats["card_text"]) > 78:
        await ctx.send("You might want to make your card text smaller.")


@bot.command(pass_context=True)
async def splitcard(ctx, name):
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
            if it == '"' or it == '”' or it == '“':
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

    print(red)

    red = red[2].split("\n")[1:]
    name = name

    der = []

    for each in red:
        seach = each.split(" ")
        for d in seach:
            der.append(prs(d))

    stats["fraction"] = []
    for each in der:
        if each.capitalize() in TYPES:
            stats["type"] = each
        elif each.capitalize() in RARITIES:
            stats["rarity"] = each
        elif each.capitalize() in FRACTIONS:
            stats["fraction"].append(each)
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

    sts = ["name", "race", "card_text", "cost", "weapon", "hp", "attack", "type", "fraction", "rarity"]
    stsp = ["name", "race", "card_text", "cost", "type", "fraction", "rarity"]
    stss = {"name": "Name", "race": "Race", "card_text": "Card text", "cost": "Cost", "weapon": "Attack type",
            "hp": "Health", "attack": "Attack", "type": "Card type", "fraction": "Faction", "rarity": "Card rarity"}

    try:
        typ = stats["type"]
        if typ == "Spell":
            for each in stsp:
                try:
                    x = stats[each]
                except:
                    await ctx.send("Attribute \"" + stss[each] + "\" is missing")
        else:
            for each in sts:
                try:
                    x = stats[each]
                except:
                    await ctx.send("Attribute \"" + stss[each] + "\" is missing")
    except:
        await ctx.send("Attribute \"" + "Card type" + "\" is missing")

    if stats["type"] != "Spell":
        img = main.dual_composite(fraction=stats["fraction"][0].lower(), faction=stats["fraction"][1].lower(),
                                  shiny=stats["shiny"], picture=stats["picture"],
                                  rarity=stats["rarity"].lower(), weapon=stats["weapon"], cost=stats["cost"],
                                  attack=stats["attack"], hp=stats["hp"], name=stats["name"], race=stats["race"],
                                  text=stats["card_text"], type=stats["type"])
    else:
        img = main.dual_composite(fraction=stats["fraction"][0].lower(), faction=stats["fraction"][1].lower(),
                                  shiny=stats["shiny"], picture=stats["picture"],
                                  rarity=stats["rarity"].lower(), cost=stats["cost"], name=stats["name"],
                                  race=stats["race"], text=stats["card_text"], type=stats["type"])
    img.save("card.png")
    await ctx.send("BEHOLD THE POWER", file=discord.File("card.png"))

    if len(stats["card_text"]) > 78:
        await ctx.send("You might want to make your card text smaller.")

if __name__ == "__main__":
    print("CRAXUS HAS ARRIVED!")
    bot.run(TOKEN)
