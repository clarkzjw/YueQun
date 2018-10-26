#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
YueQun Bot - An advanced bot to improve your Telegram group chat experiences.

"""

import logging
from io import BytesIO

import pika
import telegram
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

from broker.rabbitmq.producer import send_raw_update_to_mq
from config.common import MQ_PARAMS
from config.common import TG_BOT_TOKEN
from group.cloud import get_word_cloud
from group.common import auth, group_auth, check_in_group_message, log_command
from group.common import change_user_ignore
from group.keyword import set_keyword_reminder, get_keyword_by_user_id, user_del_keyword
from group.rank import get_rank
from model.db import init_db

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
`/help` *帮助*：显示本帮助
"""


# Define a few command handlers. These usually take the two arguments bot and
# update. Error handlers also receive the raised TelegramError object in error.
@log_command
@auth
@check_in_group_message
def start(bot, update):
    """Send a message when the command /start is issued."""
    update.message.reply_text(text=welcome_text,
                              parse_mode=telegram.ParseMode.MARKDOWN)


@log_command
@auth
@check_in_group_message
def help(bot, update):
    """Send a message when the command /help is issued."""
    update.message.reply_text(text=help_text,
                              parse_mode=telegram.ParseMode.MARKDOWN)


@group_auth
def yqbot_handler(bot, update):
    connection = pika.BlockingConnection(MQ_PARAMS)
    chan = connection.channel()
    send_raw_update_to_mq(chan, update)
    connection.close()


def error(bot, update, error):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, error)


@log_command
@auth
@check_in_group_message
def user_set_ignore(bot, update):
    user_id = update.message.from_user.id
    current_flag = change_user_ignore(update)
    if current_flag:
        update.message.reply_text(text="修改成功，您当前的状态是：*已被忽略*",
                                  parse_mode=telegram.ParseMode.MARKDOWN)
    else:
        update.message.reply_text(text="修改成功，您当前的状态是：*未被忽略*",
                                  parse_mode=telegram.ParseMode.MARKDOWN)


@log_command
@auth
@check_in_group_message
def user_set_keyword_reminder(bot, update, args):
    if not args:
        update.message.reply_text(text="使用格式为 `/set_keyword xxx`",
                                  parse_mode=telegram.ParseMode.MARKDOWN)
        return
    keywords = set_keyword_reminder(update.message.from_user.id, args)
    update.message.reply_text(keywords)


@log_command
@auth
@check_in_group_message
def user_get_keyword_reminder(bot, update):
    keywords = get_keyword_by_user_id(update.message.from_user.id)
    update.message.reply_text(keywords)


@log_command
@auth
@check_in_group_message
def user_del_keyword_reminder(bot, update, args):
    if not args:
        update.message.reply_text(text="使用格式为 `/del_keyword xxx`",
                                  parse_mode=telegram.ParseMode.MARKDOWN)
        return
    keywords = user_del_keyword(update.message.from_user.id, args)
    update.message.reply_text(keywords)


@log_command
@auth
@check_in_group_message
def user_get_cron_report(bot, update):
    update.message.reply_text("Not implemented yet.")


@log_command
@auth
@check_in_group_message
def user_get_per_user_report(bot, update):
    update.message.reply_text("Not implemented yet.")


@log_command
@auth
@check_in_group_message
def user_get_word_cloud(bot, update):
    update.message.reply_text("请稍后……")
    img = get_word_cloud()

    cloud = BytesIO()
    cloud.name = 'cloud.jpeg'
    img.save(cloud, 'JPEG')
    cloud.seek(0)

    bot.send_photo(update.message.chat_id, photo=cloud)


@log_command
@auth
@check_in_group_message
def user_get_msg_count_rank(bot, update, args):
    update.message.reply_text(text=get_rank(args),
                              parse_mode=telegram.ParseMode.MARKDOWN)


@log_command
@auth
@check_in_group_message
def user_get_reply_relation(bot, update):
    update.message.reply_text("Not implemented yet.")
    # from group.bagua import get_reply_network
    # get_reply_network()


@log_command
@auth
@check_in_group_message
def user_get_mention(bot, update):
    update.message.reply_text("Not implemented yet.")


def main():
    """Start the bot."""

    init_db()

    # Create the EventHandler and pass it your bot's token.
    updater = Updater(TG_BOT_TOKEN)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))
    dp.add_handler(CommandHandler("set_ignore", user_set_ignore))

    dp.add_handler(CommandHandler("set_keyword", user_set_keyword_reminder, pass_args=True))
    dp.add_handler(CommandHandler("get_keyword", user_get_keyword_reminder))
    dp.add_handler(CommandHandler("del_keyword", user_del_keyword_reminder, pass_args=True))

    dp.add_handler(CommandHandler("get_rank", user_get_msg_count_rank, pass_args=True))
    dp.add_handler(CommandHandler("get_cloud", user_get_word_cloud))

    dp.add_handler(CommandHandler("get_report", user_get_cron_report))
    dp.add_handler(CommandHandler("get_user", user_get_per_user_report))
    dp.add_handler(CommandHandler("get_bagua", user_get_reply_relation))
    dp.add_handler(CommandHandler("get_mention", user_get_mention))

    # on noncommand i.e message
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
