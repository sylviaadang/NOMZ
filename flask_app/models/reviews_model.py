from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app.models import users_model
from flask_app.models import restaurants_model


class Review:
    DB = 'yelp_schema'

    def __init__(self,data):
        self.id = data['id']
        self.stars = data['stars']
        self.comment = data['comment']
        self.created_at = data['created_at']
        self.udpated_at = data['updated_at']
        self.user_id = data['user_id']
        self.restaurant_id = data['restaurant_id']
        self.poster = None


    @staticmethod
    def validate_review(new_review):
        is_valid = True
        if 'stars' not in new_review:
            flash('Rating is required')
            is_valid = False
        if len(new_review['comment']) < 11:
            flash('Comments must be at least 10 characters')
            is_valid = False

        return is_valid

    @classmethod
    def create_review(cls, data):
        query = """
        INSERT INTO reviews ( stars, comment, restaurant_id, user_id)
        VALUES (%(stars)s, %(comment)s, %(restaurant_id)s, %(user_id)s);
        """
        result = connectToMySQL(cls.DB).query_db(query, data)
        return result

    @classmethod
    def get_all_reviews(cls):
        query = """
        SELECT * FROM reviews
        JOIN restaurants ON restaurants.id = reviews.restaurant_id
        JOIN users ON users.id = reviews.user_id
        """

        result = connectToMySQL(cls.DB).query_db(query)

        all_reviews = []

        for row in result:

            restaurant_data = {
                'id' : row['user_id'],
                'name' : row['name'],
                'city' : row['city'],
                'zipcode' : row['zipcode'],
                'reviews' : row['reviews'],
                'image' : row['image'],
                'phone_number' : row['phone_number'],
                'cuisine' : row['cuisine'],
                'created_at' : row['users.created_at'],
                'updated_at' : row['users.updated_at']
            }

            one_review = cls(row)
            one_review.review_post = restaurants_model.Restaurant(restaurant_data)
            all_reviews.append(one_review)

        return all_reviews

    @classmethod
    def get_one_review(cls,data):
        query = """
        SELECT * FROM reviews
        JOIN restaurants ON restaurants.id = reviews.restaurant_id
        WHERE reviews.id = %(reviews_id)s;
        """

        result = connectToMySQL(cls.DB).query_db(query, data)

        one_review = cls(result[0])

        restaurant_data = {
                'id' : result[0]['restaurant_id'],
                'restaurant_name' : result[0]['restaurant_name'],
                'stars' : result[0]['stars'],
                'text' : result[0]['text'],
                'created_at' : result[0]['users.created_at'],
                'updated_at' : result[0]['users.updated_at']
            }

        one_review.review_post = restaurants_model.Restaurant(restaurant_data)


        return one_review

    # @classmethod
    # def update_recipe(cls,data):
    #     query = """
    #     UPDATE recipes
    #     SET name = %(name)s,
    #     description = %(description)s,
    #     instructions = %(instructions)s,
    #     date = %(date)s,
    #     minutes = %(minutes)s
    #     WHERE id = %(recipe_id)s;
    #     """

    #     return connectToMySQL(cls.DB).query_db(query, data)



# This will only be applicable to those who are logged into their account and can only delete reviews theyve written
    @classmethod
    def delete_review(cls,data):
        query = """
        DELETE FROM reviews
        WHERE id = %(review_id)s;
        """

        return connectToMySQL(cls.DB).query_db(query, data)
