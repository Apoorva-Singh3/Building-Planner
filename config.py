class Config:
    SQLALCHEMY_DATABASE_URI = 'postgresql://root:root@localhost/buildingplannerdb'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class TestingConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///test.db'
    TESTING = True
