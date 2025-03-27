def caching_fibonacci():
    # Створення порожнього словника cache
    cache = {}

    # Внутрішня функція для обчислення числа Фібоначчі
    def fibonacci(n):
        if n <= 0:  
            return 0
        if n == 1: 
            return 1
        if n in cache:  # Перевірка на наявність n у cache
            return cache[n]

        # Обчислення числа Фібоначчі та збереження в cache (Рекурсивний підхід)
        cache[n] = fibonacci(n - 1) + fibonacci(n - 2)
        return cache[n]

    # Повернення функції fibonacci
    return fibonacci

# Приклад використання
fib = caching_fibonacci()
print(fib(10))
print(fib(15)) 