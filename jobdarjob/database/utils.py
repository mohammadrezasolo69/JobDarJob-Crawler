import string


class GenerateID:
    def __init__(self):
        self.current_prefix = 'aa'
        self.current_number = 10000000

    @property
    def generate_id(self):
        letters = string.ascii_lowercase
        self.current_number += 1
        if self.current_number > 99999999:
            prefix_index = letters.find(self.current_prefix[0]) + 1
            self.current_prefix = letters[prefix_index] * 2
            self.current_number = 10000000

        return f'{self.current_prefix}{self.current_number}'
