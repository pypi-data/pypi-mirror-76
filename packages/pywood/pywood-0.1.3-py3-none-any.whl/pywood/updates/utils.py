from copy import deepcopy


def get_anonymized_update(update):
    new_update = deepcopy(update)
    new_update.update_id = 123456789
    new_update.message.chat.id = 123456789
    new_update.message.chat.username = 'Username'
    new_update.message.chat.first_name = 'FirstName'
    new_update.message.from_.id = 123456789
    new_update.message.from_.username = 'blablabla'
    new_update.message.from_.first_name = 'hurraaaa'
    return new_update
