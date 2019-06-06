import cv2
import numpy as np
import math
import time
########################################################################################################################
# Helper functions
def is_on_obstacle(x,y,clr = 0):
    o1, o2, o3, o4, o5, \
    o6, o7, o8, o9, o10, \
    o11, o12, o13, o14, o15, \
    o16, o17 = False, False, False, False, \
               False, False, False, False, \
               False, False, False, False, \
               False, False, False, False, False
    if ((x + 405.05)**2 + (y - 325.05)**2 - (79.95+clr)**2) <= 0 \
            or ((x + 245.27)**2 + (y - 325.05)**2 - (79.95+clr)**2) <= 0 \
            or (y - 245.1 + clr >= 0 and y - 405 - clr <= 0 and x + 245.27 - clr <= 0 and x + 405.05 + clr >= 0):
        o1 = True
    if (x+165)**2 + (y-460)**2 - (40.5 + clr)**2 <=0:
        o2 = True
    if (x+117)**2 + (y-231)**2 - (40.5 + clr)**2 <=0:
        o3 = True
    if (y + 190 + clr >= 0 and y + 7 - clr <= 0 and x + 26 - clr <= 0 and x + 117 + clr>= 0):
        o4 = True
    if (x+117)**2 + (y+231)**2 - (40.5 + clr)**2 <=0:
        o5 = True
    if (x+165)**2 + (y+460)**2 - (40.5 + clr)**2 <=0:
        o6 = True
    if (y + 240 + clr >= 0 and y + 164 - clr <= 0 and x + 26 + clr >= 0 and x - 157 - clr <= 0):
        o7 = True
    if (x + 81 + clr >= 0 and x - 193 - clr <=0 and y + 470 + clr >=0 and y + 318 - clr <=0):
        o8 = True
    if (x - 224 + clr >= 0 and x - 341 - clr <=0 and y + 470 + clr >=0 and y + 412 - clr <=0):
        o9 = True
    if (x - 229.5 + clr >= 0 and x - 381.5 - clr <=0 and y + 121 - clr <=0 and y + 238 + clr >=0):
        o10 = True
    if (x - 372 + clr >= 0 and x - 555 - clr <=0 and y + 470 + clr >=0 and y + 394 - clr <=0):
        o11 = True
    if (x - 497 + clr >= 0 and x - 555 - clr <=0 and y + 209.75 - clr <=0 and y + 326.75 + clr >=0):
        o12 = True
    if (x - 464 + clr >= 0 and x - 555 - clr <=0 and y + 142.5 + clr >=0 and y + 56.5 - clr <=0):
        o13 = True
    if (x - 497 + clr >= 0 and x - 555 - clr <=0 and y + 56.5 + clr >=0 and y - 60.5 - clr <=0):
        o14 = True
    if (x - 189 + clr >= 0 and x - 555 - clr <=0 and y - 116 + clr >=0 and y - 192 - clr <=0):
        o15 = True
    if (x - 277 + clr >= 0 and x - 363 - clr <=0 and y - 322 + clr >=0 and y - 505 - clr <=0):
        o16 = True
    if (x - 471 - clr <= 0 and x - 428 + clr >=0 and y - 414 + clr >=0 and y - 505 - clr <=0):
        o17 = True
    return o1 or o2 or o3 or o4 or o5 or o6 or o7 or o8 or o9 or o10 or o11 or o12 or o13 or o14 or o15 or o16 or o17
########################################################################################################################
# Class structures
class Node:
    def __init__(self):
        self.is_obstacle = False
        self.parent = None
        self.neighbours = {}
        self.on_path = False
        self.g_cost = 999999  # should be infinite
        self.rhs = 999999  # should be infinite

class Graph:
    # graph constructor that creates an empty dictionary
    # nodes = {(x,y):Node} where x,y are coordinates of node
    # open_list = {(x,y): key}
    def __init__(self):
        self.nodes = {}
        self.open_list = {}
        self.obstacle_space = set()
        self.current_path = []
        self.open_length = 0
    # loop through image and create node object for each pixel
    def create_nodes(self):
        for x in range(-555, 555):
            for y in range(-505, 505):
                y = -y
                if (x,y) not in self.obstacle_space:
                    self.nodes[(x, y)] = Node()

    # for given pixel and find it's neighbours
    def calculate_neighbours(self, curr_node):
        x = curr_node[0]
        y = curr_node[1]
        dig = 1.41
        strght = 1
        if (x-1,y+1) not in self.obstacle_space and x-1 >= -555 and y+1 < 505:
            if (x-1,y+1) not in self.open_list and self.nodes[(x-1,y+1)].rhs == 999999:
                self.nodes[(x,y)].neighbours[(x-1,y+1)] = dig
        if (x,y+1) not in self.obstacle_space and y+1 < 505:
            if (x,y+1) not in self.open_list and self.nodes[(x,y+1)].rhs == 999999:
                self.nodes[(x,y)].neighbours[(x,y+1)] = strght
        if (x+1,y+1) not in self.obstacle_space and x+1 < 555 and y+1 < 505:
            if (x+1,y+1) not in self.open_list and self.nodes[(x+1,y+1)].rhs == 999999:
                self.nodes[(x,y)].neighbours[(x+1,y+1)] = dig
        if (x-1,y-1) not in self.obstacle_space and x-1 >= -555 and y-1 >= -505:
            if (x-1, y-1) not in self.open_list and self.nodes[(x-1,y-1)].rhs == 999999:
                self.nodes[(x, y)].neighbours[(x-1, y-1)] = dig
        if (x,y-1) not in self.obstacle_space and y-1 >= -505:
            if (x, y-1) not in self.open_list and self.nodes[(x,y-1)].rhs == 999999:
                self.nodes[(x, y)].neighbours[(x, y-1)] = strght
        if (x+1,y-1) not in self.obstacle_space and x+1 < 555 and y-1 >= -505:
            if (x+1,y-1) not in self.open_list and self.nodes[(x+1,y-1)].rhs == 999999:
                self.nodes[(x, y)].neighbours[(x+1, y-1)] = dig
        if (x-1,y) not in self.obstacle_space and x-1 >= -555:
            if (x-1,y) not in self.open_list and self.nodes[(x-1,y)].rhs == 999999:
                self.nodes[(x, y)].neighbours[(x-1,y)] = strght
        if (x+1,y) not in self.obstacle_space and x+1 < 555:
            if (x+1,y) not in self.open_list and self.nodes[(x+1,y)].rhs == 999999:
                self.nodes[(x,y)].neighbours[(x+1,y)] = strght
    # Check if node is consistent
    def node_is_consistent(self,node):
        if self.nodes[node].g_cost == self.nodes[node].rhs:
            return True
        else:
            return False
    # Get heuristic distance
    def h(self,node,start):
        return np.sqrt((node[0] - start[0])**2 + (node[1] - start[1])**2)

    # Get key for sorting the open_list:
    def get_key(self,node, start):
        key = min(self.nodes[node].g_cost, self.nodes[node].rhs) + self.h(node,start)
        return key
    # Get smallest element from the open_list:
    def get_smallest(self,open_list):
        smallest = 9999999;
        smallest_node = (-9999,-9999)
        for key, value in open_list.items():
            if open_list[key] < smallest:
                smallest = value
                smallest_node = key
        return smallest_node
    # D* Lite algorithm to find the shortest path
    def d_star_lite_algo(self, rob_x, rob_y, goal_x, goal_y,bg):
        bg[505 - rob_y, rob_x + 555] = (250,11,156)
        bg[505 - goal_y, goal_x + 555] = (250, 11, 156)
        ## Color declarations
        # define color for node in open list
        green = (60, 179, 113)
        # define color for the current node
        red = (0, 0, 250)
        # get coordinates for the start node
        start_node = (rob_x, rob_y)
        # get coordinates for the goal node
        goal_node = (goal_x, goal_y)
        # make cost of start node zero
        self.nodes[goal_node].rhs = 0
        self.open_list[goal_node] = 0  # key needs to be written here
        self.open_length += 1
        curr_node = goal_node
        while not curr_node == start_node and not len(self.open_list) == 0:
            #print("Curr",curr_node)
            bg[505 - curr_node[1], curr_node[0] + 555] = red
            # make g_cost = rhs
            self.nodes[curr_node].g_cost = self.nodes[curr_node].rhs
            # remove curr_node from the open list
            del self.open_list[curr_node]
            self.open_length -= 1
            # get successors of the curr_node
            self.calculate_neighbours(curr_node)
            for n in self.nodes[curr_node].neighbours:
                bg[505 - n[1], n[0] + 555] = green
                self.nodes[n].parent = curr_node
                # rhs of successor = g of parent + path cost
                self.nodes[n].rhs = self.nodes[curr_node].g_cost + self.nodes[curr_node].neighbours[n]
                if not self.node_is_consistent(n):
                    self.open_list[n] = self.get_key(n, start_node)
                    self.open_length += 1
            curr_node = self.get_smallest(self.open_list)
        current_path = []
        while not self.nodes[curr_node].parent == None:
            bg[505 - curr_node[1], curr_node[0] + 555] = (250, 0, 0)
            current_path.append(curr_node)
            curr_node = self.nodes[curr_node].parent
        current_path.append(curr_node)
        cv2.imshow("D star lite output", bg)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
        return current_path

    # new neighbours
    def new_calculate_neighbours(self, curr_node, open_list, current_path):
        x = curr_node[0]
        y = curr_node[1]
        dig = 1.41
        strght = 1
        if (x-1,y+1) not in self.obstacle_space and x-1 >= -555 and y+1 < 505:
            if (x-1,y+1) not in open_list and not self.nodes[(x,y)].parent == (x-1,y+1) and (x-1,y+1) not in current_path:
                self.nodes[(x,y)].neighbours[(x-1,y+1)] = dig
        if (x,y+1) not in self.obstacle_space and y+1 < 505:
            if (x,y+1) not in open_list and not self.nodes[(x,y)].parent == (x,y+1) and (x,y+1) not in current_path:
                self.nodes[(x,y)].neighbours[(x,y+1)] = strght
        if (x+1,y+1) not in self.obstacle_space and x+1 < 555 and y+1 < 505:
            if (x+1,y+1) not in open_list and not self.nodes[(x,y)].parent == (x+1,y+1) and (x+1,y+1) not in current_path:
                self.nodes[(x,y)].neighbours[(x+1,y+1)] = dig
        if (x-1,y-1) not in self.obstacle_space and x-1 >= -555 and y-1 >= -505:
            if (x-1, y-1) not in open_list and not self.nodes[(x,y)].parent == (x-1,y-1) and (x-1,y-1) not in current_path:
                self.nodes[(x, y)].neighbours[(x-1, y-1)] = dig
        if (x,y-1) not in self.obstacle_space and y-1 >= -505:
            if (x, y-1) not in open_list and not self.nodes[(x,y)].parent == (x,y-1) and (x,y-1) not in current_path:
                self.nodes[(x, y)].neighbours[(x, y-1)] = strght
        if (x+1,y-1) not in self.obstacle_space and x+1 < 555 and y-1 >= -505:
            if (x+1,y-1) not in open_list and not self.nodes[(x,y)].parent == (x+1,y-1) and (x+1,y-1) not in current_path:
                self.nodes[(x, y)].neighbours[(x+1, y-1)] = dig
        if (x-1,y) not in self.obstacle_space and x-1 >= -555:
            if (x-1,y) not in open_list and not self.nodes[(x,y)].parent == (x-1,y) and (x-1,y) not in current_path:
                self.nodes[(x, y)].neighbours[(x-1,y)] = strght
        if (x+1,y) not in self.obstacle_space and x+1 < 555:
            if (x+1,y) not in open_list and not self.nodes[(x,y)].parent == (x+1,y) and (x+1,y) not in current_path:
                self.nodes[(x,y)].neighbours[(x+1,y)] = strght
    # get new key for replanning
    def get_new_key(self, node, start):
        key = min(self.nodes[node].g_cost, self.nodes[node].rhs) + self.h(node, start)
        return key

    # replanning the path from current start point
    def replan(self,rob_x, rob_y, goal_x, goal_y,current_path,bg):
        # get coordinates for the start node
        start_node = (rob_x, rob_y)
        # get coordinates for the goal node
        goal_node = (goal_x, goal_y)
        new_open_list = {}
        visited = []
        # make cost of start node zero
        self.nodes[goal_node].rhs = 0
        new_open_list[goal_node] = 0  # key needs to be written here
        curr_node = goal_node
        parent = self.nodes[goal_node].parent
        while not parent == None:
            visited.append(parent)
            parent = self.nodes[parent].parent
        while not curr_node == start_node and not len(new_open_list) == 0:
            bg[505 - curr_node[1], curr_node[0] + 555] = (0,0,250)
            visited.append(curr_node)
            # make g_cost = rhs
            self.nodes[curr_node].g_cost = self.nodes[curr_node].rhs
            # print("len",len(self.open_list))
            # first make all neighbour rhs = infinitys
            # Now recalculate for new path
            self.nodes[curr_node].neighbours = {}
            self.new_calculate_neighbours(curr_node, new_open_list, visited)
            for n in self.nodes[curr_node].neighbours:
                if n in visited:
                    continue
                bg[505 - n[1], n[0] + 555] = (60, 179, 113)
                self.nodes[n].parent = curr_node
                # rhs of successor = g of parent + path cost
                self.nodes[n].rhs = self.nodes[curr_node].g_cost + self.nodes[curr_node].neighbours[n]
                if not self.node_is_consistent(n):
                    new_open_list[n] = self.get_new_key(n, start_node)
            # remove curr_node from the open list
            del new_open_list[curr_node]
            curr_node = self.get_smallest(new_open_list)
        new_path = []
        count = 0
        while not self.nodes[curr_node].parent == None:
            #while not curr_node == goal_node:
            bg[505 - curr_node[1], curr_node[0] + 555] = (250, 0, 0)
            new_path.append(curr_node)
            curr_node = self.nodes[curr_node].parent
            count += 1
        new_path.append(curr_node)
        return new_path

    # Travel across the received path
    def traverse(self,bg,current_path):
        for x in range(-175, -150):
            for y in range(-60, 60):
                self.obstacle_space.add((x, y))
                bg[505 - y, x + 555] = (0, 0, 0)
        self.obstacle_space.add((55, -30))
        bg[505 + 30, 55 + 555] = (0, 0, 0)
        for p in current_path:
            bg[505 - p[1], p[0] + 555] = (255, 255, 255)
            if self.nodes[p].parent in self.obstacle_space:
                print("Obstacle found at ", self.nodes[p].parent)
                parent = self.nodes[p].parent
                # get next available parent on path
                while parent in self.obstacle_space:
                    print("Obstacle found at ", parent)
                    parent = self.nodes[parent].parent
                new_path = self.replan(p[0], p[1], -100, 0, current_path,bg)
                if len(new_path)/len(current_path) > 1.2:
                    print("New Path Too Large.")
                    print("Human Assistance Required")
                    start_time = time.time()
                    while True:
                        print("Waiting for human")
                        elapsed = time.time() - start_time
                        print("Time taken: ", elapsed)
                        if elapsed > 15.0:
                            print("Human Assistance Not received")
                            print("Continuing on longer path")
                            break
                # travel again on new path
                self.traverse(bg, new_path)
                break
            cv2.imshow("Output", bg)
            cv2.waitKey(50)
        cv2.imshow("Output", bg)
        cv2.waitKey(5000)
        cv2.destroyAllWindows()
########################################################################################################################
def initiate():
    # scale the window size
    height = 1010
    width = 1110

    # create a background image
    bg = np.zeros((height,width,3),dtype=np.uint8)
    # Calculate Mikowski space
    r = 2
    print("Calculating Minowski Space. please wait")
    graph = Graph()
    obstacle_set_min = set()
    # iterate for each pixel and find out if it is an obstacle
    # if it is in the obstacle store it in the obstacle set
    for x in range(-555, 555):
        for y in range(-505, 505):
            y = -y
            if is_on_obstacle(x, y, r):
                graph.obstacle_space.add((x, y))
    graph.create_nodes()
    # define color for node in open list
    green = (60, 179, 113)
    # define color for unvisited node
    grey = (192, 192, 192)
    # define color for the nodes on the path
    blue = (250, 50, 50)
    # color for explored node
    black = (0, 0, 0)
    # apply appropriate colors
    for node in graph.nodes:
        x = node[0]
        y = node[1]
        # y = -y
        bg[505 - y, x + 555] = grey
    current_path = graph.d_star_lite_algo(-200,0,-100,0,bg)
    graph.traverse(bg,current_path)
initiate()
