from typing import List


def is_command(update):
    try:
        if not update.message.text.startswith('/'):
            return False
    except AttributeError:
        return False

    try:
        entities = update.message.entities
    except AttributeError:
        return False

    def check_entities(entities: List):
        def entity_is_command(entity) -> bool:
            if entity.type == 'bot_command':
                return True
            else:
                return False

        if entities:
            if len(entities) != 1:
                return False
            else:
                return entity_is_command(entities[0])
        else:
            return False

    return check_entities(entities)


def is_start_command(update):
    if not is_command(update):
        return False
    else:
        if update.message.text == '/start':
            return True
        else:
            return False
