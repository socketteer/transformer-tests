from PIL import Image, ImageDraw
import json
import numpy as np
from colorsys import hsv_to_rgb

rainbow_colors = ['#9400D3', '#4B0082', '#0000FF', '#00FF00', '#FFFF00', '#FF7F00', '#FF0000']

def draw_block_multiverse(multiverse, ground_truth='', canvas_height=1000, canvas_width=1000, block_width=200, show=True):
    img = Image.new("RGB", (canvas_width, canvas_height), 'gray')
    draw = ImageDraw.Draw(img)
    draw_downstream(multiverse, ground_truth, 0, 0, img, draw, canvas_height, block_width, 6)
    if show:
        img.show()
    return img


def draw_downstream(multiverse, ground_truth, y_offset, depth, img, draw, canvas_height, block_width, color_index):
    if not multiverse:
        return
    y = y_offset
    x = depth*block_width
    rainbow_index = color_index % len(rainbow_colors)

    for token, node in multiverse.items():   
        height = canvas_height * node['unnormalized_prob']
        is_ground_truth = (token == ground_truth[0]) if ground_truth else False
        draw.rectangle((x, y, x + block_width, y + height), fill='black' if is_ground_truth else rainbow_colors[rainbow_index])
        if height > 10:
            try:
                if token[:5] != 'bytes':
                    draw.text((x, y), token, fill='white')
                else:
                    draw.text((x, y), '', fill='white')
            except UnicodeEncodeError:
                pass
        draw_downstream(node['children'], ground_truth=ground_truth[1:] if is_ground_truth else '', y_offset=y, depth=depth + 1, img=img, draw=draw, canvas_height=canvas_height, block_width=block_width, color_index=rainbow_index)
        y += height
        rainbow_index = (rainbow_index + 1) % len(rainbow_colors)



def main():
    pass
    

if __name__ == "__main__":
    main()
