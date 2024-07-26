from telegram import Poll, InlineKeyboardMarkup, InlineKeyboardButton
import services as ser
import time
import config as conf

# part code
def start_command(update, context):
    args=context.args
    user_id = update.effective_user.id
    if user_id not in conf.users.get_all_user_id():
        conf.users.insert(user_id =user_id, name=update.effective_user.first_name)
    text = "Assalomu alaykum!\n\nCommands:\n\t/newquiz - yangi viktorina yaratish!\n\t/quizzes - mavjud viktorinalar!"
    button=None
    
    if args:
        test=conf.tests.get(id=int(args[0]))
        text = f"{test[1]}:\n\n{test[2]}\n\nTestni boshlash uchun pastdagi tugmani bosing!"
        button=InlineKeyboardMarkup(
        [[InlineKeyboardButton(text='Tayyorman!', callback_data=f'start_{args[0]}')]]
        )

    update.message.reply_text(text = text, reply_markup=button, parse_mode='HTML')


def quizzes(update, context):
    user_id = update.effective_user.id
    tests = conf.tests.get(id = user_id, id_column='user_id', all=True)
    
    text ="<b>Your tests:</b>\n\n"
    button=[]
    for i, test in enumerate(tests, start=1):
        text+=f"{i}. {test[1]}\n"
        button.append(InlineKeyboardButton(text=str(i), callback_data= f"quiz_{test[0]}"))
    
    buttons = InlineKeyboardMarkup(ser.list_page(list=button, page_number=5))
    update.message.reply_text(
        text = text,
        reply_markup=buttons,
        parse_mode="HTML"
    )


def new_quiz(update, context):
    context.user_data['step']=conf.steps['new_quiz_title']
    update.message.reply_text(text="Yaratmoqchi bo'lgan testingizga nom bering! \n\nMasalan, 'Biologiya testi'")