from .commands import is_command


def is_msg_w_text_to_bot(update) -> bool:
    if is_command(update):
        return False

    try:
        update.message.text
    except AttributeError:
        return False
    else:
        return update.message.text is not None


def is_channel_post_w_text(update) -> bool:
    if is_command(update):
        return False

    try:
        update.channel_post.text
    except AttributeError:
        return False
    else:
        return update.channel_post.text is not None
