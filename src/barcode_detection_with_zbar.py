from __future__ import print_function
import pyzbar.pyzbar as pyzbar
import numpy
import cv2
import argparse

class BarcodeDetectionWithZbar:
  def __init__(self, image_path):
    self.image = cv2.imread(image_path)

  def detect_barcode(self):
    self.process_image()
    self.display_result()

  def process_image(self):
    self.decodedObjects = pyzbar.decode(self.image)

  def display_result(self):
    for decodedObject in self.decodedObjects:
      points = decodedObject.polygon

      # find xonvex hull if points don't form a rectangle
      if len(points) > 4:
        hull = cv2.convexHull(numpy.array([point for point in points], dtype=numpy.float32))
        hull = list(map(tuple, numpy.squeeze(hull)))
      else:
        hull = points

      number_of_points = len(hull)

      for j in xrange(number_of_points):
        cv2.line(self.image, hull[j], hull[(j+1)%n], (255,0,0), 3)

    cv2.imshow('Image', self.image)
    cv2.waitKey(0)

def get_image_path_from_cmd_args():
  ap = argparse.ArgumentParser()
  ap.add_argument('-i', '--img', required = True, help = 'path to the image file')
  args = vars(ap.parse_args())
  return args['img']

if __name__ == '__main__':
  image_path = get_image_path_from_cmd_args()
  barcode_detection = BarcodeDetectionWithZbar(image_path)
  barcode_detection.detect_barcode()
