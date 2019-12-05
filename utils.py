

def delete_mentions(string):
    new_string = ''
    for st in string.split(' '):
        if st.find('|@') != -1:
            st = st[st.find('|@') + 2 : -1]
        new_string += st + ' '
    return new_string[:-1]
