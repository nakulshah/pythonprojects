class bouncy_numbers:
    def is_bouncy(self, num):
        digit_list = [int(d) for d in str(num)]
        is_increasing = False
        is_decreasing = False
        first = 0
        follow = 0
        # assume single digit number is non-bouncy
        if num < 10:
            return False
        else:
            first = digit_list[0]
            follow = digit_list[1]

            if first == follow:
                return True  # assume if same then number is bouncy
            elif first < follow:
                is_increasing = True
            else:
                is_decreasing = True

            i: int = 2
            while len(digit_list) > i:
                first = digit_list[i - 1]
                follow = digit_list[i]
                if is_increasing:
                    if first > follow:
                        return True
                if is_decreasing:
                    if first < follow:
                        return True
                i += 1

            return False

    def count_bouncy_numbers_below(self, last_num):
        i = 0
        count = 0
        while i < last_num:
            if self.is_bouncy(i):
                count += 1
            i += 1

        return count
