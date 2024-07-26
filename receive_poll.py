from telegram import Poll
import time


def receive_poll_answer(update, context):
    """Foydalanuvchi so'rovlarining natijalari"""
    answer = update.poll_answer
    poll_id = answer.poll_id
    try:
        payload = context.bot_data[poll_id]
        context.bot_data[poll_id]['count']=1
    except Exception as e:         # Bu eski so'rov uchun javob
        return
    selected_options = answer.option_ids
    true = [payload['tests'][payload['test_id']]['answers'].index(i) for i in payload['tests'][payload['test_id']]['true']]
        
    if selected_options == true:
        payload['results'][answer.user.id] = payload['results'].get(answer.user.id, 0) + 1
    else:
        payload['results'][answer.user.id] = payload['results'].get(answer.user.id, 0) + 0

    if payload['chat_id']<0:
        return
        
    if payload['tests'][payload['test_id']] == payload['tests'][-1]:
        text = f"Test tugadi!\nSiz {len(payload['tests'])}ta savoldan {list(payload['results'].values())[0]}tasiga to'g'ri javob berdingiz!"
        context.bot.send_message(
            chat_id=payload["chat_id"],
            text=text
        )
        return

    chat_id = payload["chat_id"]
    message_id = payload["message_id"]
    tests=payload['tests']
    test_id=payload['test_id']+1
    true = [tests[test_id]['answers'].index(i) for i in tests[test_id]['true']]


    
    if len(true)==1:
        poll_type=Poll.QUIZ
    else:
        poll_type='regular'
    
    timeout=10
    close_date = int(time.time())+timeout
    
    message = context.bot.send_poll(
        chat_id=payload['chat_id'], 
        question=tests[test_id]['question'],
        options=tests[test_id]['answers'],
        is_anonymous=False, 
        allows_multiple_answers=True,
        type=poll_type,
        correct_option_id=true[0],
        close_date=close_date
    )
    
    payloads = {
        message.poll.id: {
            'tests': payload['tests'],
            'test_id': payload['test_id']+1,
            'chat_id': payload['chat_id'],
            "message_id": message.message_id,
            'true': payload['tests'][payload['test_id']+1]['true'],
            'results': payload['results'],
            "count": 0,
        }
    }
    # Oraliq natijalarni `bot_data` ga saqlash
    context.bot_data.update(payloads)
    context.job_queue.run_once(close_poll, timeout, context=message.poll.id)


def close_poll(context) -> None:
    poll_id = context.job.context

    # Poll ma'lumotlarini olish
    if poll_id in context.bot_data:
        payload= context.bot_data[poll_id]
        chat_id = payload["chat_id"]
        message_id = payload["message_id"]
        tests=payload['tests']
        test_id=payload['test_id']+1

        # Pollni yopishga harakat qilishdan oldin pollning yopilganligini tekshirish
        try:
            context.bot.stop_poll(chat_id, message_id)
        except Exception as e:
            if str(e) == "Poll has already been closed":
                pass
            else:
                raise

        
        # Javoblar sonini tekshirish
        
        if payload['count'] == 0 or chat_id < 0:
            if payload['tests'][payload['test_id']] == payload['tests'][-1]:
                print('Test tugadi!')
                results = payload['results']
                users_id = list(results.keys())
        
                # Natijalarni kamayish tartibida saralash
                sorted_results = sorted(results.items(), key=lambda item: item[1], reverse=True)
                sorted_users_id = [item[0] for item in sorted_results]
                sorted_scores = [item[1] for item in sorted_results]
        
                mentions = [context.bot.get_chat(user_id).first_name for user_id in sorted_users_id]
                text = f"TEST TUGADI! \nNatijalar quyidagicha:\n"
                for i in range(len(mentions)):
                    text += f"{i+1}. <a href='tg://user?id={sorted_users_id[i]}'>{mentions[i]}</a> - {sorted_scores[i]}/{len(payload['tests'])}!\n"
                context.bot.send_message(
                    chat_id=payload["chat_id"],
                    text=text,
                    parse_mode='HTML'
                )
                return

                
            true = [tests[test_id]['answers'].index(i) for i in tests[test_id]['true']]
            if len(true)==1:
                poll_type=Poll.QUIZ
            else:
                poll_type='regular'
            
            timeout=10
            close_date = int(time.time())+timeout
            
            message = context.bot.send_poll(
                chat_id=payload['chat_id'], 
                question=payload['tests'][payload['test_id']+1]['question'],
                options=payload['tests'][payload['test_id']+1]['answers'],
                is_anonymous=False, 
                allows_multiple_answers=True,
                type=poll_type,
                correct_option_id=true[0],
                close_date=close_date
            )
            
            payloads = {
                message.poll.id: {
                    'tests': payload['tests'],
                    'test_id': test_id,
                    'chat_id': chat_id,
                    "message_id": message.message_id,
                    'results': payload['results'],
                    'count': 0
                }
            }
            # Oraliq natijalarni `bot_data` ga saqlash
            context.bot_data.update(payloads)
            context.job_queue.run_once(close_poll, timeout, context=message.poll.id)
        
