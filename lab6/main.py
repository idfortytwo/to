import random
from itertools import combinations, chain
from typing import Iterable

from lab6.proxy import MigrantRepository


def generate_names(name_parts: Iterable[str], length: int):
    yield from (assemble_name(name_parts_comb) for name_parts_comb in combinations(name_parts, length))


def assemble_name(name_parts: Iterable[str]):
    return ' '.join(randomize_case(word) for word in name_parts)


def randomize_case(word):
    return ''.join(random.choice((str.lower, str.upper))(letter) for letter in word)  # noqa


def random_coords():
    return random.randint(0, 90), random.randint(0, 90)


def main():
    name_parts = ['Siddig', 'Tahir', 'Fadil', 'Abdurrahman', 'Mohammed', 'Ahmed', 'Abdel', 'Karim', 'Mahdi', 'Abdul']

    two_parts_names = generate_names(name_parts, 2)
    three_parts_names = generate_names(name_parts, 3)
    four_parts_names = generate_names(name_parts, 4)

    repo = MigrantRepository()
    for name in two_parts_names:
        print(name)
        repo.add(name, random_coords())
    repo.save('two_parts.json')

    repo_from_file = MigrantRepository.from_file('two_parts.json')
    for name in chain(three_parts_names, four_parts_names):
        print(name)
        repo_from_file.add(name, random_coords())
    repo_from_file.save('two_three_four_parts.json')


if __name__ == '__main__':
    main()