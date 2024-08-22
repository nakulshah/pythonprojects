
class hamming_weight:

    def get_hamming_weight_number(self, number):
        result = 0
        # convert number into binary
        bin_num = self.get_binary(number)
        # convert binary into array of characters
        # count number of 1s in the array of characters, this is the hamming weight
        for i in bin_num:
            if i == '1':
                result = result + 1
        return result

    def get_binary(self, number):
        return bin(number)


# Find the Hamming Weight (https://en.wikipedia.org/wiki/Hamming_weight) of an integer passed