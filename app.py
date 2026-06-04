from flask import Flask, render_template, request, redirect, url_for
import json
import os
from datetime import datetime

app = Flask(__name__)

# Файл для хранения задач
TASKS_FILE = 'tasks.json'

# Загрузка задач из файла
def load_tasks():
    if os.path.exists(TASKS_FILE):
        with open(TASKS_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return []

# Сохранение задач в файл
def save_tasks(tasks):
    with open(TASKS_FILE, 'w', encoding='utf-8') as f:
        json.dump(tasks, f, ensure_ascii=False, indent=2)

# Глобальный список задач (для простоты, но лучше использовать файл)
# tasks = load_tasks()

# Временно используем тестовые данные для демонстрации
tasks = [
    {'id': 1, 'text': 'Купить продукты', 'done': False, 'priority': 'высокий', 'date': '2026-06-05'},
    {'id': 2, 'text': 'Сделать домашнее задание', 'done': False, 'priority': 'высокий', 'date': '2026-06-04'},
    {'id': 3, 'text': 'Позвонить маме', 'done': True, 'priority': 'средний', 'date': '2026-06-03'},
    {'id': 4, 'text': 'Записаться к врачу', 'done': False, 'priority': 'низкий', 'date': '2026-06-06'},
    {'id': 5, 'text': 'Убрать в комнате', 'done': True, 'priority': 'средний', 'date': '2026-06-02'},
]

@app.route('/')
def index():
    """Главная страница - показывает все задачи"""
    return render_template('index.html', tasks=tasks, search_query='')

@app.route('/search')
def search():
    """Поиск задач по тексту"""
    query = request.args.get('q', '').strip().lower()
    if query:
        filtered_tasks = [task for task in tasks if query in task['text'].lower()]
    else:
        filtered_tasks = tasks
    return render_template('index.html', tasks=filtered_tasks, search_query=query)

@app.route('/sort/date')
def sort_by_date():
    """Сортировка по дате (новые сверху)"""
    # Получаем параметр поиска из URL, если он есть
    search_query = request.args.get('search_query', '')
    
    # Сортируем задачи
    sorted_tasks = sorted(tasks, key=lambda t: t.get('date', ''), reverse=True)
    
    # Если есть поисковый запрос, фильтруем дополнительно
    if search_query:
        sorted_tasks = [task for task in sorted_tasks if search_query.lower() in task['text'].lower()]
    
    return render_template('index.html', tasks=sorted_tasks, search_query=search_query)

@app.route('/sort/status')
def sort_by_status():
    """Сортировка по статусу (сначала активные)"""
    search_query = request.args.get('search_query', '')
    
    # False (0) идет раньше True (1)
    sorted_tasks = sorted(tasks, key=lambda t: t.get('done', False))
    
    if search_query:
        sorted_tasks = [task for task in sorted_tasks if search_query.lower() in task['text'].lower()]
    
    return render_template('index.html', tasks=sorted_tasks, search_query=search_query)

@app.route('/sort/priority')
def sort_by_priority():
    """Сортировка по приоритету (высокий → средний → низкий)"""
    search_query = request.args.get('search_query', '')
    
    priority_order = {'высокий': 1, 'средний': 2, 'низкий': 3}
    sorted_tasks = sorted(
        tasks,
        key=lambda t: priority_order.get(t.get('priority', 'средний'), 2)
    )
    
    if search_query:
        sorted_tasks = [task for task in sorted_tasks if search_query.lower() in task['text'].lower()]
    
    return render_template('index.html', tasks=sorted_tasks, search_query=search_query)

@app.route('/sort/alpha')
def sort_by_alpha():
    """Сортировка по алфавиту (А → Я)"""
    search_query = request.args.get('search_query', '')
    
    sorted_tasks = sorted(tasks, key=lambda t: t.get('text', '').lower())
    
    if search_query:
        sorted_tasks = [task for task in sorted_tasks if search_query.lower() in task['text'].lower()]
    
    return render_template('index.html', tasks=sorted_tasks, search_query=search_query)

# Дополнительно: маршрут для сброса всех фильтров и сортировок
@app.route('/reset')
def reset():
    """Сброс всех фильтров и сортировок"""
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)