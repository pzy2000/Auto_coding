with open('base/tasks1.txt','r') as f:
    list_ = f.readlines()
    list_2 = []
    for i in list_:
        list_2.append(i.replace('\n', '').split())
    
print(list_2)
