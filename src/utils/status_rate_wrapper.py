class StatusRateWrapper:
    def __init__(self):
        self.status = None
        self.rate = 0

    def __str__(self):
        return f'Number is {self.rate}'

    def __f(self, x):
        return x % 16

    def __lt__(self, obj):
        """self < obj."""
        return self.__f(self.rate) < self.__f(obj.rate)

    def __le__(self, obj):
        """self <= obj."""
        return self.__f(self.rate) <= self.__f(obj.rate)

    def __eq__(self, obj):
        """self == obj."""
        return self.__f(self.rate) == self.__f(obj.rate)

    def __ne__(self, obj):
        """self != obj."""
        return self.__f(self.rate) != self.__f(obj.rate)

    def __gt__(self, obj):
        """self > obj."""
        return self.__f(self.rate) > self.__f(obj.rate)

    def __ge__(self, obj):
        """self >= obj."""
        return self.__f(self.rate) >= self.__f(obj.rate)
