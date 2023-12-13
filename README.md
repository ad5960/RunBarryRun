## Project Demo

https://github.com/gmadnani/RunBarryRun/assets/13947675/1e6e7f83-ad6a-40a7-bfd6-e612ffccfb89

## Introduction
“Run Barry Run” is a pathfinding algorithm visualizer using PyGame. Our project aims to create an interactive visualization of multiple famous pathfinding algorithms to compare how they perform when reaching from a source to a destination while avoiding obstacles in between.

Users can place a source point (which in our case is the character Flash – Barry Allen, a famous superhero from DC Comics), a destination point, and obstacles between the source and the destination point using mouse clicks. The essence of the project lies in simulating pathfinding algorithms like A*, Dijkstra, Depth-First Search, and Breadth-First Search, to dynamically find a path from the source to the destination while navigating around obstacles. 

## Setup and Running the project

1.	Install all the required libraries for the project to run. (you can either install it using the requirements.txt or download and install requirements separately)
2.	Run the python app using `python app.py`
3.	This will start a new pygame window

##### Navigating through the project
4.	Use your mouse click to add objects on the grid. 
  a.	First mouse click will add the Flash character on the gird (this will be your source)
  b.	Second mouse click will add the Goal on the grid (this will be your destination)
  c.	Now you can click and drag your mouse across the grid to create obstacles
5.	Once you’re satisfied with the grid and the objects, click on either 1, 2, 3, 4 to choose your pathfinding algorithm of choice (1 = DFS, 2 = BFS, 3 = A* Algorithm, 4 = Dijkstra’s Algorithm)
6.	Click Space to start the visualization


## Technologies Used
This project leverages the below technologies
-	PyGame: Used for creating the graphical visualization of the grid environment & character movement
-	Python: We used Python for implementing the pathfinding algorithms, grid logic, and user interactions

## Pathfinding Algorithms Used
The project mostly uses four pathfinding algorithms:
1.	A*: It’s a widely-used algorithm that combines the aspects of Dijkstra’s algorithm and a heuristic to find the most efficient path.
2.	Dijkstra: A pathfinding algorithm that explores all possible paths to find the shortest path possible 
3.	Depth-First Search (DFS): This algorithm explores as far as possible along each branch before backtracking and exploring the neighbor path.
4.	Breadth-First Search (BFS): This algorithm explores all the neighbor nodes at the current depth before moving on to nodes at the next depth level.
