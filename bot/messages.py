start_message = "Hello! I'm a bot that transfers style from one photo " \
    "to another with the help of a neural network. \To start working with me, type the command /style"

help_message = 'You can see an example of my work by typing the command /example.\n' + \
    'To get started, type the command /style\n' + \
    'Upload your picture and then a style one!' + \
    ' In response, you will receive a stylized picture!\n' + \
    'You can always view this information again by typing /help.'

echo_message = 'Type /style to start, or /help to view the help.'

end_message = 'To transfer the style again, type the command /style'


MESSAGES = {
    'start': start_message,
    'help': help_message,
    'echo': echo_message,
    'end': end_message
}
