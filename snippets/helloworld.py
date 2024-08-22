
def printhello():
    print('hello world!')
# printhello()

one_d_1 = []
one_d_2 = []
two_d = []

one_d_1.append(0)
one_d_1.append(1)
one_d_1.append(2)
one_d_2.append(10)
one_d_2.append(11)
one_d_2.append(12)

two_d.append(one_d_1)
two_d.append(one_d_2)

def print_d():
    for i in two_d:
        print(i)
        for j in i:
            print(j)
print_d()



