from fractions import Fraction

class Matrix:
    def __init__(self, a):
        self.matr = [list(map(lambda x: Fraction(x, 1), a[i])) for i in range(len(a))]

    def __str__(self):
        return '\n'.join(map(lambda x: '\t'.join(map(str, x)), self.matr))

    def size(self):
        lenStr = 0
        if len(self.matr) != 0:
            lenStr = len(self.matr[0])
        return (len(self.matr), lenStr)

    def __add__(self, other):
        if self.size()[0] != other.size()[0] or \
           self.size()[1] != other.size()[1]:
            raise MatrixError(self, other)
        newMatr = [[Fraction(0, 1)] * self.size()[1] for i in range(self.size()[0])]
        for i in range(len(self.matr)):
            for j in range(len(self.matr[i])):
                newMatr[i][j] = self.matr[i][j] + other.matr[i][j]
        return Matrix(newMatr)

    def __mul__(self, x):
        if isinstance(x, int) or isinstance(x, float) or isinstance(x, Fraction):
            newMatr = [[Fraction(0, 1)] * self.size()[1] for i in range(self.size()[0])]
            for i in range(len(self.matr)):
                for j in range(len(self.matr[i])):
                    newMatr[i][j] = self.matr[i][j] * x
            return Matrix(newMatr)
        elif isinstance(x, Matrix) and self.size()[1] == x.size()[0]:
            newMatr = [[Fraction(0, 1)] * x.size()[1] for i in range(self.size()[0])]
            for i in range(len(self.matr)):
                for j in range(x.size()[1]):
                    for k in range(self.size()[1]):
                        newMatr[i][j] += self.matr[i][k] * x.matr[k][j]
            return Matrix(newMatr)
        else:
            raise MatrixError(self, x)

    __rmul__ = __mul__
    
    def inverse(self): # находим обратную методом Гаусса
        n = self.size()[0]
        newMatr = [list(self.matr[i]) for i in range(n)] # копия нашей матрицы
        theInverse = [[Fraction(0, 1)] * n for i in range(n)] # единичная матрица, в конце здесь будет лежать обратная
        for i in range(n):
            theInverse[i][i] = Fraction(1, 1) # заполняем её единицами на диагонали
        for i in range(n): # в этом цикле приводим матрицу к ступенчатому виду, будем называть текущей строкой i-ую строку
            j = i
            while j < n and newMatr[j][i] == 0: # ищем в столбце ненулевой элемент
                j += 1
            if j >= n: # не нашли ненулевой элемент, значит, матрица необратима
                raise MatrixError(self)
            tmp = list(newMatr[i])
            newMatr[i] = list(newMatr[j])
            newMatr[j] = list(tmp)
            invTmp = list(theInverse[i])
            theInverse[i] = list(theInverse[j])
            theInverse[j] = list(invTmp) # поменяли местами строку с ненулевым элементом и текущую, чтобы в текущей на нужной позиции был ненулевой элемент
            for k in range(i + 1, n): # в этом цикле зануляем столбец ниже текущей позиции
                coeff = newMatr[k][i] / newMatr[i][i]
                newMatr[k][i] = 0
                for ind in range(i, n): # в этом и следующем циклах вычитаем из строки текущую строку, домноженную на коэффициент
                    newMatr[k][ind] -= coeff * newMatr[i][ind]
                for ind in range(n):
                    theInverse[k][ind] -= coeff * theInverse[i][ind]
        for i in range(n): # в этом цикле делаем все элементы на диагонали равными 1
            coeff = newMatr[i][i]
            for j in range(n):
                newMatr[i][j] /= coeff
                theInverse[i][j] /= coeff
        for i in range(1, n): # в этом цикле делаем все элементы выше диагонали равными 0
            for j in range(i):
                coeff = newMatr[j][i]
                for k in range(i, len(newMatr)):
                    newMatr[j][k] -= coeff * newMatr[i][k]
                for k in range(n):
                    theInverse[j][k] -= coeff * theInverse[i][k]
        return Matrix(theInverse)


class MatrixError(BaseException):
    def __init__(self, m1, m2):
        self.matrix1 = m1
        self.matrix2 = m2

alpha = [[-2, -2, 3, 3], [1, -2, -1, -3], [-3, -1, 2, -3], [3, 2, -3, 3]]
beta = [[20, 11, -17, -16], [-12, -18, 5, -14], [-3, 16, -8, -8], [-20, -10, 12, -6]]
gamma = [[-3, -1, -3, -1], [1, 3, -3, 1], [3, 2, -3, 2], [1, 1, -1, 2]]
delta = [[-1, -2, 1, 2], [2, 3, -4, -1], [-2, -2, 5, -1], [2, 2, -4, 1]] # до этого момента -- входные данные
alphaM = Matrix(alpha)
betaM = Matrix(beta)
gammaM = Matrix(gamma)
deltaM = Matrix(delta)
rightPart = alphaM.inverse() * deltaM
rightPart = rightPart * gammaM.inverse()
rightPart = rightPart.inverse() # здесь возвели левую и правую части в -1 степень
x = rightPart + ((-1) * betaM)
print(x)
