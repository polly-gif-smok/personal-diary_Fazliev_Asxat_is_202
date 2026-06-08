from flask import Flask, render_template, request, redirect, session
from database import init_db, get_all_messages, add_message
import locale
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'your-secret-key-here-change-in-production'  # Для сессий
init_db()

# Для задания Д: преобразование даты в русский формат
def format_date_russian(date_str):
    """Преобразует дату из формата YYYY-MM-DD в русский формат."""
    months = {
        '01': 'января', '02': 'февраля', '03': 'марта',
        '04': 'апреля', '05': 'мая', '06': 'июня',
        '07': 'июля', '08': 'августа', '09': 'сентября',
        '10': 'октября', '11': 'ноября', '12': 'декабря'
    }
    date_obj = datetime.strptime(date_str, '%Y-%m-%d')
    return f"{date_obj.day} {months[date_obj.strftime('%m')]} {date_obj.year}"

@app.route('/')
def index():
    """Главная страница: показывает все сообщения."""
    messages = get_all_messages()
    
    # Для задания Д: преобразуем даты
    for msg in messages:
        msg = dict(msg)
        msg['created_at_ru'] = format_date_russian(msg['created_at'])
    
    # Получаем сообщение об ошибке из сессии (для задания Г)
    error = session.pop('error', None)
    # Получаем сообщение об успехе из сессии (для задания В)
    success = session.pop('success', None)
    
    return render_template('index.html', 
                         messages=messages, 
                         error=error, 
                         success=success)

@app.route('/add', methods=['POST'])
def add():
    """Обрабатывает отправку нового сообщения."""
    name = request.form.get('name', '').strip()
    message = request.form.get('message', '').strip()
    
    # Задание Г: проверка на пустые поля
    if not name or not message:
        session['error'] = 'Пожалуйста, заполните все поля!'
        return redirect('/')
    
    # Добавляем сообщение
    add_message(name, message)
    
    # Задание В: добавляем сообщение об успехе в сессию
    session['success'] = 'Сообщение успешно добавлено!'
    
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)