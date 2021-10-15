from lab1.interface import CurrencyCalculator


def main():
    calc = CurrencyCalculator('https://www.nbp.pl/kursy/xml/lasta.xml')
    calc.run()


if __name__ == '__main__':
    main()