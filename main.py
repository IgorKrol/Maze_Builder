import random

import cv2.cv2 as cv
import numpy as np
import time
import sys
sys.setrecursionlimit(5000)


BACKGROUND_HEIGHT, BACKGROUND_WIDTH = 780,1200
NODES_IN_ROW = int (BACKGROUND_WIDTH / 20)
NODES_IN_COL = int (BACKGROUND_HEIGHT / 20)

# represent nodes in divided rectangle
class Node:

    def __init__(self, position):
        self.pos = position
        self.neighbors = []
        self.visited = False

    # checker if node has single neighbor (parent)
    def is_leaf(self):
        if len(self.neighbors) == 1:
            return True
        else:
            return False

    # create connection between 2 nodes
    def connect_nodes(self, other):
        self.neighbors.append(other)
        other.neighbors.append(self)

    # draw connection between 2 nodes
    def draw_connection(self, mat, other):

        mat = cv.rectangle(mat, (self.pos[0] - 5, self.pos[1] - 5),
                     (other.pos[0] + 5, other.pos[1] + 5),
                     (255, 255, 255), -1)
        mat = cv.rectangle(mat, (self.pos[0] - 5, self.pos[1] - 5),
                                 (self.pos[0] + 5, self.pos[1] + 5),
                                 (255, 0, 0), -1)
        mat = cv.rectangle(mat, (other.pos[0] - 5, other.pos[1] - 5),
                              (other.pos[0] + 5, other.pos[1] + 5),
                              (0, 255, 0), -1)

        return mat



# init rectangle graph with connected neighbors
def create_graph():
    # creating rectangle of nodes with 10 pixels in between
    nodes = [[Node((i * 20 + 5, j * 20 + 5)) for i in range(NODES_IN_ROW)] for j in range(NODES_IN_COL)]
    # connect neighboring nodes
    for i in range(1,len(nodes)):
        for j in range(0,len(nodes[0])):
            nodes[i][j].connect_nodes(nodes[i - 1][j])
    for i in range(0, len(nodes)):
         for j in range(1, len(nodes[0])):
            nodes[i][j].connect_nodes(nodes[i][j - 1])

    # return back list with neighbors connected
    return nodes


# draw maze with random dfs
def draw_maze(mat, root):
    if (not root.is_leaf()):
        root.visited = True
        neighborsCircus = np.random.randint(len(root.neighbors),size=len(root.neighbors))
        print(len(root.neighbors))
        random.shuffle(neighborsCircus)
        for n in neighborsCircus:
            mat = make_path(mat, root, root.neighbors[n])
    return mat

def make_path(mat, prevNode, presentNode):
    if presentNode.visited != True :
        presentNode.visited = True
        mat = presentNode.draw_connection(mat, prevNode)
        # time.sleep(0.1)
        # if(not presentNode.is_leaf()):
        neighborsCircus = np.random.randint(len(presentNode.neighbors),size=len(presentNode.neighbors))
        random.shuffle(neighborsCircus)
        for n in neighborsCircus:
            mat = make_path(mat, presentNode, presentNode.neighbors[n])
    return mat

# init all needed variables and builds the maze
def build_maze():
    # black blank image
    blank_image = np.zeros(shape=[BACKGROUND_HEIGHT, BACKGROUND_WIDTH, 3], dtype=np.uint8)
    maze = blank_image  #background black screen
    nodes = create_graph()
    maze = draw_maze(maze, nodes[0][0])
    # maze = nodes[1][1].draw_connection(maze, nodes[2][1])
    # maze = nodes[1][1].draw_connection(maze, nodes[1][2])
    # maze = cv.rectangle(maze, nodes[0][0].pos, nodes[0][1].pos, (255, 255, 255), -1)


    # for row in nodes:
    #     for n in row:
    #         for neighbor in n.neighbors:
    #             maze = n.draw_connection(maze, neighbor)
    #             cv.imshow("Black Blank", maze)
    #             time.sleep(0.1)

    # print(blank_image.shape)
    # cv.imshow("Black Blank", blank_image)
    cv.imshow("Black Blank", maze)
    # white blank image
    cv.waitKey(0)
    cv.destroyAllWindows()


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    build_maze()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
