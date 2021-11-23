# This is a sample Python script.


# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

import cv2.cv2 as cv
import numpy as np

NODES_IN_ROW = 40
NODES_IN_COL = 40
BACKGROUND_HEIGHT, BACKGROUND_WIDTH = NODES_IN_ROW * 20, NODES_IN_COL * 20


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

    def connect_nodes(self, other):
        self.neighbors.append(other)
        other.neighbors.append(self)


# init rectangle graph with connected neighbors
def create_graph():
    # creating rectangle of nodes with 10 pixels in between
    nodes = [[Node((i * 20 + 5, j * 20 + 5)) for i in range(NODES_IN_ROW)] for j in range(NODES_IN_COL)]

    # connect neighboring nodes
    for i in range(1, len(nodes)):
        for j in range(1, len(nodes[0])):
            nodes[i][j].connect_nodes(nodes[i - 1][j])
            nodes[i][j].connect_nodes(nodes[i][j - 1])

    # return back list with neighbors connected
    return nodes


# draw maze with random dfs
def draw_maze():
    pass


# init all needed variables and builds the maze
def build_maze():
    # black blank image
    blank_image = np.zeros(shape=[BACKGROUND_WIDTH, BACKGROUND_HEIGHT, 3], dtype=np.uint8)
    maze = blank_image
    nodes = create_graph()
    for row in nodes:
        for n in row:
            for neighbor in n.neighbors:
                maze = cv.rectangle(maze, n.pos, neighbor.pos, (255, 255, 255), -1)

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
