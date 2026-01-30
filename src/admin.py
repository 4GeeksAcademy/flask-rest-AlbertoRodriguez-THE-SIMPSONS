import os
from flask_admin import Admin
from models import db, User, Character, Locations
from flask_admin.contrib.sqla import ModelView

def setup_admin(app):
    app.secret_key = os.environ.get('FLASK_APP_KEY', 'sample key')
    app.config['FLASK_ADMIN_SWATCH'] = 'cerulean'
    admin = Admin(app, name='4Geeks Admin', template_mode='bootstrap3')

    class UserAdmin(ModelView):
        form_columns = ["email","password", "favorites","favorite_locations"]


    
    # Add your models here, for example this is how we add a the User model to the admin

    admin.add_view(UserAdmin(User, db.session))
    admin.add_view(ModelView(Character, db.session))
    admin.add_view(ModelView(Locations, db.session))

    # You can duplicate that line to add mew models
    # admin.add_view(ModelView(YourModelName, db.session))