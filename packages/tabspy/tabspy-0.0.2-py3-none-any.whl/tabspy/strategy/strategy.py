class Strategy:
    def __init__(self, name=None):
        self._name = name

    def welcome(self):
        print(f'Welcome {self._name} : tabspy >> strategy >> strategy.Strategy.welcome()')
        return