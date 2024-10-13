import numpy as np

class Radar:
    

    def __init__(self, height=3.689, theta=45):
        self.MAJOR = 24*np.pi/180
        self.MINOR = 12*np.pi/180

        self.height = height
        self.theta = -theta*np.pi/180
        
        self.__compute_ellipse()


    def __compute_ellipse(self):
        alpha = self.height**2 * (1/np.cos(self.theta)**2) * (1 + np.tan(self.theta)**2 / ((1 / np.sin(self.MAJOR)**2) - np.tan(self.theta)**2))

        self.a = np.sqrt(alpha * np.sin(self.MINOR)**2)
        b = np.sqrt(alpha / ((1 / np.sin(self.MAJOR)**2) - np.tan(self.theta)**2))
        k = - self.height * np.tan(self.theta) * (1 / np.cos(self.theta)) / ((1 / np.sin(self.MAJOR)**2) - np.tan(self.theta)**2)
        
        self.b = 0.5 * ( (np.cos(self.theta)*(k+b) + np.sin(self.theta)*self.__get_z(0, k+b)) - (np.cos(self.theta)*(k-b) + np.sin(self.theta)*self.__get_z(0, k-b)) )
        self.k = np.cos(self.theta)*k + np.sin(self.theta)*self.__get_z(self.a, k)


    def __get_z(self, x, y):
        return -np.sqrt(x**2 / np.sin(self.MINOR)**2 + y**2 / np.sin(self.MAJOR)**2)


    def filter_point(self, x, y):
        return x**2 / self.a**2 + (y - self.k)**2 / self.b**2 <= 1
