import sys # используется для работы с аргументами командной строки.
from collections import defaultdict # помогает подсчитывать количество записей логов по уровням логирования.
from colorama import Fore, Style # предоставляет возможность добавления цвета в вывод текста в консоли.

# Скрипт має зчитувати і аналізувати лог-файл, підраховуючи кількість записів для кожного рівня логування

# Функція яка приймає рядок з логу як вхідний параметр і повертає словник з розібраними компонентами: дата, час, рівень, повідомлення. 
def parse_log_line(line: str) -> dict:
    try:
        # Разделение строки на части с использованием split()
        date, time, level, *message = line.strip().split()
        # Проверка корректности уровня логирования
        valid_levels = {"INFO", "ERROR", "DEBUG", "WARNING"}
        if level not in valid_levels:
            print(f"Предупреждение: Некорректный уровень логирования: {level}")
            return None
        # Возвращение структуры с разделением даты и времени
        return {
            "date": date,
            "time": time,
            "level": level,
            "message": " ".join(message)  # Объединение оставшихся частей сообщения
        }
    except ValueError:
        # Обработка строки неправильного формата
        print(f"Предупреждение: Некорректный формат строки лога: {line.strip()}")
        return None

# Функція відкриває файл, читає кожен рядок і застосовує до нього функцію parse_log_line, зберігаючи результати в список.
def load_logs(file_path: str) -> list:
    logs = []
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            for line in file:
                log_entry = parse_log_line(line)
                if log_entry:
                    logs.append(log_entry)
    # скрипт повинен вміти обробляти різні види помилок, такі як відсутність файлу або помилки при його читанні
    except FileNotFoundError:
        print(f"Помилка: Файл не знайдено: {file_path}")
        sys.exit(1)
    except Exception as e:
        print(f"Помилка при читанні файлу: {e}")
        sys.exit(1)
    return logs

# Функція виконує фільтрацію за рівнем логування
def filter_logs_by_level(logs: list, level: str) -> list:
    return list(filter(lambda log: log['level'] == level.upper(), logs))

# Функція виконує підрахунок записів за рівнем логування
def count_logs_by_level(logs: list) -> dict:
    log_stats_cache = defaultdict(int)
    for log in logs:
        log_stats_cache[log['level']] += 1
    return dict(log_stats_cache)

# Функція форматує та виводить результати підрахунку в читабельній формі.
def display_log_counts(counts: dict):
    # Вивід заголовка таблиці
    print(f"{'Рівень логування':<17} | {'Кількість'}")
    print(f"{'-' * 17} | {'-' * 10}")
    # Вивід даних з підрахунком
    for level, count in counts.items():
        if level == "ERROR":
            # Фиолетовый цвет для уровня "ERROR"
            level_text = f"{Fore.MAGENTA}{level:<17}{Style.RESET_ALL}"
        else:
            level_text = f"{level:<15}"
        print(f"{level_text:<17} | {count}")

def display_filtered_logs(logs: list):
    for log in logs:
        if log.get('date') and log.get('time') and log.get('message'):
            # Разделяем дату на части для выделения дня и месяца
            date_parts = log['date'].split('-')  # Ожидается формат YYYY-MM-DD
            if len(date_parts) == 3:
                # Выводим год, а день и месяц выделяем зелёным цветом
                formatted_date = f"{date_parts[0]}-{Fore.LIGHTGREEN_EX}{date_parts[2]}-{date_parts[1]}{Style.RESET_ALL}"
            else:
                formatted_date = log['date']  # Если формат не соответствует ожиданиям
            print(f"{formatted_date} {log['time']} - {log['message']}")
        else:
            print(f"Ошибка: некорректная запись лога: {log}")

# Скрипт повинен приймати шлях до файлу логів як аргумент командного рядка
def main():
    if len(sys.argv) < 2:
        print("Використання: python task_3.py <шлях_до_файлу> [<рівень_логування>]")
        sys.exit(1)
    file_path = sys.argv[1]
    # Скрипт повинен приймати не обов'язковий аргумент командного рядка, після аргументу шляху до файлу логів
    log_level = sys.argv[2].upper() if len(sys.argv) > 2 else None
    
    # Перевірка на правильність рівня логування
    valid_levels = {"INFO", "ERROR", "DEBUG", "WARNING"}
    if log_level and log_level not in valid_levels:
        print(f"Помилка: Неправильний рівень логування: {log_level}")
        sys.exit(1)

    logs = load_logs(file_path)
    log_counts = count_logs_by_level(logs)
    # display_log_counts яка форматує та виводить результати. Вона приймає результати виконання функції count_logs_by_level
    display_log_counts(log_counts)
    
    # Если указан уровень логирования, фильтрует логи и выводит соответствующие записи
    if log_level:
        filtered_logs = filter_logs_by_level(logs, log_level)
        print(f"\nДеталі логів для рівня '{log_level}':")
        display_filtered_logs(filtered_logs)

# Условие выполнения скрипта:
if __name__ == "__main__":
    main()
