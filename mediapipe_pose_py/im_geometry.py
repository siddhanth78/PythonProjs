import math

def distance(x1, y1, x2, y2):
    return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
    
def midpoint(x1, y1, x2, y2):
    mx = (x1 + x2) / 2
    my = (y1 + y2) / 2
    return (mx, my)
    
def getSlope(x1, y1, x2, y2):

    if x1 == x2:
        x1 = x2+1
        y2 = y1
    slope = (y2 - y1) / (x2 - x1)
    return slope

def getAngle(m1, m2):

    tan_theta = (m1 - m2) / (1 + m1 * m2)

    theta_radians = math.atan(tan_theta)
    theta_degrees = math.degrees(theta_radians)
    
    if theta_degrees < 0:
        theta_degrees += 180
        
    return theta_degrees