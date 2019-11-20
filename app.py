import numpy as np
import cv2
from connected_component import ConnectedComponent

test = np.array(
    [[1, 0, 0, 1, 1],
     [1, 1, 0, 1, 1],
     [0, 1, 0, 1, 0],
     [1, 0, 0, 0, 1],
     [1, 1, 0, 0, 1]]
    )

img = cv2.imread('images\\coins.jpg')
test_img_8 = ConnectedComponent.from_color(img)
test_img_8.connected_component_iterative(8)
print("image test 8 ways iterative\n{} connected components found.\n".format(test_img_8.component_count))

test_img_4 = ConnectedComponent.from_color(img)
test_img_4.connected_component_iterative()
print("image test 4 ways iterative\n{} connected components found.\n".format(test_img_4.component_count))

iterative4 = ConnectedComponent(test)
iterative8 = ConnectedComponent(test)

recursive4 = ConnectedComponent(test)
recursive8 = ConnectedComponent(test)

print("4 ways iterative:\n{}\n".format(iterative4.connected_component_iterative()))
print("The number on components: {}".format(iterative4.component_count))
print("8 ways iterative:\n{}\n".format(iterative8.connected_component_iterative()))
print("The number on components: {}".format(iterative8.component_count))
print("4 ways recursive:\n{}\n".format(recursive4.connected_component_recursive()))
print("The number on components: {}".format(recursive4.component_count))
print("8 ways recursive:\n{}\n".format(recursive8.connected_component_recursive()))
print("The number on components: {}".format(recursive8.component_count))









