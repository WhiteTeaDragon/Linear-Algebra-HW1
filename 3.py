from fractions import Fraction # для работы с рациональными числами

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

def genBin(n, k, ones, chosen, perms): # функция, которая возвращает все последовательности из 0 и 1 длины n с ровно k единицами
    if len(chosen) == n:
        perms.append(list(chosen))
    else:
        if n - len(chosen) > k - ones: # если можно поставить 0, то есть останется место для k единиц, ставим 0
            chosen.append(0)            
            genBin(n, k, ones, chosen, perms)
            chosen.pop()
        if ones < k: # если единиц меньше k, ставим 1
            chosen.append(1)
            genBin(n, k, ones + 1, chosen, perms)
            chosen.pop()

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
    
    def __pow__(self, n): # бинарное возведение в степень, в данной задаче матрицы квадратные, поэтому в степень всегда можно возвести
        if n == 0:
            newMatr = [[0] * self.size()[0] for i in range(self.size()[0])]
            for i in range(self.size()[0]):
                newMatr[i][i] = 1
            return Matrix(newMatr)
        if n % 2 == 1:
            return self * (self ** (n - 1))
        mid = self ** (n / 2)
        return mid * mid
    
    def det(self): # считаем определитель по определению
        if self.size()[0] != self.size()[1]: # если не квадратная, не можем посчитать
            raise MatrixError(self)
        n = self.size()[0]
        if n == 0: # если размер = 0, то дальше будет удобно считать, что определитель равен 1
            return 1
        permutations = genPerms(n, set(range(n)))
        det = Fraction(0, 1)
        for elem in permutations: # рассматриваем все перестановки
            numInv = 0 # считаем число инверсий
            for i in range(n):
                for j in range(i + 1, n):
                    if elem[i] > elem[j]:
                        numInv += 1
            mult = Fraction((-1) ** numInv, 1) # это знак
            for i in range(n):
                mult *= self.matr[i][elem[i]]
            det += mult
        return det    
    
    def characterPolynom(self): # возвращает степени хар. многочлена от 0 степени до n-ой
        if self.size()[0] != self.size()[1]: # проверка на квадратность
            raise MatrixError(self)
        n = self.size()[0]
        coeff = [0] * (n + 1) # заводим массив коэффициентов
        for k in range(n + 1):
            curr = (-1) ** (n - k) # это знак
            summ = 0
            perms = []
            genBin(n, k, 0, [], perms) # все подмножества размера k
            for elem in perms:
                tmpMatrix = [[0] * (n - k) for i in range(n - k)] # здесь будет матрица после того, как выбросим лишние строки и столбцы
                ind = 0
                for i in range(n):
                    jind = 0
                    if elem[i] == 1:
                        continue
                    for j in range(n):
                        if elem[j] == 1:
                            continue
                        tmpMatrix[ind][jind] = self.matr[i][j]
                        jind += 1
                    ind += 1
                tmpMatrix = Matrix(tmpMatrix)
                summ += tmpMatrix.det()
            coeff[k] = summ * curr
        return coeff
    
    def inverse(self): # находим обратную методом Гаусса
        if self.size()[0] != self.size()[1]:
            raise MatrixError(self)
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

a = [[4, 1, 1, -2], [2, 1, -2, -2], [5, 1, -2, -1], [0, 0, 5, -3]] # входные данные
E = Matrix([[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]]) # единичная матрица
A = Matrix(a)
B = (A ** 2 + (-1) * A + (-1) * E) ** 2
B = B.inverse() # считаем матрицу из условия
print(*A.characterPolynom())
print(B.det())
