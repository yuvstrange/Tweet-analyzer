from tinydb import TinyDB, Query

def signup(username,email,password):
    db = TinyDB('db.json')
    User = Query()
    res = db.search(User.username==username)
    if len(res)==1:
        return 'Already exists'
    
    db.insert({'username':username,'email':email,'password':password})
    return 'success'

def check(username,password):
    db = TinyDB('db.json')
    User = Query()
    res = db.search((User.username == username) & (User.password == password))
    if len(res)==1:
        return 'success'
    return res