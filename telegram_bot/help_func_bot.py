import re


def verify_word(text):
    if re.match("^[А-Яа-яёЁЇїІіЄєҐґ_а-яА-Яa-zA-z]+$", text):
        return text
    else:
        return None


def show_list_keyword(data):
    b = []
    for i in data:
        b.append(i['keyword'])

    a = []
    for i in range(len(b)):
        q = (str(i + 1) + '. ' + str(b[i]))
        a.append(q)
    list_string = '\n'.join(a)
    return list_string
