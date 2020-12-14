import sys 

#Cell of the grid
class Cell:
	def __init__(self,parent_i = -1, parent_j = -1, f = 1e10, g = 1e10, h = 1e10):
		self.parent_i = parent_i
		self.parent_j = parent_j
		self.f = f
		self.g = g
		self.h = h
		

	def details(self):
		print(self.parent_i,self.parent_j,self.f,self.g,self.h)


#Pair Class just like pair template in C++
class Pair:
	first = None
	second = None

	def __init__(self, first = None, second = None):
		self.first = first
		self.second = second

	def make_pair(self, first, second):
		self.first = first
		self.second = second

	def first(self):
		return self.first

	def second(self):
		return self.second


class MinHeap: 

	def __init__(self, maxsize): 
		self.maxsize = maxsize 
		self.size = 0
		self.Heap = [Pair()]*(self.maxsize + 1) 
		# self.Heap[0] = -1 * sys.maxsize 
		self.FRONT = 1

	
	def parent(self, pos): 
		return pos//2

	
	def leftChild(self, pos): 
		return 2 * pos 

	 
	def rightChild(self, pos): 
		return (2 * pos) + 1

	
	def isLeaf(self, pos): 
		if pos >= (self.size//2) and pos <= self.size: 
			return True
		return False

	
	def swap(self, fpos, spos): 
		self.Heap[fpos], self.Heap[spos] = self.Heap[spos], self.Heap[fpos] 

	
	def minHeapify(self, pos): 

		if not self.isLeaf(pos): 
			if (self.Heap[pos].first > self.Heap[self.leftChild(pos)].first or
			self.Heap[pos].first > self.Heap[self.rightChild(pos)]).first: 


				if self.Heap[self.leftChild(pos)].first < self.Heap[self.rightChild(pos)].first: 
					self.swap(pos, self.leftChild(pos)) 
					self.minHeapify(self.leftChild(pos)) 


				else: 
					self.swap(pos, self.rightChild(pos)) 
					self.minHeapify(self.rightChild(pos)) 


	def insert(self, element): 
		if self.size >= self.maxsize : 
			return
		self.size+= 1
		self.Heap[self.size] = element 

		current = self.size 
		try:
			while self.Heap[current].first < self.Heap[self.parent(current)].first:
				self.swap(current, self.parent(current)) 
				current = self.parent(current)
		except:
			pass 


	def Print(self): 
		for i in range(1, (self.size//2)+1): 
			print(" PARENT : "+ str(self.Heap[i].first)+" LEFT CHILD : "+
								str(self.Heap[2 * i].first)+" RIGHT CHILD : "+
								str(self.Heap[2 * i + 1].first)) 


	def minHeap(self): 

		for pos in range(self.size//2, 0, -1): 
			self.minHeapify(pos) 


	def remove(self):
		popped = self.Heap[self.FRONT] 
		try: 
			self.Heap[self.FRONT] = self.Heap[self.size] 
			self.size-= 1
			self.minHeapify(self.FRONT) 
		except:
			pass
		return popped

#Check Whether given configuration is valid or not
def isValid(row,col):
	return (row >= 0) and (row < ROW) and (col >= 0) and (col < COL)

#Check if the cell is blocked or not
def isUnblocked(grid, row, col):
	if(grid[row][col] == 1):
		return True
	else:
		return False

#Check if we have reached the destination
def isDestination(row, col, dest):
	if (row == dest.first and col == dest.second):
		return True
	else:
		return False

#Returns the manhatten distance between the current cell and the destination cell
def calculateHeuristics(row, col, dest):
	return abs(row - dest.first) + abs(col - dest.second)

#Trace the path
def Path(cellDetails, dest):
	row = dest.first
	col = dest.second
	Path = []

	while(not(cellDetails[row][col].parent_i == row and cellDetails[row][col].parent_j == col)):
		pair = Pair()
		pair.make_pair(row,col)
		Path.append(pair)
		del pair

		row1 = row

		row = cellDetails[row][col].parent_i
		col = cellDetails[row1][col].parent_j

	pair = Pair()
	pair.make_pair(row,col)
	Path.append(pair)

	grid2 = [["-" for i in range(COL)] for j in range(ROW)]

	while(len(Path) != 0):
		p = Path.pop(0)
		grid2[p.first][p.second] = "X"
		# print(f"->({p.first,p.second})")

	for i in range(ROW):
		for j in range(COL):
			print(grid2[i][j],end=" ")
		print()

#Return the index of the cell with minimum fValue
def minimum(openList):
	index = 0
	value = 1000000.0
	for i,item in enumerate(openList):
		if(item.first < value):
			value = item.first
			index = i
		
	return int(index)

#Main Algorithm
def aStarSearch(grid, src, dest):
	if((isValid(src.first, src.second) == False) or (isValid(dest.first,dest.second) == False)):
		print("Source Or Destination Is Invalid")
		return

	if((isUnblocked(grid,src.first,src.second) == False) or (isUnblocked(grid,dest.first,dest.second) == False)):
		print("Source Or Destination Is Blocked")
		return

	if(isDestination(src.first,src.second,dest) == True):
		print("We are already at the destination")
		return

	#Track of all closed cells
	closedList = [[False for i in range(COL)] for j in range(ROW)]

	#Details of each cell
	cellDetails = [[Cell() for i in range(COL)] for j in range(ROW)]


	i,j = src.first,src.second
	cellDetails[i][j].parent_i = i
	cellDetails[i][j].parent_j = j
	cellDetails[i][j].f = 0
	cellDetails[i][j].g = 0
	cellDetails[i][j].h = 0

	outer_cell = Pair()
	inner_cell = Pair()
	inner_cell.make_pair(i,j)
	outer_cell.make_pair(0.0,inner_cell)

	#Contains all the cells that we may consider later
	# openList = []
	openList = MinHeap(ROW*COL)
	# openList.append(outer_cell)
	openList.insert(outer_cell)
	del inner_cell
	del outer_cell

	#Flag to show if we have reached the destination or not
	success = False

	# while(len(openList) != 0):
	while(openList.size != 0):
		# index = minimum(openList)
		# p = openList.pop(index)
		p = openList.remove()
		i = p.second.first
		j = p.second.second
		closedList[i][j] = True

        ###############################
		#(i-1,j-1)#( i-1,j )#(i-1,j+1)#
		###############################
		#( i,j-1 )#( i , j )#( i,j+1 )#
		###############################
		#(i+1,j-1)#( i+1,j )#(i+1,j+1)#
		###############################
        

        #( i-1,j )
		if(isValid(i-1,j) == True):
			if(isDestination(i-1,j,dest) == True):
				cellDetails[i-1][j].parent_i = i
				cellDetails[i-1][j].parent_j = j
				print("The Destination Is Found 1")
				Path(cellDetails,dest)
				success = True
				return

			elif(closedList[i-1][j] == False and isUnblocked(grid,i-1,j) == True):
				gNew = cellDetails[i][j].g + 1.0
				hNew = calculateHeuristics(i-1, j, dest)
				fNew = gNew + hNew

				if(cellDetails[i-1][j].f == 1e10 or cellDetails[i-1][j].f > fNew):
					outer_cell = Pair()
					inner_cell = Pair()
					inner_cell.make_pair(i-1,j)
					outer_cell.make_pair(fNew,inner_cell)
					
					# openList.append(outer_cell)
					openList.insert(outer_cell)
					del inner_cell
					del outer_cell

					
					cellDetails[i-1][j].f = fNew
					cellDetails[i-1][j].g = gNew
					cellDetails[i-1][j].h = hNew
					cellDetails[i-1][j].parent_i = i
					cellDetails[i-1][j].parent_j = j


        #( i+1,j )
		if(isValid(i+1,j) == True):
			if(isDestination(i+1,j,dest) == True):
				cellDetails[i+1][j].parent_i = i
				cellDetails[i+1][j].parent_j = j
				print("The Destination Is Found 2")
				Path(cellDetails,dest)
				success = True
				return

			elif(closedList[i+1][j] == False and isUnblocked(grid,i+1,j) == True):
				gNew = cellDetails[i][j].g + 1.0
				hNew = calculateHeuristics(i+1, j, dest)
				fNew = gNew + hNew

				if(cellDetails[i+1][j].f == 1e10 or cellDetails[i+1][j].f > fNew):
					outer_cell = Pair()
					inner_cell = Pair()
					inner_cell.make_pair(i+1,j)
					outer_cell.make_pair(fNew,inner_cell)
					
					# openList.append(outer_cell)
					openList.insert(outer_cell)
					del inner_cell
					del outer_cell
					

					cellDetails[i+1][j].f = fNew
					cellDetails[i+1][j].g = gNew
					cellDetails[i+1][j].h = hNew
					cellDetails[i+1][j].parent_i = i
					cellDetails[i+1][j].parent_j = j


        #( i,j+1 )
		if(isValid(i,j+1) == True):
			if(isDestination(i,j+1,dest) == True):
				cellDetails[i][j+1].parent_i = i
				cellDetails[i][j+1].parent_j = j
				print("The Destination Is Found 3")
				Path(cellDetails,dest)
				success = True
				return

			elif(closedList[i][j+1] == False and isUnblocked(grid,i,j+1) == True):
				gNew = cellDetails[i][j].g + 1.0
				hNew = calculateHeuristics(i, j+1, dest)
				fNew = gNew + hNew

				if(cellDetails[i][j+1].f == 1e10 or cellDetails[i][j+1].f > fNew):
					outer_cell = Pair()
					inner_cell = Pair()
					inner_cell.make_pair(i,j+1)
					outer_cell.make_pair(fNew,inner_cell)
					# openList.append(outer_cell)
					openList.insert(outer_cell)
					del inner_cell
					del outer_cell
					

					cellDetails[i][j+1].f = fNew
					cellDetails[i][j+1].g = gNew
					cellDetails[i][j+1].h = hNew
					cellDetails[i][j+1].parent_i = i
					cellDetails[i][j+1].parent_j = j



        #( i,j-1 )
		if(isValid(i,j-1) == True):
			if(isDestination(i,j-1,dest) == True):
				cellDetails[i][j-1].parent_i = i
				cellDetails[i][j-1].parent_j = j
				print("The Destination Is Found 4")
				Path(cellDetails,dest)
				success = True
				return

			elif(closedList[i][j-1] == False and isUnblocked(grid,i,j-1) == True):
				gNew = cellDetails[i][j].g + 1.0
				hNew = calculateHeuristics(i, j-1, dest)
				fNew = gNew + hNew

				if(cellDetails[i][j-1].f == 1e10 or cellDetails[i][j-1].f > fNew):
					outer_cell = Pair()
					inner_cell = Pair()
					inner_cell.make_pair(i,j-1)
					outer_cell.make_pair(fNew,inner_cell)
					
					# openList.append(outer_cell)
					openList.insert(outer_cell)
					del inner_cell
					del outer_cell
					

					cellDetails[i][j-1].f = fNew
					cellDetails[i][j-1].g = gNew
					cellDetails[i][j-1].h = hNew
					cellDetails[i][j-1].parent_i = i
					cellDetails[i][j-1].parent_j = j



        #(i-1,j+1)
		if(isValid(i-1,j+1) == True):
			if(isDestination(i-1,j+1,dest) == True):
				cellDetails[i-1][j+1].parent_i = i
				cellDetails[i-1][j+1].parent_j = j
				print("The Destination Is Found 5")
				Path(cellDetails,dest)
				success = True
				return

			elif(closedList[i-1][j+1] == False and isUnblocked(grid,i-1,j+1) == True):
				gNew = cellDetails[i][j].g + 1.414
				hNew = calculateHeuristics(i-1, j+1, dest)
				fNew = gNew + hNew

				if(cellDetails[i-1][j+1].f == 1e10 or cellDetails[i-1][j+1].f > fNew):
					outer_cell = Pair()
					inner_cell = Pair()
					inner_cell.make_pair(i-1,j+1)
					outer_cell.make_pair(fNew,inner_cell)
					
					# openList.append(outer_cell)
					openList.insert(outer_cell)
					del inner_cell
					del outer_cell
					

					cellDetails[i-1][j+1].f = fNew
					cellDetails[i-1][j+1].g = gNew
					cellDetails[i-1][j+1].h = hNew
					cellDetails[i-1][j+1].parent_i = i
					cellDetails[i-1][j+1].parent_j = j



        #(i-1,j-1)
		if(isValid(i-1,j-1) == True):
			if(isDestination(i-1,j-1,dest) == True):
				cellDetails[i-1][j-1].parent_i = i
				cellDetails[i-1][j-1].parent_j = j
				print("The Destination Is Found 6")
				Path(cellDetails,dest)
				success = True
				return

			elif(closedList[i-1][j-1] == False and isUnblocked(grid,i-1,j-1) == True):
				gNew = cellDetails[i][j].g + 1.414
				hNew = calculateHeuristics(i-1, j-1, dest)
				fNew = gNew + hNew

				if(cellDetails[i-1][j-1].f == 1e10 or cellDetails[i-1][j-1].f > fNew):
					outer_cell = Pair()
					inner_cell = Pair()
					inner_cell.make_pair(i-1,j-1)
					outer_cell.make_pair(fNew,inner_cell)
					
					# openList.append(outer_cell)
					openList.insert(outer_cell)
					del inner_cell
					del outer_cell
					

					cellDetails[i-1][j-1].f = fNew
					cellDetails[i-1][j-1].g = gNew
					cellDetails[i-1][j-1].h = hNew
					cellDetails[i-1][j-1].parent_i = i
					cellDetails[i-1][j-1].parent_j = j



        #(i+1,j+1)
		if(isValid(i+1,j+1) == True):
			if(isDestination(i+1,j+1,dest) == True):
				cellDetails[i+1][j+1].parent_i = i
				cellDetails[i+1][j+1].parent_j = j
				print("The Destination Is Found 7")
				Path(cellDetails,dest)
				success = True
				return

			elif(closedList[i+1][j+1] == False and isUnblocked(grid,i+1,j+1) == True):
				gNew = cellDetails[i][j].g + 1.414
				hNew = calculateHeuristics(i+1, j+1, dest)
				fNew = gNew + hNew

				if(cellDetails[i+1][j+1].f == 1e10 or cellDetails[i+1][j+1].f > fNew):
					outer_cell = Pair()
					inner_cell = Pair()
					inner_cell.make_pair(i+1,j+1)
					outer_cell.make_pair(fNew,inner_cell)
					
					# openList.append(outer_cell)
					openList.insert(outer_cell)
					del inner_cell
					del outer_cell

					cellDetails[i+1][j+1].f = fNew
					cellDetails[i+1][j+1].g = gNew
					cellDetails[i+1][j+1].h = hNew
					cellDetails[i+1][j+1].parent_i = i
					cellDetails[i+1][j+1].parent_j = j



        #(i+1,j-1)
		if(isValid(i+1,j-1) == True):
			if(isDestination(i+1,j-1,dest) == True):
				cellDetails[i+1][j-1].parent_i = i
				cellDetails[i+1][j-1].parent_j = j
				print("The Destination Is Found 8")
				Path(cellDetails,dest)
				success = True
				return

			elif(closedList[i+1][j-1] == False and isUnblocked(grid,i+1,j-1) == True):
				gNew = cellDetails[i][j].g + 1.414
				hNew = calculateHeuristics(i+1, j-1, dest)
				fNew = gNew + hNew

				if(cellDetails[i+1][j-1].f == 1e10 or cellDetails[i+1][j-1].f > fNew):
					outer_cell = Pair()
					inner_cell = Pair()
					inner_cell.make_pair(i+1,j-1)
					outer_cell.make_pair(fNew,inner_cell)
					
					# openList.append(outer_cell)
					openList.insert(outer_cell)
					del inner_cell
					del outer_cell
					

					cellDetails[i+1][j-1].f = fNew
					cellDetails[i+1][j-1].g = gNew
					cellDetails[i+1][j-1].h = hNew
					cellDetails[i+1][j-1].parent_i = i
					cellDetails[i+1][j-1].parent_j = j

    
	if(success == False):
		print("Failed To Find The Destination Cell")
		return

ROW = 9
COL = 10
if __name__ == "__main__":
	grid = [
		[1,0,1,1,1,1,0,1,1,1],
		[1,1,1,0,1,1,1,0,1,1],
		[1,1,1,0,1,1,0,1,0,1],
		[0,0,1,0,1,0,0,0,0,1],
		[1,1,1,0,1,1,1,0,1,0],
		[1,0,1,1,1,1,0,1,0,0],
		[1,0,0,0,0,1,0,0,0,1],
		[1,0,1,1,1,1,0,1,1,1],
		[1,1,1,0,0,0,1,0,0,1]
	]

	src = Pair()
	src.make_pair(8,0)

	dest = Pair()
	dest.make_pair(0,9)

	print(f"Source  is : ({src.first,src.second})")
	print(f"Destination  is : ({dest.first,dest.second})")
	for i in range(ROW):
		for j in range(COL):
			print(grid[i][j],end=" ")
		print()

	print()
	
	aStarSearch(grid, src, dest)

