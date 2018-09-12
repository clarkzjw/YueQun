#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
YueQun Bot - An advanced bot to improve your Telegram group chat experiences.

"""

import telegram
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import logging

from pprint import pprint


from config.common import TG_BOT_TOKEN

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

welcome_text = """
欢迎使用阅群小助手!

获取更多帮助，请输入 `/help`. 
"""

help_text = """
阅群小助手目前支持以下设置:

`/set_ignore` *将我忽略*： 本设置开启后，您在群内的发言将不会被记录
`/set_keyword` *关键词提醒*： 您可以在此处设置若干关键词，群内发言若提及您设置的关键词，将会向您发送通知
`/get_rank` *谁最水*： 获取群内发言数排行榜
`/get_bagua` *关系网预测*： 通过数据智能分析，列举群内发言互动排行榜，推测群内八卦
`/get_mention` *关于我的消息*：获取一定时间段内群内与您有关的消息
`/get_user` *获取某用户的水群报告*：根据某用户在群内发言的记录，分析该用户的行为习惯
`/get_report` *获取水群消息摘要*：通过一定时间段内，总结群内发言消息的摘要
"""


# Define a few command handlers. These usually take the two arguments bot and
# update. Error handlers also receive the raised TelegramError object in error.
def start(bot, update):
    """Send a message when the command /start is issued."""
    update.message.reply_text(text=welcome_text,
                              parse_mode=telegram.ParseMode.MARKDOWN)


def help(bot, update):
    """Send a message when the command /help is issued."""
    update.message.reply_text(text=help_text,
                              parse_mode=telegram.ParseMode.MARKDOWN)




def yqbot_handler(bot, update):
    """Echo the user message."""
    # TODO: send message to rabbitmq
    update.message.reply_text(update.message.text)


def error(bot, update, error):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, error)


def user_set_ignore(bot, update):
    update.message.reply_text("Not implemented yet.")


def user_set_keyword_reminder(bot, update):
    # TODO: write an function about get keyword list by user
    update.message.reply_text("Not implemented yet.")


def user_get_cron_report(bot, update):
    update.message.reply_text("Not implemented yet.")


def user_get_per_user_report(bot, update):
    update.message.reply_text("Not implemented yet.")


def user_get_msg_count_rank(bot, update):
    update.message.reply_text("Not implemented yet.")


def user_get_reply_relation(bot, update):
    update.message.reply_text("Not implemented yet.")


def user_get_mention(bot, update):
    update.message.reply_text("Not implemented yet.")



def main():
    """Start the bot."""

    # Create the EventHandler and pass it your bot's token.
    updater = Updater(TG_BOT_TOKEN)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))
    dp.add_handler(CommandHandler("set_ignore", user_set_ignore))
    dp.add_handler(CommandHandler("set_keyword", user_set_keyword_reminder))
    dp.add_handler(CommandHandler("get_report", user_get_cron_report))
    dp.add_handler(CommandHandler("get_user", user_get_per_user_report))
    dp.add_handler(CommandHandler("get_rank", user_get_msg_count_rank))
    dp.add_handler(CommandHandler("get_bagua", user_get_reply_relation))
    dp.add_handler(CommandHandler("get_mention", user_get_mention))

    # on noncommand i.e message - echo the message on Telegram
    dp.add_handler(MessageHandler(Filters.all, yqbot_handler))

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
