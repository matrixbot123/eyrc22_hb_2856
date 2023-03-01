import cv2


# TODO: generalise the function
def image_mode():
    # @param:   None
    # @return:  Contour coordinates as numpy array
    
    # read the snapchat logo image 
    img = cv2.imread("./taskImages/snapchat.png")
    # resizing the image to 500, 500
    img_resized = cv2.resize(img, (500, 500))
    # testing if properly resized
    assert img_resized.shape == (500, 500)
    # getting the edges of the shape
    edges = cv2.Canny(img_resized, 30, 200)
    # getting the contour coordinates
    contours = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[0]

    return contours[0]
