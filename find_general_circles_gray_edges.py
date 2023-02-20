import sensor, image, time

sensor.reset()
sensor.set_pixformat(sensor.RGB565) # grayscale is faster
sensor.set_framesize(sensor.QVGA)
sensor.set_hmirror(1)
sensor.set_vflip(1)
sensor.skip_frames(time = 2000)
clock = time.clock()
sharp = -1,-1,-1,-1,9,-1,-1,-1,-1
min_degree = 0
max_degree = 179
while(True):
    clock.tick()
    img = sensor.snapshot()
    img.conv3(sharp)
    # Circle objects have four values: x, y, r (radius), and magnitude. The
    # magnitude is the strength of the detection of the circle. Higher is
    # better...

    # `threshold` controls how many circles are found. Increase its value
    # to decrease the number of circles detected...

    # `x_margin`, `y_margin`, and `r_margin` control the merging of similar
    # circles in the x, y, and r (radius) directions.

    # r_min, r_max, and r_step control what radiuses of circles are tested.
    # Shrinking the number of tested circle radiuses yields a big performance boost.

    #camera is at 15cm from the gauge
    #for c in img.find_circles(threshold = 3500, x_margin = 10, y_margin = 10, r_margin = 10,
            #r_min = 90, r_max = 200, r_step = 2):
        #img.draw_circle(c.x(), c.y(), c.r(), color = (255, 0, 0))
        #print(c)
    ##finds any line
    for l in img.find_lines(threshold = 2000, theta_margin = 25, rho_margin = 25):
        #if (min_degree <= l.theta()) and (l.theta() <= max_degree):
            img.draw_line(l.line(), color = (255, 0, 0))
            print(l)
    #for l in img.find_line_segments(merge_distance = 20, max_theta_diff = 25, roi=(80,60,160,120)):
        #img.draw_line(l.line(), color = (255, 0, 0))
    print("FPS %f" % clock.fps())
