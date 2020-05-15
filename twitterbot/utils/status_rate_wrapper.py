class StatusRateWrapper:
    def __init__(self):
        self.status = None
        self.rate = 0

    def __str__(self):
        return f'Number is {self.rate}'

    def __lt__(self, obj):
        """self < obj."""
        return self.rate < obj.rate

    def __le__(self, obj):
        """self <= obj."""
        return self.rate <= obj.rate

    def __eq__(self, obj):
        """self == obj."""
        return self.rate == obj.rate and self.status.id == obj.status.id

    def __ne__(self, obj):
        """self != obj."""
        return self.rate != obj.rate or self.status.id != obj.status.id

    def __gt__(self, obj):
        """self > obj."""
        return self.rate > obj.rate

    def __ge__(self, obj):
        """self >= obj."""
        return self.rate >= obj.rate
