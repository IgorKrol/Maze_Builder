import random

import cv2.cv2 as cv
import numpy as np
import time
import sys

sys.setrecursionlimit(5000)

BACKGROUND_HEIGHT, BACKGROUND_WIDTH = 780, 1200
NODES_IN_ROW = int(BACKGROUND_WIDTH / 20)
NODES_IN_COL = int(BACKGROUND_HEIGHT / 20)


# represent nodes in divided rectangle
class Node:

    def __init__(self, position):
        self.pos = position
        self.neighbors = []
        self.visited = False
        self.endNode = False

    # checker if node has single neighbor (parent) - NOT NEEDED
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
    def draw_connection(self, mat, other, color=(155, 155, 155)):
        mat = cv.rectangle(mat, (self.pos[0] - 4, self.pos[1] - 4),
                           (other.pos[0] + 4, other.pos[1] + 4),
                           color, -1)
        mat = cv.rectangle(mat, (self.pos[0] - 4, self.pos[1] - 4),
                           (self.pos[0] + 4, self.pos[1] + 4),
                           color, -1)
        mat = cv.rectangle(mat, (other.pos[0] - 4, other.pos[1] - 4),
                           (other.pos[0] + 4, other.pos[1] + 4),
                           color, -1)

        return mat


class DrawAnimation:
    def __init__(self, startNode: Node, endNode: Node):
        self.endNode = endNode
        self.startNode = startNode

    def draw(self, window_name, mat):
        self.startNode.draw_connection(mat, self.startNode, (0, 0, 255))
        self.endNode.draw_connection(mat, self.endNode, (0, 0, 255))
        cv.imshow(window_name, mat)
        return


# init rectangle graph with connected neighbors
def create_graph():
    # creating rectangle of nodes with 10 pixels in between
    nodes = [[Node((i * 20 + 5, j * 20 + 5)) for i in range(NODES_IN_ROW)] for j in range(NODES_IN_COL)]
    # connect neighboring nodes
    for i in range(1, len(nodes)):
        for j in range(0, len(nodes[0])):
            nodes[i][j].connect_nodes(nodes[i - 1][j])
    for i in range(0, len(nodes)):
        for j in range(1, len(nodes[0])):
            nodes[i][j].connect_nodes(nodes[i][j - 1])

    # return back list with neighbors connected
    return nodes


# draw maze with random dfs
def draw_maze(mat, startNode, endNode):
    if (not startNode.is_leaf()):
        startNode.visited = True
        neighborsCircus = np.random.randint(len(startNode.neighbors), size=len(startNode.neighbors))
        da = DrawAnimation(startNode, endNode)
        random.shuffle(neighborsCircus)
        for n in neighborsCircus:
            mat = make_path(mat, da, startNode, startNode.neighbors[n])
    return mat


def make_path(mat, da: DrawAnimation, prevNode: Node, presentNode: Node):
    if presentNode.visited != True:
        presentNode.visited = True
        mat = presentNode.draw_connection(mat, prevNode)
        cv.waitKey(3)
        da.draw("main_window", mat)
        if (not presentNode.endNode):
            # neighborsCircus = np.random.randint(len(presentNode.neighbors), size=len(presentNode.neighbors)-1)
            neighborsCircus = []
            [neighborsCircus.append(i) for i in range (len(presentNode.neighbors))]
            random.shuffle(neighborsCircus)

            for n in neighborsCircus:
                mat = make_path(mat, da, presentNode, presentNode.neighbors[n])
    return mat


# init all needed variables and builds the maze
def build_maze():
    # black blank image
    blank_image = np.full(shape=[BACKGROUND_HEIGHT, BACKGROUND_WIDTH, 3], fill_value=[0, 0, 0], dtype=np.uint8)
    maze = blank_image  # background black screen
    nodes = create_graph()  # building graph based on matrix rectangle

    finishNode, startNode = nodes[len(nodes) - 1][len(nodes[0]) - 1], nodes[0][0]
    finishNode.endNode = True
    maze = draw_maze(maze, startNode, finishNode)

    # cv.imshow("Black Blank", maze)
    cv.waitKey(0)
    cv.destroyAllWindows()


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    build_maze()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
