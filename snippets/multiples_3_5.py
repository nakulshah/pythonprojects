# https://projecteuler.net/problem=1
class three_five:

    def find_3_5_sum(self, num):
        sum = 0
        i = 1
        while (i < num):
            if(i % 3 == 0):
                sum += i
            elif(i % 5 == 0):
                sum += i
            i += 1

        return sum
