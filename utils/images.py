from PIL import ImageFont, Image, ImageDraw, ImageColor
from textwrap import wrap

colors = [
(173, 216, 230),
  (0, 191, 255),
 (30, 144, 255),
  (0,   0, 255),
  (0,   0, 139),
 (72,  61, 139),
(123, 104, 238),
(138,  43, 226),
(128,   0, 128),
(218, 112, 214),
(255,   0, 255),
(176,  48,  96),
    (255,  20, 147),
(220,  20,  60),
(240, 128, 128),
(255,  69,   0),
(255, 165,   0),
(244, 164,  96),
(240, 230, 140),
(128, 128,   0),
(139,  69,  19),
(255, 255,   0),
(154, 205,  50),
(124, 252,   0),
(144, 238, 144),
(143, 188, 143),
 (34, 139,  34),
  (0, 255, 127),
  (0, 255, 255),
  (0, 139, 139),
(128, 128, 128),
(255, 255, 25)]

titles = [
"Pride and Prejudice",
"Great Expectations",
"The Old Man and the Sea",
"To the Lighthouse",
"The Great Gatsby",
"Anna Karenina",
"Wuthering Heights",
"The Adventures of Huckleberry Finn",
"Harry Potter and the Sorcerer's Stone",
"To Kill a Mockingbird",
"Beloved",
"One Hundred Years of Solitude",
"1984",
"Murder on the Orient Express",
"The Shining",
"Half of a Yellow Sun",
"Emma",
"David Copperfield",
"One Flew Over the Cuckoo's Nest",
"The Catcher in the Rye",
"The Picture of Dorian Gray",
"Crime and Punishment",
"Gone with the Wind",
"The Hobbit",
"Moby-Dick",
"The Road",
"Americanah",
"Sense and Sensibility",
"Les MisÃ©rables",
"The Sun Also Rises"
]

def cover(text, id):
    size = 35
    color = (0, 0, 0, 255)
    strings = wrap(text, width=15)
    string = "\n".join(strings)

    font = ImageFont.truetype("./app/static/fonts/Roboto-Regular.ttf", size=size)

    img = Image.new("RGBA", (400, 600))
    draw = ImageDraw.Draw(img)

    draw.rectangle((0, 0, 400, 600), fill=(0, 0, 0))
    draw.rectangle((20, 20, 380, 580), fill=(255, 255, 255))

    draw.rectangle((40, 240, 360, 560), fill=colors[id])

    draw_point = (40, 40)
    draw.multiline_text(draw_point, string, font=font, fill=color, align="center")

    img.save(f"app/static/covers/{id + 1}.png")

for (id, title) in enumerate(titles):
    cover(title, id)
