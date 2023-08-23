import subprocess


def check_linter_file(file_path: str) -> str:
    """Проверяем файл на ошибки линтеров и формируем сообщение"""

    run_pycodestyle = subprocess.run(['python3', '-m', 'pycodestyle', f'media/{file_path}'],
                                     stdout=subprocess.PIPE,
                                     text=True)

    errors = run_pycodestyle.stdout.split(':')[1:]
    if errors:
        message_text = 'Ваш файл проверен и вот некоторые ошибки \n' + ' '.join(run_pycodestyle.stdout.split(':')[1:])
    else:
        message_text = 'Проверка прошла успешно\nЗамечаний нет :)'

    return message_text
