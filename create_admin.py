from app import create_app
from app.extensions import db
from app.models.User import User

app = create_app()
with app.app_context():
    user = User(
        username="Shakiran",
        email="devkiran256@gmail.com",
        is_admin=True,
        first_name="Shakiran",
        last_name="Nannyombi"
    )
    user.set_password("lockedaway")
    db.session.add(user)
    db.session.commit()
    print("Admin user created:", user)
