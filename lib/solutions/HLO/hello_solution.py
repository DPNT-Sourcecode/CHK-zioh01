class HelloSolution:
    # friend_name = unicode string
    def hello(self, friend_name: str) -> str:
        """Return a greeting message for the given friend name."""
        if not isinstance(friend_name, str):
            raise TypeError("friend_name must be a string")
        if len(friend_name) == 0:
            raise ValueError("friend_name cannot be empty")
        return f"Hello, {friend_name}!"

