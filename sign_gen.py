
class Sign:
    def __init__(self):
        self.signs = [10,20,30]

    def find_sign(self):
        self.sidx = 0
        while True:
            yield self.signs[self.sidx]
            self.sidx += 1
            if self.sidx > len(self.signs)-1:
                self.sidx = 0

s = Sign()

for _ in range(5):
    a = s.find_sign()
    print(a)



