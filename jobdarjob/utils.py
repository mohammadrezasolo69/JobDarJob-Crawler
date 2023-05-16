import string


def generate_id():
    letters = string.ascii_lowercase
    current_prefix = 'aa'
    current_number = 10000000

    while True:

        yield f'{current_prefix}{current_number}'
        current_number += 1
        if current_number > 99999999:
            prefix_index = letters.find(current_prefix[0]) + 1

            if prefix_index >= len(letters):
                break

            current_prefix = letters[prefix_index] * 2
            current_number = 10000000




