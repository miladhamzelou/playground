# -*- coding: utf-8 -*-
alist = [i for i in range(3)]
words = ['hello', 'my', 'friend']

for i, w in zip(alist, words):
    print(i, w)

letters = [letter for word in words
           for letter in word]
print(letters)

# avoid combine range and len
for i in range(len(alist)):
    print(alist[i])

for i in alist:
    print(i)

for i,v in enumerate(alist):
    print(i, v)

# avoid use 'len(positive_numbers) > 0'
numbers = [-1, -2, -3]
positive_numbers = [i for i in numbers if i > 0]
if positive_numbers:
    print('positive_numbers is false')

if positive_numbers is None:
    print('positive_numbers is none')
