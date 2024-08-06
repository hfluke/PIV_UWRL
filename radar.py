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
        compute_points(float(sys.argv[1]), float(sys.argv[2]) * np.pi / 180)


def compute_points(h, theta):
    print('height:', h, '\tangle:', theta)

    alpha = h**2 * (1 / np.cos(theta)**2) * (1 + np.tan(theta)**2 / ((1 / np.sin(MAJOR)**2) - np.tan(theta)**2))
    k = - h * np.tan(theta) * (1 / np.cos(theta)) / ((1 / np.sin(MAJOR)**2) - np.tan(theta)**2)
    a = np.sqrt(alpha * np.sin(MINOR)**2)
    b = np.sqrt(alpha / ((1 / np.sin(MAJOR)**2) - np.tan(theta)**2))

    points = [
        {'x': 0, 'y': k + b},
        {'x': 0, 'y': k - b},
        {'x': a, 'y': k},
        {'x': -a, 'y': k},
    ]

    for point in points:
        point['z'] = get_z(point['x'], point['y'])

    for point in points:
        point = rotate_translate_point(point, theta)
    
        print(point)

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







if __name__ == '__main__':
    main()
