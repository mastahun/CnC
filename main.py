from PIL import Image, ImageFont, ImageDraw
import xml.etree.ElementTree as ET

CARDS = {"neutral": [2, 573, 431, 545], "shiny": [2, 19, 437, 552], "crusader": [435, 573, 430, 545],
         "druid": [1307, 19, 430, 545], "ninja": [441, 19, 431, 545], "pirate": [2, 1120, 431, 545],
         "viking": [874, 19, 431, 545], "warlock": [435, 1120, 430, 545]}

BADGES = {"fabled": [1797, 1461, 48, 45], "melee": [1838, 317, 57, 55], "ranged": [770, 1890, 55, 59],
          "hp": [1782, 1908, 65, 54], "common": [296, 1995, 48, 45], "rare": [1808, 1556, 48, 45],
          "epic": [1797, 1461, 48, 45], "legendary": [1748, 1602, 48, 45]}

FONT = {}

png = "saturator_fa_halfStroke.png"

# white font initialization
tree = ET.parse('saturator_fa_halfStroke.fnt')
root = tree.getroot()
for each in root[3]:
    FONT[each.attrib["id"]] = each.attrib

# normal fonts initialization
font_fat = ImageFont.truetype("FranklinGothicLTPro-Dm.ttf", 30)
font_skinny = ImageFont.truetype("FranklinGothicLTPro-Md.ttf", 30)


def main():
    # all litlle icons
    ui = Image.open("ui-everywhere.png")

    for each in CARDS:
        coords = CARDS[each]
        ui.crop((coords[0], coords[1], coords[0] + coords[2], coords[1] + coords[3])).save(each + ".png", mode="RGBA")

    img = composite(fraction="neutral", shiny=False, picture="dragon.png", rarity="rare", weapon="melee", cost=1,
                    type="Unit", attack=1, hp=2, name="Baby drake", race="Dragon",
                    text="Summon a rat with [Deflect] that gets 1/1 for each rat summoned this game")
    img.save("card.png")



def composite(**kwargs):
    img = Image.new("RGBA", (437, 552))

    # 1 fraction
    if kwargs["fraction"] in CARDS:
        img.paste(Image.open(kwargs["fraction"] + ".png"),
                  box=(0, 0, CARDS[kwargs["fraction"]][2], CARDS[kwargs["fraction"]][3]))
    else:
        img.paste(Image.open(kwargs["fraction"] + ".png").resize((437, 552)),
                  box=(0, 0, 437, 552))
    # 2 shiny
    if kwargs["shiny"]:
        img = img.resize((437, 552), resample=0)
        img = Image.alpha_composite(img, Image.open("shiny.png"))

    # 3 picture
    pic = Image.open(kwargs["picture"])
    pic = pic.resize((344, 197), Image.LANCZOS)

    img.paste(pic, (50, 77))
    pic.close()

    # 4 icons

    x = Image.new("RGBA", img.size)
    x.paste(Image.open(kwargs["rarity"] + ".png"), (200, 260))

    if kwargs["type"] != "Spell":
        x.paste(Image.open(kwargs["weapon"] + ".png"), (80, 420))

        x.paste(Image.open("hp.png"), (300, 420))

    img = Image.alpha_composite(img, x)

    # 5 numbers

    timed = []
    cost = str(kwargs["cost"])
    alphabet = Image.open("saturator_fa_halfStroke.png")
    n = 0

    while cost != "":
        x = cost[0]
        stat = FONT[str(ord(x))]
        letter = alphabet.crop((int(stat["x"]), int(stat["y"]), int(stat["x"]) + int(stat["width"]),
                                int(stat["y"]) + int(stat["height"])))
        s = letter.size
        letter = letter.resize((int(s[0] / 5* 3), int(s[1] / 5 *3)), 3)
        timed.append(letter)
        cost = cost[1:]
        n += int(int(stat["xadvance"]) / 5*3)

    f = Image.new("RGBA", img.size)

    off = 0
    for seach in timed:
        z = Image.new("RGBA", img.size)
        z.paste(seach, (int(off + 33 - n / 2), 15))
        off += seach.size[0]
        f = Image.alpha_composite(f, z)

    img = Image.alpha_composite(img, f)

    if kwargs["type"] != "Spell":
        timed = []
        attack = str(kwargs["attack"])
        n = 0

        while attack != "":
            x = attack[0]
            stat = FONT[str(ord(x))]
            letter = alphabet.crop((int(stat["x"]), int(stat["y"]), int(stat["x"]) + int(stat["width"]),
                                    int(stat["y"]) + int(stat["height"])))
            s = letter.size
            letter = letter.resize((int(s[0] / 4 * 3), int(s[1] / 4 * 3)), 3)
            timed.append(letter)
            attack = attack[1:]
            n += int(int(stat["xadvance"]) / 4 * 3)

        f = Image.new("RGBA", img.size)

        off = 0
        for seach in timed:
            z = Image.new("RGBA", img.size)
            z.paste(seach, (int(off + 110 - n / 2), 420))
            off += seach.size[0]
            f = Image.alpha_composite(f, z)

        img = Image.alpha_composite(img, f)

        timed = []
        hp = str(kwargs["hp"])
        n = 0

        while hp != "":
            x = hp[0]
            stat = FONT[str(ord(x))]
            letter = alphabet.crop((int(stat["x"]), int(stat["y"]), int(stat["x"]) + int(stat["width"]),
                                    int(stat["y"]) + int(stat["height"])))
            s = letter.size
            letter = letter.resize((int(s[0] / 4 * 3), int(s[1] / 4 * 3)), 3)
            timed.append(letter)
            hp = hp[1:]
            n += int(int(stat["xadvance"]) / 4 * 3)

        f = Image.new("RGBA", img.size)
        off = 0
        for seach in timed:
            z = Image.new("RGBA", img.size)
            z.paste(seach, (int(off + 330 - n / 2), 420))
            off += seach.size[0]
            f = Image.alpha_composite(f, z)

        img = Image.alpha_composite(img, f)

    # 6 Text

    timed = []
    name = str(kwargs["name"])
    n = 0
    if len(name) < 14:
        while name != "":
            x = name[0]
            stat = FONT[str(ord(x))]
            letter = alphabet.crop((int(stat["x"]), int(stat["y"]), int(stat["x"]) + int(stat["width"]),
                                    int(stat["y"]) + int(stat["height"])))
            s = letter.size
            letter = letter.resize((int(s[0] / 3 * 2), int(s[1] / 3 * 2)), 3)

            z = Image.new("RGBA", img.size)
            z.paste(letter, (n + 80 + int(int(stat["xoffset"]) / 3 * 2), 20 + int(int(stat["yoffset"]) / 3 * 2)))

            timed.append(z)
            name = name[1:]
            n += int(int(stat["xadvance"]) / 3 * 2)
    else:
        while name != "":
            x = name[0]
            stat = FONT[str(ord(x))]
            letter = alphabet.crop((int(stat["x"]), int(stat["y"]), int(stat["x"]) + int(stat["width"]),
                                    int(stat["y"]) + int(stat["height"])))
            s = letter.size
            letter = letter.resize((int(s[0] / 2), int(s[1] / 2)), 3)

            z = Image.new("RGBA", img.size)
            z.paste(letter, (n + 80 + int(int(stat["xoffset"]) / 2), 20 + int(int(stat["yoffset"]) / 2)))

            timed.append(z)
            name = name[1:]
            n += int(int(stat["xadvance"]) / 2)

    f = Image.new("RGBA", img.size)

    for seach in timed:
        f = Image.alpha_composite(f, seach)

    img = Image.alpha_composite(img, f)

    timed = []
    race = str(kwargs["race"])
    n = 0

    w = 0
    for let in race:
        stat = FONT[str(ord(let))]
        w += int(stat["width"])

    while race != "":
        x = race[0]
        stat = FONT[str(ord(x))]
        letter = alphabet.crop((int(stat["x"]), int(stat["y"]), int(stat["x"]) + int(stat["width"]),
                                int(stat["y"]) + int(stat["height"])))
        s = letter.size
        letter = letter.resize((int(s[0] / 2), int(s[1] / 2)), 3)

        z = Image.new("RGBA", img.size)
        z.paste(letter, (n + 20 + int((440 - int(w/2))/2) + int(int(stat["xoffset"]) / 2), 490 + int(int(stat["yoffset"]) / 2)))
        timed.append(z)
        race = race[1:]
        n += int(int(stat["xadvance"]) / 2)

    f = Image.new("RGBA", img.size)
    off = 0
    for seach in timed:
        off += seach.size[0]
        f = Image.alpha_composite(f, seach)

    img = Image.alpha_composite(img, f)

    # 7 THE TEXT

    draw = ImageDraw.Draw(img)
    text = kwargs["text"]

    def diss(st):
        wor = []
        t = ""
        for lett in st:
            if lett == ' ':
                wor.append(t)
                t = ""
            elif lett == '[':
                wor.append(t)
                t = "["
            elif lett == ']':
                wor.append(t+']')
                t = ""
            else:
                t += lett

        if t != "":
            wor.append(t)

        ret = []
        for wo in wor:
            if wo != "":
                ret.append(wo)
        return ret

    if text is not None:
        if len(text) > 0:
            font_size = 30

            words = []

            frame_box = [240, 100]

            w = diss(text)
            print(w)
            is_fat = False

            for word in w:

                if word[0] == "[":
                    is_fat = True
                    if word[-1] != "]":
                        words.append([word[1:], is_fat, []])
                        continue
                if word[-1] == "]":
                    if word[0] == "[":
                        words.append([word[1:-1], is_fat, []])
                    else:
                        words.append([word[:-1], is_fat, []])
                    is_fat = False
                    continue
                words.append([word, is_fat, []])

            kek = True
            fonts = {True: ImageFont.truetype("FranklinGothicLTPro-Dm.ttf", font_size),
                     False: ImageFont.truetype("FranklinGothicLTPro-Md.ttf", font_size)}
            while kek:
                fonts = {True: ImageFont.truetype("FranklinGothicLTPro-Dm.ttf", font_size),
                         False: ImageFont.truetype("FranklinGothicLTPro-Md.ttf", font_size)}
                xy = [0, 0]
                for word in words:
                    word[2] = [xy[0], xy[1]]
                    xy[0] += draw.textsize(word[0], fonts[word[1]])[0] + draw.textsize(" ", fonts[word[1]])[0]

                    if xy[0] > frame_box[0]:
                        xy[0] = 0
                        xy[1] += 5 + draw.textsize("A", font=fonts[False])[1]

                if xy[1] > frame_box[1]:
                    font_size = font_size - 5
                    for arw in words:
                        arw[2] = []

                else:
                    kek = False

            box = [0, 320]

            lines = {}
            l = 0
            le = []
            for word in words:
                if word[2][1] not in le:
                    le.append(word[2][1])
                    l = word[2][1]
                lines[l] = word[2][0] + draw.textsize(word[0], fonts[word[1]])[0]

            spare = Image.new("RGBA", img.size)
            sp_draw = ImageDraw.Draw(spare)


            for word in words:
                if l < 30:
                    draw.text((word[2][0] + (445 - lines[word[2][1]]) / 2, word[2][1] + box[1] + (30 - l)), word[0],
                                fill=(102, 63, 19), font=fonts[word[1]])
                else:
                    draw.text((word[2][0] + (445 - lines[word[2][1]]) / 2, word[2][1] + box[1]), word[0],
                                fill=(102, 63, 19), font=fonts[word[1]])
    return img


if __name__ == '__main__':
    main()
