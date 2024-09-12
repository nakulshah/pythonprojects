
class Calculator:

    def calculate(self, num1, num2, operator):
        if '+' == operator:
            return num1 + num2
        elif '-' == operator:
            return num1 - num2
        elif '*' == operator:
            return num1 * num2
        elif '/' == operator:
            return num1 / num2
        print("something")
        return 0



