a = [10,20,30,40,50]

A_invertida = a[::-1]


for index, item in enumerate(a):
    a[:-index].append(item)
    a.pop(index)
    qtd_item +- 1
    

print(a)