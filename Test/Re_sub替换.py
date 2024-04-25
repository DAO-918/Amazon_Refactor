from calendar import c
import re

a = '\n\t\n\t[]'
print(a)
# 匹配 \n (换行符) 或者 \t (制表符) 并将它们替换为空字符串，无论它们如何排列组合。
b = re.sub(r'[\n\t]', '', a)
print(b)
# 匹配 \n\t (即一个换行符紧接着一个制表符) 并将它们替换为空字符串
c = re.sub(r'\n\t', '', a)
print(c)

d = re.sub(r'\[\n\t\]', '', a)
print(d)
e = re.sub(r'[\[\]\n\t]', '', a)
print(e)