from flask_app.models import register
from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash, request


class Review:

    db = "thriftelmore_schema"

    def __init__(self, db_data):
        self.id = db_data['id']
        self.review = db_data['review']
        self.image = db_data['image']
        self.created_at = db_data['created_at']
        self.updated_at = db_data['updated_at']

        self.reviewed_items = []

    # SAVE REVIEW FROM USER
    @classmethod
    def save_review(cls, data):
        query = """
        INSERT INTO reviews (review, image, created_at, updated_at, user_id, item_id)
        VALUES (%(review)s, %(image)s, NOW(), NOW(), %(user_id)s, %(item_id)s);
        """

        results = connectToMySQL(cls.db).query_db(query, data)

        return results

    # GET ITEMS WITH REVIEWS
    @classmethod
    def get_reviewed_items(cls, data):
        query = "SELECT * FROM items JOIN reviews ON items.id = reviews.item_id WHERE items.id = %(id)s;"

        results = connectToMySQL(cls.db).query_db(query, data)

        review = cls(results[0])

        for row in results:
            item_data = {
                "id": row['items.id'],
                "item_name": row['item_name'],
                "item_type": row['item_type'],
                "item_description": row['item_description'],
                "item_price": row['item_price'],
                "item_picture": row['item_picture'],
                "created_at": row['items.created_at'],
                "updated_at": row['items.updated_at'],
                "user_id": row['user_id']
            }
            review.reviewed_items.append(register.Items(item_data))

        return review

    # GET USER WITH THEIR REVIEWS
    @classmethod
    def get_user_with_reviews(cls, data):
        query = "SELECT * FROM users JOIN reviews ON users.id = reviews.user_id WHERE users.id = %(id)s;"

        results = connectToMySQL(cls.db).query_db(query, data)

        review = cls(results[0])

        for row in results:
            user_data = {
                "id": row['users.id'],
                "first_name": row['first_name'],
                "last_name": row['last_name'],
                "email": row['email'],
                "date_of_birth": row['date_of_birth'],
                "username": row['username'],
                "password": row['password'],
                "created_at": row['users.created_at'],
                "updated_at": row['users.updated_at']
            }
            review.reviewed_items.append(register.User(user_data))

        return review

    # UPDATE REVIEW
    @classmethod
    def update_review(cls, data):
        query = """
        UPDATE reviews SET review = %(review)s, image = %(image)s, updated_at = NOW()
        WHERE id = %(id)s;
        """

        results = connectToMySQL(cls.db).query_db(query, data)

        return results

    # DELETE REVIEW
    @classmethod
    def delete_review(cls, data):
        query = "DELETE FROM reviews WHERE id = %(id)s;"

        results = connectToMySQL(cls.db).query_db(query, data)

        return results

    # VALIDATE REVIEW
    @staticmethod
    def validate_review(data):
        is_valid = True

        if len(data['review']) < 1:
            flash("Review cannot be empty.")
            is_valid = False

        if len(data['image']) < 1:
            flash("Image cannot be empty.")
            is_valid = False

        return is_valid
