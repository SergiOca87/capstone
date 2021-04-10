Why you believe your project satisfies the distinctiveness and complexity requirements, mentioned above.

-   My project uses both Django and Javascript and the core concepts teached on this course, to enumerate some, I've covered the such the creation of different models with different kinds of fields, which are not only simple text fields but more complex ones like image or date fields and some functionalities not covered in the course as well.

The app also has several relations between models and interactions with the database for the creation of users, projects and phases that are added to those projects.

There's also routing, editing, and conditional rendering of different parts of the application covering different case scenarios where for example a user should only view data if they are logged in.

Finally, the usage of Javascript is used to make those interactions witht he app, more attractive to the user by using mostly the fetch API to prevent page reloads in order to interact with our database.

What’s contained in each file you created.

-   On the templates folder we can find the different templates used on this app.
    On the admin.py file we can find the models that have been registered for the app.
    On models.py, the definition of the models used on the app.
    ON urls.py the definition of the routes.
    And finally on views.py, the logic for rendering the different views.

How to run your application.

-   My app can be run by running the "python manage.py runserver" command.
