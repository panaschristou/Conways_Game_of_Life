import pygame
import cv2
import numpy as np
import time
import random

pygame.init()
screen_width = 800
screen_height = 800
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Game of Life")
done = False

color_black = (0, 0, 0)
color_white = (255, 255, 255)
blockSize = 20 #Set the size of the grid block
grid_width = screen_width / blockSize # width of the grid in blocks
grid_height = screen_height / blockSize # height of the grid in blocks

generation_count = 0

configuration = [[1,1],[1,2],[2,1],[2,2],[3,1],[3,2]]

def drawGrid():
  # Draw the grid by going from left to right in increments of block size and drawing 
  # a rectangle of size blockSize x blockSize (i.e. a square) of width 1
  for x in range(0, screen_width, blockSize):
    for y in range(0, screen_height, blockSize):
      rect = pygame.Rect(x, y, blockSize, blockSize)
      pygame.draw.rect(screen, color_white, rect, 1)

def initializeGrid(grid_width,grid_height):
  # Create a 2D array of size grid_width x grid_height and initialize each element to 0
  # 0 represents a dead cell and 1 represents a live cell
  grid = [[0 for i in range(int(grid_width))] for j in range(int(grid_height))]
  return grid

def startingGenerationRandom(grid,num_alive = 5):
  # Randomly select num_alive cells to be alive in the starting generation
  for i in range(num_alive):
    x = random.randint(0,grid_width-1)
    y = random.randint(0,grid_height-1)
    grid[x][y] = 1
  return grid

def startingGenerationConfiguration(grid,configuration):
  for i in configuration:
    grid[i[0]][i[1]] = 1

def drawCells(grid):
  # Draw the cells on the screen
  for x in range(int(grid_width)):
    for y in range(int(grid_height)):
      if grid[x][y] == 1:
        rect = pygame.Rect(x*blockSize, y*blockSize, blockSize, blockSize)
        pygame.draw.rect(screen, color_white, rect)

def getNeighborCounts(grid):
  # Get the number of live neighbors for each cell in the grid
  neighbor_count = initializeGrid(grid_width,grid_height)
  for x in range(int(grid_width)):
    for y in range(int(grid_height)):
      neighbor_count[x][y] = getLiveNeighbors(grid,x,y)
  return neighbor_count
      
def getLiveNeighbors(grid, x, y):
  # Get the number of live neighbors for a given cell
  live_neighbors = 0
  for i in range(-1,2):
    for j in range(-1,2):
      if i ==0 and j == 0:
        continue
      elif x+i < 0 or y+j < 0 or x+i >= grid_width or y+j >= grid_height:
        continue
      elif grid[x+i][y+j] == 1:
        live_neighbors += 1
  return live_neighbors

def updateGrid(grid):
  # Update the grid based on the rules of the game
  neighbor_count = getNeighborCounts(grid)
  for x in range(int(grid_width)):
    for y in range(int(grid_height)):
      if grid[x][y] == 1:
        if neighbor_count[x][y] < 2 or neighbor_count[x][y] > 3:
          grid[x][y] = 0
      else:
        if neighbor_count[x][y] == 3:
          grid[x][y] = 1

while not done:
    if generation_count == 0:
      drawGrid()
      initialGrid = initializeGrid(grid_width,grid_height)
      # startingGenerationRandom(initialGrid, 7)
      startingGenerationConfiguration(initialGrid,configuration)
      generation_count += 1
      drawCells(initialGrid)
      Grid = initialGrid
    else:
      updateGrid(Grid)
      drawCells(Grid)
      generation_count += 1
      pygame.time.delay(100)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
    
 
    pygame.display.flip() #Update the full display Surface to the screen