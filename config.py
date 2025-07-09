class Config:
    SECRET_KEY = 'your-secret-key'  # Change this in production
    SQLALCHEMY_DATABASE_URI = 'sqlite:///tourizo.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
