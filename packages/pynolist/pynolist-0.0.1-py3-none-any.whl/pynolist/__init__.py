import random

def emax(list):
    nl = [i for i in list if i%2==0]
    return max(nl)

def omax(list):
    nl = [i for i in list if i%2 != 0]
    return max(nl)

def emin(list):
    nl = [i for i in list if i%2==0]
    return min(nl)

def omin(list):
    nl = [i for i in list if i%2!=0]
    return min(nl)

def prime_search(list):
    nl = []
    for i in list:
        if i == 1:
            nl.append(i)
        elif i == 0:
            continue
        for j in range(2,i):
            if i%j == 0:
                break
        else:
            nl.append(i)
    return nl

def duplicate_search(list):
    nl = []
    for item in list:
        if list.count(item) > 1:
            if item not in nl:
                nl.append(item)
                nl.append('count :' + str(list.count(item)))
        elif type(item) == int or float:
            if list.count(str(item)) > 1:
                if item not in nl:
                    nl.append(item)
    return nl

def esum(list):
    nl = [i for i in list if i % 2 == 0]
    return sum(nl)

def osum(list):
    nl = [i for i in list if i % 2 != 0]
    return sum(nl)

def quick_list(length=int,max_number=int):
    nl = []
    for i in range(length):
        nl.append(random.randint(0,max_number))
    return nl


