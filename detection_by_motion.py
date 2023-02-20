import sensor, image, lcd, time

sensor.reset()
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.QVGA)
sensor.set_hmirror(1)
sensor.set_vflip(1)
sensor.run(1)
sensor.skip_frames(30)

sensor.set_auto_gain(False) # must be turned off for color tracking
sensor.set_auto_whitebal(False) # must be turned off for color tracking



def get_average(histogram):
    sum = 0
    average = 0
    for object in histogram:
       sum = average + object
    average = sum / 8
    return average

r = [(320//2)-(50//2), (240//2)-(50//2), 50, 50] # 50x50 center of QVGA.
tim = time.ticks_ms()

while(True):
    img = sensor.snapshot()
    img.draw_rectangle(r)
    hist = img.get_statistics(bins=8,roi=r)
    print(hist)
    rgb_value = image.lab_to_rgb((hist.l_mean(),hist.a_mean(),hist.b_mean()))
    img.draw_string(0, 0, str(rgb_value), color = (rgb_value[0], rgb_value[1], rgb_value[2]), scale = 2)
    lcd.display(img)
    time.sleep_ms(500)
print("finish")

lcd.clear()
