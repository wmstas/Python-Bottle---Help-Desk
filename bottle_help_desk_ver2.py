# Требуется: база данных sqlite:  create table main (id INTEGER PRIMARY KEY, Name text, Desc text);
# а также: CREATE TABLE "comments" (
#    "main_id"   INTEGER NOT NULL,
#    "id_com"    INTEGER NOT NULL UNIQUE,
#    "comment"   TEXT,
#    FOREIGN KEY("main_id") REFERENCES "main"("id"),
#    PRIMARY KEY("id_com")
#);

from bottle import get, post, run, template, request, install
from bottle_sqlite import SQLitePlugin

install(SQLitePlugin(dbfile='helpdb.db'))

############################ (+) ШАБЛОН ДЛЯ ВЫВОДА ВСЕХ СТРАНИЦ
def outTemplate(head,body):
    htmlText = '''<!DOCTYPE HTML>
                <html>
                <head>
                    <title>HELP DESK: '''+head+'''</title>
                    <style type="text/css">
                        html {background-color: #eee; font-family: sans;}
                        body {background-color: #fff; border: 1px solid #ddd; padding: 15px; margin: 15px;}
                        pre {background-color: #eee; border: 1px solid #ddd; padding: 5px;}
                        H1 {background-color: #99FFCC; border: 1px solid #ddd; padding: 2px;}
                    </style>
                </head>
                <body>
                <H1><a href="/">Help Desk</a>: '''+head+'''</H1>
                <p align="right"><a href="/new_task"> добавить новую задачу</a></p>
                '''+body+'''
                </body>
                </html>'''
    return htmlText

@post('/testpost')
def test1():
    print('testpost request')
    return "Post11"
@get('/testget')
def test1():
    return "get222"

############################ (-) ПОКАЗ ЗАДАЧИ
@get('/task/<taskId>')
def showtask(db,taskId):
    
    # ------------------ вывод самойзадачи
    res=''
    task = db.execute('SELECT * from main where id = '+taskId).fetchone()
    res+= '<p><h7>Номер задачи: '+str(task[0])+'</h7></p>'
    res+= '<p><h7>Наименование задачи: '+task[1]+'</h7></p>'
    res+= '<p>Описание задачи:</p><p><pre>'+task[2]+'</pre></p>'
    
    # ------------------ вывод комментариев
    comments = db.execute('SELECT comment from comments where main_id = '+taskId).fetchall()
    res+= '<p>&nbsp;</p>'
    res+= '<table style="border-collapse: collapse; width: 100%;" border="1"><tbody>'
    for c in comments:
        res+= '<tr><td>'+c[0]+'</td></tr>'
    res+= '</tbody></table><p>&nbsp;</p>'
    
    # ------------------ вывод формы добавления задачи
    res+= '''
        <form action="/add_comment" method="post">
        <input type="hidden" name="main_id" value="'''
    res+=taskId
    res+='''">
            <p>Комментарий: <textarea name="comment"></textarea><br></p>
            <input value="Добавить комментарий" type="submit" />
            </form>'''    

    return outTemplate('Просмотр задачи '+taskId, res)

############################ (+) ЗАПИСЬ ЗАДАЧИ В БАЗУ
@post('/add_comment')
def newTaskToDB(db):
    main_id = request.forms.main_id
    comment = request.forms.comment
    dbcommand = 'insert into comments values('+main_id+',null,"'+comment+'")'
    db.execute(dbcommand)
    return showtask(db,main_id)

############################ (+) ВЫВОД ФОРМЫ ДЛЯ ДОБАВЛЕНИЯ ЗАДАЧИ
@get('/new_task')
def newTaskForm():
    res = '''
        <form action="/new_task" method="post">
            <p>Название задачи: <input name="name" type="text" /></p>
            <p>Полное описание: <textarea name="desc"></textarea><br></p>
            <input value="Добавить задачу" type="submit" />
        </form>'''
    return outTemplate('Добавление новой задачи', res)


############################ (+) ЗАПИСЬ ЗАДАЧИ В БАЗУ
@post('/new_task')
def newTaskToDB(db):
    name = request.forms.name
    desc = request.forms.desc
    #adr = str(request["REMOTE_ADDR"]
    dbcommand = 'insert into main values(null,"'+name+'","'+desc+'")'
    db.execute(dbcommand)
    return outTemplate('Добавление новой задачи', 'задача добавлена: '+name)

############################ (+) ГЛАВНАЯ СТРАНИЦА, СПИСОК ЗАДАЧ
@get('/')
def index(db):
    select1 = db.execute('SELECT * from main order by id desc')
    res=''
    rows = select1.fetchall()
    for row in rows:
        res+='<p> #'+str(row[0])+' <a href="/task/'+str(row[0])+'"> '+row[1]+'</a></p>'
    return outTemplate("Список задач",str(res))

############################ (+) ФОРМА ДЛЯ ЛОГИНА, НЕ ИСПОЛЬЗУЕТСЯ, ОСТАВЛЕНА ДЛЯ БУДУЩЕГО
@get('/login')
def login():
    return '''
        <form action="/login" method="post">
            Username: <input name="username" type="text" />
            Password: <input name="password" type="password" />
            <input value="Login" type="submit" />
        </form>
    '''
############################ (+) ОСУЩЕСТВЛЕНИЕ ЛОГИНА, НЕ ИСПОЛЬЗУЕТСЯ, ОСТАВЛЕНО ДЛЯ БУДУЩЕГО
@post('/login', method='POST')
def do_login():
    username = request.forms.get('username')
    password = request.forms.get('password')
    if check_login(username, password):
        return "<p>Your login information was correct.</p>"
    else:
        return "<p>Login failed.</p>"

def check_login(username,password):
    return True


############################ (+) ЗАПУСК СЕРВЕРА HTTP (ОСНОВНАЯ ПРОЦЕДУРА)

run(host='localhost', port=80)
#run(host='192.168.1.35', port=80)