from fractions import Fraction

def genPerms(n, items):
    if n == 1:
        ans = []
        for elem in items:
            ans.append([elem])
        return ans
    permutations = []
    for elem in items:
        smallerPerms = genPerms(n - 1, items - {elem})
        for array in smallerPerms:
            permutations.append([elem] + array)
    return permutations

def func(x): # чтобы отличать x от чисел
    if x != 'x':
        return Fraction(x, 1)
    else:
        return 'x'

class Matrix:
    def __init__(self, a):
        self.matr = [list(map(func, a[i])) for i in range(len(a))]

    def __str__(self):
        return '\n'.join(map(lambda x: '\t'.join(map(str, x)), self.matr))

    def size(self):
        lenStr = 0
        if len(self.matr) != 0:
            lenStr = len(self.matr[0])
        return (len(self.matr), lenStr)
    
    def detChanged(self, numX): # возвращает коэффициент в определителе перед х ** numX
        if self.size()[0] != self.size()[1]: # проверка на квадратность
            raise MatrixError(self)
        n = self.size()[0]
        permutations = genPerms(n, set(range(n)))
        det = Fraction(0, 1)
        for elem in permutations:
            cntX = 0 # проверяем, входит ли в эту перестановку х ** 5
            for i in range(n):
                if self.matr[i][elem[i]] == 'x':
                    cntX += 1
            if cntX != numX: # если не входит, не рассматриваем её
                continue
            numInv = 0
            for i in range(n):
                for j in range(i + 1, n):
                    if elem[i] > elem[j]:
                        numInv += 1
            mult = Fraction((-1) ** numInv, 1)
            for i in range(n):
                if self.matr[i][elem[i]] != 'x':
                    mult *= self.matr[i][elem[i]]
            det += mult
        return det


class MatrixError(BaseException):
    def __init__(self, m1, m2):
        self.matrix1 = m1
        self.matrix2 = m2

a = [['x', 8, -9, -4, 8, 7, 'x'], [9, -2, 8, 3, 'x', -1, 7], [-1, 9, 7, -6, 4, 'x', -3],\
     [-4, -2, -8, 2, 'x', 9, -5], [7, 5, 2, 'x', 9, -8, 5], [-3, 'x', -1, -3, -8, -3, -8],\
     [2, -7, 'x', -5, -9, 4, -1]]
power = 5 # до этой строчки -- входные данные
A = Matrix(a)
print(A.detChanged(power))
