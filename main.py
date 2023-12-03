import cv2
import numpy as np
#from PIL import Image

#from utils import get_limits

class Entity:
    def __init__(self, color_name: str, color_bgr: tuple, lower, upper):
        self.color_name = color_name
        self.color_bgr = color_bgr
        self.lower = np.array(lower, np.uint8)
        self.upper = np.array(upper, np.uint8)

def create_mask(hsv, entity: Entity):
    mask = cv2.inRange(hsv, entity.lower, entity.upper)
    contours, hierarchy = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    print(entity.color_name)
    if len(contours) != 0:
        for contour in contours:
            if cv2.contourArea(contour) > 500:
                x, y, w, h = cv2.boundingRect(contour)
                cv2.rectangle(frame, (x, y), (x + w, y + h), entity.color_bgr, 3)

# https://stackoverflow.com/questions/10948589/choosing-the-correct-upper-and-lower-hsv-boundaries-for-color-detection-withcv/48367205#48367205

entities = [
    #       name      color BGR        lower HSV       upper HSV
    Entity('red 1',  (000, 000, 255), [0, 150, 150],   [10, 255, 255]),
    Entity('orange', (000, 100, 255), [11, 100, 100], [19, 255, 255]),
    Entity('yellow', (000, 255, 255), [20, 100, 100], [40, 255, 255]),
    Entity('green',  (000, 255, 000), [41, 100, 70],  [99, 255, 255]),
    Entity('blue',   (255, 000, 000), [100, 50, 70],  [130, 255, 255]),
    Entity('purple', (255, 000, 255), [131, 50, 70],  [139, 255, 255]),
    Entity('pink',   (255, 100, 255), [140, 50, 100],  [165, 255, 255]),
    #Entity('red',    (000, 000, 255), [136, 87, 111], [180, 255, 255]),
    Entity('red 2',  (000, 000, 255), [166, 150, 150], [180, 255, 255]),
]

# 012 ~ 019 orange
# 023 ~ 040 yellow
# 050 ~ 093 green
# 100 ~ 120 blue
# 136 ~ 180 red

cap = cv2.VideoCapture(0)

####################
# caixa wpp - fies #
#   0800-104-0104  #
####################

while True:
    ret, frame = cap.read()
    frame = cv2.flip(frame, 1)

    hsvImage = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    for entity in entities:
        create_mask(hsvImage, entity)
    
    # mask_ = Image.fromarray(mask)

    # bbox = mask_.getbbox()

    # if bbox is not None:
    #     x1, y1, x2, y2 = bbox
    #     frame = cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 5)

    cv2.imshow('frame', frame)

    key = cv2.waitKey(1)

    if key == ord('q'):
        break

    if cv2.getWindowProperty('frame', cv2.WND_PROP_VISIBLE) < 1:
        break

cv2.destroyAllWindows()
cap.release()


