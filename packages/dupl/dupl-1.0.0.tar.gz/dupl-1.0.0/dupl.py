def duplicate_remover(list):
    l2= []
    for i in list:
        if i not in l2:
            l2.append(i)
    return l2