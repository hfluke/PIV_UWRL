import sys
import numpy as np


MAJOR = 24 * np.pi / 180
MINOR = 12 * np.pi / 180


def main():
    if len(sys.argv) < 2:
        print('please specify a height')
    elif len(sys.argv) < 3:
        print('please specify an angle')
    else:
        compute_points(
            h=float(sys.argv[1]), # 3.689m 
            theta=float(sys.argv[2])*np.pi/180 # 45 degrees
        )


def compute_points(h, theta):
    print('height:', h, '\tangle:', theta)
    theta = -theta # this is necessary for positive y-values in output

    alpha = h**2 * (1/np.cos(theta)**2) * (1 + np.tan(theta)**2 / ((1 / np.sin(MAJOR)**2) - np.tan(theta)**2))
    k = - h * np.tan(theta) * (1 / np.cos(theta)) / ((1 / np.sin(MAJOR)**2) - np.tan(theta)**2)
    a = np.sqrt(alpha * np.sin(MINOR)**2)
    b = np.sqrt(alpha / ((1 / np.sin(MAJOR)**2) - np.tan(theta)**2))

    k_0 = np.cos(theta)*k + np.sin(theta)*get_z(a, k)
    b_0 = 0.5 * ( (np.cos(theta)*(k+b) + np.sin(theta)*get_z(0, k+b)) - (np.cos(theta)*(k-b) + np.sin(theta)*get_z(0, k-b)) )

    points = [
        {'x': 0, 'y': k + b},
        {'x': 0, 'y': k - b},
        {'x': a, 'y': k},
        {'x': -a, 'y': k},
    ]

    for point in points:
        point['z'] = get_z(point['x'], point['y'])

    for i in range(len(points)):
        points[i] = rotate_translate_point(points[i], theta)

    print(f"points: {points_toString(points)}")
    # print(f"equation: {equation_toString(k_0, a, b_0)}")

    return


def get_z(x, y):
    return -np.sqrt(x**2 / np.sin(MINOR)**2 + y**2 / np.sin(MAJOR)**2)


def rotate_translate_point(point, theta):
    new_point = {
        'x': point['x'],
        'y': np.cos(theta) * point['y'] + np.sin(theta) * point['z'],
        'z': 0 # 'z': -np.sin(theta) * point['y'] + np.cos(theta) * point['z']
    }

    return new_point


def points_toString(points):
    pointstr = "{ \n"
    for point in points:
        pointstr += f"({point['x']}, {point['y']})\n"
    pointstr += "}"
    
    return pointstr


# def equation_toString(a, b, k):
#     eqstr = ""
#     return eqstr


if __name__ == '__main__':
    main()
