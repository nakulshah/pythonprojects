import tokenize


class BirthDateAddition:

    def addBirthDateNumbers(self, birthdate):
        addition = 0
        numbers = birthdate.split('/')
        for i in numbers:
            addition = addition + int(i)
        return addition


