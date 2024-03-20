def cache_string(filename, string_to_add):
    try:
        with open(filename, 'r+') as file:
            lines = file.readlines()
            if string_to_add + '\n' not in lines:
                file.write(string_to_add + '\n')
    except FileNotFoundError:
        with open(filename, 'w') as file:
            file.write(string_to_add + '\n')

def get_cached_strings(filename):
    try:
        with open(filename, 'r') as file:
            lines = file.readlines()
            cached_strings = [line.strip() for line in lines]
            return cached_strings
    except FileNotFoundError:
        return []