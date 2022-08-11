import random

with open('base/tasks.txt','r') as f:
    list_ = f.readlines()
    list_2 = []
    list_3 = []
    for i in list_:
        list_2.append(i.replace('\n', '').split())
        list_3.append(i.replace('\n', '').split())
    
    for i in range(len(list_2)):
        random.shuffle(list_2[i])


print(list_2, '\n', list_3)
