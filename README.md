# simple-computer-vision
A scanning and OCR experiment.

Using an uploaded image, this script will do some basic image processing including:
* resize small images to improve OCR accuracy
* convert RGB to grayscale
* apply basic processing like blur, threshold and Gaussian, depending on the file quality

After basic processing, OCR the image using Tesseract and print the result.

And finally, test the accuracy of the OCR output against a control file (ground truth document).

# Currently Unresolved:

The best OCR accuracy occurs when the image is converted to RGB, then to grayscale. Why this works is a mystery.
