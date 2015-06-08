# -*- coding: utf-8 -*-

def gen(s):
    a = []
    rus = "йцукенгшщзхъфывапролджэячсмитьбюё"
    eng = "qwertyuiop[]asdfghjkl;'zxcvbnm,.`"
    trans = {}
    for i in range(len(rus)):
        trans[rus[i]] = eng[i]
        trans[eng[i]] = rus[i]
    l = len(s)
    for i in range(l + 1): 
        for c in rus:
            a.append([s[:i] + c + s[i:]])
        if i > 0 and i < l:
            a.append([s[:i], s[i:]])
        if i < l:
            for c in rus:
                a.append([s[:i] + c + s[i + 1:]])
            a.append([s[:i] + s[i + 1:]])
    try:
        a.append([''.join([trans[i] for i in s])])
    except:
        pass    
    return a
    
blol = {}

def freq():
    f = open('dictionary.txt', 'r')
    for i in f.readlines():
        t = i.split()
        x = float(t[1])
        #if x > 5:
        blol[t[0]] = x
    #print('dictionary loaded')
    return blol
            
blol = freq()

def iter(a, depth):
    b = blol
    c = []
    for i in a:
        k = 1
        for j in i:
            if j in b:
                k *= b[j]
            else:
                k = 0
                break
        k **= 1.0/len(i)
        if k > 0:
            c.append((i, k))
    if len(c) == 0:
        if depth == 0:
            #print('fail')
            return None
        q = []
        for t in a:
            k = 0
            for j in range(len(t)):
                if not t[j] in b:
                    k += 1
            if k > depth:
                continue
            for j in range(len(t)):
                if not t[j] in b:
                    x = gen(t[j])
                    for i in x:
                        q.append(t[:j] + i + t[j + 1:])
                #if j > 0:
                #    q.append(t[:j - 1] + [t[j - 1] + t[j]] + 
                #        t[j + 1:]) 
        return iter(q, depth - 1)
    else:
        return max(c, key = lambda x: x[1])
        #c.sort(key = lambda x: x[1], reverse=True)
        #return c[0]

def spell(a):
    arr = []
    x = sos(a, 2)
    if x is not None:
        arr.append(x)
    for i in range(len(a) - 1):
        x = sos(a[:i] + [a[i] + a[i + 1]] + a[i + 2:], 1)
        if x is not None:
            arr.append(x)
    arr.sort(key = lambda x:x[1], reverse=True)
    if len(arr) > 0:
        return arr[0][0]
    else:
        return None

def check2(a):
    s = a[0]
    l = len(s)
    q = ''
    m = l + 1
    for w in blol:
        if len(w) != l:
            continue
        k = 0
        for i in range(l):
            k += s[i] != w[i]
            if k > m:
                continue
        if k < m:
            m = k
            q = w
    return q


def check(a, depth=0): # not used
    x = sos(a)
    print(x)
    if x is not None:
        arr.append(x)
        #print('ololo', arr)
    if depth > -1:
        return
    for i in range(len(a) - 1):
        check(a[:i] + [a[i] + a[i + 1]] + a[i + 2:], depth - 1)

def sos(a, depth = 0):
    b = []
    for i in range(len(a)):
        x = iter([[a[i]]], depth)
        if x is not None:
            b += x[0]
        else:
            return None
    return iter([b], 0)

if __name__ == '__main__':
    freq(dict())
    check(input().lower().split(), 0)
    arr.sort(key = lambda x:x[1], reverse=True)
    print(arr)
    print(arr[0][0])
