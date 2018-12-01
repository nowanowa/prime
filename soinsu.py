# -*- coding: utf-8 -*-
import json
from copy import deepcopy
from math import sqrt
from os import mkdir
from re import sub

### calc prime-factorizations less than 'sup' ###

def bunkai(sup, numbers=None):
  if numbers is None or len(numbers) < 4:
    numbers = {
      0: [{'p':0,'e':1}],
      1: [],
      2: [{'p':2,'e':1}],
      3: [{'p':3,'e':1}]
    }
  for n in range(len(numbers),sup):
    factors = []
    divided = 0
    for k in range(2,int(sqrt(n))+1):
      if n % k == 0:
        l = n / k
        factors = merge(numbers[l],numbers[k])
        divided = 1
        break
    if not divided:
      factors = [{'p':n,'e':1}]
    numbers[n] = factors
  return numbers

def merge(n1,n2):
  if len(n1) > len(n2):
    nl = deepcopy(n1)
    ns = deepcopy(n2)
  else:
    nl = deepcopy(n2)
    ns = deepcopy(n1)
  for lfac in nl:
    added = 0
    for sfac in ns:
      if sfac['p'] == lfac['p']:
        sfac['e'] += lfac['e']
        added = 1
    if not added:
      ns.append(lfac)
  ns.sort(key = lambda x: x['p'])
  return ns


### check the prime-factorizations ###

def letterall(numbers):
  for i in numbers:
    letter(numbers[i])

def letter(n):
  txt = '1'
  for fac in n:
    txt += ' * ' + str(fac['p']) + '^' +str(fac['e'])
  print(txt)

def checkall(numbers):
  for i in numbers:
    u = calc(numbers[i])
    if i != u:
      print(i,u)

def calc(n):
  u = 1
  for fac in n:
    u *= fac['p'] ** fac['e']
  return u


### output json file of prime-factorizations ###

def dump(dic,path='./factorization-dump.json'):
  j = json.dumps(dic)
  j = sub(r'^{','{\n  ',j)
  j = sub(r'}$','\n}',j)
  j = j.replace('], ','],\n  ')
  with open(path,mode='w') as f:
    f.write(j)

def slice(numbers,inf,sup):
  nums = {}
  for i in range(inf,sup):
    nums[i] = numbers[i]
  return nums


### make 10 json files of prime-factorizations less than 1000000 ###

if __name__ == '__main__':
  num = bunkai(100000)
  mkdir('./factorization')
  dump(num,'./factorization/0.json')
  print('dumped 000000 - 099999')
  for i in range(1,10):
    l = str(i)
    num = bunkai((i+1)*100000, num)
    dump(slice(num, i*100000, (i+1)*100000), './factorization/' + l + '.json')
    print('dumped ' + l + '00000 - ' + l + '99999')


