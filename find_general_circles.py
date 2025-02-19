#Traceback (most recent call last):
#  File "<stdin>", line 33, in <module>
#Exception: IDE interrupt
#MicroPython v0.5.0-63-g2d307ae on 2020-05-11; Sipeed_M1 with kendryte-k210
#Type "help()" for more information.
#>>>

import sensor, image, time

sensor.reset()
sensor.set_pixformat(sensor.RGB565) # grayscale is faster
sensor.set_framesize(sensor.QVGA)
sensor.set_hmirror(1)
sensor.set_vflip(1)
sensor.skip_frames(time = 2000)
clock = time.clock()

while(True):
    clock.tick()
    img = sensor.snapshot().lens_corr(1.8)

    # Circle objects have four values: x, y, r (radius), and magnitude. The
    # magnitude is the strength of the detection of the circle. Higher is
    # better...

    # `threshold` controls how many circles are found. Increase its value
    # to decrease the number of circles detected...

    # `x_margin`, `y_margin`, and `r_margin` control the merging of similar
    # circles in the x, y, and r (radius) directions.

    # r_min, r_max, and r_step control what radiuses of circles are tested.
    # Shrinking the number of tested circle radiuses yields a big performance boost.

    for c in img.find_circles(threshold = 2000, x_margin = 50, y_margin = 50, r_margin = 50,
            r_min = 2, r_max = 100, r_step = 2):
        img.draw_circle(c.x(), c.y(), c.r(), color = (255, 0, 0))
        print(c)

    print("FPS %f" % clock.fps())
