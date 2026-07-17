from PIL import Image, ImageDraw


def make_dot_icon(color: str) -> Image.Image:
    size = 64
    image = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    ImageDraw.Draw(image).ellipse((4, 4, size - 4, size - 4), fill=color)
    return image


ICON_ON = make_dot_icon("#2ecc71")
ICON_OFF = make_dot_icon("#95a5a6")
