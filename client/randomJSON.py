
from random import randint
import json

a = []
for _ in range(1400):
    a.append(randint(1000, 5000))

with open('testData2.json','a') as f:
    for _ in range(100):
        tempJson = {'pH':a.pop(0),'P':a.pop(0),'K':a.pop(0),
                'Ca':a.pop(0),'Mg':a.pop(0),'Na':a.pop(0),
                'Cl':a.pop(0),'Cu':a.pop(0),'Zn':a.pop(0),
                'Mn':a.pop(0),'Fe':a.pop(0),'S':a.pop(0),
                'N':a.pop(0),'C':a.pop(0)}
        json.dump(tempJson, f)
        f.write("\n")

f.close()
