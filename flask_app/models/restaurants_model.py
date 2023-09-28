from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app.models import users_model
from flask_app.models import reviews_model


class Restaurant:
    DB = 'yelp_schema'

    def __init__(self,data):
        self.id = data['id']
        self.name = data['name']
        self.city = data['city']
        self.zipcode = data['zipcode']
        self.reviews = data['reviews']
        self.image = data['image']
        self.phone_number = data['phone_number']
        self.cuisine = data['cuisine']
        self.created_at = data['created_at']
        self.udpated_at = data['updated_at']
        self.reviews = []


    @staticmethod
    def validate_restaurant(new_restaurant):
        is_valid = True
        if len(new_restaurant['name']) < 0:
            flash('Name must be at least 1 characters')
            is_valid = False
        if len(new_restaurant['city']) < 4:
            flash('City must be at least 3 characters')
            is_valid = False
        if len(new_restaurant['zipcode']) < 6:
            flash('Zipcode must be at least 5 characters')
            is_valid = False
        if len(new_restaurant['phone_number']) < 11:
            flash('Phone number must be at least 10 characters')
            is_valid = False
        if len(new_restaurant['cuisine']) < 4:
            flash('Cuisine must be at least 3 characters')
            is_valid = False

        return is_valid

    # @classmethod
    # def create_restaurant(cls, data):
    #     query = """
    #     INSERT INTO restaurants (name, city, zipcode, image, phone_number, cuisine)
    #     VALUES (%(name)s, %(city)s, %(zipcode)s, %(image)s, %(phone_number)s, %(cuisine)s);
    #     """
    #     result = connectToMySQL(cls.DB).query_db(query, data)
    #     return result

    # @classmethod
    # def get_all_restaurants(cls):
    #     query = """
    #     SELECT * FROM restaurants
    #     # JOIN users ON users.id = paintings.user_id;
    #     """

    #     result = connectToMySQL(cls.DB).query_db(query)

    #     all_paintings = []

    #     for row in result:

    #         user_data = {
    #             'id' : row['user_id'],
    #             'first_name' : row['first_name'],
    #             'last_name' : row['last_name'],
    #             'email' : row['email'],
    #             'password' : row['password'],
    #             'created_at' : row['users.created_at'],
    #             'updated_at' : row['users.updated_at']
    #         }

    #         one_painting = cls(row)
    #         one_painting.painting_poster = users_model.User(user_data)
    #         all_paintings.append(one_painting)

    #     return all_paintings

    @classmethod
    def get_one_restaurant(cls,data):
        query = """
        SELECT * FROM restaurants
        LEFT JOIN reviews ON restaurants.id = reviews.restaurant_id
        LEFT JOIN users ON users.id = reviews.user_id
        WHERE restaurants.id = %(restaurant_id)s;
        """

        result = connectToMySQL(cls.DB).query_db(query, data)
        print(result)
        one_restaurant = cls(result[0])

        for i in result:
            review_data = {
                **i,
                'id' : i['reviews.id'],
                'created_at' : i['reviews.created_at'],
                'updated_at' : i['reviews.updated_at']
                }

            user_data = {
                **i,
                'id' : i['users.id'],
                'created_at' : i['users.created_at'],
                'updated_at' : i['users.updated_at']
            }

            one_review = reviews_model.Review(review_data)
            one_review.poster = users_model.User(user_data)

            one_restaurant.reviews.append(one_review)

        return one_restaurant

    # @classmethod
    # def update_painting(cls,data):
    #     query = """
    #     UPDATE paintings
    #     SET name = %(name)s,
    #     description = %(description)s,
    #     price = %(price)s
    #     WHERE id = %(painting_id)s;
    #     """

    #     return connectToMySQL(cls.DB).query_db(query, data)


    # @classmethod
    # def delete_painting(cls,data):
    #     query = """
    #     DELETE FROM paintings
    #     WHERE id = %(painting_id)s;
    #     """

    #     return connectToMySQL(cls.DB).query_db(query, data)

    @classmethod
    def get_all_restaurants(cls):
        query = """
        SELECT * FROM restaurants LIMIT 15
        """

        result = connectToMySQL(cls.DB).query_db(query)

        restaurants = []

        for i in result:
            restaurants.append(cls(i))

        return restaurants
