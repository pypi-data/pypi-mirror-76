def is_callback_query(update) -> bool:
    return update.callback_query is not None
