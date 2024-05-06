class Config:
    # Configuraciones base
    SECRET_KEY = 'mira_esta_clave_toda_dificil'
    # Configuraciones comunes que podrían ser extendidas o sobreescritas por configuraciones específicas

class ConfigDesarrollo(Config):
    #Configuraciones específicas para el entorno de desarrollo
    DEBUG = True
    #Configuraciones para bd
    MYSQL_HOST = 'localhost'
    MYSQL_USER = 'root'
    MYSQL_PASSWORD = ''
    MYSQL_DB = 'bgdestacionamiento'