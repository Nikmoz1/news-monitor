help_message = 'Я бот по пошука чотких і нужних новин, работаю даби ти узнавав тільки нужну інфу і нічого більше'

# start_message = 'Привіт, "{message.from_user.first_name}"!'\
#                             f'Я бот NewsAnalyzer.\n'\
#                             f'Допоможу тобі бути в курсі усіх улюблених подій'
add_keyword = 'Здороу, яке слово добавить?'
confirm_add = 'Якщо ти дійсно хочеш записати це слово натисни "Так"'
confirm_invalid = 'Я не розумію тебе, натисни "так" або "ні"'
confirm_add_keyword = 'Я тепер відслідковую таке слово'
add_no_change = 'OK, я нічого не добавив'
remove_keyword = 'Здороу, яке слово удалить?'
confirm_remove_keyword = 'Якщо ти дійсно хочеш видалити це слово натисни "Так"'
# confirm_remove = 'Я видалив таке слово', '"', "md.bold(data['keyword'])", '"'
remove_no_change = 'OK, я нічого не видалив'
wrong_word = 'А слово то неправильне'
empty_list_user = 'У вас немає слів за якими ви слідкуєте'


MESSAGES = {
    # 'start': start_message,
    'help': help_message,
    'add_keyword': add_keyword,
    'confirm_keyword': confirm_add_keyword,
    'add_confirm_invalid': confirm_invalid,
    'confirm_add_keyword': confirm_add_keyword,
    'add_no_change': add_no_change,
    'remove_keyword': remove_keyword,
    'confirm_remove_keyword': confirm_remove_keyword,
    'remove_no_change': remove_no_change,
    'wrong_word': wrong_word,
    'empty_list_user': empty_list_user
}


class MessagesFunc:
    def prepare_welcome_msg(first_name):
        return (f"Привіт, {first_name}!\n"
                f"Я бот NewsAnalyzer.\n"
                f"Допоможу тобі бути в курсі усіх улюблених подій")

    def delete_keyword(keyword):
        return 'Я видалив таке слово', '"', keyword, '"'

    def show_keywords(list_keyword):
        return "Ми відслідковуєм такі слова:\n" + list_keyword

