from .utils import Utils

import random
import math


class EllipticPoint:
    def __init__(self, x=0, y=0, inf=False):
        self.x = x if not inf else math.inf
        self.y = y if not inf else math.inf
        self.inf = inf

    def get_x(self):
        return self.x
    
    def get_y(self):
        return self.y
    
    def is_infinity(self):
        return self.inf
    
    def mirror(self):
        return EllipticPoint(self.x, -self.y, self.inf)

    def __eq__(self, point):
        if(isinstance(point, EllipticPoint)):
            if(self.inf):
                return self.inf == point.inf
            else:
                return self.x == point.x and self.y == point.y
            
        return False

    def __str__(self):
        return "({0}, {1})".format(self.x, self.y)


class EllipticCurve:
    def __init__(self, a, b, p):
        ''' y^2 = x^3 + ax + b '''
        self.a = a
        self.b = b
        self.p = p
        self.points = []
        if(self.is_singular()):
            print("Error: Curve is Singular!.")
    
    def is_singular(self):
        return((((4 * (self.a ** 3)) + (27 * (self.b ** 2))) % self.p) == 0)

    def get_points(self):
        points = [EllipticPoint(inf=True)]
        
        for x in range(self.p):
            y_square = x ** 3 + self.a * x + self.b

            for point in Utils.mod_sqrt(y_square % self.p, self.p):
                points.append(EllipticPoint(x, point))
        self.points = points 
    
    def get_y_square(self, x):
        y_square = x ** 3 + self.a * x + self.b

        for point in Utils.mod_sqrt(y_square % self.p, self.p):
            return(EllipticPoint(x, point))

    def point_addition(self, P, Q):
        if(P == Q):
            return self.point_multiplication(P)
        else:
            xp = P.get_x(); yp = P.get_y();
            xq = Q.get_x(); yq = Q.get_y();

            if(xp == xq):
                return EllipticPoint(inf=True)
            else:
                m = ((yp-yq) * pow((xp-xq), -1, self.p)) % self.p

                xr = (m ** 2 - xp - xq) % self.p
                yr = (m * (xp - xr) - yp) % self.p
                return EllipticPoint(xr, yr)

    def point_substraction(self, P, Q):
        return self.point_addition(P, Q.mirror())

    def point_multiplication(self, P):
        
        xp = P.get_x(); yp = P.get_y();

        if(yp == 0):
            return EllipticPoint(inf=True)
        else:
            m = ((3 * (xp ** 2) + self.a) * pow((2 * yp), -1, self.p)) % self.p
            xr = (m ** 2 - 2 * xp) % self.p
            yr = (m * (xp - xr) - yp) % self.p
            return EllipticPoint(xr, yr)

    def point_scalar_multiplication(self, P, k):
        if(k == 1):
            return P
        elif(k == 2):
            return self.point_multiplication(P)
        else:
            prev = P
            res = self.point_multiplication(P)
            for i in range(k-2):
                if(res.is_infinity()):
                    res = self.point_addition(prev, self.point_multiplication(P))
                else:
                    prev = res
                    res = self.point_addition(res, P)
    
            return res


class ECCElGamalMachine:
    def __init__(self):
        pass

    def is_prime(self, num, test_count=1000):
        if(num == 1):
            return False
        if(test_count >= num):
            test_count = num - 1
        for _ in range(test_count):
            val = random.randint(1, num - 1)
            if(pow(val, num-1, num) != 1):
                return False
        return True
    def create_random_prime(self, bit):
        found = False
        while not found:
            p = random.randint(2**(bit-1)+1, 2**bit-1)
            if self.is_prime(p):
                return p
    
    def create_agreement(self, bit):
        p = self.create_random_prime(bit)
        curve_a = random.randint(-p, p)
        curve_b = random.randint(-p, p)

        curve = EllipticCurve(curve_a, curve_b, p)
        curve.get_points()

        found = False

        B = None

        while(not found):
            B = curve.points[random.randint(1, len(curve.points) - 2)]
            if(not B.is_infinity()):
                found = True
        
        return p, curve_a, curve_b, B

    def create_key(self, p, curve_a, curve_b, B):

        pri = random.randint(1, p-2)

        curve = EllipticCurve(curve_a, curve_b, p)
        curve.get_points()
       
        public_key = curve.point_scalar_multiplication(B, pri)
        private_key = pri

        return public_key, private_key

    def encrypt(self, message, p, public_key):

        for m in message:
            k = random.randint(1, p-1)
            
