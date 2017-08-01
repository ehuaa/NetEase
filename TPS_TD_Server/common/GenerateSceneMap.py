def generate_grid(width=50, high=100):

	grid = []
	for i in xrange(high):
		row = []
		for j in xrange(width):
			row.append('.')
		grid.append(row)

	# boundary not walkable
	boundary = 1
	for i in xrange(high):
		for j in xrange(boundary):
			grid[i][j] = '*'
			grid[i][width - j - 1] = '*'

	for j in xrange(width):
		for i in xrange(boundary):
			grid[i][j] = '*'
			grid[high - i - 1][j] = '*'

	# center not walkable
	for i in xrange(30, 69):
		for j in xrange(15, 37):
			grid[i][j] = '*'

	# car not walkable
	for i in xrange(0, 5):
		for j in xrange(19, 33):
			grid[i][j] = '*'

	# train not walkable
	for i in xrange(92, high):
		for j in xrange(19, 33):
			grid[i][j] = '*'

	with open('SceneLevelOneMap.txt', 'w') as f:
		for i in xrange(len(grid)):
			for j in xrange(len(grid[i])):
				f.write(grid[i][j])
			f.write('\n')

if __name__ == '__main__':
	generate_grid()




