import os
import time
import config as conf
import services as ser
import receive_poll as rec
from telegram import Poll, InlineKeyboardMarkup, InlineKeyboardButton

# part code
def inlines(update, context):
    query=update.callback_query
    user_id=query.from_user.id
    chat_id=query.message.chat_id
    
    if query.data.startswith('quiz'):
        test_id = query.data.split('_')[1]
        test = conf.tests.get(test_id)
        text=f'<b>{test[1]}</b>\n\n{test[2]}\n\t<a href="https://t.me/{context.bot.username}?start={test_id}">Boshlash</a>'
        buttons=InlineKeyboardMarkup(
        [
            [InlineKeyboardButton(text='Update', callback_data=f'update_{test_id}'), InlineKeyboardButton(text='Delete', callback_data=f'delete_{test_id}')],
            [InlineKeyboardButton(text='Boshlash', url=f"https://t.me/{context.bot.username}?start={test_id}")],
            [InlineKeyboardButton(text='Guruhda boshlash', url=f"https://t.me/{context.bot.username}?startgroup={test_id}")]
        ]
        )
        query.edit_message_text(text=text, parse_mode='HTML', reply_markup=buttons)

    elif query.data.startswith('start'):
        if chat_id<0:
            if context.bot_data.get(chat_id, 0)<1:
                context.bot_data[chat_id]=context.bot_data.get(chat_id, 0)+1
                return
        test_id = query.data.split('_')[1]
        text="<b>Boshladik!</b>"
        
        tests = ser.quizes(filename=conf.tests.get(id=test_id)[3])
        chat_id = query.message.chat_id
        query.edit_message_text(text=text, parse_mode='HTML')
        
        questions = tests[0]['question']
        answer = tests[0]['answers']
        correct_option_id=[ tests[0]['answers'].index(i) for i in tests[0]['true']]
        timeout=10
        close_date = int(time.time())+timeout
        if len(correct_option_id)==1:
            poll_type=Poll.QUIZ
        else:
            poll_type='regular'
        # So'rovni chatga yuborish
        message = context.bot.send_poll(
            chat_id, 
            questions, 
            answer, 
            correct_option_id=correct_option_id[0],
            is_anonymous=False, 
            type=poll_type,
            allows_multiple_answers=True,
            close_date=close_date
        )
        payload = {
            message.poll.id: {
                'tests': tests,
                'test_id': 0,
                "message_id": message.message_id,
                "chat_id": chat_id,
                "results": {},
                "count": 0,
            }
        }
        context.bot_data.update(payload)
        
        context.job_queue.run_once(rec.close_poll, timeout, context=message.poll.id)
    elif query.data.startswith('delete'):
        test_id = query.data.split('_')[1]
        filename=conf.tests.get(id=test_id)[3]
        os.remove(filename)
        conf.tests.delete(id=test_id)
        query.edit_message_text(text="Muvaffaqiyatli bajarildi!", parse_mode='HTML')
        
        
