class Reverse():
    ip = ''
    op = ''

    def rev(self, input):
        self.ip = input
        self.op = self.rev_loc(str(input), 0)
        return self.op

    def rev_loc(self, input, loc):
        if loc == len(input) - 1:
            return input[loc]
        else:
            return self.rev_loc(input, loc+1) + input[loc]

    def serialize(self):
        # test comment
        return ({'string': str(self.ip),
                'reverse': str(self.op)})

