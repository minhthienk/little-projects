# Import required libraries
from PIL import Image, ImageDraw
import numpy as np

# Load image and convert to array
image = Image.open('noria.bmp')
array = np.array(image)

# Define starting point and ending point
start = (16, 13)
end = (130, 220)

# Define colors as RGB tuples
white = (255, 255, 255)
black = (0, 0, 0)
green = (0, 255, 0)

# Define function to check if a pixel is white
def is_white(pixel):
    return pixel[0] == white[0] and pixel[1] == white[1] and pixel[2] == white[2]

# Define function to get neighboring pixels
def get_neighbors(pixel):
    x, y = pixel
    neighbors = []
    if x > 0:
        neighbors.append((x-1, y))
    if x < 249:
        neighbors.append((x+1, y))
    if y > 0:
        neighbors.append((x, y-1))
    if y < 249:
        neighbors.append((x, y+1))
    return neighbors

# Define function to find shortest path using BFS algorithm
def find_path(start, end):
    queue = [(start, [start])]
    visited = set([start])

    while queue:
        (node, path) = queue.pop(0)
        if node == end:
            return path
        for neighbor in get_neighbors(node):
            if neighbor not in visited and is_white(array[neighbor]):
                queue.append((neighbor, path + [neighbor]))
                visited.add(neighbor)

# Find shortest path
path = find_path(start, end)

# Draw green path on a copy of the original image
image_copy = image.copy()
draw = ImageDraw.Draw(image_copy)
for i in range(len(path)-1):
    if is_white(array[path[i]]) and is_white(array[path[i+1]]):
        draw.line((path[i], path[i+1]), fill=green, width=2)

# Save the resulting image
image_copy.save("path.png")
