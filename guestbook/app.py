from flask import Flask, render_template
from database import init_db, get_all_messages

# Создаём экземпляр приложения Flask
app = Flask(__name__)

# Инициализируем базу данных при запуске приложения
# Таблица создастся автоматически, если её нет
init_db()

@app.route('/')
def index():
    """
    Обработчик главной страницы
    Получает все сообщения из БД и передаёт их в шаблон
    """
    # Получаем список всех сообщений
    messages = get_all_messages()
    
    # Отображаем шаблон и передаём в него сообщения
    return render_template('index.html', messages=messages)

@app.route('/about')
def about():
    """
    Дополнительная страница с информацией о проекте
    """
    return render_template('about.html')

# Запуск приложения
if __name__ == '__main__':
    # debug=True - автоматическая перезагрузка при изменении кода
    # host='0.0.0.0' - доступ с других устройств в сети
    app.run(debug=True, host='0.0.0.0', port=5000)