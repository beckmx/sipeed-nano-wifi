#find rects in color
import sensor, image, lcd, time

lcd.init()
sensor.reset()
sensor.set_contrast(1)
sensor.set_gainceiling(16)
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.QVGA)
sensor.set_hmirror(1)
sensor.set_vflip(1)
sensor.run(1)
sensor.skip_frames(30)

tim = time.ticks_ms()

while(time.ticks_diff(time.ticks_ms(), tim)<30000):
    img = sensor.snapshot()
    for r in img.find_rects(threshold = 18000,roi=(0,0,320,240)):
        img.draw_rectangle(r.rect(), color = (255, 0, 0))
        for p in r.corners(): img.draw_circle(p[0], p[1], 5, color = (0, 255, 0))
    img.draw_rectangle(80,60,160,120)

    lcd.display(img)
print("finish")
lcd.clear()
