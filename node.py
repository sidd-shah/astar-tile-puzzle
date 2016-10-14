import copy
# We will use the Node data structure to store the current state
# The current state will include the tiles positions
# Path so far, which is g(n)
# Position of the empty tile

class Node:

	tiles =[[]]
	distance_from_source_node = 0
	path_so_far = []
	empty_pos = []
	heuristic = 1
	# Generate the tile structure by passing an argument containting the arrangement of the tiles
	def __init__(self, node=None, action=None, heuristic=1):
		if node!=None and action!=None:
			self.heuristic = heuristic
			self.tiles = copy.deepcopy(node.tiles)
			
			self.calculate_empty_pos()
			self.make_move(action)
			self.distance_from_source_node = node.distance_from_source_node+1
			self.path_so_far = node.path_so_far[:]
			self.path_so_far.append(action)
		else:
			path_so_far=[]
			tiles = [[]]
			empty_pos = []

	# Calculate the position of the empty tile 
	def calculate_empty_pos(self):
		for i, row in enumerate(self.tiles):
			for j, element in enumerate(row):
				if self.tiles[i][j] == '':
					self.empty_pos = [i,j]

	# This function returns the list of possible moves that the empty tile can make
	# Possible values are L, R, U, D
	def find_possible_moves(self):
		# index of the empty tile 
		index = self.empty_pos
		# print(index)
		possible_moves = []
		if index[1] != len(self.tiles[0])-1:
			possible_moves.append('R')
		if index[1] != 0:
			possible_moves.append('L')
		if index[0] != len(self.tiles[0])-1:
			possible_moves.append('D')
		if index[0] != 0:
			possible_moves.append('U')
		return possible_moves

	def make_move(self,action):
		# print(action)
		if action == 'L':
			self.tiles[self.empty_pos[0]][self.empty_pos[1]], self.tiles[self.empty_pos[0]][self.empty_pos[1]-1] =  \
			self.tiles[self.empty_pos[0]][self.empty_pos[1]-1], self.tiles[self.empty_pos[0]][self.empty_pos[1]]
		elif action == 'R':
			self.tiles[self.empty_pos[0]][self.empty_pos[1]], self.tiles[self.empty_pos[0]][self.empty_pos[1]+1] =  \
			self.tiles[self.empty_pos[0]][self.empty_pos[1]+1], self.tiles[self.empty_pos[0]][self.empty_pos[1]]
		elif action == 'U':
			self.tiles[self.empty_pos[0]][self.empty_pos[1]], self.tiles[self.empty_pos[0]-1][self.empty_pos[1]] =  \
			self.tiles[self.empty_pos[0]-1][self.empty_pos[1]], self.tiles[self.empty_pos[0]][self.empty_pos[1]]
		elif action == 'D':
			self.tiles[self.empty_pos[0]][self.empty_pos[1]], self.tiles[self.empty_pos[0]+1][self.empty_pos[1]] =  \
			self.tiles[self.empty_pos[0]+1][self.empty_pos[1]], self.tiles[self.empty_pos[0]][self.empty_pos[1]]
		# print(self.tiles)
		self.calculate_empty_pos()

	# HEURISTIC FUNCTION - Number of misplaced tiles
	def heuristic_misplaced_tiles(self):
		misplaced_tiles = 0
		n = len(self.tiles)
		for k in range(n*n):
			i = int(k/n)
			j = k%n
			if self.tiles[i][j] == '':
				continue
			if int(self.tiles[i][j]) != k+1:
				misplaced_tiles+=1
		# print('Misplaced tiles ', misplaced_tiles)
		return  misplaced_tiles
	
	# HEURISTIC - Manhattan Distance
	def distance_to_goal_node(self):
		misplaced_tiles = 0
		n = len(self.tiles)
		# print(self.tiles)
		for k in range(n*n):
			i = int(k/n)
			j = k%n
			# We are ignoring the manhattan distance of the empty tile
			# as it will be accounted for in some other misplaced tile
			if self.tiles[i][j] == '':
				continue
				
			if int(self.tiles[i][j]) != k+1:
				num = int(self.tiles[i][j])
				row = (int)((num-1)/n)
				column = (num-1)%n
				misplaced_tiles+=abs(row-i) + abs(column-j)

		# print(self.tiles)
		# print(misplaced_tiles)
		return  misplaced_tiles

	# This function calculates the f(n) value for two nodes and chooses the heuristic 
	# based on the self.heuristic field which is set in the constructor
	def calculate_distances_for_comp(self, other):
		if self.heuristic == 1:
			return self.distance_from_source_node + self.distance_to_goal_node(),\
		 	other.distance_from_source_node + other.distance_to_goal_node()
		else:
			return self.distance_from_source_node + self.heuristic_misplaced_tiles(),\
		 	other.distance_from_source_node + other.heuristic_misplaced_tiles()

	def __le__(self, other):
		distance_self, distance_other = self.calculate_distances_for_comp(other)
		return distance_self <= distance_other

	def __ge__(self,other):
		distance_self, distance_other = self.calculate_distances_for_comp(other)
		return distance_self >= distance_other

	def __lt__(self,other):
		distance_self, distance_other = self.calculate_distances_for_comp(other)
		return distance_self < distance_other

	def __gt__(self,other):
		distance_self, distance_other = self.calculate_distances_for_comp(other)
		return distance_self > distance_other


