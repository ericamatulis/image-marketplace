from django.shortcuts import render, get_object_or_404, redirect
from personal.models import Product, Category, Order, Profile, ChangeLog
from django.db import transaction
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import logout, authenticate, login, get_user
from django.contrib import messages
from .forms import ProductForm
import locale
from django.forms.models import model_to_dict
from django.views.generic.edit import CreateView, UpdateView, DeleteView


# Marketplace view
def index(request):
        
    # If user is authenticated, show views
    if request.user.is_authenticated:
        
        product_list = Product.objects.exclude(seller=get_user(request)).filter(is_active=True)
        # Actions based on form request (when user submits a form by clicking one of the buttons)
        if request.method == 'POST':
            name = request.POST.get('name')
            number = int(request.POST.get('quantity'))
            product = Product.objects.get(product_name=name)
            
            if (Profile.objects.get(user=get_user(request)).credit_left > number*product.product_price) and (number > 0):
                
                
                product.product_quantity = product.product_quantity-number
                product.number_sold = product.number_sold + number
                product.amount_sold = product.amount_sold + (number*product.product_price)
                product.save()
                transaction.commit()

                order = Order(product=product, customer=get_user(request), quantity=number, price = product.product_price, total=(number*product.product_price), seller=product.seller)
                order.save()
                transaction.commit()

                sold_profile = Profile.objects.get(user=product.seller)
                bought_profile = Profile.objects.get(user=get_user(request))

                sold_profile.amount_sold = sold_profile.amount_sold + number*product.product_price
                sold_profile.credit_left = sold_profile.credit_left + number*product.product_price
                sold_profile.save()
                bought_profile.credit_left = bought_profile.credit_left - number*product.product_price
                bought_profile.amount_spent = bought_profile.amount_spent - number*product.product_price
                bought_profile.save()

                transaction.commit()

                product_list = Product.objects.exclude(seller=get_user(request)).filter(is_active=True)

                return render(request,
                    'personal/marketplace.html', {'product_list': product_list, 'available_credit': "${:,.2f}".format(Profile.objects.get(user=get_user(request)).credit_left)}
                )
            else:
                return render(request, 'personal/marketplace.html', {'product_list': product_list, 'available_credit': "${:,.2f}".format(Profile.objects.get(user=get_user(request)).credit_left)})


        # Otherwise, just load the default view
        else:
            return render(request, 'personal/marketplace.html', {'product_list': product_list, 'available_credit': "${:,.2f}".format(Profile.objects.get(user=get_user(request)).credit_left)})
    else:
        return redirect("personal:login")
    
    
# Your Market view
def your_market_request(request):
        
    # If user is authenticated, show views
    if request.user.is_authenticated:
        user_profile = Profile.objects.get(user=get_user(request))
        product_list = Product.objects.filter(seller=get_user(request)) # list of products user is selling
        amount_sold = "${:,.2f}".format(user_profile.amount_sold)
        return render(request, 'personal/your_market.html', {'product_list': product_list, 'amount_sold': amount_sold,})
    else:
        return redirect("personal:login")
    
    
def transactions_request(request):
        
    # If user is authenticated, show views
    if request.user.is_authenticated:
        order_list = Order.objects.filter(customer=get_user(request))
        total = sum(list(order_list.values_list('total',flat=True)))
        sold_list = Order.objects.filter(seller=get_user(request))
        return render(request, 'personal/your_transactions.html', {'order_list': order_list, 'total':total, 'sold_list': sold_list})
    else:
        return redirect("personal:login")
    

# View with product details
def product_request(request):
            
    # If user is authenticated, show views
    if request.user.is_authenticated:
        product = Product.objects.get(pk=request.GET.get('product',''))
        return render(request, 'personal/product.html', {'product': product})
    return redirect("personal:login")

## Profile, registration, login and logout views

# Profile view
def profile(request):
        
    # If user is authenticated, show views
    if request.user.is_authenticated:
        user_profile = Profile.objects.get(user=get_user(request))
        amount_sold = "${:,.2f}".format(user_profile.amount_sold)
        credit_left = "${:,.2f}".format(user_profile.credit_left)
        return  render(request, 'personal/profile.html', {'amount_sold': amount_sold,'credit_left': credit_left })
    else:
        return redirect("personal:login")
    
    
# Registration view
def register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f"New account created: {username}")
            login(request, user)
            return redirect("personal:index")
        else:
            for msg in form.error_messages:
                messages.error(request, f"{msg}: {form.error_messages[msg]}")

            return render(request = request,
                          template_name = "personal/register.html",
                          context={"form":form})

    form = UserCreationForm
    return render(request = request,
                  template_name = "personal/register.html",
                  context={"form":form})


# Login view
def login_request(request):
    # If user is authenticated, go to homepage
    if request.user.is_authenticated:
        return redirect("personal:index")
    else:
        if request.method == 'POST':
            form = AuthenticationForm(request=request, data=request.POST)
            if form.is_valid():
                username = form.cleaned_data.get('username')
                password = form.cleaned_data.get('password')
                user = authenticate(username=username, password=password)
                if user is not None:
                    login(request, user)
                    messages.info(request, f"You are now logged in as {username}")
                    return redirect("personal:index")
                else:
                    messages.error(request, "Invalid username or password.")
            else:
                messages.error(request, "Invalid username or password.")
        form = AuthenticationForm()
        return render(request = request,
                        template_name = "personal/login.html",
                        context={"form":form})


# Logout view
def logout_request(request):
    # If user is authenticated, show logout request
    if request.user.is_authenticated:
        logout(request)
        messages.info(request, "Logged out successfully!")
    return redirect("personal:login")


class ProductDeleteView(DeleteView):
    model = Product
    success_url = '/your_market'

    def delete(self, request, *args, **kwargs):
        # If user is authenticated, allow deletion
        if request.user.is_authenticated:
            self.object = self.get_object()
            can_delete = not(bool(Order.objects.filter(product=self.object))) and (get_user(request)==self.object.seller) # check if user has delete permissions and object has not been sold yet

            if can_delete:
                change = ChangeLog(changed_by=get_user(request), previous_product=model_to_dict(self.object), new_product="DELETE", type_of_change=1)
                change.save()
                transaction.commit()
                return super(ProductDeleteView, self).delete(
                    request, *args, **kwargs)
            else:
                return redirect("personal:your_market")
        
        return redirect("personal:login")
    
    
def upload_request(request):
            
    # If user is authenticated, show views
    if request.user.is_authenticated:
        if request.method == 'POST':
            form = ProductForm(request.POST, request.FILES)
            if form.is_valid():
                image = form.cleaned_data['product_image']
                title = form.cleaned_data['product_name']
                price = form.cleaned_data['product_price']
                description = form.cleaned_data['product_description']
                quantity = form.cleaned_data['product_quantity']
                categories = form.cleaned_data['categories']
                new_product = Product(product_image=image, product_name=title, seller=get_user(request), product_price=price, product_description=description, product_quantity=quantity)
                new_product.save()
                new_product.categories.set(categories.all())
                new_product.save()
                transaction.commit()
                img_obj = new_product
                change = ChangeLog(changed_by=get_user(request), previous_product="UPLOAD", new_product=model_to_dict(new_product), type_of_change=3)
                change.save()
                transaction.commit()
                return redirect("personal:your_market")
        else:
            form = ProductForm(initial={'is_active': True})
        return render(request, 'personal/upload.html', {'form': form})
    return redirect("personal:login")


def update_request(request):
            
    # If user is authenticated, show views
    if request.user.is_authenticated:    
        product = Product.objects.get(pk=request.GET.get('product',''))
        if product.seller != get_user(request):
            return redirect("personal:your_market")
        
        if request.method == 'POST':
            form = ProductForm(request.POST, request.FILES)
            if form.is_valid():
                obj_dict = model_to_dict(product)
                image = form.cleaned_data['product_image']
                title = form.cleaned_data['product_name']
                price = form.cleaned_data['product_price']
                description = form.cleaned_data['product_description']
                quantity = form.cleaned_data['product_quantity']
                categories = form.cleaned_data['categories']
                is_active = form.cleaned_data['is_active']
                if image:
                    product.product_image=image
                product.product_name=title
                product.product_price=price
                product.product_description=description
                product.product_quantity=quantity
                product.categories.set(categories.all())
                product.is_active=is_active
                product.save()
                transaction.commit()  

                change = ChangeLog(changed_by=get_user(request), previous_product=obj_dict, new_product=model_to_dict(product), type_of_change=2)
                change.save()
                transaction.commit()

                return redirect("personal:your_market")
        else:
            form = ProductForm(initial={'product_image': product.product_image,
                                        'product_name': product.product_name,
                                        'product_price': product.product_price,
                                        'product_quantity': product.product_quantity,
                                        'product_description': product.product_description,
                                        'categories': product.categories.all(),
                                        'is_active': product.is_active
                                       })
            return render(request, 'personal/edit.html', {'form': form})
    return redirect("personal:login")
