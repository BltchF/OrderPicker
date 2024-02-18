project tree as below:
```
📦2_order_picker  
├ 📁app
│   ├ 📁models
│   │   ├ 📄store.py
│   │   └ 📄user.py
│   ├ 📁routes
│   │   ├ 📄auth.py
│   │   ├ 📄bot.py
│   │   └ 📄order.py
│   ├ 📁static
│   │   ├ 📁css
│   │   │   └ 📄style.css
│   │   ├ 📁images
│   │   │   └ 📄orderpicker.svg
│   │   └ 📁js
│   ├ 📁templates
│   │   ├ 📄base.html
│   │   ├ 📄index.html
│   │   ├ 📄login.html
│   │   ├ 📄order.html
│   │   └ 📄summary.html
│   ├ 📁tests
│   │   └ 📄text_template.py
│   ├ 📁utils
│   │   ├ 📄gettree.bat
│   │   ├ 📄gettree.ps1
│   │   └ 📄line_helper.py
│   ├ 📄extensions.py
│   ├ 📄info.txt
│   └ 📄__init__.py
├ 📁bin
├ 📄.env
├ 📄.gitignore
├ 📄config.py
├ 📄Procfile
├ 📄README.md
├ 📄requirements.txt
├ 📄run.py
└ 📄run_local.py
```
# app purpose as below:
```
this project has features below:
1. this project is develop locally using ngrok. i placed this in run_loacal.py under root directory. another deploy version of entry is run.py placed in the same directory as well.
2. this project would eventually hosted on heroku. and using it's plugin of postgres. i have put it's url into config.py.
3. this project contains two LINE channel.
one is messaging API channel use for bot that can invited into group than it's main purpose is throwing the link of flask app entry into the group when receiving sepecific message.
4. all the sensitive information has set into nor ".env" to develop locally or environment variable of heroku.
5. when user login via LINE login channel. they can perform "choice store" at index.html. then with specific store access "order.html". they will take orders here. session starts from user's login.
6. the app then collect ordering from different users. when the last user trigger complete ordering. the bot then pass whole the order_list back to their line group.
```


# database design
```
1. `users` table: Stores user data.
    - `id`: Primary key
    - `name`: User's name
    - `line_id`: User's LINE ID
    - `privilege`: User's role, ENUM('user', 'admin', 'teacher')
    - `created_at`: Timestamp of when the user was created
    - `updated_at`: Timestamp of when the user information was last updated

2. `roles` table: Stores different roles for users (Optional, for future use).
    - `id`: Primary key
    - `name`: Name of the role
    - `description`: Description of what the role entails

3. `user_roles` table: Maps users to roles (Optional, for future use).
    - `user_id`: Foreign key referencing `users.id`
    - `role_id`: Foreign key referencing `roles.id`
    - Composite primary key (`user_id`, `role_id`)

4. `stores` table: Stores information about each store.
    - `id`: Primary key
    - `name`: Store's name
    - `phone_number`: Store's phone number
    - `description`: Store's description
    - `created_at`: Timestamp of when the store was created
    - `updated_at`: Timestamp of when the store information was last updated

5. `menus` table: Stores information about each menu item.
    - `item_id`: Primary key
    - `store_id`: Foreign key referencing `stores.id`
    - `item_name`: Menu item's name
    - `price`: Menu item's price
    - `size`: ENUM('small', 'medium', 'large', etc.), Size of the menu item
    - `additional_option`: JSON field for additional options like "add spicy", "add extra cheese" (Optional)
    - `category`: Category of the menu item (e.g., "Breakfast", "Snacks", "Drinks")
    - `created_at`: Timestamp of when the menu item was created
    - `updated_at`: Timestamp of when the menu item was last updated

6. `orders` table: Stores information about each order.
    - `order_id`: Primary key
    - `user_id`: Foreign key referencing `users.id`
    - `store_id`: Foreign key referencing `stores.id`
    - `status`: ENUM('pending', 'completed', 'cancelled'), Order status
    - `created_at`: Timestamp of when the order was placed
    - `updated_at`: Timestamp of when the order status was last updated

7. `order_items` table: Stores information about each item in an order.
    - `id`: Primary key
    - `order_id`: Foreign key referencing `orders.order_id`
    - `menu_id`: Foreign key referencing `menus.item_id`
    - `quantity`: Amount of each item
    - `customizations`: JSON field for customizations or special instructions (Optional)
    - `created_at`: Timestamp of when the order item was added
    - `updated_at`: Timestamp of when the order item was last updated
```