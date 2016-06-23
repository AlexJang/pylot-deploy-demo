""" 
    Sample Model File

    A Model should be in charge of communicating with the Database. 
    Define specific model method that query the database for information.
    Then call upon these model method in your controller.

    Create a model using this template.
"""
from system.core.model import Model
import  re

class Login(Model):
    def __init__(self):
        super(Login, self).__init__()
    """
    Below is an example of a model method that queries the database for all users in a fictitious application
    
    Every model has access to the "self.db.query_db" method which allows you to interact with the database

    def get_users(self):
        query = "SELECT * from users"
        return self.db.query_db(query)

    def get_user(self):
        query = "SELECT * from users where id = :id"
        data = {'id': 1}
        return self.db.get_one(query, data)

    def add_message(self):
        sql = "INSERT into messages (message, created_at, users_id) values(:message, NOW(), :users_id)"
        data = {'message': 'awesome bro', 'users_id': 1}
        self.db.query_db(sql, data)
        return True
    
    def grab_messages(self):
        query = "SELECT * from messages where users_id = :user_id"
        data = {'user_id':1}
        return self.db.query_db(query, data)

    """

    # def check_for_email(self, new_email):
    #     query = 'select email from users'
    #
    #
    #     self.db.query_db(query, data)



    def add_new_user(self, new_user):
        NAME_REGEX = re.compile(r'^[a-zA-Z]*$')
        EMAIL_REGEX = re.compile(r'^[a-za-z0-9\.\+_-]+@[a-za-z0-9\._-]+\.[a-za-z]*$')
        errors = []

        query = 'SELECT email FROM users'

        emails = self.db.query_db(query)

        for email in emails:
            for value in email.values():
                if new_user['email'] == value:
                    errors.append('email already exists!')
                    break
                break

        if len(new_user['first_name']) < 2 or len(new_user['last_name']) < 2:
            errors.append('Name must be longer that 2 characters')
        elif not NAME_REGEX.match(new_user['first_name']) or not NAME_REGEX.match(new_user['last_name']):
            errors.append('Name must only have letters')

        if not EMAIL_REGEX.match(new_user['email']):
            errors.append('email entered is incorrect')

        if len(new_user['pw']) < 8:
            errors.append('password must be longer than 8 character')
        elif new_user['pw'] != new_user['con_pw']:
            errors.append('passwords do not match')

        if errors:
            return {'status': False, 'errors': errors}

        else:
            query = 'INSERT INTO users (first_name, last_name, email, pw_hash, created_at, updated_at) ' \
                    'VALUES (:first_name, :last_name, :email, :pw_hash, NOW(), NOW())'

            password = new_user['pw']
            hash_pw = self.bcrypt.generate_password_hash(password)

            data = {
                'first_name': new_user['first_name'],
                'last_name': new_user['last_name'],
                'email': new_user['email'],
                'pw_hash': hash_pw
            }

            self.db.query_db(query, data)

            return {'status': True}


    def find_user(self, search_user):

        query = 'SELECT * FROM users where email = :email LIMIT 1'

        data = {
            'email': search_user['email']
        }

        user = self.db.query_db(query, data)

        if self.bcrypt.check_password_hash(user[0]['pw_hash'], search_user['pw']):
            return { 'login_status': True, 'user': user[0]['first_name']}
        else:
            error = 'Passwords do not match'
            return {'login_status': False, 'error': error}




























