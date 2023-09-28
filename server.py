from flask_app import app


from flask_app.controllers import users_controller, restaurants_controller, reviews_controller

if __name__ == '__main__':
    app.run(debug=True)
