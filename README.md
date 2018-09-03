# detect_barcode

Image processing library to detect barcode in an image.

### Sample result
<img src="https://github.com/obedtandadjaja/detect_barcode/blob/master/sample_result.png" width="300px"/><img src="https://github.com/obedtandadjaja/detect_barcode/blob/master/sample_result_1.png" width="300px"/>

2 versions:
1. with Zbar (open-sourced barcode detection library)
2. with customizable image processing algorithm using OpenCV

Zbar can occasionally be unreliable when it comes to blurry pictures, or pictures with more than one barcodes shown. This is where the customizable image processing algorithm comes in, in which you can tweak the algorithm to better fit your needs. Below is an overview of how I construct the algorithm.

### Custom image processing algorithm
Basic idea: barcodes should have a white background with black stripes going down vertically; we use image processing to detect this trend.

1. Turn the image to grayscale
2. Compute Scharr gradient magnitude representation of the image (horizontal and vertical)
3. Subtract the x and y-gradient to get the regions of the image with high horizontal gradients and low vertical gradients.
4. Blur the image to reduce noise
5. Threshold the blurred image, and set any pixels with less than 225 to black
6. Morph the white parts of the image into a rectangle
7. Do iterations of erosion and dilation to remove small blobs
8. Display all the countours in the image
