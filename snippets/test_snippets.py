import unittest
import hamming_weight as hw
import multiples_3_5 as mul
import my_random as my_rand
from snippets.add_bdate_numbers import BirthDateAddition
from snippets.bouncy_numbers import bouncy_numbers
from snippets.printsomething import Calculator
from snippets.spiral_matrix import Solution


class MyTestCase(unittest.TestCase):

    def test_bouncy(self):
        bouncy = bouncy_numbers()
        print(bouncy.is_bouncy(1))
        print(bouncy.is_bouncy(123))
        print(bouncy.is_bouncy(321))
        print(bouncy.is_bouncy(7987))

    def test_count_bouncy_below(self):
        bouncy = bouncy_numbers()
        print(bouncy.count_bouncy_numbers_below(10))
        print(bouncy.count_bouncy_numbers_below(20))
        print(bouncy.count_bouncy_numbers_below(1000000))

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

    def test_calculator(self):
        calc = Calculator()
        print(calc.calculate(1, 2, '+'))

    def test_birthdate(self):
        birthdateadd = BirthDateAddition()
        birthdate = '08/07/1984'
        output = birthdateadd.addBirthDateNumbers(birthdate)
        print(birthdate + ' output is ' + str(output.addition))
        self.assertEqual(1999, output.addition, '')

        birthdate = '01/29/1985'
        output = birthdateadd.addBirthDateNumbers(birthdate)
        print(birthdate + ' output is ' + str(output.addition))
        self.assertEqual(2015, output.addition, '')

        birthdate = '03/06/2014'
        output = birthdateadd.addBirthDateNumbers(birthdate)
        print(birthdate + ' output is ' + str(output.addition))
        self.assertEqual(2023, output.addition, '')

        birthdate = '01/01/2000'
        output = birthdateadd.addBirthDateNumbers(birthdate)
        print(birthdate + ' output is ' + str(output.addition))
        self.assertNotEqual(2023, output.addition, '')




if __name__ == '__main__':
    unittest.main()
