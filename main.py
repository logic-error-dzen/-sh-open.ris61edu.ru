import requests, json, time
import fake_useragent as fu
from bs4 import BeautifulSoup as BS
import telebot
with open("cfg.json", "r") as read_file:
    cfg = read_file.read()
print(cfg)
cfg=eval(cfg)
TOKEN=cfg['token']
channelid=cfg['channelid']
ownernick=cfg['ownernick']
channel=cfg['channel']
print(TOKEN,channelid,ownernick,channel)
rstatus= ['administrator', 'member', 'creator']
bot = telebot.TeleBot(TOKEN)
def startbot(id):
    with open('role.json', 'r') as f:
        roleuser = f.read()
    with open('login.json', 'r') as f:
        login = f.read()

    if not str(id) in roleuser:
        with open('role.json', 'w+') as f:
            list=str(roleuser)[:-1]+", '"+str(id)+"':'"+"new"+"'}"
            list=eval(list)
            f.write(json.dumps(list))
    if not str(id) in login:
        bot.send_message(id,'Пожалуйста введите логин и пароль от дневника через команду \n/pass [логин] [пароль]\nНапример /pass МойЛогин Мой_ПаР0ль_103')

def checkpassword(id, logdt):
    with open('login.json', 'r') as f:
        login = f.read()
    try:
        logdata = {
            'login_login': logdt.split()[1],
            'login_password': logdt.split()[2]
        }
    except Exception as e:
        bot.send_message(id,
                         f'Ошибка {e}. Попробуйте еще раз')
    user = fu.UserAgent().random
    session = requests.Session()
    link = 'https://sh-open.ris61edu.ru/auth/login'
    header = {
        'user-agent': user
    }
    responce = session.post(link, data=data, headers=header)
    if responce.status_code == 200:
        if responce.json()['success']:
            bot.send_message(id,'Добавление логина и пароля прошло успешно')
            with open('login.json', 'w+') as f:
                list = str(login)[:-1] + ", '" + str(id) + "':" + str([logdt.split()[1],logdt.split()[2]]) + "}"
                list = eval(list)
                f.write(json.dumps(list))
        else:
            bot.send_message(id,'Ошибка авторизации. Проверьте логин и пароль')
    else:
        bot.send_message(id,'Ошибка на сервере. Попробуйте еще раз')
def reqmark(id, datereq):
    with open('role.json', 'r') as f:
        roleuser = f.read()
    with open('login.json', 'r') as f:
        login = f.read()
    logdata = eval(login)[str(id)]
    logdata = {
        'login_login': logdata[0],
        'login_password': logdata[1]
    }
    #bot.send_message(id, str(logdata))
    user = fu.UserAgent().random
    session = requests.Session()
    link = 'https://sh-open.ris61edu.ru/auth/login'
    testreq = ('https://sh-open.ris61edu.ru/personal-area/#marks')
    header= {
        'user-agent':user
    }
    role=eval(roleuser)[str(id)]
    sessionlog=''
    zad=5 # Задержка для на премиум пользователей, можно убрать
    if role == 'new':
        bot.send_message(id, f'Запрос отправлен. Обычно получение ответа занимает от {zad} до {zad+5} секунд. Хочешь быстрее? Напиши {ownernick}')
        time.sleep(5) # Задержка для на премиум пользователей, можно убрать
    if role == 'admin' or role == 'vip':
        bot.send_message(id, 'Запрос отправлен. Обычно получение ответа занимает до 5 секунд')
    responce = session.post(link, data=logdata, headers=header)
    #print('Статус авторизации:', responce.status_code,responce.json())

    sessionlog=sessionlog+'Код авторизации '+str(responce.status_code)+'\n'
    if responce.json()['success']:
        sessionlog = sessionlog + 'Авторизация прошла успешно ' + '\n'
    else:
        sessionlog = sessionlog + 'Не удалось авторизироваться, проверьте логин и пароль' + '\n'
    # запрос страницы оценок

    testreq_responce=session.get(testreq)
    #print('Статус запроса:',testreq_responce.status_code)
    sessionlog=sessionlog+'Код входа в дневник '+str(testreq_responce.status_code)+'\n'

    # запрос итоговых
    birth = ('https://sh-open.ris61edu.ru/api/MarkService/GetTotalMarks?date='+str(datereq))
    birth_responce=session.get(birth)
    #print(birth_responce.status_code,birth_responce.json())
    if birth_responce.status_code==200:
        with open('markstotal.json', 'w+') as f:
            f.write(json.dumps(birth_responce.json()))
    sessionlog=sessionlog+'Код запроса totalmarks '+str(birth_responce.status_code)+'\n'
    marks = ('https://sh-open.ris61edu.ru/api/MarkService/GetSummaryMarks?date='+str(datereq))
    mark_responce=session.get(marks)
    #print(mark_responce.status_code,mark_responce.json())
    sessionlog=sessionlog+'Код запроса summarymarks '+str(mark_responce.status_code)
    if birth_responce.status_code==200:
        with open('marks.json', 'w+') as f:
            f.write(json.dumps(mark_responce.json()))
    #print(birth_responce.status_code, mark_responce.json())
    if testreq_responce.status_code==200 and birth_responce.status_code==200 and mark_responce.status_code==200 and responce.status_code==200 and responce.json()['success']:
        sessionlog = sessionlog + ('\n+ Успешно +')
        noerrors=True
    else:
        sessionlog = sessionlog + ('\n- Ошибка совершения запроса -')
    #print(testreq_responce.status_code, mark_responce.json())
    bot.send_message(id, str(sessionlog)) # Статус запроса



    import re
    with open("markstotal.json", "r") as read_file:
        profiledata = json.load(read_file)
    with open("marks.json", "r") as read_file:
        marksdata = json.load(read_file)
    prfd=profiledata
    mksd=marksdata

    dsm=mksd['discipline_marks']
    marks=formatted_data = str(f"{format(dsm)}")
    mrklst=re.findall(r"'([^']*)'", marks)

    ind=prfd['discipline_marks']
    profile=formatted_data = str(f"{format(ind)}")
    prflst=re.findall(r"'([^']*)'", profile)

    #print(mrklst)
    #print(prflst)
    ### ТЕКУЩИИ ОЦЕНКИ
    plst=[]
    mlst_predm='{'
    mlst_time=[]
    predlst=[]
    date=[] # дата
    mark=[] # оценка
    desc=[] # описание
    aver=[] # среднее
    for i in range(len(mrklst)):
        if mrklst[i] == 'discipline':
            date = []  # дата
            mark = []  # оценка
            desc = []  # описание
            aver = []  # среднее
            predmet=mrklst[i+1]
            predlst.append(predmet)
        elif mrklst[i] == 'date':
            date.append(mrklst[i+1])
        elif mrklst[i] == 'mark':
            mark.append(mrklst[i+1])
        elif mrklst[i] == 'description':
            desc.append(mrklst[i+1])
        elif mrklst[i] == 'average_mark':
            aver.append(mrklst[i+1])
            mlst_predm= mlst_predm+"'"+str(predmet+"'"+str(':')+str([aver, date, mark, desc])+', ')
    mlst_predm= mlst_predm+'}'
    printmarksbydiscipl=[]
    totalmarks=[]
    #{'Предмет1':[[4.82],['01-01-1000','02-01-1000','03-01-1000'],['5','2','4'],['Описание','desr2', 'desc3']}
    #print(mlst_predm)
    # перевод в привычный вид
    for i in range(len(predlst)):
        marki=eval(mlst_predm)[predlst[i]]
        for i2 in range(len(marki[1])):
            totalmarks.append(marki[2][i2])
    for i in range(len(predlst)):
        marki=eval(mlst_predm)[predlst[i]]
        printmarksbydiscipl.append('*** '+str(predlst[i])+str(' ')+marki[0][0]+' = '+str(len(marki[2]))+' оценок')
        for i2 in range(len(marki[1])):
            if str(marki[3][i2]) != 'Работа на уроке: нет темы':
                temp=' ('+str(marki[3][i2])+')'
            else:
                temp=''
            printmarksbydiscipl.append(str(marki[1][i2])+' = '+str(marki[2][i2])+temp)
    tgout=''
    for i in printmarksbydiscipl:
        tgout = tgout+i+'\n'
    ### Отправка текущих оценок
    tmks='Всего '+str(len(totalmarks))+' оценок\n'
    for i in range(len(totalmarks)):
        tmks=tmks+' '+str(totalmarks[i])
        if i%20==19:
            tmks=tmks+'\n'
    if noerrors:
        bot.send_message(id, str(tmks))
        for i in range(len(tgout.split('***'))-1):
            bot.send_message(id, str(tgout.split('***')[i+1]))

        ### Итоговые
        chetmarks = []
        chmrk1 = []
        for i in range(len(prflst)):
            if prflst[i] == 'discipline':
                chetmarks.append(chmrk1)
                chmrk1 = []
                chmrk1.append(prflst[i + 1])
            if prflst[i] in ['mark']:
                chmrk1.append(prflst[i + 1])
        pr = ''
        pri = ''
        for i in range(len(chetmarks)):
            for i2 in range(len(chetmarks[i])):
                pr = pr + ' ' + chetmarks[i][i2]
            pri = pri + pr + '\n'
            pr = ''
        bot.send_message(id, pri)

@bot.message_handler(commands=['start'])
def start(message):
    startbot(message.from_user.id)
@bot.message_handler(commands=['zap'])
def requestmarks(message):
    global rstatus
    if bot.get_chat_member(channelid, message.from_user.id).status in rstatus:
        try:
            if len(message.text.split()[1])==10:
                a = message.text.split()[1]
                try:
                    year = int(a[0:4])
                    if i[5] == '0':
                        month = int(a[6:7])
                        month = a[5:7]
                    else:
                        month = int(a[5:7])
                    if i[8]=='0':
                        day = int(a[9:10])
                        day = a[8:10]
                    else:
                        day = int(a[8:10])
                    date = f'{year}-{month}-{day}'
                except Exception as e:
                    #bot.send_message(message.from_user.id, 'Ошибка ввода даты, будет отправлен запрос с сегодняшней датой')
                    date='2024-12-12'

            reqmark(message.from_user.id, date)
        except Exception as e:
            #bot.send_message(message.from_user.id, f'Ошибка {e}')
            date = '2024-12-12'
            reqmark(message.from_user.id, date)
    else:
        bot.send_message(message.from_user.id, f'Подпишись {channel}')
@bot.message_handler(commands=['pass'])
def check(message):
    checkpassword(message.from_user.id, message.text)
#https://sh-open.ris61edu.ru/api/MarkService/GetSummaryMarks?date=2024-05-18
#https://sh-open.ris61edu.ru/static/personal_area/js/vendor/sferum/auth_script.js
bot.polling(non_stop=True, interval=0)