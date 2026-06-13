from PIL import Image, ImageDraw, ImageFont
import os

ASSETS_DIR = os.path.join(os.path.dirname(__file__), 'assets')
os.makedirs(ASSETS_DIR, exist_ok=True)


def create_ascii_image(text_lines, filename, fg=(0, 255, 0), bg=(0, 0, 0, 0)):
    """Create a PNG from ASCII art lines."""
    font_size = 14
    try:
        font = ImageFont.truetype("/data/data/com.termux/files/usr/share/fonts/TTF/DejaVuSansMono.ttf", font_size)
    except (OSError, IOError):
        font = ImageFont.load_default()

    # Measure text
    dummy = Image.new('RGBA', (1, 1))
    draw = ImageDraw.Draw(dummy)

    max_w = 0
    total_h = 0
    line_heights = []
    for line in text_lines:
        bbox = draw.textbbox((0, 0), line, font=font)
        w = bbox[2] - bbox[0]
        h = bbox[3] - bbox[1]
        max_w = max(max_w, w)
        line_heights.append(h)
        total_h += h + 2

    img = Image.new('RGBA', (max_w + 4, total_h + 4), bg)
    draw = ImageDraw.Draw(img)

    y = 2
    for i, line in enumerate(text_lines):
        draw.text((2, y), line, fill=fg, font=font)
        y += line_heights[i] + 2

    path = os.path.join(ASSETS_DIR, filename)
    img.save(path)
    print(f"Created {path} ({img.size[0]}x{img.size[1]})")


# Player ship - ASCII art
player_art = [
    "  /\\  ",
    " /  \\ ",
    "/ A  \\",
    "|    |",
    "|    |",
    "\\    /",
    " \\  / ",
    "  \\/  ",
]

# Enemy ship
enemy_art = [
    "\\    /",
    " \\  / ",
    "  \\/  ",
    " /  \\ ",
    "/    \\",
    "|    |",
    " \\  / ",
    "  \\/  ",
]

# Bullet
bullet_art = [
    " | ",
    " | ",
    " * ",
]

create_ascii_image(player_art, 'player.png', fg=(0, 255, 100))
create_ascii_image(enemy_art, 'enemy.png', fg=(255, 50, 50))
create_ascii_image(bullet_art, 'bullet.png', fg=(255, 255, 0))
print("All assets created!")
