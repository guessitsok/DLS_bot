start_message = 'Привет! Я бот, который переносит стиль с одной фотографии ' \
    'на другую с помощью нейронной сети. \nЧтобы начать работу со мной, набери команду /style'

help_message = 'Вы можете посмотреть пример моей работы, набрав команду /example.\n' + \
               'Чтобы начать работу, набери команду /style\n' + \
               'Загрузи свою картинку а после стилевую!' + \
               ' В ответ Вы получите стилизованную картинку!\n' + \
               'Вы всегда можете посмотреть эту инфомацию снова, набрав команду /help.'

echo_message = 'Type /style to start, or /help to view the help.'

end_message = 'To transfer the style again, type the command /style'


MESSAGES = {
    'start': start_message,
    'help': help_message,
    'echo': echo_message,
    'end': end_message
}
