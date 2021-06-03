def allow_access():
    """Декоратор, показывающий разрешён ли хэндлер"""
    def decorator(func):
        setattr(func, 'allow', True)
        return func

    return decorator
