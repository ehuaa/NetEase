class Node:
	def __init__(self, value, point):
		self.value = value
		self.point = point
		self.parent = None
		self.H = 0
		self.G = 0

	def move_cost(self):
		return 1 if self.value != '*' else 100000


class PathFinding(object):
	def __init__(self):
		super(PathFinding, self).__init__()

	@staticmethod
	def run(start, goal, grid):
		try:
			return PathFinding.a_star(grid[start[0]][start[2]], grid[goal[0]][goal[2]], grid)
		except:
			print "find path error"
			pass
	@staticmethod
	def children(point, grid):
		x, y = point[0], point[1]
		links = [grid[d[0]][d[1]] for d in [(x - 1, y), (x, y - 1), (x, y + 1), (x + 1, y)]]
		return [link for link in links if link.value != '*']

	@staticmethod
	def manhattan(p1, p2):
		return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])

	@staticmethod
	def check_walkable(node):
		return node.value != '*'

	@staticmethod
	def a_star(start, goal, grid):
		"""
		Return None if we can't find a path
		"""
		if not PathFinding.check_walkable(start) or not PathFinding.check_walkable(goal):
			return None

		# Try to find a path
		open_set = set()
		closed_set = set()
		# set start parent
		start.parent = None
		# Current point is the starting point
		current = start
		# Add the starting point to the open set
		open_set.add(current)
		# While the open set is not empty
		while open_set:
			# Find the item in the open set with the lowest G + H score
			current = min(open_set, key=lambda o: o.G + o.H)
			# If it is the item we want, retrace the path and return it
			if current == goal:
				path = []
				while current.parent:
					path.append(current)
					current = current.parent
				path.append(current)
				return path[::-1]
			# Remove the item from the open set
			open_set.remove(current)
			# Add it to the closed set
			closed_set.add(current)
			# Loop through the node's children/siblings
			for node in PathFinding.children(current.point, grid):
				# If it is already in the closed set, skip it
				if node in closed_set:
					continue
				# Otherwise if it is already in the open set
				if node in open_set:
					# Check if we beat the G score
					new_g = current.G + node.move_cost()
					if node.G > new_g:
						# If so, update the node to have a new parent
						node.G = new_g
						node.parent = current
				else:
					# If it isn't in the open set, calculate the G and H score for the node
					node.G = current.G + node.move_cost()
					node.H = PathFinding.manhattan(node.point, goal.point)
					# Set the parent to our current item
					node.parent = current
					# Add it to the set
					open_set.add(node)
		# There is no path
		# print "Find path error, start: ", start.point, start.value
		# print "goal: ", goal.point, goal.value
		return None
