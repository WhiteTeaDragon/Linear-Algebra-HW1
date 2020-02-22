def genPerms(n, items): # ������� ���������� ������������ ����� n �� ���� ��������� items
    if n == 1: # ���� n == 1, ��������� � ����� ������ ������� �� items
        ans = []
        for elem in items:
            ans.append([elem])
        return ans
    permutations = []
    for elem in items: # ����� � ������ ������ ������������ �������� ������� ��� ������-�� �������� items ������ ���� �������
        smallerPerms = genPerms(n - 1, items - {elem})
        for array in smallerPerms:
            permutations.append([elem] + array)
    return permutations

class Permutation:
    def __init__(self, a):
        self.perm = list(a)
        
    def __str__(self): # ������� ������������ � ���� ���� �����
        return ' '.join(map(str, range(1, self.size() + 1))) + '\n' + ' '.join(map(lambda x: str(x + 1), self.perm))
    
    def size(self):
        return len(self.perm)
    
    def __mul__(self, other):
        if isinstance(other, Permutation) and other.size() == self.size():
            newPerm = [0] * self.size()
            for i in range(len(newPerm)):
                newPerm[i] = self.perm[other.perm[i]]
            return Permutation(newPerm)
        
    def __pow__(self, n): # �������� ���������� � �������
        if n < 0: # ��� ������������� n �������� � ������������� �������, ����� ������� ��������
            curr = self ** (-n)
            ans = [0] * curr.size()
            for i in range(curr.size()):
                ans[curr.perm[i]] = i
            return Permutation(ans)
        elif n == 0:
            return Permutation(list(range(self.size())))
        elif n > 0:
            if n % 2 == 0:
                mult = self ** (n // 2)
                return mult * mult
            else:
                return self * (self ** (n - 1))

n = 8
alpha = [6, 1, 8, 4, 7, 2, 3, 5]
beta1 = [5, 2, 3, 1, 6, 4, 7, 8]
beta1power = 13
beta2 = [8, 4, 5, 2, 1, 7, 3, 6]
beta2power = -1
rightPower = 161 # �� ����� ����� -- ������� ������
alphaP = Permutation(map(lambda x: x - 1, alpha)) # ����� �������� �������, ����� ��������� ���������� �� �������
beta1P = Permutation(map(lambda x: x - 1, beta1))
beta2P = Permutation(map(lambda x: x - 1, beta2))
rightPart = ((beta1P ** beta1power) * (beta2P ** beta2power)) ** rightPower # ��������� ������ ����� ���������
permutations = genPerms(n, set(range(1, n + 1))) # ��� ������������ ����� n = 8
for sigma in permutations:
    sigmaP = Permutation(map(lambda x: x - 1, sigma))
    leftPart = sigmaP * (alphaP * sigmaP) # ����� ����� ���������
    if leftPart.perm == rightPart.perm:
        print(sigmaP)
        print()
