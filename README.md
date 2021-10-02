# HTML CRUD TEMPLATE

This was meant to be a basic CRUD app template for a small company.
However I keep adding and adding features, but hopefully one day it will be finished, until then I will keep updating this readme 
with entries similar to a blog.

18/9/2021:

I decided to build a basic CRUD app to help a company keep track of their orders, this will most likely be my final project for Harvard CS50x, so today I spent the whole day wireframing how the front-end would look, but most importantly I invested a lot of time thinking how to properly structure the database and how the information would flow, in the static folder is the MER diagram showing how I decided to structure the database, chances are that it is very flawed but it's my first one, I hope it does the work ok.


24/9/2021:

Spent 10 hours figuring out how to hash a password and how to properly store it in a DB, I learned about SHA256, PBKDF2, BCrypt and lastly Argon2, and Argon2id, which I ultimately decided to used.....there is no library for Argon2id so I had to spent another hour or 2 figuring out which module to use in order to implement the Argon algorithm as well as tunning it....**I'M FULLY AWARE THAT THE UP IS MEANT FOR NO MORE THAN 3 PEOPLE**... Anyway I actually enjoyed the process and learned a lot, but I wish I didn't get carried away with every little detail just like this one.

25/9/2021:

Like the previous days it seems like today all I will be doing is studying a topic for over 5 hours to implement a small function, today's topic is: cookies, local storage and session storage. I need to fully understand this topics in order to be able to implement a proper login function as well as to secure the session of the **LITERALLY 2 OR 3 USERS MY APP WILL HAVE**, anyway, as I was saying the login function in helpers.py is deeply flawed, and I want to check if the staff implementation of the same pset is also flawed, I will try to find the session cookie and change it to a random int value, since the function in helpers uses the primay key of SQL table as the session user_id. CS50x staff usually leave easter eggs in their psets and I want to know if I can hijack another session, if so, I will try to hijack user_id 1 and see if it works. After doing this I will try to implement a proper access token based on what is currently used in more corporative websites such as google, youtube and so on.

It's been about an hour or so and I'd like to add JWT to the topics that I have to study.
Ok, so, after fiddling around with the staff implementation of finance, I realized that they have a proper JWT implemented (or it looks like it, I'm no security expert, not even close), that is stored in a cookie with the name of session, however thei implementation of login generates a new token each time the user log in, and the token is not just simple integer such as a primary key in an SQL database (unlike the helpers.py function they provided to us in the distribution code), so I'm out of luck, it seems I can't hijack another session in their implementation of finance....but what if I used an old token to try and authenticate, will it work?...nope it did not, so it seems they keep a copy of the current session token in their end and authenticate my local copy agains it every time I make a request. Also it seems like they clear their copy every time I log out so I'm definitely out of ideas on how to hijack another's person session in this app....

12:16AM of the 26th, I came across Auth0 and a 3 hour video from Ben Awad on how to implement JWT authentication I will rest now and watch it tomorrow.

28/09/2021:

For the past 3 hours I have been setting the DB up, the MERD I previously had was wrong, so I updated it and fixed all the issues I had trying to create the db. After finally getting the database up and running, I was able to load some testing data into one of the tables and succesfully got it communicating with the front-end with the use of sqlalchemy and flask-sqlalchemy, it took me a while to figure it out but I think I learned the very very basics about ORMs. I also spent some time organizing the way I am approaching this, and decided that for my first delivery, I'm going to focuss solely in the login page as well as orders.html, and will try to have this done by end of next week. With some dummy data properly displayed in the screen and the total being displayed in the orders table as well.

30/08/2021:

Another day, another 2 versions of the database. I consulted with someone with more experience than me on the topic and after a few modifications I think I have finally managed to get the correct architecture for the database, and this time is for real (hopefully). I could not spend much time coding, instead I studied a while, mainly trying to figure out how to get the aforementioned architecture correctly.
