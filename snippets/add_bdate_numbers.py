import tokenize


class BirthDateAddition:

    def addBirthDateNumbers(self, birthdate):
        addition = 0
        numbers = birthdate.split('/')
        for i in numbers:
            addition = addition + int(i)

        birthdateadd = BirthdateAdd()
        birthdateadd.birthdate = birthdate
        birthdateadd.addition = addition
        return birthdateadd


class BirthdateAdd:
    birthdate = ''
    addition = 0

    def serialize(self):
        return ({'birthdate': str(self.birthdate),
                'addition': int(self.addition)})