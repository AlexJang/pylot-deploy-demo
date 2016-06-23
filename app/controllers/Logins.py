"""
    Sample Controller File

    A Controller should be in charge of responding to a request.
    Load models to interact with the database and load views to render them to the client.

    Create a controller using this template
"""
from system.core.controller import *
from flask import Flask, redirect, render_template, session, request

class Logins(Controller):
    def __init__(self, action):
        super(Logins, self).__init__(action)
        """
        This is an example of loading a model.
        Every controller has access to the load_model method.
        """
        self.load_model('Login')
        self.db = self._app.db

        """
        
        This is an example of a controller method that will load a view for the client 

        """
   
    def index(self):
        """
        A loaded model is accessible through the models attribute 
        self.models['WelcomeModel'].get_users()
        
        self.models['WelcomeModel'].add_message()
        # messages = self.models['WelcomeModel'].grab_messages()
        # user = self.models['WelcomeModel'].get_user()
        # to pass information on to a view it's the same as it was with Flask
        
        # return self.load_view('index.html', messages=messages, user=user)
        """

        return self.load_view('/logins/login.html')

    def register(self):
        register_user = {
            'first_name': request.form['f_name'],
            'last_name': request.form['l_name'],
            'email': request.form['email'],
            'pw': request.form['pw'],
            'con_pw': request.form['confirm_pw']
        }

        values = self.models['Login'].add_new_user(register_user)

        if values['status'] == True:
            session['status'] = 'Registered'
            session['first_name'] = request.form['f_name']

            return redirect('/logins/success')
        else:

            for errors in values['errors']:
                print errors
            return redirect('/')


    def login(self):
        login_user = {
            'email': request.form['email'],
            'pw': request.form['pw']
        }

        login = self.models['Login'].find_user(login_user)

        if login['login_status'] == True:
            session['status'] = 'Login'
            session['first_name'] = login['user']
            return redirect('/logins/success')
        else:
            print login['error']
            return redirect('/')

    def success(self):
        return self.load_view('/logins/success.html', first_name=session['first_name'], status=session['status'])

    def back(self):
        return redirect('/')