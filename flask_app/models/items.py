from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash, request
from flask_app.models import register, reviews
from datetime import datetime

# Creating an Items Class


class Items:
    db = "thriftelmore_schema"

    # Constructor
    def __init__(self, data):
        self.id = data['id']
        self.item_name = data['item_name']
        self.item_type = data['item_type']
        self.item_description = data['item_description']
        self.item_price = data['item_price']
        self.item_picture = data['item_picture']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user_id = data['user_id']

        self.creator = None
        self.reviews = []
        self.user = None

    # GET ITEMS WITH REVIEWS
    @classmethod
    def get_items_with_reviews(cls, data):
        query = "SELECT * FROM items LEFT JOIN reviews ON items.id = reviews.item_id WHERE items.id = %(id)s;"
        results = connectToMySQL(cls.db).query_db(query, data)

        item = cls(results[0])
        for row_from_db in results:

            review_data = {
                "id": row_from_db['reviews.id'],
                "review": row_from_db['review'],
                "image": row_from_db['image'],
                "created_at": row_from_db['reviews.created_at'],
                "updated_at": row_from_db['reviews.updated_at'],
                "item_id": row_from_db['item_id']
            }
            item.reviews.append(reviews.Review(review_data))

        return item

    # GET ALL ITEMS
    @classmethod
    def get_all_items(cls):
        query = "SELECT * FROM items;"
        results = connectToMySQL(cls.db).query_db(query)

        items = []
        for row in results:
            items.append(cls(row))
        return items

    # GET ALL ITEMS BY USER
    @classmethod
    def get_all_items_by_user(cls, data):
        query = "SELECT * FROM items WHERE user_id = %(id)s;"
        results = connectToMySQL(cls.db).query_db(query, data)

        items = []
        for row in results:
            items.append(cls(row))
        return items

    # GET ITEM BY ID

    @classmethod
    def get_item_by_id(cls, data):
        query = "SELECT * FROM items WHERE id = %(id)s;"
        results = connectToMySQL(cls.db).query_db(query, data)

        return cls(results[0])

    # SAVE ITEM
    @classmethod
    def save_item(cls, data):
        query = """
        INSERT INTO items (item_name, item_type, item_description, item_price, item_picture, created_at, updated_at, user_id)
        VALUES (%(item_name)s, %(item_type)s, %(item_description)s, %(item_price)s, %(item_picture)s, NOW(), NOW(), %(user_id)s);
        """
        results = connectToMySQL(cls.db).query_db(query, data)
        return results

    # UPDATE ITEM
    @classmethod
    def update_item(cls, data):
        query = """
        UPDATE items SET item_name = %(item_name)s, item_type = %(item_type)s, item_description = %(item_description)s, 
        item_price = %(item_price)s, item_picture = %(item_picture)s, updated_at = NOW() 
        WHERE id = %(id)s;
        """
        results = connectToMySQL(cls.db).query_db(query, data)
        return results

    # DELETE ITEM
    @classmethod
    def delete_item(cls, data):
        query = "DELETE FROM items WHERE id = %(id)s;"
        results = connectToMySQL(cls.db).query_db(query, data)
        return results

    # VALIDATE ITEM
    @staticmethod
    def validate_item(data):
        is_valid = True

        # Item Name
        if len(data['item_name']) < 3:
            flash("Item name must be at least 3 characters.")
            is_valid = False

        # Item Type
        if len(data['item_type']) < 3:
            flash("Item type must be at least 3 characters.")
            is_valid = False

        # Item Description
        if len(data['item_description']) < 3:
            flash("Item description must be at least 3 characters.")
            is_valid = False

        # Item Price
        if len(data['item_price']) < 1:
            flash("Item price must be at least 1 character.")
            is_valid = False

        # Item Picture
        if len(data['item_picture']) < 1:
            flash("Item picture must be at least 1 character.")
            is_valid = False

        return is_valid
