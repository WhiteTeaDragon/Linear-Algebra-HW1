from fractions import Fraction # ��� ������ � ������������� �������

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

def genBin(n, k, ones, chosen, perms): # �������, ������� ���������� ��� ������������������ �� 0 � 1 ����� n � ����� k ���������
    if len(chosen) == n:
        perms.append(list(chosen))
    else:
        if n - len(chosen) > k - ones: # ���� ����� ��������� 0, �� ���� ��������� ����� ��� k ������, ������ 0
            chosen.append(0)            
            genBin(n, k, ones, chosen, perms)
            chosen.pop()
        if ones < k: # ���� ������ ������ k, ������ 1
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
    
    def __pow__(self, n): # �������� ���������� � �������, � ������ ������ ������� ����������, ������� � ������� ������ ����� ��������
        if n == 0:
            newMatr = [[0] * self.size()[0] for i in range(self.size()[0])]
            for i in range(self.size()[0]):
                newMatr[i][i] = 1
            return Matrix(newMatr)
        if n % 2 == 1:
            return self * (self ** (n - 1))
        mid = self ** (n / 2)
        return mid * mid
    
    def det(self): # ������� ������������ �� �����������
        if self.size()[0] != self.size()[1]: # ���� �� ����������, �� ����� ���������
            raise MatrixError(self)
        n = self.size()[0]
        if n == 0: # ���� ������ = 0, �� ������ ����� ������ �������, ��� ������������ ����� 1
            return 1
        permutations = genPerms(n, set(range(n)))
        det = Fraction(0, 1)
        for elem in permutations: # ������������� ��� ������������
            numInv = 0 # ������� ����� ��������
            for i in range(n):
                for j in range(i + 1, n):
                    if elem[i] > elem[j]:
                        numInv += 1
            mult = Fraction((-1) ** numInv, 1) # ��� ����
            for i in range(n):
                mult *= self.matr[i][elem[i]]
            det += mult
        return det    
    
    def characterPolynom(self): # ���������� ������� ���. ���������� �� 0 ������� �� n-��
        if self.size()[0] != self.size()[1]: # �������� �� ������������
            raise MatrixError(self)
        n = self.size()[0]
        coeff = [0] * (n + 1) # ������� ������ �������������
        for k in range(n + 1):
            curr = (-1) ** (n - k) # ��� ����
            summ = 0
            perms = []
            genBin(n, k, 0, [], perms) # ��� ������������ ������� k
            for elem in perms:
                tmpMatrix = [[0] * (n - k) for i in range(n - k)] # ����� ����� ������� ����� ����, ��� �������� ������ ������ � �������
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
    
    def inverse(self): # ������� �������� ������� ������
        if self.size()[0] != self.size()[1]:
            raise MatrixError(self)
        n = self.size()[0]
        newMatr = [list(self.matr[i]) for i in range(n)] # ����� ����� �������
        theInverse = [[Fraction(0, 1)] * n for i in range(n)] # ��������� �������, � ����� ����� ����� ������ ��������
        for i in range(n):
            theInverse[i][i] = Fraction(1, 1) # ��������� � ��������� �� ���������
        for i in range(n): # � ���� ����� �������� ������� � ������������ ����, ����� �������� ������� ������� i-�� ������
            j = i
            while j < n and newMatr[j][i] == 0: # ���� � ������� ��������� �������
                j += 1
            if j >= n: # �� ����� ��������� �������, ������, ������� ����������
                raise MatrixError(self)
            tmp = list(newMatr[i])
            newMatr[i] = list(newMatr[j])
            newMatr[j] = list(tmp)
            invTmp = list(theInverse[i])
            theInverse[i] = list(theInverse[j])
            theInverse[j] = list(invTmp) # �������� ������� ������ � ��������� ��������� � �������, ����� � ������� �� ������ ������� ��� ��������� �������
            for k in range(i + 1, n): # � ���� ����� �������� ������� ���� ������� �������
                coeff = newMatr[k][i] / newMatr[i][i]
                newMatr[k][i] = 0
                for ind in range(i, n): # � ���� � ��������� ������ �������� �� ������ ������� ������, ����������� �� �����������
                    newMatr[k][ind] -= coeff * newMatr[i][ind]
                for ind in range(n):
                    theInverse[k][ind] -= coeff * theInverse[i][ind]
        for i in range(n): # � ���� ����� ������ ��� �������� �� ��������� ������� 1
            coeff = newMatr[i][i]
            for j in range(n):
                newMatr[i][j] /= coeff
                theInverse[i][j] /= coeff
        for i in range(1, n): # � ���� ����� ������ ��� �������� ���� ��������� ������� 0
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

a = [[4, 1, 1, -2], [2, 1, -2, -2], [5, 1, -2, -1], [0, 0, 5, -3]] # ������� ������
E = Matrix([[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]]) # ��������� �������
A = Matrix(a)
B = (A ** 2 + (-1) * A + (-1) * E) ** 2
B = B.inverse() # ������� ������� �� �������
print(*A.characterPolynom())
print(B.det())
