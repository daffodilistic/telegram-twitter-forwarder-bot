from functools import wraps
import re


def with_touched_chat(f):
    @wraps(f)
    def wrapper(bot, update=None, *args, **kwargs):
        if update is None:
            return f(bot, *args, **kwargs)

        chat = bot.get_chat(update.message.chat)
        chat.touch_contact()

        if self.sudo(msg.from_user.id):
            kwargs.update(chat=chat)
            return f(bot, update, *args, **kwargs)
        else:
            bot.reply(msg, str(update.from_user.name) + ' is not in the sudoers file. This incident will be reported.')
    return wrapper


def escape_markdown(text):
    """Helper function to escape telegram markup symbols"""
    escape_chars = '\*_`\['
    return re.sub(r'([%s])' % escape_chars, r'\\\1', text)


def markdown_twitter_usernames(text):
    """Restore markdown escaped usernames and make them link to twitter"""
    return re.sub(r'@([^\s]*)',
                  lambda s: '[@{username}](https://twitter.com/{username})'
                  .format(username=s.group(1).replace(r'\_', '_')),
                  text)

def sudo(bot, uid):
        for tg_user_id in bot.sudoers:
            bot.logger.debug("comparing " + str(uid) + " with " + str(tg_user_id))
            if tg_user_id == uid:
                bot.logger.debug("User " + str(uid) + " is a sudoer!")
                return True
                
        bot.logger.debug("User " + str(uid) + " is NOT a sudoer!")
        return False