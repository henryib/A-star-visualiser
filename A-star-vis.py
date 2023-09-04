import pygame, time
from queue import PriorityQueue

#Display settings 
WIDTH = 1000
WIN = pygame.display.set_mode((WIDTH, WIDTH))
pygame.display.set_caption("A* Path Finding visualistion")


#Cell color constants 
RED = (219,62,121)
GREEN = (0,168,107)
BLUE = (0,0,255)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
BLACK = (31,32,34)
PURPLE = (255,233,0)
ORANGE = (255, 165 ,0)
GREY = (128, 128, 128)
TURQUOISE = (64, 224, 208)

class Node:
	"""
   	represents a single cell in the grid
    """
	def __init__(self, row, col, width, total_rows):
		self.row = row
		self.col = col
		self.x = row * width
		self.y = col * width
		self.color = WHITE
		self.neighbors = []
		self.width = width
		self.total_rows = total_rows
	# Respresenting:  unexplored nodes, explore nodes , obstacle nodes , the start node and the end node
	def get_position(self):
		return self.row, self.col

	def closed_node(self):
		return self.color == RED

	def open_node(self):
		return self.color == GREEN

	def wall_node(self):
		return self.color == BLACK

	def start_node(self):
		return self.color == ORANGE

	def end_node(self):
		return self.color == TURQUOISE

	def reset(self):
		self.color = WHITE

	def make_start_node(self):
		self.color = ORANGE

	def make_closed_node(self):
		self.color = RED

	def make_open_node(self):
		self.color = GREEN

	def make_wall_node(self):
		self.color = BLACK

	def make_end_node(self):
		self.color = TURQUOISE

	def make_path(self):
		self.color = PURPLE

	def draw(self, win):
		pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.width))

	def update_adjacent_nodes(self, grid):
		"""
			Checks for valid neighbors around a given node
        	returns nothing 
		
   		"""
		self.neighbors = []
		if self.row < self.total_rows - 1 and not grid[self.row + 1][self.col].wall_node(): # DOWN
			self.neighbors.append(grid[self.row + 1][self.col])

		if self.row > 0 and not grid[self.row - 1][self.col].wall_node(): # UP
			self.neighbors.append(grid[self.row - 1][self.col])

		if self.col < self.total_rows - 1 and not grid[self.row][self.col + 1].wall_node(): # RIGHT
			self.neighbors.append(grid[self.row][self.col + 1])

		if self.col > 0 and not grid[self.row][self.col - 1].wall_node(): # LEFT
			self.neighbors.append(grid[self.row][self.col - 1])

	def __lt__(self, other):
		return False

def heuristic(A, B): 
    """
	Calculates the Manhattan distance between two cells

	"""
    return abs(A[0] - B[0]) + abs(A[1] - B[1])


def reconstruct_path(previous_node, current_node, draw):
	"""
	Traces the path from the start cell to the end cell.

	"""
	while current_node in previous_node:
		current_node = previous_node[current_node]
		current_node.make_path()
		draw()



def algorithm(draw, grid, start, end):
	"""
    Implements the A* algorthim while keeping track of how long it took to run 

    Parameters:
       	draw (list of list of float): A square matrix representing the distances between each pair of cities.
        grid (list of tuple of float): A list of tuples representing the (x, y) coordinates of each city.
		start (list of tuple of float): A list of tuples representing the (x, y) coordinates of each city.
		end (list of tuple of float): A list of tuples representing the (x, y) coordinates of each city.
    Returns:
        true or false.
    """
	start_time = time.time()
	counter = 0
	set_of_open_nodes = PriorityQueue()
	set_of_open_nodes.put((0, counter, start))
	previous_node = {}
	g_score = {node: float("inf") for row in grid for node in row}
	g_score[start] = 0
	f_score = {node: float("inf") for row in grid for node in row}
	f_score[start] = heuristic(start.get_position(), end.get_position())

	set_of_open_nodes_hash = {start}

	while not set_of_open_nodes.empty():
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()

		current_node = set_of_open_nodes.get()[2]
		set_of_open_nodes_hash.remove(current_node)

		if current_node == end:
			end_time = time.time()
			reconstruct_path(previous_node, end, draw)
			end.make_end_node()
			print(f"done in {end_time - start_time:.2f} seconds")
			return True

		for neighbor in current_node.neighbors:
			temp_g_score = g_score[current_node] + 1

			if temp_g_score < g_score[neighbor]:
				previous_node[neighbor] = current_node
				g_score[neighbor] = temp_g_score
				f_score[neighbor] = temp_g_score + heuristic(neighbor.get_position(), end.get_position())
				if neighbor not in set_of_open_nodes_hash:
					counter += 1
					set_of_open_nodes.put((f_score[neighbor], counter, neighbor))
					set_of_open_nodes_hash.add(neighbor)
					neighbor.make_open_node()

		draw()

		if current_node != start:
			current_node.make_closed_node()

	return False


def generate_grid(rows, width):
	"""
	Generates a two-dimensional list of Node objects to represent the grid.
    """
	grid = []
	cell_width = width // rows
	for i in range(rows):
		grid.append([])
		for j in range(rows):
			node = Node(i, j, cell_width, rows)
			grid[i].append(node)

	return grid


def draw_grid(win, rows, width):
	"""
	Draws the grid on the screen
    """
	cell_width = width // rows
	for i in range(rows):
		pygame.draw.line(win, GREY, (0, i * cell_width), (width, i * cell_width))
		for j in range(rows):
			pygame.draw.line(win, GREY, (j * cell_width, 0), (j * cell_width, width))


def draw_window(win, grid , rows, width):
	"""
   	Generates the window with the approriate parameters
    """
	win.fill(WHITE)

	for row in grid:
		for node in row:
			node.draw(win)

	draw_grid(win, rows, width)
	pygame.display.update()


def get_mouse_click_position(pos, rows, width):
	"""
   	Gets the location of a given mouse click
    """
	cell_width = width // rows
	y, x = pos

	row = y // cell_width
	col = x // cell_width

	return row, col


def main(win, width):
	"""
	Main loop is contained here
    """
	ROWS = 50
	grid = generate_grid(ROWS, width)

	start = None
	end = None

	run = True
	while run:
		draw_window(win, grid , ROWS, width)
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				run = False

			if pygame.mouse.get_pressed()[0]: # LEFT
				pos = pygame.mouse.get_pos()
				row, col = get_mouse_click_position(pos, ROWS, width)
				node = grid[row][col]
				if not start and node != end:
					start = node
					start.make_start_node()

				elif not end and node != start:
					end = node
					end.make_end_node()

				elif node != end and node != start:
					node.make_wall_node()

			elif pygame.mouse.get_pressed()[2]: # RIGHT
				pos = pygame.mouse.get_pos()
				row, col = get_mouse_click_position(pos, ROWS, width)
				node = grid[row][col]
				node.reset()
				if node == start:
					start = None
				elif node == end:
					end = None

			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_SPACE and start and end:
					for row in grid:
						for node in row:
							node.update_adjacent_nodes(grid)

					algorithm(lambda: draw_window(win, grid , ROWS, width), grid, start, end)

				if event.key == pygame.K_c:
					start = None
					end = None
					grid = generate_grid(ROWS, width)

	pygame.quit()

main(WIN, WIDTH)