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

# Загружаем задачи при старте
tasks = load_tasks()

# Главная страница
@app.route('/')
def index():
    return render_template('index.html', tasks=tasks, search_query='')

# Поиск задач
@app.route('/search')
def search():
    query = request.args.get('q', '').strip().lower()
    if query:
        filtered_tasks = [task for task in tasks if query in task['text'].lower()]
    else:
        filtered_tasks = tasks
    return render_template('index.html', tasks=filtered_tasks, search_query=query)

# Сортировка по дате (новые сверху)
@app.route('/sort/date')
def sort_by_date():
    sorted_tasks = sorted(tasks, key=lambda t: t.get('date', ''), reverse=True)
    return render_template('index.html', tasks=sorted_tasks, search_query='')

# Сортировка по статусу (сначала активные)
@app.route('/sort/status')
def sort_by_status():
    sorted_tasks = sorted(tasks, key=lambda t: t.get('done', False))
    return render_template('index.html', tasks=sorted_tasks, search_query='')

# Сортировка по приоритету (высокий → средний → низкий)
@app.route('/sort/priority')
def sort_by_priority():
    priority_order = {'высокий': 1, 'средний': 2, 'низкий': 3}
    sorted_tasks = sorted(
        tasks,
        key=lambda t: priority_order.get(t.get('priority', 'средний'), 2)
    )
    return render_template('index.html', tasks=sorted_tasks, search_query='')

# Сортировка по алфавиту (А → Я)
@app.route('/sort/alpha')
def sort_by_alpha():
    sorted_tasks = sorted(tasks, key=lambda t: t.get('text', '').lower())
    return render_template('index.html', tasks=sorted_tasks, search_query='')

# Добавление новой задачи
@app.route('/add', methods=['POST'])
def add_task():
    task_text = request.form.get('task_text', '').strip()
    task_priority = request.form.get('priority', 'средний')
    task_date = datetime.now().strftime('%Y-%m-%d')
    
    if task_text:
        new_task = {
            'id': len(tasks) + 1,
            'text': task_text,
            'done': False,
            'priority': task_priority,
            'date': task_date
        }
        tasks.append(new_task)
        save_tasks(tasks)
    
    return redirect(url_for('index'))

# Переключение статуса выполнения задачи
@app.route('/toggle/<int:task_id>')
def toggle_task(task_id):
    for task in tasks:
        if task['id'] == task_id:
            task['done'] = not task['done']
            break
    save_tasks(tasks)
    return redirect(request.referrer or url_for('index'))

# Удаление задачи
@app.route('/delete/<int:task_id>')
def delete_task(task_id):
    global tasks
    tasks = [task for task in tasks if task['id'] != task_id]
    save_tasks(tasks)
    return redirect(request.referrer or url_for('index'))

# Запуск приложения
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)