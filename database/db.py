from flask_mysqldb import MySQL    

def conectar_bd():
    try:
        return MySQL().connect
    except Exception as ex:
        print(ex)