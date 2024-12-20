import numpy as np

def transform(anchor, points, theta):
    theta = theta*np.pi/180 # degrees to radians
    
    translate(anchor, points)
    rotate(points, theta)
    translate([-anchor[0], 0], points)

    for point in points:
        [point[0], point[1]] = np.round(point, 3)

    print(points)

    return points


def translate(anchor, points):
    for point in points:
        point[0] -= anchor[0]
        point[1] -= anchor[1]


def rotate(points, theta):
    for point in points:
        x = point[0]*np.cos(theta) - point[1]*np.sin(theta)
        y = point[0]*np.sin(theta) + point[1]*np.cos(theta)
        
        point[0] = x
        point[1] = y
