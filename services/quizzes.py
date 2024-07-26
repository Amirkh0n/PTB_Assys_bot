import random as r
import config as conf

def quizes(filename ='FILES/aaa.txt', len_test=5, test_title='TEST', description='TESTS', user_id=0, new_test=False):
    if new_test:
       test_id = conf.tests.insert(title=test_title, description=description, user_id=user_id, filename=filename)
       return test_id
    
    with open(filename, 'r', encoding='utf-8') as file:
        lines = file.read().split('\n\n')
    
    tests=[]

    for str_test in lines:
        dict_test={
            'question' : '', 
            'answers': [],
            'true': []
        }
        test=str_test.split('\n')
        
        for i in test:
            if '#' in i[:3]: # i.startswith('#'):
              #  question_id = conf.questions.insert(question=i[1:], test_id=test_id)
                dict_test['question']=i[1:]
                #str_tests+=f"#{i}\n"
            elif '+' in  i[:3]: # i.startswith('+'):
              #  conf.answers.insert(answer = i[1:], is_true=1, test_id=test_id, question_id=question_id, user_id=user_id)
                dict_test['answers'].append(i[:])
                dict_test['true'].append(i[:])
                #str_tests+=f"+{i}\n"
            elif '-' in  i[:3]: # i.startswith('-'):
             #   conf.answers.insert(answer = i[1:], is_true=0, test_id=test_id, question_id=question_id, user_id=user_id)
                step=-1
                dict_test['answers'].append(i[1:])
                tests.append(dict_test)
                
                #str_tests+=f"-{i}\n\n"
            else:
                dict_test['answers'].append(i)
                #str_tests+=f"-{i}\n"
        r.shuffle(dict_test['answers'])
    r.shuffle(tests)
    return tests[:len_test]