import sys
from session import create_session, load_session
from api_requests import login, add_post

def print_welcome_message():
    print("Добро пожаловать в Delement!")

def print_help():
    print("Доступные команды:")
    print("LOGIN <email> <password> - вход в систему")
    print("POST <текст> - создание поста")
    print("help - отображение этого сообщения")

def main():
    if len(sys.argv) < 2:
        print_welcome_message()
        print_help()
        return

    command = sys.argv[1]

    if command == 'LOGIN':
        if len(sys.argv) != 4:
            print("Использование: python main.py LOGIN <email> <password>")
            return
        email, password = sys.argv[2], sys.argv[3]
        session_key = login(email, password)
        if session_key:
            create_session('default', session_key)
            print("Вход успешен")
        else:
            print("Ошибка входа")

    elif command == 'POST':
        if len(sys.argv) < 3:
            print("Использование: python main.py POST <текст>")
            return
        session_key = load_session('default')
        if session_key:
            text = ' '.join(sys.argv[2:])
            result = add_post(session_key, text)
            if result:
                print("Пост создан")
            else:
                print("Ошибка создания поста")
        else:
            print("Сессия закончена. Войдите снова.")

    elif command == 'help':
        print_help()

    else:
        print("Неизвестная команда")

if __name__ == "__main__":
    main()
