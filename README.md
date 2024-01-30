# SneakerShop
The main purpose of this project was to learn how to build the backend of an E-Commerce website using the Django Framework. 

You can find a live demo [here](https://maximerochat.ch/shop), some features are buggy (certain filters induce crashes, recommendation always working, etc...) but the main educational goal was met. 

If you want to run this project locally, you just need to follow these steps :

1) Clone this repo.
2) Open a terminal and download all python dependencies using the command `pip install -r requirements.txt`.
3) Perform initial db migration for Django by running `python manage.py makemigrations` and `python manage.py migrate`.
4) Start the server by running `python manage.py runserver`, this should open the server on 127.0.0.1:8000.

Then to add items you first need to have an admin account that you create by running `python manage.py createsuperuser`, then you can go to 127.0.0.1:8000/admin, and you will be prompted to type the credentials you just created. 
Then you land on a page where on the left there should be different categories and you need to look for "Shoess", next to it, you should see a button that says "add" and when you click on that you will be prompted to fill different field that correspond to a shoe product. Then when you are finished, you click on the save button on the bottom right, and can look for the "Imagess" section on the left of the screen. 

As you did before click on the "add" button and you will be prompted to choose an image file and to select and to select an "Img id", if you already created a shoe, it should be available there, this field links the image to a product. Then you can save and if everything went good you should see a shoe appear on the home page. 