from app.extensions import db

class ChatbotSettings(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    groq_api_key = db.Column(db.String(128), nullable=False)
    groq_model = db.Column(db.String(64), nullable=False)

    @staticmethod
    def get_settings():
        # Always return the first row (singleton pattern)
        return ChatbotSettings.query.first()
