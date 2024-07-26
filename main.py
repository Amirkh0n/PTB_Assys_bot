import receive_poll as polls
import commands as comm
import messages as msg
import inlines as inl
import config
from telegram.ext import (
    Updater,
    CommandHandler,
    PollAnswerHandler,
    # PollHandler,
    MessageHandler,
    Filters,
    CallbackQueryHandler,
)


def main():
    updater=Updater(token=config.TOKEN)
    dp=updater.dispatcher
    dp.add_handler(CommandHandler('start', comm.start_command))
    dp.add_handler(CommandHandler('quizzes', comm.quizzes))
    dp.add_handler(CommandHandler('newquiz', comm.new_quiz))
    
    dp.add_handler(PollAnswerHandler(polls.receive_poll_answer))
    
    dp.add_handler(MessageHandler(Filters.text, msg.messages))
    dp.add_handler(MessageHandler(Filters.document, msg.save_file))

    dp.add_handler(CallbackQueryHandler(inl.inlines))

    updater.start_polling()
    print("""\t★★★Running bot!!!★★★
》》》to stop -> CTRL + C《《《
""")
    updater.idle()
    print('\t•••STOPPED!!!•••')

if __name__=='__main__':
    main()
