def repeat(times=3):
    """The 'Factory' that takes the argument"""
    def decorator(func):
        """The actual decorator"""
        def wrapper(*args, **kwargs):
            """The logic execution"""
            for _ in range(times):
                result = func(*args, **kwargs)
            return result
        return wrapper
    return decorator

# Usage
@repeat()
def greet(name):
    print(f"Hello, {name}!")

greet("Alice")