from PIL import Image
import cv2

# brew install tesseract --all-languages
# convert input.png -resize 400% -type Grayscale input.tif
# tesseract -l eng input.tif output

image = cv2.imread("2.png")
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# check to see if we should apply thresholding to preprocess the
# image
gray = cv2.threshold(gray, 0, 255,
                     cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]


# make a check to see if median blurring should be done to remove
# noise
gray = cv2.medianBlur(gray, 3)

# write the grayscale image to disk as a temporary file so we can
# apply OCR to it
cv2.imwrite('1.gray.jpg', gray)

text = pytesseract.image_to_string(Image.open('1.gray.jpg'), lang='eng')
print("text: {}".format(text))

# show the output images
cv2.imshow("Image", image)
cv2.imshow("Output", gray)
