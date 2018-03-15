file_a = 'kadj.txt'
f = open(file_a, 'w')

f.write(("haha " + '\n') * 50)

f.close()

l = [
    "a\n",
    "b\n",
    "c\n"
]

print "".join(l)