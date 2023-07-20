# import necessary libraries
import numpy as np
from PIL import Image, ImageDraw
import heapq

# Load the image and convert it to grayscale
origin_image = Image.open('noria.bmp')
img = origin_image.convert('L')
img_arr = np.array(img)
height, width = img_arr.shape

# Create a new image to draw the path on
path_img = Image.new('RGB', img.size, (255, 255, 255))
path_img = origin_image
draw = ImageDraw.Draw(path_img)




# Define the starting and ending points on the image

start = (16, 13)
end = (130, 220)

# Define a function to calculate the Euclidean distance between two points
def distance(a, b):
    x1, y1 = a
    x2, y2 = b
    return np.sqrt((x2 - x1)**2 + (y2 - y1)**2)

# Define a function to check if a point is valid (in bounds and not black)
def valid_point(p):
    x_, y_ = p
    if (0 <= x_ < width) and (0 <= y_ < height):
        if img_arr[y_][x_] == 0:
            return False
        return True
    return False

# Define the algorithm to find the shortest path between two points
def find_shortest_path(start, end):
    
    pq = []  # priority queue to keep the open set of nodes to visit
    heapq.heappush(pq, (0, start))  # add the starting node with priority 0
    
    came_from = {}  # to keep track of the parent node for each visited node
    cost_so_far = {}  # to keep track of the cost of each path to a visited node
    came_from[start] = None  # the starting node has no parent
    cost_so_far[start] = 0  # the cost to reach the starting node is 0
    
    while pq:  # while there are still unexplored nodes
        
        # get the node with the lowest cost so far from the priority queue
        current_cost, current_node = heapq.heappop(pq)
        
        if current_node == end:  # if the end node has been reached, break out of the loop
            break
            
        # Check the neighbours of the current node
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                
                if dx == 0 and dy == 0:  # skip the current node
                    continue
                
                # Calculate the new position and cost to move to the neighbour node
                neighbour = (current_node[0]+dx, current_node[1]+dy)
                new_cost = cost_so_far[current_node] + distance(current_node, neighbour)
                
                # Check if the neighbour is a valid point and update the path to it
                if valid_point(neighbour) and (neighbour not in cost_so_far or new_cost < cost_so_far[neighbour]):
                    cost_so_far[neighbour] = new_cost
                    priority = new_cost + distance(end, neighbour)  # add the Euclidean distance to the end point as priority
                    heapq.heappush(pq, (priority, neighbour))  # add the neighbour node with its priority to the priority queue
                    came_from[neighbour] = current_node  # set the parent node for the neighbour node
        
    # Reconstruct the path by starting from the end node and following the parent nodes back
    path = [end]
    while path[-1] != start:
        path.append(came_from[path[-1]])
    
    return path[::-1]  # Reverse the order of the path to go from start to end

# Use the algorithm to find the shortest path between the start and end points
path = find_shortest_path(start, end)

# Draw the path on the new image
draw.line(path, fill='green', width=1)

# Save the path image
path_img.save('path.png')



'''
from PIL import ImageDraw, Image

# Load the image
img = Image.open("noria.bmp").convert("L")

# Define the start and end points
start_point = (16, 13)
end_point = (130, 220)

# Define a mask to avoid black objects and only navigate the white pixels
mask = img.point(lambda p: 255 if p > 250 else 0, mode="1")

# Create a path using the Draw module
path = Image.new(mode="1", size=img.size)
draw = ImageDraw.Draw(path)

# Define the color green to draw the path
color = 1

# Use breadth-first search to generate the path between the start and end points
queue = [start_point]
visited = set()
parent = {}
found = False

while queue and not found:
    current = queue.pop(0)
    visited.add(current)
    if current == end_point:
        found = True
        break
    for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0), (1, 1), (1, -1), (-1, 1), (-1, -1)]:
        next_point = current[0] + dx, current[1] + dy
        if next_point not in visited and 0 <= next_point[0] < img.size[0] and 0 <= next_point[1] < img.size[1] and mask.getpixel(next_point):
            queue.append(next_point)
            parent[next_point] = current

# Draw the path on the path image using the parent dictionary
if found:
    current = end_point
    while current != start_point:
        draw.point(current, fill=color)
        current = parent[current]

    # Draw the start and end markers
    draw.rectangle((start_point[0]-5, start_point[1]-5, start_point[0]+5, start_point[1]+5), fill=color)
    draw.rectangle((end_point[0]-5, end_point[1]-5, end_point[0]+5, end_point[1]+5), fill=color)
    
    # Show the final result
    path.show()
else:
    print("No path found.")

'''
'''

import numpy as np
import heapq
from PIL import Image, ImageDraw

# load image as grayscale numpy array
img = Image.open('noria.bmp').convert('L')
img_arr = np.array(img)

# define heuristic function for A* algorithm
def heuristic(a, b):
    return np.sqrt((b[0] - a[0])**2 + (b[1] - a[1])**2)

# define A* search algorithm
def astar(array, start, goal):
    frontier = [(0, start)]
    came_from = {}
    cost_so_far = {}
    came_from[start] = None
    cost_so_far[start] = 0

    while frontier:
        current = heapq.heappop(frontier)[1]

        if current == goal:
            break

        for next in neighbors(array, current):
            new_cost = cost_so_far[current] + 1  # Assuming step cost for each step is 1
            if next not in cost_so_far or new_cost < cost_so_far[next]:
                cost_so_far[next] = new_cost
                priority = new_cost + heuristic(goal, next)
                heapq.heappush(frontier, (priority, next))
                came_from[next] = current

    if goal not in came_from:
        print("Goal is not reachable from start.")
        return None, None
    
    # Reconstruct shortest path from start to goal
    path = []
    current = goal
    while current != start:
        path.append(current)
        current = came_from[current]

    path.append(start)
    path.reverse()
    
    return path, cost_so_far[goal]




def neighbors(array, coords):
    neighbors_list = []
    for neighbor in (-1, 0), (0, -1), (0, 1), (1, 0):
        neighbor_row = coords[0] + neighbor[0]
        neighbor_col = coords[1] + neighbor[1]
        if 0 <= neighbor_row < array.shape[0] and 0 <= neighbor_col < array.shape[1] and array[neighbor_row][neighbor_col] == 255 and not any(array[row][col] == 0 for row, col in neighbors_in_between(coords, (neighbor_row, neighbor_col))):
            # Check if the neighboring pixel is within the bounds of the image, has a white color, and does not have black neighbors
            neighbors_list.append((neighbor_row, neighbor_col))
    return neighbors_list


# define function to get neighboring pixels for A* algorithm
def neighbors_in_between(coords1, coords2):
    dx = abs(coords1[1] - coords2[1])
    dy = abs(coords1[0] - coords2[0])
    x = coords1[1]
    y = coords1[0]
    n = 1 + dx + dy
    incx = 1 if coords2[1] > coords1[1] else -1
    incy = 1 if coords2[0] > coords1[0] else -1
    d = dx - dy
    dx *= 2
    dy *= 2
    neighbors_list = []
    for i in range(n):
        if coords1 != (y, x) and coords2 != (y, x):
            neighbors_list.append((y, x))
        if d > 0:
            x += incx
            d -= dy
        else:
            y += incy
            d += dx
    return neighbors_list




# define function to draw path on image
def draw_patzzh(array, path, color):
    img_color = np.zeros((array.shape[0], array.shape[1], 3), dtype=np.uint8)
    img_color[:, :, :] = 255
    for pixel in path:
        img_color[pixel[0], pixel[1]] = color
    img_color = Image.fromarray(img_color)
    img_color.save('noria_shortest_path.bmp')

def draw_path(array, path, color):
    img = Image.open('noria.bmp')
    img_draw = ImageDraw.Draw(img)
    for pixel in path:
        img_draw.point(pixel, fill=color)
    img.save('noria_shortest_path.bmp')





# define start and goal nodes
start = (16, 13)
goal = (130, 220)

# run A* algorithm to find shortest path
path, cost = astar(img_arr, start, goal)

if path is not None:
    print(f"Shortest path cost: {cost}")
    draw_path(img_arr, path, color=(0, 255, 0))
else:
    print("Unable to find shortest path.")


'''
'''
The code first loads the image into a numpy array and defines the heuristic and A* search algorithm functions. 
The `astar` function loops through the frontier until the goal is reached, and the `neighbors` function gets 
the possible neighbor nodes for a given pixel. The `draw_path_from_goal` function takes the path to the goal as 
input and draws it on the image. Finally, we define the start and goal points, run A* algorithm to get the shortest 
path, and draw the path on the image.
'''


'''
import numpy as np
from PIL import Image
import heapq

# Load image and convert it to numpy array
img = Image.open('noria.bmp').convert('L')
img_arr = np.array(img)

# Define heuristic function for A* algorithm
def heuristic(a, b):
    return np.sqrt((b[0] - a[0])**2 + (b[1] - a[1])**2)

# Define A* search algorithm
def astar(array, start, goal):
    
    # Define required variables
    frontier = [(0, start)]
    came_from = {}
    cost_so_far = {}
    came_from[start] = None
    cost_so_far[start] = 0
    
    # Loop through frontier until goal is found
    while frontier:
        current = heapq.heappop(frontier)[1]
        
        if current == goal:
            break
            
        for next in neighbors(array, current):
            new_cost = cost_so_far[current] + 1  # Assuming step cost for each step is 1
            if next not in cost_so_far or new_cost < cost_so_far[next]:
                cost_so_far[next] = new_cost
                priority = new_cost + heuristic(goal, next)
                heapq.heappush(frontier, (priority, next))
                came_from[next] = current
    
    return came_from, cost_so_far

# Define function to get neighbor nodes for A* search algorithm
def neighbors(array, coords):
    neighbors_list = []
    for neighbor in (-1, 0), (0, -1), (0, 1), (1, 0):
        neighbor_row = coords[0] + neighbor[0]
        neighbor_col = coords[1] + neighbor[1]
        if 0 <= neighbor_row < array.shape[0] and 0 <= neighbor_col < array.shape[1] and array[neighbor_row][neighbor_col] == 255:
            neighbors_list.append((neighbor_row, neighbor_col))
    return neighbors_list

# Define function to draw path on image
def draw_path_from_goal(path, img_file):
    img = Image.open(img_file).convert('L')
    img_arr = np.array(img)
    img_green = Image.fromarray(img_arr).convert('RGB')
    for pixel in path:
        img_green.putpixel(pixel, (0, 255, 0))
    img_green.save('noria_shortest_path.bmp')

# Define start and goal points
start = (0, 0)
goal = (img_arr.shape[0]-1, img_arr.shape[1]-1)

# Run A* algorithm on image
came_from, cost_so_far = astar(img_arr, start, goal)

# Get shortest path as a list of pixels
current = goal
path = [current]
while current != start:
    current = came_from[current]
    path.append(current)

# Draw shortest path on image and save it
draw_path_from_goal(path, 'noria.bmp')

'''






'''
from PIL import Image
import heapq

# Load the image and define start and end points
img = Image.open("noria.bmp")
start = (10, 10)
end = (50, 50)

# Convert the image to a two-dimensional array where each element represents a pixel of the image
img_pixels = img.load()
img_array = [[0 if img_pixels[i, j][0] == 255 else 1 for j in range(img.size[1])] for i in range(img.size[0])]



# Define A* algorithm for finding the shortest path
def astar(start, end, grid):
    frontier = []
    heapq.heappush(frontier, (0, start))
    came_from = {}
    cost_so_far = {start: 0}

    while frontier:
        current = heapq.heappop(frontier)[1]

        if current == end:
            break

        for next in neighbors(current, grid):
            new_cost = cost_so_far[current] + cost(current, next)
            if next not in cost_so_far or new_cost < cost_so_far[next]:
                cost_so_far[next] = new_cost
                priority = new_cost + heuristic(end, next)
                heapq.heappush(frontier, (priority, next))
                came_from[next] = current

    return came_from, cost_so_far

def cost(current, next):
    return 1

def heuristic(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def neighbors(node, grid):
    result = []
    for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
        x2 = node[0] + dx
        y2 = node[1] + dy
        if x2 >= 0 and x2 < len(grid) and y2 >= 0 and y2 < len(grid[0]) and grid[x2][y2] == 0:
            result.append((x2, y2))
    return result

# Find the shortest path using A* algorithm
came_from, cost_so_far = astar(start, end, img_array)

print(came_from)
print(cost_so_far)

# Mark the path pixels in a separate array
path_array = [[0 for j in range(img.size[1])] for i in range(img.size[0])]
current = end
while current != start:
    path_array[current[0]][current[1]] = 1
    current = came_from[current]

# Draw the path on the original image
draw = ImageDraw.Draw(img)
for i in range(img.size[0]):
    for j in range(img.size[1]):
        if path_array[i][j]:
            draw.point((i, j), fill=(0, 255, 0))

# Save the modified image
img.save("image_with_path.png")

'''


'''
from PIL import Image, ImageDraw

import math
import heapq

img = Image.open("noria.bmp")
start = (10, 10)  # Starting point
end = (245, 245)  # Ending point

# Define the A* algorithm
def astar(start, end, image):
    # Define the heuristic function
    def heuristic(a, b):
        return math.sqrt((b[0] - a[0]) ** 2 + (b[1] - a[1]) ** 2)
    
    # Define the cost function
    def cost(current, neighbor):
        return abs(current[0] - neighbor[0]) + abs(current[1] - neighbor[1])
    
    # Initialize the open and closed sets
    open_set = []
    closed_set = set()
    heapq.heappush(open_set, (0, start, None))
    
    # Keep searching until we reach the end or run out of options
    while open_set:
        current_cost, current_node, parent = heapq.heappop(open_set)
        if current_node == end:
            # Reconstruct the path
            path = []
            while parent:
                path.append(parent)
                parent = parent[2]
            path.reverse()
            return path
        if current_node in closed_set:
            continue
        for neighbor in [(current_node[0] - 1, current_node[1]), 
                         (current_node[0] + 1, current_node[1]),
                         (current_node[0], current_node[1] - 1),
                         (current_node[0], current_node[1] + 1)]:
            if (0 <= neighbor[0] < image.width and 
                0 <= neighbor[1] < image.height and 
                image.getpixel(neighbor) == 255):
                new_cost = current_cost + cost(current_node, neighbor)
                priority = new_cost + heuristic(neighbor, end)
                heapq.heappush(open_set, (priority, neighbor, (neighbor, current_node, parent)))
        closed_set.add(current_node)
    
    # If we reach this point, there is no path to the end
    return []

path = astar(start, end, img)
print(path)
draw = ImageDraw.Draw(img)

# Draw the path on the image
for i in range(len(path) - 1):
    draw.line((path[i], path[i+1]), fill=(0, 255, 0), width=1)

img.show()
'''