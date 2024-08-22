import unittest
import hamming_weight as hw
import multiples_3_5 as mul
import my_random as my_rand
from snippets.spiral_matrix import Solution


class MyTestCase(unittest.TestCase):

    def test_random(self):
        rand = my_rand.my_random()
        print(rand.generate_random(893))

    def test_something(self):
        self.assertEqual(True, False)  # add assertion here

    def test_binary_conversion(self):
        h = hw.hamming_weight()
        number = 3
        hamm = h.get_hamming_weight_number(number)
        print('hamming weight for ' + str(number) + ' is ' + str(hamm))
        self.assertEqual(hamm, 2)

        number = 25
        hamm = h.get_hamming_weight_number(number)
        print('hamming weight for ' + str(number) + ' is ' + str(hamm))
        self.assertEqual(hamm, 3)

        number = 250
        hamm = h.get_hamming_weight_number(number)
        print('hamming weight for ' + str(number) + ' is ' + str(hamm))
        self.assertEqual(hamm, 6)

    def test_spiral_matrix(self):
        spiral = Solution()
        result = spiral.spiralMatrixIII(1, 2, 3, 4)

        print(result)

    def test_3_5(self):
        m = mul.three_five()
        sum = m.find_3_5_sum(10)
        print(sum)
        self.assertEqual(23, sum)

        sum = m.find_3_5_sum(1000)
        print(sum)
        self.assertEqual(233168, sum)




if __name__ == '__main__':
    unittest.main()
