# Auctions Galaxy
An online bidding website.

## Screenshot
![Auctions demonstration screeshot](https://github.com/prasanna-lakshmi18/Auctions/blob/main/image.png)

## Files & Directories

- `**Commerce**` - project directory.
- `**utils.py**` - Contains all Django helper functions used in views.py.
- `**urls.py**` - This file handles all the URLs of the project.
- `**auctions**` - main application directory.
- `**static**` - contains all static content.
- `**templates/auctions**` - Contains all application templates.
  - `**All_listings.html**` - Template for showing all the items.
  - `**category.html**` - Template for showing all the categories of projects under a category.
  - `**index.html**` - Home page template.
  - `**layout.html**` - Base template for all pages except login & register page.
  - `**login.html**` - Login user page.
  - `**Create_User.html**` - Page for adding a new item by the user.
  - `**Product.html**` - Product page.
  - `**register.html**` - Register user page.
  - `**watchlist.html**` - Template for showing all the items added for watchlist.
- `**admin.py**` - Contains some models for access to the Django administrator.
- `**models.py**` - All models used in the application are created here.
- `**urls.py**` - This file handles all the URLs of the web application.
- `**views.py**` - This file contains all the application views.
- `**manage.py**` - This file is used basically as a command-line utility and for deploying, debugging, or running our web application.

## Installation
- Install `Python3.9` from [here](https://www.python.org/downloads/) manually.
- Run the commands `py manage.py makemigrations` and `py manage.py migrate` in the project directory to make and apply migrations.
- Create superuser with `py manage.py createsuperuser`. This step is optional.
- Run the command `py manage.py runserver` to run the web server.
- Open web browser and goto `127.0.0.1:8000` url to start using the web application.
