# Image Marketplace
### Erica Matulis

The task given was to build an image repository. The basic functionality includes:
* Buying and selling images
* Uploading and updating images for selling
* Creating user accounts to manage your transactions, uploads and bought products

This project has been implemented in using Django, in Python with HTML, CSS and minor JavaScript.
It uses sqlite3 to store the images that have been added to the image repository.

## Main Files

* `personal/models.py` includes all models in the database
* `personal/views.py` includes all page requests and their respective actions (such as viewing products, deleting products, editing products, adding to the database, etc.)
* `personal/forms.py` includes the custom form for users to edit their products
* CSS and JS files are included in `personal/static/personal/`
* HTML templates are included in `personal/templates/personal/`
* `personal/tests.py` contains basic tests against the data model and user access to different pages

## Usage

To use this application, first download its contents.

Then change `settings.py` to have your Django secret key SECRET_KEY:
`    with open(os.path.join(BASE_DIR, os.pardir, "django_secret_key")) as f:
          SECRET_KEY = f.read()`
          
Then, create your superuser using `python3 manage.py createsuperuser` and run `python3 manage.py runserver` from the terminal/command line
inside its folder.

After this, open a web browser at the address given in the terminal/command line.

You will then be redirected to the login page (`/login.html`), where you should click "Register" (`/register.html`)
and make an account.

After registering, log in to your account and you will be sent to the marketplace (`/marketplace.html`) where you will be able to see images that have been uploaded by other users and are currently for sale on the website (served under the `media/images` folder). Images are associated with names, price, stock and images which are all displayed per product in the marketplace. At the top of the page, the total credit left is displayed ($100 when user joins, by default)

If an image is available for purchase (i.e. active and stock > 0) and you have enough credit to buy the given quantity of that image, you are able to buy the image by clicking "Buy" after selecting the desired quantity.

This will record the transaction in the database (under `Order` model) with the product, price, quantity, customer, seller, date, and order total. It will also update the product's inventory, the user's credit and the sellers credit (when a user purchases a product, their credit decreases while the purchase amount is added to the sellers store credit).

On the "Your Transactions" page (`/your_transactions.html`), the user is able to see a table of transactions purchased by them and details of all transactions, as well as
a separate table showing transaction sales made to other customers of their products. They are able to click on the product name to go to a page that shows details of the product.

On the "[username]" page (`/profile.html`), the user is able to see their total amount sold and their credit left to purchase
items.

The user is able to upload an image for sale by clicking "Upload" from the navigation bar (`/upload.html`), where they are able to choose the image, their name, description, image categories it belongs to (only two available at the moment, for demonstration purposes), price, inventory, whether it is active/inactive. If a product is inactive, it will not be shown in the marketplace to other users.

The user is able to view their uploaded products by selecting "Your Market" from the navigation bar (`/your_market.html`) where they can see the list of items they have put for sale, their price, inventory, total number and amount sold, whether they are active/inactive and select whether they'd like to edit or delete the product. Sellers are only able to delete their product from the database (not other users' products) if the no customers have bought it yet, otherwise they have the option to changing it to "inactive". At the top, the user is able to see the total amount they have sold across all transactions.

By clicking "edit", the user is redirected to edit the selected product and its information (where they are able to make it "active/inactive")

## Models

The models currently implemented in the database are the following 5:
* Profile: associated with the user account, includes: amount sold, amount spent, credit left
* Category: associated with products, includes: category name, category description (currently only possible to add/remove in admin)
* Product: main model used to store image products, includes: name, description, image, quantity, price, discount, number sold, amount sold, seller, categories, is_active
* Order: model to store product transactions, includes: product, customer, seller, date, price, quantity, total amount
* ChangeLog: model to store changes in product attributes such as adding, removing or editing a product, includes: previous product details (in dictionary format), new product details (in dictionary format), type of change (Add/Delete/Update), date, changed_by. It is not currently used, but available for reference and potential added features


## Testing

To run the tests, simply run `./manage.py test` from the command line/terminal. The tests included are not exhaustive due to time constraints, but they include:
* Making sure images are added/deleted with the proper seller information and changes in number of products
* Making sure unauthenticated users are not able to access certain pages

Additional tests that could be added include, but are not limited to:
* Testing that only product creator is able to delete the image
* Testing that images that have been already sold cannot be deleted
* Testing that users can't edit product information from other users

## Possible Features

The models created allow for additional features to be implemented, such as:
* Ability to add/remove discounts to images (by utilizing `Product.discount` field)
* Ability to add an image category to the database
* Ability to upload/edit multiple images at the same time
* Ability for user to see their selling history per month/year/etc.

Other features that could be added:
* Ability to search for images
* Purchasing multiple products at the same time, by adding a "add to cart" functionality and saving the user's cart information in the database.
* Adding success/failure messages
