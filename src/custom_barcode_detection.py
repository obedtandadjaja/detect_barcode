import numpy
import argparse
import imutils
import cv2

class CustomBarcodeDetection:
  def __init__(self, image_path):
    self.image = cv2.imread(image_path)

  def detect_barcode(self):
    self.process_image()
    self.find_contours()
    self.display_result()

  def process_image(self):
    # convert to grayscale
    grayscale = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)

    # compute the Scharr gradient magnitude representation of the images
    # in both the x and y direction
    ddepth = cv2.CV_32F
    gradX = cv2.Sobel(grayscale, ddepth=ddepth, dx=1, dy=0, ksize=-1)
    gradY = cv2.Sobel(grayscale, ddepth=ddepth, dx=0, dy=1, ksize=-1)

    # subtract the y-gradient from the x-gradient
    gradient = cv2.subtract(gradX, gradY)
    gradient = cv2.convertScaleAbs(gradient)

    # blur and threshold the image
    blurred = cv2.blur(gradient, (9, 9))
    (_, thresh) = cv2.threshold(blurred, 225, 255, cv2.THRESH_BINARY)

    # construct a closing kernel and apply it to the thresholded image
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (27, 9))
    closed = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)

    # perform a series of erosions and dilations
    eroded = cv2.erode(closed, None, iterations = 10)
    dilated = cv2.dilate(eroded, None, iterations = 10)

    self.processed_image = dilated

  def find_contours(self):
    self.contours = cv2.findContours(
      self.processed_image.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
    )
    self.contours = self.contours[1]

  def display_result(self):
    for x in xrange(len(self.contours)):
      contour = self.contours[x]

      # compute the rotated bounding box of the largest contour
      rect = cv2.minAreaRect(contour)
      box = cv2.cv.BoxPoints(rect) if imutils.is_cv2() else cv2.boxPoints(rect)
      box = numpy.int0(box)

      print 'bottom-right: ' + str(box[0])
      print 'bottom-left: ' + str(box[1])
      print 'top-left: ' + str(box[2])
      print 'top-right: ' + str(box[3])

      # draw a bounding box arounded the detected barcode and display the image
      cv2.drawContours(self.image, [box], -1, (255, 0, 0), 3)

    cv2.imshow('Image', self.image)
    cv2.waitKey(0)

def get_image_path_from_cmd_args():
  ap = argparse.ArgumentParser()
  ap.add_argument('-i', '--img', required = True, help = 'path to the image file')
  args = vars(ap.parse_args())
  return args['img']

if __name__ == '__main__':
  image_path = get_image_path_from_cmd_args()
  barcode_detection = CustomBarcodeDetection(image_path)
  barcode_detection.detect_barcode()
