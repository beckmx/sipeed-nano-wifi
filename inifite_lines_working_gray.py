#find infinite lines looks to work better in GRAYSCALE
import sensor, image, lcd, time
enable_lens_corr = True
lcd.init()
sensor.reset()
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.QVGA)
sensor.set_hmirror(1)
sensor.set_vflip(1)
sensor.run(1)
sensor.skip_frames(time = 2000)
sharp = -1,-1,-1,-1,9,-1,-1,-1,-1
#v = video.open("/sd/capture_inf_lines.avi", record=1, interval=200000, quality=50)
min_degree = 0
max_degree = 179
tim = time.ticks_ms()

def does_line_intersect_circle(x1, y1, x2, y2, cx, cy, r):
    # calculate the distance between the circle center and the line segment
    d = ((cx - x1) * (y2 - y1) - (cy - y1) * (x2 - x1)) ** 2 / ((x2 - x1) ** 2 + (y2 - y1) ** 2)

    # check if the distance is less than or equal to the radius of the circle
    if d <= r ** 2:
        # calculate the distance between the circle center and the endpoints of the line segment
        d1 = ((cx - x1) ** 2 + (cy - y1) ** 2) ** 0.5
        d2 = ((cx - x2) ** 2 + (cy - y2) ** 2) ** 0.5

        # check if either endpoint of the line segment is inside the circle
        if d1 <= r or d2 <= r:
            return True

        # calculate the distance between the circle center and the closest point on the line segment
        a = ((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5
        b = ((cx - x1) * (x2 - x1) + (cy - y1) * (y2 - y1)) / a
        c = ((cx - x1) * (y2 - y1) - (cy - y1) * (x2 - x1)) / a
        x = x1 + b * (x2 - x1) / a
        y = y1 + b * (y2 - y1) / a

        # check if the closest point on the line segment is inside the circle
        if c <= 0 and d <= r ** 2:
            return True
        elif c >= a and ((cx - x2) ** 2 + (cy - y2) ** 2) <= r ** 2:
            return True
        elif c > 0 and c < a and d <= r ** 2:
            return True

    # if none of the above conditions are met, the line segment does not intersect the circle
    return False

# Define a function to calculate the average position of lines defined by two points.
def avg_line_position(lines):
    # Initialize variables for calculating the average position.
    total_x = 0
    total_y = 0
    count = 0

    # Calculate the total x and y coordinates for all lines.
    for line in lines:
        x1 = line.x1()
        x2 = line.x2()
        y1 = line.y1()
        y2 = line.y2()
        total_x += x1 + x2
        total_y += y1 + y2
        count += 2

    # Calculate the average x and y coordinates.
    avg_x = total_x / count
    avg_y = total_y / count

    # Filter out any lines that deviate too far from the average position.
    max_deviation = 50  # You can adjust this value as per your needs.
    filtered_lines = []
    for line in lines:
        x1 = line.x1()
        x2 = line.x2()
        y1 = line.y1()
        y2 = line.y2()
        if abs(x1 + x2 - total_x) < max_deviation and abs(y1 + y2 - total_y) < max_deviation:
            filtered_lines.append(line)

    # Calculate the average position for the filtered lines.
    total_x = 0
    total_y = 0
    count = 0
    for line in filtered_lines:
        x1 = line.x1()
        x2 = line.x2()
        y1 = line.y1()
        y2 = line.y2()
        total_x += x1 + x2
        total_y += y1 + y2
        count += 2

    # Calculate the final average x and y coordinates.
    avg_x = total_x / count
    avg_y = total_y / count

    return avg_x, avg_y

# Define a function to calculate the average position of points defining lines.
def avg_point_position(lines):
    # Initialize variables for calculating the average position.
    total_x1 = 0
    total_y1 = 0
    total_x2 = 0
    total_y2 = 0
    count = 0

    # Calculate the total x and y coordinates for all lines.
    for line in lines:
        x1 = line.x1()
        x2 = line.x2()
        y1 = line.y1()
        y2 = line.y2()
        total_x1 += x1
        total_y1 += y1
        total_x2 += x2
        total_y2 += y2
        count += 2

    # Calculate the average x and y coordinates.
    avg_x1 = total_x1 / (count / 2)
    avg_y1 = total_y1 / (count / 2)
    avg_x2 = total_x2 / (count / 2)
    avg_y2 = total_y2 / (count / 2)

    # Filter out any lines that deviate too far from the average position.
    max_deviation = 50  # You can adjust this value as per your needs.
    filtered_lines = []
    for line in lines:
        x1 = line.x1()
        x2 = line.x2()
        y1 = line.y1()
        y2 = line.y2()
        if abs(x1 - avg_x1) < max_deviation and abs(y1 - avg_y1) < max_deviation and abs(x2 - avg_x2) < max_deviation and abs(y2 - avg_y2) < max_deviation:
            filtered_lines.append(line)

    # Calculate the average position for the filtered lines.
    total_x1 = 0
    total_y1 = 0
    total_x2 = 0
    total_y2 = 0
    count = 0
    for line in filtered_lines:
        x1 = line.x1()
        x2 = line.x2()
        y1 = line.y1()
        y2 = line.y2()
        total_x1 += x1
        total_y1 += y1
        total_x2 += x2
        total_y2 += y2
        count += 2

    # Calculate the final average x and y coordinates.
    avg_x1 = 0
    avg_y1 = 0
    avg_x2 = 0
    avg_y2 = 0
    if count > 0:
        avg_x1 = total_x1 / (count / 2)
        avg_y1 = total_y1 / (count / 2)
        avg_x2 = total_x2 / (count / 2)
        avg_y2 = total_y2 / (count / 2)

    return int(avg_x1), int(avg_y1), int(avg_x2), int(avg_y2)



while(True):
    img = sensor.snapshot()
    #the sharpness alhough looks better the image, something happens and actually breaks the recognition
    #this is not recommended for image processing
    #img.conv3(sharp)

    #originally this was the line that was giving most of the initial good results (even at night these values work=
    #for l in img.find_lines(threshold = 1000, theta_margin = 50, rho_margin = 50):
    #these values are working for the nano, decreasing theta and margin, can give us more "near lines"
    #for some wierd reason these values for the sipeed maix nano at 9pm light on 3rd floor was working better
    #maybe because of the light? refer to the screenshot marked as 9pm_3rd_floor
    lines_found = img.find_lines(threshold = 800, theta_margin = 20, rho_margin = 20)
    #lets clean lines
    if len(lines_found)>0:
        point1_x,point1_y,point2_x,point2_y=avg_point_position(lines_found)
        if (point1_x != 0 or point1_y != 0 or point2_x != 0 or point2_y != 0):
            if does_line_intersect_circle(point1_x,point1_y,point2_x,point2_y,160,120,30):
                img.draw_line(point1_x,point1_y,point2_x,point2_y, color = (255, 0, 0))
    #for l in lines_found:
    ##looks like for the maix amigo the camera threshold is smaller
    ##for l in img.find_lines(threshold = 700, theta_margin = 12, rho_margin = 12):
        ##if (min_degree <= l.theta()) and (l.theta() <= max_degree):
        #if does_line_intersect_circle(l.x1(),l.y1(),l.x2(),l.y2(),160,120,30):
            #img.draw_line(l.line(), color = (255, 0, 0))
            #print(l)
    img.draw_circle(160, 120, 30, color = (255, 0, 0))
    lcd.display(img)
    time.sleep_ms(500)
    #img_len = v.record(img)
print("finish")
#v.record_finish()
lcd.clear()
