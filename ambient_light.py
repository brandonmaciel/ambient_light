# must run script with sudo
import itertools as it
import cv2
import board
import neopixel

num_leds_t_b = 67 # LEDs on top and bottom strip, must be same for top and bottom
num_leds_l_r = 37 # LEDs on left and right strip, must be same for left and right

# led starts at the bottom left corner and goes clock wise UP RIGHT DOWN LEFT
matrix_size = num_leds_t_b*2 + num_leds_l_r*2

matrix_color = neopixel.NeoPixel(board.D18, matrix_size, auto_write=False)
# coordinate list for led
led_matrix = [(0, 0)] * matrix_size


path = "/dev/video0" # path of video input
vcap = cv2.VideoCapture(path)
width = vcap.get(3)-1  # float
height = vcap.get(4)-1  # float

color_l_r = height/num_leds_l_r
color_t_b = width/num_leds_t_b

while vcap.isOpened():
    ret, frame = vcap.read()
#     cv2.imshow('Video Input', frame) # show video feed (slows down program)
    heightc = height
    widthc = 0

    # left and right LED strip of TV
    for led in it.chain(range(num_leds_l_r),
                        range(num_leds_t_b + num_leds_l_r, num_leds_t_b + (num_leds_l_r * 2))):
        # left LED strip range
        if 0 <= led <= num_leds_l_r:
            led_matrix[led] = (0, heightc)
            heightc = heightc - color_l_r
        # right LED strip range
        elif (num_leds_t_b+num_leds_l_r) <= led <= (num_leds_t_b+(num_leds_l_r*2)):
            led_matrix[led] = (width, heightc)
            heightc = heightc + color_l_r

    # top and bottom LED strip of TV
    for led in it.chain(range(num_leds_l_r, num_leds_t_b+num_leds_l_r),
                        range(num_leds_t_b + (num_leds_l_r * 2), matrix_size)):
        # top LED strip range
        if num_leds_l_r <= led <= (num_leds_t_b+num_leds_l_r):
            led_matrix[led] = (widthc, 0)
            widthc = widthc + color_t_b
        # bottom LED strip range
        elif (num_leds_t_b + (num_leds_l_r * 2)) <= led <= matrix_size:
            led_matrix[led] = (widthc, height)
            widthc = widthc - color_t_b

    # assign each LED the corresponding color
    for i in range(len(matrix_color)):
        # 719, 1279
        matrix_color[i] = (frame[int(led_matrix[i][1]), int(led_matrix[i][0])][2],
                           frame[int(led_matrix[i][1]), int(led_matrix[i][0])][1],
                           frame[int(led_matrix[i][1]), int(led_matrix[i][0])][0])

    matrix_color.show()

    # print color of each LED every frame
    # for i in range(len(matrix_color)):
    #     print(int(led_matrix[i][1]), int(led_matrix[i][0]))


vcap.release()
cv2.destroyAllWindows()
