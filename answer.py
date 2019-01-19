# 1#######################################################

# list = []
# for i in range(2000, 3201):
#     if (i % 7) == 0 and (i % 5) != 0:
#         list.append(str(i))
#
# print(','.join(list))

# 2#######################################################

# num = int(input('Please input an integal: '))
# if num >= 1:
#     total =1
#     for i in range(1, num +1):
#         total *=i
#     print(total)
#
# def fact(x):
#     if x == 0:
#         return 1
#     return x * fact(x - 1)
#
# x = int(input())
# print(fact(x))

# 3#######################################################
# def dic(num):
#     dic = {}
#     for i in range(1, num + 1):
#         dic.update({i : i*i})
#     return dic
#
# n = int(input())
# print(dic(n))
# 4#######################################################

"""
Question 4
Level 1

Question:
Write a program which accepts a sequence of comma-separated numbers from console and generate a list and a tuple which contains every number.
Suppose the following input is supplied to the program:
34,67,55,33,12,98
Then, the output should be:
['34', '67', '55', '33', '12', '98']
('34', '67', '55', '33', '12', '98')
"""
#
# keyin = input('Pls input:')
# lst = keyin.split(',')
# tpl = tuple(lst)
# print(lst)
# print(tpl)

"""
Question 5
Level 1

Question:
Define a class which has at least two methods:
getString: to get a string from console input
printString: to print the string in upper case.
Also please include simple test function to test the class methods.

"""
# class Myclass:
#
#     def __init__(self):
#         self.keyin = ""
#
#     def getString(self):
#         self.keyin = input('Pls input:')
#
#     def uppercase(self):
#         print(self.keyin.upper())
#
# myclass = Myclass()
# myclass.getString()
# myclass.uppercase()

"""
Question 6
Level 2

Question:
Write a program that calculates and prints the value according to the given formula:
Q = Square root of [(2 * C * D)/H]
Following are the fixed values of C and H:
C is 50. H is 30.
D is the variable whose values should be input to your program in a comma-separated sequence.
Example
Let us assume the following comma separated input sequence is given to the program:
100,150,180
The output of the program should be:
18,22,24
"""

# import math
# C = 50
# H = 30
#
# dlist = input('pls input  ').split(',')
# qlist = []
#
# for i in dlist:
#     qlist.append(str(int(math.sqrt(2 * C * int(i) / H))))
#
# print(','.join(qlist))


"""
Question 7
Level 2

Question:
Write a program which takes 2 digits, X,Y as input and generates a 2-dimensional array. The element value in the i-th row and j-th column of the array should be i*j.
Note: i=0,1.., X-1; j=0,1,¡­Y-1.
Example
Suppose the following inputs are given to the program:
3,5
Then, the output of the program should be:
[[0, 0, 0, 0, 0], [0, 1, 2, 3, 4], [0, 2, 4, 6, 8]]

"""

# x, y = input('pls input :').split(',')
# lst = []
# for i in range(int(x)):
#     l =[]
#     for j in range(int(y)):
#         l.append(i*j)
#     lst.append(l)
# print(lst)

"""
Question 8
Level 2

Question:
Write a program that accepts a comma separated sequence of words as input and prints the words in a comma-separated sequence after sorting them alphabetically.
Suppose the following input is supplied to the program:
without,hello,bag,world
Then, the output should be:
bag,hello,without,world
"""

# keyin = input('pls keyin : ').split(',')
# keyin.sort()
# print(','.join(keyin))


"""
Question 9
Level 2

Question£º
Write a program that accepts sequence of lines as input and prints the lines after making all characters in the sentence capitalized.
Suppose the following input is supplied to the program:
Hello world
Practice makes perfect
Then, the output should be:
HELLO WORLD
PRACTICE MAKES PERFECT

"""
#
# lines = []
#
# while True:
#     keyin = input('pls input')
#     if keyin:
#         lines.append(keyin.upper())
#     else:
#         break
#
# for line in lines:
#     print(line)


"""
Question 10
Level 2

Question:
Write a program that accepts a sequence of whitespace separated words as input and prints the words after removing all duplicate words and sorting them alphanumerically.
Suppose the following input is supplied to the program:
hello world and practice makes perfect and hello world again
Then, the output should be:
again and hello makes perfect practice world

"""

# words = input('pls input :').split(' ')
# print(' '.join(sorted(set(words))))

"""
Question 11
Level 2

Question:
Write a program which accepts a sequence of comma separated 4 digit binary numbers as its input and then check whether they are divisible by 5 or not. The numbers that are divisible by 5 are to be printed in a comma separated sequence.
Example:
0100,0011,1010,1001
Then the output should be:
1010
Notes: Assume the data is input by console.

"""

# binary = input('pls input :').split(',')
# answer = []
# for b in binary:
#     if not int(b, 2) % 5:
#         answer.append(b)
# print(','.join(answer))

"""
Question 12
Level 2

Question:
Write a program, which will find all such numbers between 1000 and 3000 (both included) 
such that each digit of the number is an even number.
The numbers obtained should be printed in a comma-separated sequence on a single line.

"""
# numlist =[]
# for num in range(1000, 3000 + 1):
#     isok = False
#     for digital in str(num):
#         if int(digital) % 2:
#             isok = False
#             break
#         else:
#             isok = True
#     if isok:
#         numlist.append(str(num))
# print(",".join(numlist))

"""
Question 13
Level 2

Question:
Write a program that accepts a sentence and calculate the number of letters and digits.
Suppose the following input is supplied to the program:
hello world! 123
Then, the output should be:
LETTERS 10
DIGITS 3

"""

# words = input('pls input : ')
# lettercount = 0
# digitcount = 0
# for i in words:
#     if i in 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz':
#         lettercount += 1
#     elif i in '0123456789':
#         digitcount += 1
#
# print('LETTERS ' + str(lettercount))
# print('DIGITS ' + str(digitcount))


"""
Question 14
Level 2

Question:
Write a program that accepts a sentence and calculate 
the number of upper case letters and lower case letters.
Suppose the following input is supplied to the program:
Hello world!
Then, the output should be:
UPPER CASE 1
LOWER CASE 9

"""
# words = input('pls input : ')
# uppercount = 0
# lowercount = 0
# for i in words:
#     if i in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ':
#         uppercount += 1
#     elif i in 'abcdefghijklmnopqrstuvwxyz':
#         lowercount += 1
#
# print('UPPER CASE ' + str(uppercount))
# print('LOWER CASE ' + str(lowercount))


"""
Question 15
Level 2

Question:
Write a program that computes the value of a+aa+aaa+aaaa with a given digit as the value of a.
Suppose the following input is supplied to the program:
9
Then, the output should be:
11106

"""
# import math
# number = int(input('pls input :'))
# sum = 0
# for i in range(1, 4 + 1):
#     for j in range(i):
#         sum += number * int(math.pow(10, j))
# print(sum)



