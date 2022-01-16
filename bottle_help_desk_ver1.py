# Требуется: база данных sqlite:  create table main (id INTEGER PRIMARY KEY, Name text, Desc text);
from bottle import get, post, run, template, request, install
from bottle_sqlite import SQLitePlugin

install(SQLitePlugin(dbfile='helpdb.db'))

############################ (+) Template for page
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

############################ (-) SHOW TOPIC
@get('/task/<taskId>')
def showtask(db,taskId):
    res=''
    task = db.execute('SELECT * from main where id = '+taskId).fetchone()
    res+= '<p><h7>Номер задачи: '+str(task[0])+'</h7></p>'
    res+= '<p><h7>Наименование задачи: '+task[1]+'</h7></p>'
    res+= '<p>Описание задачи:</p><p><pre>'+task[2]+'</pre></p>'
    #return template('<b>View task {{taskId}}</b>!', taskId=taskId)
    return outTemplate('Просмотр задачи '+taskId, res)

############################ (+) ADD TASK FORM
@get('/new_task')
def newTaskForm():
    res = '''
        <form action="/new_task" method="post">
            <p>Название задачи: <input name="name" type="text" /></p>
            <p>Полное описание: <textarea name="desc"></textarea><br></p>
            <input value="Добавить задачу" type="submit" />
        </form>'''
    return outTemplate('Добавление новой задачи', res)


############################ (+) ADD TASK TO DB
@post('/new_task')
def newTaskToDB(db):
    name = request.forms.name
    desc = request.forms.desc
    #adr = str(request["REMOTE_ADDR"]
    dbcommand = 'insert into main values(null,"'+name+'","'+desc+'")'
    db.execute(dbcommand)
    return outTemplate('Добавление новой задачи', 'задача добавлена: '+name)

############################ (+) MAIN PAGE
@get('/')
def index(db):
    select1 = db.execute('SELECT * from main order by id desc')
    res=''
    rows = select1.fetchall()
    for row in rows:
        res+='<p> #'+str(row[0])+' <a href="/task/'+str(row[0])+'"> '+row[1]+'</a></p>'
    return outTemplate("Список задач",str(res))

############################ (+) LOGIN GET FORM // not used, for future
@get('/login')
def login():
    return '''
        <form action="/login" method="post">
            Username: <input name="username" type="text" />
            Password: <input name="password" type="password" />
            <input value="Login" type="submit" />
        </form>
    '''
############################ (+) LOGIN POST ACTION // not used, for future
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


############################ (+) MAIN

run(host='localhost', port=80)
#run(host='192.168.1.35', port=80)