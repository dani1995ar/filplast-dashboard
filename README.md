- [Order tracking dashboard](#order-tracking-dashboard)
- [Video Demo:  https://youtu.be/3oe57_YFgPo](#video-demo--httpsyoutube3oe57_yfgpo)
- [Description:](#description)
- [What does the app do?](#what-does-the-app-do)
- [How does it do it?](#how-does-it-do-it)
- [Features:](#features)
  - [search bar:](#search-bar)
  - [Name suggestion with autocomplete for new orders:](#name-suggestion-with-autocomplete-for-new-orders)
  - [Multiple items in one order:](#multiple-items-in-one-order)
  - [Each name is an anchor:](#each-name-is-an-anchor)
  - [Order numbers are anchors too:](#order-numbers-are-anchors-too)
- [The database more in depth:](#the-database-more-in-depth)
  - [Cost and price:](#cost-and-price)
  - [Product:](#product)
  - [Orders:](#orders)
- [Issues / Challenges:](#issues--challenges)
- [Conclusion:](#conclusion)
# Order tracking dashboard

# Video Demo:  https://youtu.be/3oe57_YFgPo

# Description:
![screenshot with overview of the page](static/Screen%20Shot%202021-12-06%20at%205.55.23%20PM.png)

My name is Daniel Agudelo, I'm from Medellin, Colombia, and this is my final project for CS50x.

As part of my final project I decided to take on the challenge of doing something that was of interest to me, that solved an actual problem and that it could impact my community in a positive way, that is how I came up with the idea of this dashboard.

I decided that it was best to not show the actual company name, just for security reasons, since my code is going to be public I would hate to see someone exploiting a potential vulnerability, that is why the project has the very original, very engaging name of "order tracking dashboard", before that it was called "company name dashboard" (I know, I am the best when it comes to naming things, not unlike variables).


# What does the app do?
It allows the company to keep track of their customer's orders, the item of each order, and all of the orders of each customer, in an organized, clean and intuitive way.


# How does it do it?

By saving all of the orders in an industry standard database rather than on an excel spreadsheet. This allows the company to further develop the dashboard, should they wish to. It also adds some functionality that would not otherwise have been there, such as the option of easily keeping track of their cost vs. prices for each product over time (the database is design to support this feature, however in the current state the dashboard does not yet support this). The database is designed from the ground up with the company as its cornerstone, and therefore it takes into account current and potential future needs of the business, (more on this later).

The entire app is meant to be a web app (this is because the business is currently using Google sheets which is available on mobile, and I wanted to develop something that could have the same benefits to the solution that they are currently using), the app is responsive and is built using Flask, mysql, javascript, bootstrap and jquery.

The submitted app is just the basic part of what hopefully will be an entire solution that integrates multiple dimensions of the business such as cost and price analysis, customer management, basic warehousing and potentially more. The current version of the app allows the users to create and review current and new orders, as well as keep track of the price of each item and the total price of the order.

# Features:

## search bar:
![searchbar screenshot](static/search%20bar%20screenshot.png)

The dashboard comes with a useful search bar that searches for the customer name, and displays all of the orders the curstome has placed, as well of all the items each order has. The search bar uses the following MYSQL statement on the back-end:

```mysql
SELECT o.note, o.id, p.full_name, pr.name, oi.quantity, cp.price FROM `order` AS o
        INNER JOIN person AS p ON o.person_id = p.id
        JOIN order_item AS oi ON oi.order_id = o.id
        JOIN product AS pr ON  pr.id = oi.product_id
        JOIN cost_price AS cp ON cp.product_id = pr.id
        WHERE p.full_name LIKE :pn
```
So that if the user enters a full or partial name of the customer he can easily find all of the orders associated with the person.

## Name suggestion with autocomplete for new orders:
![autocomplete gif](static/name%20suggestion%20gif.gif)

When creating a new order, the form will start suggesting existing customer names, and if the user click on them it will fill the sanitized input name automatically with the customer's full name.

## Multiple items in one order:
![adding items to order gif](satic/../static/Adding%20items%20to%20order.gif)

An order can have multiple items, and therefore the user can add or remove how many different items each order has at will.

## Each name is an anchor:

![searchbar screenshot](static/Names%20are%20anchors.gif)

In the landing page I made it so that if the user clicks on the customer name, they are immediately redirected to a page that displays all of that customer's orders, the items as well as the totals.

## Order numbers are anchors too:

If the user wishes to review an specific order, all they have to do is click on the order number and they can do so.

# The database more in depth:

The design of the database is probably the one thing I spent the most time on, and it is probably the one thing that they will continue to use long after I finished the project, so this is why I tried to design it with future need in mind, let's take a closer look on a few of my database design choices:

## Cost and price:

> *"Cost is typically the expense incurred for creating a product or service a company sells. ... Price is the amount a customer is willing to pay for a product or service. The difference between price paid and costs incurred is profit."*

![searchbar screenshot](static/Cost%20price%20ERD.png)

And this company's goal is to make profit, and that is why, the more data they have about how and where they are expending and receiving money, the better. This is the reason why I made a table called cost_price, which keeps track of each time total cost to produce, the current price it is being sold at, and the date the record is kept, this is done so that in the future (the dashboard is nowhere near finished yet) if the users would like to have a nice visual way to see how their prices and costs have changed over time, they have an easy way to do so.

## Product:

![searchbar screenshot](static/product%20ERD.png)

The hearth of the company is its products, that is why the corresponding portion of the database is also the hearth of it. Each product has a category (such as plastic filament, rubber filament, parts, kits and so on), so this is also kept track of. Another important detail to notice is that the database keeps record of products that are not currently being sold, this is just in case the users would like to review past products and its prices in order to develop/improve current products or future releases.

## Orders:

![searchbar screenshot](static/order%20ERD.png)

Finally the last item from the database I would like to explore a bit more is the  \`order\`  table. The order table includes which customer order is it, the date the order is required to be delivered, the date the order was placed, as well as some notes that might be important to keep for each order, even though the dashboard does not support it yet, I also made sure to include a property for any potential discounts and to include the total price of each order item. All of these decisions were discussed with the final user of the dashboard.

# Issues / Challenges:

Most of the problems I had during the development of this project where related in one way or another to the ORM and or the database. This is because I designed an schema that could support functions that are not yet implemented in the application, as it is much easier and faster and easier to develop new features for an app with a database that already support these features, rather than migrating an existing database to a new one, just so that the app can support a new feature. An instance of this is the way to store passwords in the database (so that in the future the app can be used by both the company and their customers), I knew storing them as plaintext was not a good idea at all, what I did not know however was just how many ways of storing passwords there are, and just like this I spent some good 8-10 hours researching about key derivation functions, hashing algorithms and so on. And just like that, and with every little detail or feature that I needed to or was planning to implement, I spent countless hours researching topic after topic and reading discussion after discussion, this, I believe, was the biggest challenge, because every step of the way I was unsure what was "the correct way to do things in this specific scenario", I can't say I enjoyed the process, yet I love the fact that I now know that much more about that many topics.

# Conclusion: 

The current status of this app is "still under development" and would probably be for the forseeable future, so far I have learnt a lot about so many different topics, such as JWT, DB, password hashing and so much more, that I am eager and looking forward to continue with this project, and to keep building upon the base app I developed so far.