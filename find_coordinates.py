import cv2

import numpy

from analytics import Analytics


def main():
    a = Analytics()
    a.start_timer()
    img = cv2.imread('lvision/assets/images/locations/basing.png')
    points = numpy.where(numpy.all(img == [0, 255, 0], axis=-1))
    points = list(zip(*points[::-1]))
    print(points)
    a.end_timer()


if __name__ == "__main__":
    main()
