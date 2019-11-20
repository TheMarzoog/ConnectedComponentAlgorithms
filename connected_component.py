import numpy as np
import cv2


class ConnectedComponent:
    def __init__(self, bw):
        self.bw = bw
        self.labeled_img = None
        self.label = 1
        self._classes = set()
        self.component_count = 0

    @classmethod
    def from_color(cls, img):
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        (thresh, bw) = cv2.threshold(img, 127, 255, cv2.THRESH_BINARY)
        bw = (255 - bw)
        bw = bw // 255
        return cls(bw)

    @classmethod
    def from_gray(cls, img):
        (thresh, bw) = cv2.threshold(img, 127, 255, cv2.THRESH_BINARY)
        bw = bw // 255
        return cls(bw)

    def _update_classes(self, low, high):
        for x, y in self._classes:
            if y == low:
                self._classes.add((x, high))

    def _get_border_img(self):
        img = np.zeros((self.bw.shape[0] + 2, self.bw.shape[1] + 2), dtype=int)
        img[1:-1, 1:-1] = self.bw[:, :]
        self.bw = img

    def _iterative_labeling_4(self, i, j):
        if self.bw[i - 1, j] != 1 and self.bw[i, j - 1] != 1:
            self.labeled_img[i, j] = self.label
            self.label += 1
        elif self.bw[i - 1, j] == 1 and self.bw[i, j - 1] != 1:
            self.labeled_img[i, j] = self.labeled_img[i - 1, j]
        elif self.bw[i - 1, j] != 1 and self.bw[i, j - 1] == 1:
            self.labeled_img[i, j] = self.labeled_img[i, j - 1]
        else:
            x = self.labeled_img[i - 1, j]
            y = self.labeled_img[i, j - 1]
            if x > y:
                x, y = y, x
            self.labeled_img[i, j] = x
            self._update_classes(x, y)

    def _iterative_labeling_8(self, i, j):
        labels_set = {self.labeled_img[i-1, j+1],
                      self.labeled_img[i-1, j],
                      self.labeled_img[i-1, j-1],
                      self.labeled_img[i, j-1]}
        if 0 in labels_set:
            labels_set.remove(0)
        if len(labels_set) == 0:
            self.labeled_img[i, j] = self.label
            self.label += 1
        elif len(labels_set) == 1:
            self.labeled_img[i, j] = labels_set.pop()
        else:
            x = labels_set.pop()
            y = labels_set.pop()
            self.labeled_img[i, j] = x
            self._update_classes(x, y)

    def connected_component_iterative(self, ways: int = 4):
        self._get_border_img()
        self.labeled_img = np.zeros_like(self.bw)

        for i in range(1, self.bw.shape[0] - 1):
            for j in range(1, self.bw.shape[1] - 1):
                if self.bw[i, j] == 1:
                    if ways == 8:
                        self._iterative_labeling_8(i, j)
                    else:
                        self._iterative_labeling_4(i, j)

        for i in range(1, self.labeled_img.shape[0] - 1):
            for j in range(1, self.labeled_img.shape[1] - 1):
                for x, y in self._classes:
                    if self.labeled_img[i, j] == y:
                        self.labeled_img[i, j] = x
        self.labeled_img = self.labeled_img[1:-1, 1:-1]
        self.component_count = self.label - len(self._classes) - 1
        return self.labeled_img

    def _recursive_labeling_4(self, i, j):
        if self.bw[i, j] == 0 or self.labeled_img[i, j] != 0:
            pass
        else:
            self.labeled_img[i, j] = self.label
            self._recursive_labeling_4(i, j + 1)
            self._recursive_labeling_4(i + 1, j)
            self._recursive_labeling_4(i, j - 1)
            self._recursive_labeling_4(i - 1, j)

    def _recursive_labeling_8(self, i, j):
        if self.bw[i, j] == 0 or self.labeled_img[i, j] != 0:
            pass
        else:
            self.labeled_img[i, j] = self.label
            self._recursive_labeling_8(i, j + 1)
            self._recursive_labeling_8(i + 1, j + 1)
            self._recursive_labeling_8(i + 1, j)
            self._recursive_labeling_8(i + 1, j - 1)
            self._recursive_labeling_8(i, j - 1)
            self._recursive_labeling_8(i - 1, j - 1)
            self._recursive_labeling_8(i - 1, j)
            self._recursive_labeling_8(i - 1, j + 1)

    def connected_component_recursive(self, ways: int = 4):
        self._get_border_img()
        self.labeled_img = np.zeros_like(self.bw)

        for i in range(1, self.bw.shape[0] - 1):
            for j in range(1, self.bw.shape[1] - 1):
                if self.bw[i, j] == 1 and self.labeled_img[i, j] == 0:
                    if ways == 8:
                        self._recursive_labeling_8(i, j)
                    else:
                        self._recursive_labeling_4(i, j)
                    self.label += 1
        self.labeled_img = self.labeled_img[1:-1,  1:-1]
        self.component_count = self.label - 1
        return self.labeled_img





