"""
 *  MIT License
 *
 *  Copyright (c) 2019 Arpit Aggarwal
 *
 *  Permission is hereby granted, free of charge, to any person obtaining a
 *  copy of this software and associated documentation files (the "Software"),
 *  to deal in the Software without restriction, including without
 *  limitation the rights to use, copy, modify, merge, publish, distribute,
 *  sublicense, and/or sell copies of the Software, and to permit persons to
 *  whom the Software is furnished to do so, subject to the following
 *  conditions:
 *
 *  The above copyright notice and this permission notice shall be included
 *  in all copies or substantial portions of the Software.
 *
 *  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
 *  IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
 *  FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL
 *  THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
 *  LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
 *  FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
 *  DEALINGS IN THE SOFTWARE.
"""

# header files
import numpy as np
import cv2
from heapq import heappush, heappop

# class for AStar
class AStar(object):
    # init function
    def __init__(self, start, goal, clearance, radius):
        self.start = start
        self.goal = goal
        self.numRows = 200
        self.numCols = 300
        self.clearance = clearance
        self.radius = radius
        self.graph = {}
        self.distance = {}
        self.path = {}
        self.costToCome = {}
        self.costToGo = {}
        self.visited = {}
        
        for row in range(1, self.numRows + 1):
            for col in range(1, self.numCols + 1):
                self.visited[(row, col)] = False
                self.path[(row, col)] = -1
                self.graph[(row, col)] = [1, 1, 1, 1, 1.414, 1.414, 1.414, 1.414]
                self.costToCome[(row, col)] = float('inf')
                self.costToGo[(row, col)] = float('inf')
                self.distance[(row, col)] = float('inf') 
    
    # move is valid 
    def IsValid(self, currRow, currCol):
        return (currRow >= (1 + self.radius + self.clearance) and currRow <= (self.numRows - self.radius - self.clearance) and currCol >= (1 + self.radius + self.clearance) and currCol <= (self.numCols - self.radius - self.clearance))
    
    # checks for an obstacle
    def IsObstacle(self, row, col):
        # constants
        sum_of_c_and_r = self.clearance + self.radius
        sqrt_of_c_and_r = 1.4142 * sum_of_c_and_r
        
        # check circle
        dist1 = ((row - 150) * (row - 150) + (col - 225) * (col - 225)) - ((25 + sum_of_c_and_r) * (25 + sum_of_c_and_r))
        
        # check eclipse
        dist2 = ((((row - 100) * (row - 100)) / ((20 + sum_of_c_and_r) * (20 + sum_of_c_and_r))) + (((col - 150) * (col - 150)) / ((40 + sum_of_c_and_r) * (40 + sum_of_c_and_r)))) - 1
        
        # check triangles
        (x1, y1) = (120 - (2.62 * sum_of_c_and_r), 20 - (1.205 * sum_of_c_and_r))
        (x2, y2) = (150 - sqrt_of_c_and_r, 50)
        (x3, y3) = (185 + sum_of_c_and_r, 25 - (sum_of_c_and_r * 0.9247))
        first = ((col - y1) * (x2 - x1)) - ((y2 - y1) * (row - x1))
        second = ((col - y2) * (x3 - x2)) - ((y3 - y2) * (row - x2))
        third = ((col - y3) * (x1 - x3)) - ((y1 - y3) * (row - x3))
        dist3 = 1
        if(first <= 0 and second <= 0 and third <= 0):
            dist3 = 0
            
        (x1, y1) = (150 - sqrt_of_c_and_r, 50)
        (x2, y2) = (185 + sum_of_c_and_r, 25 - (sum_of_c_and_r * 0.9247))
        (x3, y3) = (185 + sum_of_c_and_r, 75 + (sum_of_c_and_r * 0.714))
        first = ((col - y1) * (x2 - x1)) - ((y2 - y1) * (row - x1))
        second = ((col - y2) * (x3 - x2)) - ((y3 - y2) * (row - x2))
        third = ((col - y3) * (x1 - x3)) - ((y1 - y3) * (row - x3))
        dist4 = 1
        if(first >= 0 and second >= 0 and third >= 0):
            dist4 = 0
        
        # check rhombus
        (x1, y1) = (10 - sqrt_of_c_and_r, 225)
        (x2, y2) = (25, 200 - sqrt_of_c_and_r)
        (x3, y3) = (40 + sqrt_of_c_and_r, 225)
        (x4, y4) = (25, 250 + sqrt_of_c_and_r)
        first = ((col - y1) * (x2 - x1)) - ((y2 - y1) * (row - x1))
        second = ((col - y2) * (x3 - x2)) - ((y3 - y2) * (row - x2))
        third = ((col - y3) * (x4 - x3)) - ((y4 - y3) * (row - x3))
        fourth = ((col - y4) * (x1 - x4)) - ((y1 - y4) * (row - x4))
        dist5 = 1
        dist6 = 1
        if(first >= 0 and second >= 0 and third >= 0 and fourth >= 0):
            dist5 = 0
            dist6 = 0
        
        # check square
        (x1, y1) = (150 - sqrt_of_c_and_r, 50)
        (x2, y2) = (120 - sqrt_of_c_and_r, 75)
        (x3, y3) = (150, 100 + sqrt_of_c_and_r)
        (x4, y4) = (185 + sum_of_c_and_r, 75 + (sum_of_c_and_r * 0.714))
        first = ((col - y1) * (x2 - x1)) - ((y2 - y1) * (row - x1))
        second = ((col - y2) * (x3 - x2)) - ((y3 - y2) * (row - x2))
        third = ((col - y3) * (x4 - x3)) - ((y4 - y3) * (row - x3))
        fourth = ((col - y4) * (x1 - x4)) - ((y1 - y4) * (row - x4))
        dist7 = 1
        dist8 = 1
        if(first <= 0 and second <= 0 and third <= 0 and fourth <= 0):
            dist7 = 0
            dist8 = 0
        
        # check rod
        first = ((col - 95) * (8.66 + sqrt_of_c_and_r)) - ((5 + sqrt_of_c_and_r) * (row - 30 + sqrt_of_c_and_r))
        second = ((col - 95) * (37.5 + sqrt_of_c_and_r)) - ((-64.95 - sqrt_of_c_and_r) * (row - 30 + sqrt_of_c_and_r))
        third = ((col - 30.05 + sqrt_of_c_and_r) * (8.65 + sqrt_of_c_and_r)) - ((5.45 + sqrt_of_c_and_r) * (row - 67.5))
        fourth = ((col - 35.5) * (-37.49 - sqrt_of_c_and_r)) - ((64.5 + sqrt_of_c_and_r) * (row - 76.15 - sqrt_of_c_and_r))
        dist9 = 1
        dist10 = 1
        if(first <= 0 and second >= 0 and third >= 0 and fourth >= 0):
            dist9 = 0
            dist10 = 0
        
        if(dist1 <= 0 or dist2 <= 0 or dist3 == 0 or dist4 == 0 or dist5 == 0 or dist6 == 0 or dist7 == 0 or dist8 == 0 or dist9 == 0 or dist10 == 0):
            return True
        return False
    
    # action move one
    def ActionMoveOne(self, currRow, currCol, theta):
        newRow = currRow + np.cos(0 * (3.14159 / 180))
        newCol = currCol + np.sin(0 * (3.14159 / 180))
        newTheta = theta + 0
        if(self.IsValid(newRow, newCol) and self.IsObstacle(newRow, newCol) == False and self.visited[(int(round(newRow)), int(round(newCol)), newTheta)] == False):
            return True
        return False

    # action move two
    def ActionMoveTwo(self, currRow, currCol, theta):
        newRow = currRow + np.cos(30 * (3.14159 / 180))
        newCol = currCol + np.sin(30 * (3.14159 / 180))
        newTheta = theta + 30
        if(self.IsValid(newRow, newCol) and self.IsObstacle(newRow, newCol) == False and self.visited[(int(round(newRow)), int(round(newCol)), newTheta)] == False):
            return True
        return False

    # action move three
    def ActionMoveThree(self, currRow, currCol, theta):
        newRow = currRow + np.cos(60 * (3.14159 / 180))
        newCol = currCol + np.sin(60 * (3.14159 / 180))
        newTheta = theta + 60
        if(self.IsValid(newRow, newCol) and self.IsObstacle(newRow, newCol) == False and self.visited[(int(round(newRow)), int(round(newCol)), newTheta)] == False):
            return True
        return False

    # action move four
    def ActionMoveFour(self, currRow, currCol, theta):
        newRow = currRow + np.cos(-30 * (3.14159 / 180))
        newCol = currCol + np.sin(-30 * (3.14159 / 180))
        newTheta = theta - 30
        if(self.IsValid(newRow, newCol) and self.IsObstacle(newRow, newCol) == False and self.visited[(int(round(newRow)), int(round(newCol)), newTheta)] == False):
            return True
        return False

    # action move five
    def ActionMoveFive(self, currRow, currCol, theta):
        newRow = currRow + np.cos(-60 * (3.14159 / 180))
        newCol = currCol + np.sin(-60 * (3.14159 / 180))
        newTheta = theta - 60
        if(self.IsValid(newRow, newCol) and self.IsObstacle(newRow, newCol) == False and self.visited[(int(round(newRow)), int(round(newCol)), newTheta)] == False):
            return True
        return False
    
    # animate path
    def animate(self, explored_states, backtrack_states, path):
        fourcc = cv2.VideoWriter_fourcc(*'XVID')
        out = cv2.VideoWriter(str(path), fourcc, 20.0, (self.numCols, self.numRows))
        image = np.zeros((self.numRows, self.numCols, 3), dtype=np.uint8)
        count = 0
        for state in explored_states:
            image[self.numRows - state[0], state[1] - 1] = (255, 255, 0)
            if(count%80 == 0):
                out.write(image)
            count = count + 1

        count = 0
        for row in range(1, self.numRows + 1):
            for col in range(1, self.numCols + 1):
                if(image[self.numRows - row, col - 1, 0] == 0 and image[self.numRows - row, col - 1, 1] == 0 and image[self.numRows - row, col - 1, 2] == 0):
                    if(self.IsValid(row, col) and self.IsObstacle(row, col) == False):
                        image[self.numRows - row, col - 1] = (154, 250, 0)
                        if(count%80 == 0):
                            out.write(image)
                        count = count + 1
            
        if(len(backtrack_states) > 0):
            for state in backtrack_states:
                image[self.numRows - state[0], state[1] - 1] = (0, 0, 255)
                out.write(image)
                cv2.imshow('result', image)
                cv2.waitKey(5)
                
        cv2.waitKey(0)
        cv2.destroyAllWindows()
        out.release()

    # euc heuristic
    def euc_heuristic(self, row, col):
        return np.sqrt(((self.goal[0] - row)**2) + ((self.goal[1] - col)**2))
    
    # a-star algo
    def search(self):
        # mark source node and create a queue
        explored_states = []
        queue = []
        heappush(queue, (0, self.start))
        self.distance[self.start] = 0
        self.costToCome[self.start] = 0
        self.costToGo[self.start] = 0
        
        # run a-star
        while(len(queue) > 0):
            # get current node
            _, current_node = heappop(queue)
            self.visited[current_node] = True
            explored_states.append(current_node)
            
            # if goal node then break
            if(current_node[0] == self.goal[0] and current_node[1] == self.goal[1]):
                break
               
            # traverse the edges
            if(self.ActionMoveLeft(current_node[0], current_node[1])):
                new_cost_to_come = self.costToCome[current_node] + self.graph[current_node][0]
                new_cost_to_go = self.euc_heuristic(current_node[0], current_node[1] - 1)
                new_distance = new_cost_to_come + new_cost_to_go
                
                if(self.distance[(current_node[0], current_node[1] - 1)] > new_distance):
                    self.distance[(current_node[0], current_node[1] - 1)] = new_distance
                    self.costToCome[(current_node[0], current_node[1] - 1)] = new_cost_to_come
                    self.costToGo[(current_node[0], current_node[1] - 1)] = new_cost_to_go
                    self.path[(current_node[0], current_node[1] - 1)] = current_node
                    heappush(queue, (new_distance, (current_node[0], current_node[1] - 1)))
            
            if(self.ActionMoveRight(current_node[0], current_node[1])):
                new_cost_to_come = self.costToCome[current_node] + self.graph[current_node][1]
                new_cost_to_go = self.euc_heuristic(current_node[0], current_node[1] + 1)
                new_distance = new_cost_to_come + new_cost_to_go
                
                if(self.distance[(current_node[0], current_node[1] + 1)] > new_distance):
                    self.distance[(current_node[0], current_node[1] + 1)] = new_distance
                    self.costToCome[(current_node[0], current_node[1] + 1)] = new_cost_to_come
                    self.costToGo[(current_node[0], current_node[1] + 1)] = new_cost_to_go
                    self.path[(current_node[0], current_node[1] + 1)] = current_node
                    heappush(queue, (new_distance, (current_node[0], current_node[1] + 1)))
                    
            if(self.ActionMoveUp(current_node[0], current_node[1])):
                new_cost_to_come = self.costToCome[current_node] + self.graph[current_node][2]
                new_cost_to_go = self.euc_heuristic(current_node[0] - 1, current_node[1])
                new_distance = new_cost_to_come + new_cost_to_go
                
                if(self.distance[(current_node[0] - 1, current_node[1])] > new_distance):
                    self.distance[(current_node[0] - 1, current_node[1])] = new_distance
                    self.costToCome[(current_node[0] - 1, current_node[1])] = new_cost_to_come
                    self.costToGo[(current_node[0] - 1, current_node[1])] = new_cost_to_go
                    self.path[(current_node[0] - 1, current_node[1])] = current_node
                    heappush(queue, (new_distance, (current_node[0] - 1, current_node[1])))
                    
            if(self.ActionMoveDown(current_node[0], current_node[1])):
                new_cost_to_come = self.costToCome[current_node] + self.graph[current_node][3]
                new_cost_to_go = self.euc_heuristic(current_node[0] + 1, current_node[1])
                new_distance = new_cost_to_come + new_cost_to_go
                
                if(self.distance[(current_node[0] + 1, current_node[1])] > new_distance):
                    self.distance[(current_node[0] + 1, current_node[1])] = new_distance
                    self.costToCome[(current_node[0] + 1, current_node[1])] = new_cost_to_come
                    self.costToGo[(current_node[0] + 1, current_node[1])] = new_cost_to_go
                    self.path[(current_node[0] + 1, current_node[1])] = current_node
                    heappush(queue, (new_distance, (current_node[0] + 1, current_node[1])))
                    
            if(self.ActionMoveRightDown(current_node[0], current_node[1])):
                new_cost_to_come = self.costToCome[current_node] + self.graph[current_node][4]
                new_cost_to_go = self.euc_heuristic(current_node[0] + 1, current_node[1] + 1)
                new_distance = new_cost_to_come + new_cost_to_go
                
                if(self.distance[(current_node[0] + 1, current_node[1] + 1)] > new_distance):
                    self.distance[(current_node[0] + 1, current_node[1] + 1)] = new_distance
                    self.costToCome[(current_node[0] + 1, current_node[1] + 1)] = new_cost_to_come
                    self.costToGo[(current_node[0] + 1, current_node[1] + 1)] = new_cost_to_go
                    self.path[(current_node[0] + 1, current_node[1] + 1)] = current_node
                    heappush(queue, (new_distance, (current_node[0] + 1, current_node[1] + 1)))
                    
            if(self.ActionMoveRightUp(current_node[0], current_node[1])):
                new_cost_to_come = self.costToCome[current_node] + self.graph[current_node][5]
                new_cost_to_go = self.euc_heuristic(current_node[0] - 1, current_node[1] + 1)
                new_distance = new_cost_to_come + new_cost_to_go
                
                if(self.distance[(current_node[0] - 1, current_node[1] + 1)] > new_distance):
                    self.distance[(current_node[0] - 1, current_node[1] + 1)] = new_distance
                    self.costToCome[(current_node[0] - 1, current_node[1] + 1)] = new_cost_to_come
                    self.costToGo[(current_node[0] - 1, current_node[1] + 1)] = new_cost_to_go
                    self.path[(current_node[0] - 1, current_node[1] + 1)] = current_node
                    heappush(queue, (new_distance, (current_node[0] - 1, current_node[1] + 1)))
                    
            if(self.ActionMoveLeftUp(current_node[0], current_node[1])):
                new_cost_to_come = self.costToCome[current_node] + self.graph[current_node][6]
                new_cost_to_go = self.euc_heuristic(current_node[0] - 1, current_node[1] - 1)
                new_distance = new_cost_to_come + new_cost_to_go
                
                if(self.distance[(current_node[0] - 1, current_node[1] - 1)] > new_distance):
                    self.distance[(current_node[0] - 1, current_node[1] - 1)] = new_distance
                    self.costToCome[(current_node[0] - 1, current_node[1] - 1)] = new_cost_to_come
                    self.costToGo[(current_node[0] - 1, current_node[1] - 1)] = new_cost_to_go
                    self.path[(current_node[0] - 1, current_node[1] - 1)] = current_node
                    heappush(queue, (new_distance, (current_node[0] - 1, current_node[1] - 1)))
                    
            if(self.ActionMoveLeftDown(current_node[0], current_node[1])):
                new_cost_to_come = self.costToCome[current_node] + self.graph[current_node][7]
                new_cost_to_go = self.euc_heuristic(current_node[0] + 1, current_node[1] - 1)
                new_distance = new_cost_to_come + new_cost_to_go
                
                if(self.distance[(current_node[0] + 1, current_node[1] - 1)] > new_distance):
                    self.distance[(current_node[0] + 1, current_node[1] - 1)] = new_distance
                    self.costToCome[(current_node[0] + 1, current_node[1] - 1)] = new_cost_to_come
                    self.costToGo[(current_node[0] + 1, current_node[1] - 1)] = new_cost_to_go
                    self.path[(current_node[0] + 1, current_node[1] - 1)] = current_node
                    heappush(queue, (new_distance, (current_node[0] + 1, current_node[1] - 1)))
                    
        # return if no optimal path
        if(self.distance[self.goal] == float('inf')):
            return (explored_states, [], self.distance[self.goal])
        
        # backtrack path
        backtrack_states = []
        node = self.goal
        while(self.path[node] != -1):
            backtrack_states.append(node)
            node = self.path[node]
        backtrack_states.append(self.start)
        backtrack_states = list(reversed(backtrack_states))      
        return (explored_states, backtrack_states, self.distance[self.goal])
