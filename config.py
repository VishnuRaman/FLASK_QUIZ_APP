class BaseConfig(object):
    DEBUG = False
    SECRET_KEY = 'YOUR_SECRET_KEY'
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:Arsenal920531@localhost:5432/postgres2'
    WTF_CSRF_SECRET_KEY = 'SECRET_KEY'

class DevelopmentConfig(BaseConfig):
    DEBUG = True
    TESTING = True #makes login_required decorator get ignored

class ProductionConfig(BaseConfig):
    DEBUG = False
    TESTING = False