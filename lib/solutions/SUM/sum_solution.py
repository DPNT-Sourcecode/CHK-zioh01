class SumSolution:
    def compute(self, x: int, y: int) -> int:
        """Return the sume of two integrer between a minimum and maximum range."""
        if not isinstance(x, int) or not isinstance(y, int):
            raise TypeError("Both arguments must be integers.")
        if x < 0 or y < 0:
            raise ValueError("Both arguments must be non-negative.")
        if x > 100 or y > 100:
            raise ValueError("Both arguments must be less than or equal to 100.")
        return x + y
