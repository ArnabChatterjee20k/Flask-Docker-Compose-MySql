# import json
# with open("t.json") as c:
#     print(json.load(c))
#
class Calc:
    def __init__(self,x):
        self.x=x
    def add(self):
        a=self.x.split()
        sum=0
        for i in a:
            sum+=int(i)
        print(sum)
        return sum

l=Calc("1 2 4 334").add()



