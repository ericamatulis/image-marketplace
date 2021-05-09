from django.test import TestCase
from .models import *

## Helper functions
def create_product(product_name="A", product_price=1, product_image="/media/images/bananaphone.jpeg"):
    return Product.objects.create(product_name=product_name, product_price=product_price, product_image=product_image)

## Tests

### User authentication/allowed pages
class UserAuthenticationTests(TestCase):
    def test_marketplace_view_unauthenticated(self):
        response = self.client.get('/', follow=True)
        self.assertRedirects(response, '/login')
        response = self.client.post('/', follow=True)
        self.assertRedirects(response, '/login')

    def test_marketplace_view_authenticated(self):
        self.user = User.objects.create_user(username='testuser', password='12345')
        login = self.client.login(username='testuser', password='12345')
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'personal/marketplace.html')

    def test_your_market_view_unauthenticated(self):
        response = self.client.get('/your_market', follow=True)
        self.assertRedirects(response, '/login')
        response = self.client.post('/your_market', follow=True)
        self.assertRedirects(response, '/login')

    def test_your_market_view_authenticated(self):
        self.user = User.objects.create_user(username='testuser', password='12345')
        login = self.client.login(username='testuser', password='12345')
        response = self.client.get('/your_market')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'personal/your_market.html')

    def test_upload_view_unauthenticated(self):
        response = self.client.get('/upload/', follow=True)
        self.assertRedirects(response, '/login')
        response = self.client.post('/upload/', follow=True)
        self.assertRedirects(response, '/login')

    def test_upload_view_authenticated(self):
        self.user = User.objects.create_user(username='testuser', password='12345')
        login = self.client.login(username='testuser', password='12345')
        response = self.client.get('/upload/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'personal/upload.html')

    def test_your_transactions_view_unauthenticated(self):
        response = self.client.get('/your_transactions/', follow=True)
        self.assertRedirects(response, '/login')
        response = self.client.post('/your_transactions/', follow=True)
        self.assertRedirects(response, '/login')

    def test_your_transactions_view_authenticated(self):
        self.user = User.objects.create_user(username='testuser', password='12345')
        login = self.client.login(username='testuser', password='12345')
        response = self.client.get('/your_transactions/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'personal/your_transactions.html')

### Product tests
class ProductTests(TestCase):
    def test_add_product(self):
        self.user = User.objects.create_user(username='testuser', password='12345')
        login = self.client.login(username='testuser', password='12345')
        product = create_product()
        product.seller = self.user
        product.save()
        self.assertEqual(Product.objects.count(), 1)
        self.assertEqual(Product.objects.get(seller=product.seller), product)
    def test_remove_product(self):
        self.user = User.objects.create_user(username='testuser', password='12345')
        login = self.client.login(username='testuser', password='12345')
        product = create_product()
        product.seller = self.user
        product.save()
        product.delete()
        self.assertEqual(Product.objects.count(), 0)
