import os
import numpy as np
from PIL import Image, ImageDraw

input_directory = "./input/"
output_directory = "./output/"

if not os.path.exists(output_directory):
    os.makedirs(output_directory)


# background_color = (0,   230,   157,   38)

colors = {
    "green": "0, 230, 157",
    "red": "254, 66, 77",
    "pink": "244, 114, 181",
    "acid": "89, 240, 0",
    "yellow": "248, 203, 20",
    "orange": "254, 125, 39",
    "light_blue": "76, 202, 253",
    "gold": "253, 184, 34",
    "indigo": "129, 142, 249",
    "purple": "168, 139, 246",
    "light_red": "247, 111, 109",
    "blue": "96, 165, 248",
    "mono": "0, 0, 0",
}


def create_mask_with_rounded_corners(image, radius):
    mask = Image.new("L", image.size, 255)
    draw = ImageDraw.Draw(mask)
    draw.rectangle((0, 0, image.width, image.height), fill=0)
    draw.ellipse((0, 0, radius * 2, radius * 2), fill=255)
    draw.ellipse((0, image.height - radius * 2, radius * 2, image.height), fill=255)
    draw.ellipse((image.width - radius * 2, 0, image.width, radius * 2), fill=255)
    draw.ellipse(
        (
            image.width - radius * 2,
            image.height - radius * 2,
            image.width,
            image.height,
        ),
        fill=255,
    )
    draw.rectangle((0, radius, image.width, image.height - radius), fill=255)
    draw.rectangle((radius, 0, image.width - radius, image.height), fill=255)
    return mask


for color_name, rgb_string in colors.items():
    if color_name == "mono":
        prebg = (183, 185, 189, 255)
        background_color = (40, 40, 40, 255)
        imageColor = prebg
    else:
        prebg = tuple(map(int, rgb_string.split(", ")))
        background_color = (*prebg, 38)
        imageColor = (*prebg, 255)

    for filename in os.listdir(input_directory):
        if filename.lower().endswith(".png"):
            img_path = os.path.join(input_directory, filename)
            img = Image.open(img_path).convert("RGBA")

            data = np.array(img)

            mask = data[:, :, 3] != 0

            data[mask] = imageColor

            img = Image.fromarray(data)

            background = Image.new("RGBA", (512, 512), background_color)

            corner_radius = 90
            mask = create_mask_with_rounded_corners(background, corner_radius)
            background = Image.composite(
                background, Image.new("RGBA", background.size, (0, 0, 0, 0)), mask
            )

            position = (
                (background.width - img.width) // 2,
                (background.height - img.height) // 2,
            )

            background.paste(img, position, img)

            output_filename = f"{color_name}_{filename}"
            output_path = os.path.join(output_directory, output_filename)

            background.save(output_path, "PNG")
