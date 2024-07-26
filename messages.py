import os
import config as conf
import commands as comm
import services as ser
from datetime import datetime
# from telegram import KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton

# part code
def messages(update, context):
    message = update.message.text
    user_id = update.effective_user.id
    step = context.user_data.get('step', 0)
    
    text = '/start buyrug\'ini bosing!'
    buttons=None
    
    if step == conf.steps['main_menu']:
        comm.start_command(update, context)
        return
        
    elif step == conf.steps['new_quiz_title']:
        context.user_data['new_test']={'title': message}
        context.user_data['step']=conf.steps['new_quiz_description']
        text = "Testning tavsifini yozing!"
        
    elif step == conf.steps['new_quiz_description']:
        context.user_data['new_test']['description']=message
        context.user_data['step']=conf.steps['new_quiz_file']
        text = "Iltimos testingiz faylini yuboring! \n\nTestingiz fayli quyidagi formatga javob bera olishi shart!:\n1. Har bir test savoli # bilan boshlanishi kerak!\n2. Har bir to'gri javob + belgisi bilan boshlanishi kerak!\n3. Har bir xato javoblar - belgisi bilan boshlanishi kerak!\n4. Har bir test orasida 2ta bo'sh qator bo'lishi kerak!\n5. Test fayli .txt formatdagi fayl bo'lishi kerak!"

    elif step == conf.steps['new_quiz_file']:
        text = "Iltimos testingiz faylini yuboring! \n\nTestingiz fayli quyidagi formatga javob bera olishi shart!:\n1. Har bir test savoli # bilan boshlanishi kerak!\n2. Har bir to'gri javob + belgisi bilan boshlanishi kerak!\n3. Har bir xato javoblar - belgisi bilan boshlanishi kerak!\n4. Har bir test orasida 2ta bo'sh qator bo'lishi kerak!\n5. Test fayli .txt formatdagi fayl bo'lishi kerak!"
    
    update.message.reply_text(
        text=text,
        reply_markup=buttons,
        parse_mode='HTML'
    )


def save_file(update, context):
    if context.user_data.get('step', 0) == conf.steps['new_quiz_file']:
        user_id = update.message.from_user.id
        file = update.message.document
        test = context.user_data.get('new_test', {})
        
        # FILES katalogini yaratish agar mavjud bo'lmasa
        if not os.path.exists('FILES'):
            os.makedirs('FILES')
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        file_path = os.path.join('FILES', f'{user_id}_{timestamp}_{file.file_name}')
    
        # Faylni yuklab olish
        file.get_file().download(custom_path=file_path)
        
        ser.quizes(new_test=True, test_title=test.get('title', 'TEST'), description=test.get('description', 'TESTS'), filename=file_path, user_id = user_id)
        update.message.reply_text(f'Fayl saqlandi: {file_path}')
    