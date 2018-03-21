import cv2
import numpy as np
pts = []
thickness = 5
drawing = None
colour = (0,0,255)

def track(image):
    global pts, thickness, drawing,colour

    blur = cv2.GaussianBlur(image, (5,5),0)
    hsv = cv2.cvtColor(blur, cv2.COLOR_BGR2HSV)
    # Threshold the HSV image for only red colors
    lower_red = np.array([0, 128, 100])
    upper_red = np.array([10, 255, 255])
    mask = cv2.inRange(hsv, lower_red, upper_red)
    bmask = cv2.GaussianBlur(mask, (5,5),0)
    if drawing is None:
        drawing = np.zeros((image.shape), np.uint8)
    # Take the moments to get the centroid
    moments = cv2.moments(bmask)
    m00 = moments['m00']
    centroid_x, centroid_y = None, None
    if m00 != 0:
        centroid_x = int(moments['m10']/m00)
        centroid_y = int(moments['m01']/m00)
    # Assume no centroid
    ctr = (-1,-1)
    # Use centroid if it exists
    if centroid_x != None and centroid_y != None:
        ctr = (centroid_x, centroid_y)
        # Put black circle in at centroid in image
        cv2.circle(image, ctr, 4, (0,0,0))
        
    RECTANGLE_LENGTH  = 45; 
    cv2.rectangle(image,(5,5),(RECTANGLE_LENGTH,RECTANGLE_LENGTH),(1,0,0))
    cv2.rectangle(image,(5,RECTANGLE_LENGTH),(RECTANGLE_LENGTH,2*RECTANGLE_LENGTH),(1,0,0))
    cv2.rectangle(image,(5,RECTANGLE_LENGTH*2),(RECTANGLE_LENGTH,RECTANGLE_LENGTH*3),(1,0,0))
    cv2.rectangle(image,(5,RECTANGLE_LENGTH*3),(RECTANGLE_LENGTH,RECTANGLE_LENGTH*4),(1,0,0))

    if 5<ctr[0]<RECTANGLE_LENGTH and 5<ctr[1]<RECTANGLE_LENGTH: 
        colour = (0,0,255) #colour red
    if 5<ctr[0]<RECTANGLE_LENGTH and RECTANGLE_LENGTH*3<ctr[1]<RECTANGLE_LENGTH*4 :
        colour = (0,0,0) #make colour black
     
    if ctr is not None and not ((5<ctr[0]<RECTANGLE_LENGTH) and (5<ctr[1]<RECTANGLE_LENGTH*4)):
        cv2.circle(drawing, ctr, thickness, colour, -1)
    
        #cv2.circle(image, pts[i],thickness, (0, 0, 255), -1)
        #cv2.line(image, pts[i - 1], pts[i], (0, 0, 255), thickness)
    # Display full-color image
    image = cv2.add(image, drawing)
    cv2.imshow('CA', image)
    # Force image display, setting centroid to None on ESC key input
    if cv2.waitKey(1) & 0xFF == 27:
        ctr = None
    return ctr





if __name__ == '__main__':
    capture = cv2.VideoCapture(0)
    while True:
        isOk, image = capture.read()
        if isOk:
            if not track(cv2.flip(image,1)):
                break
            if cv2.waitKey(1) & 0xFF == 27:
                break
        else:
           print('Capture failed')
           break
       
    capture.release()
    cv2.destroyAllWindows()
