from functools import wraps
from envparse import Env
import re

env = Env(ENABLE_SUDO=bool)

def with_touched_chat(f):
    @wraps(f)
    def wrapper(bot, update=None, *args, **kwargs):
        if update is None:
            return f(bot, *args, **kwargs)

        chat = bot.get_chat(update.message.chat)
        chat.touch_contact()

        if sudo(bot, update.message.from_user.id):
            kwargs.update(chat=chat)
            return f(bot, update, *args, **kwargs)
        else:
            bot.reply(update, str(update.message.from_user.name) + ' is not in the sudoers file. This incident will be reported.')
    return wrapper


def escape_markdown(text):
    """Helper function to escape telegram markup symbols"""
    escape_chars = '\*_`\['
    return re.sub(r'([%s])' % escape_chars, r'\\\1', text)


def markdown_twitter_usernames(text):
    """Restore markdown escaped usernames and make them link to twitter"""
    return re.sub(r'@([A-Za-z0-9_\\]+)',
                  lambda s: '[@{username}](https://twitter.com/{username})'
                  .format(username=s.group(1).replace(r'\_', '_')),
                  text)


def markdown_twitter_hashtags(text):
    """Restore markdown escaped hashtags and make them link to twitter"""
    return re.sub(r'\B#([^\s]*)',
                  lambda s: '[#{tag}](https://twitter.com/hashtag/{tag})'
                  .format(tag=s.group(1).replace(r'\_', '_')),
                  text)


def prepare_tweet_text(text):
    """Do all escape things for tweet text"""
    res = escape_markdown(text)
    res = markdown_twitter_usernames(res)
    res = markdown_twitter_hashtags(res)
    return res


def sudo(bot, uid):
    if env('ENABLE_SUDO') is False:
        return True
    else:
        for tg_user_id in bot.sudoers:
            bot.logger.debug("comparing " + str(uid) + " with " + str(tg_user_id))
            if tg_user_id == uid:
                bot.logger.debug("User " + str(uid) + " is a sudoer!")
                return True
                
        bot.logger.debug("User " + str(uid) + " is NOT a sudoer!")
        return False
