# THE MODIFICATION IS NOT FINISHED. IT STILL NEEDS CV-RELATED CORRECTION. SO, BECAREFUL WHILE IMPLEMENTING
#EEM561 2023 Spring, Machine Vision
#Assesment no: 1
#Detecting Vanishing Points
#Enes DURAN
import numpy as np
import cv2

# Load the image
img = cv2.imread('/home/enes/PycharmProjects/pythonProject/example_images/example4vanishingpoint/test images/test_02.jpg')

# Convert to grayscale
gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

# Detect edges using Canny
edges = cv2.Canny(gray, threshold1=40, threshold2=150)

# Detect lines using the Hough transform
lines = cv2.HoughLines(edges,1,np.pi/180,200)

# Convert polar coordinates to Cartesian coordinates
cart_lines = []
for line in lines:
    rho, theta = line[0]
    m = -1 / np.tan(theta)
    b = rho / np.sin(theta)
    cart_lines.append((m, b))

# Find intersection point of lines
vp = []
for i in range(len(cart_lines)):
    for j in range(i+1, len(cart_lines)):
        m1 = cart_lines[i][0]
        b1 = cart_lines[i][1]
        m2 = cart_lines[j][0]
        b2 = cart_lines[j][1]
        if abs(m1 - m2) > 1e-6:
            x0 = (b2 - b1) / (m1 - m2)
            y0 = m1 * x0 + b1
            x0, y0 = int(np.round(x0)), int(np.round(y0))
            vp.append((x0, y0))

# Calculate the minimum and maximum x and y coordinates of all vanishing points
min_x = min([p[0] for p in vp])
max_x = max([p[0] for p in vp])
min_y = min([p[1] for p in vp])
max_y = max([p[1] for p in vp])

# Compute the amount by which the image needs to be extended in each direction
top = abs(min_y) if min_y < 0 else 0
bottom = max_y - img.shape[0] + 1 if max_y > img.shape[0] else 0
left = abs(min_x) if min_x < 0 else 0
right = max_x - img.shape[1] + 1 if max_x > img.shape[1] else 0

# Extend the image using the np.pad() function
img = np.pad(img, ((top, bottom), (left, right), (0, 0)), mode='constant')

# Update the coordinates of the vanishing points to match their new positions in the extended image
vp = [(p[0]+left, p[1]+top) for p in vp]

# Draw the lines and intersection points on the extended image
for line in cart_lines:
    m, b = line
    x1 = 0
    y1 = int(b)
    x2 = img.shape[1]
    y2 = int(m * x2 + b)
    cv2.line(img, (x1, y1), (x2, y2), (0,0,255), 1)

for p in vp:
    cv2.circle(img, p, 5, (255, 0, 0), -1)

# Display the image
cv2.imshow('image', img)
cv2.waitKey(0)
cv2.destroyAllWindows()
