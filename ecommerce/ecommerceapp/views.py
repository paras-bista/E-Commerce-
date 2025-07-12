from django.shortcuts import render, redirect,get_object_or_404
from django.contrib import messages
from .models import Contact,Product
from math import ceil
from ecommerceapp.models import Order  # Replace 'ecommerceapp' with your app name
from .models import Order, Product, OrderItem
from django.contrib.auth.decorators import login_required

# Create your views here.
def index(request):
    products = Product.objects.all()
    print("Products:", products)  # Debug: Verify product retrieval

    allProducts = []
    categories = Product.objects.values('category').distinct()
    print("Categories:", categories)  # Debug: Verify categories

    for cat in categories:
        prod = Product.objects.filter(category=cat['category'])
        print("Products in category:", cat['category'], prod)  # Debug: Verify products in each category
        n = len(prod)
        # Calculate number of slides for a carousel display (assuming 4 items per slide)
        nSlides = n // 4 + ceil((n / 4) - (n // 4))
        allProducts.append([prod, range(1, nSlides), nSlides])

    print("All Products:", allProducts)  # Debug: Verify the structure of allProducts

    context = {'allProducts': allProducts}
    if request.user.is_authenticated:
        messages.success(request, "Login Successful!")
    return render(request, 'index.html', context)

def contact(request):
    if request.method == "POST":
        name = request.POST['name']
        email = request.POST['email']
        description = request.POST['description']
        pnumber = request.POST['pnumber']
        myquery = Contact(name=name, email=email, description=description, Phonenumber=pnumber)
        myquery.save()
        messages.success(request, "Your message has been sent successfully.")
        return redirect('contact')
    return render(request, 'contact.html')

def about(request):
    return render(request, 'about.html')


def checkout(request):
    # If you expect only POST for placing an order
    if request.method == 'POST':
        full_name = request.POST.get('full_name')
        phone     = request.POST.get('phone')
        address   = request.POST.get('address')
        payment   = request.POST.get('payment_method')

        # TODO: validate and process the order
        # e.g. create Order object, clear cart, send confirmation email, etc.
        messages.success(request, 'Your order has been placed successfully!')
        return redirect('order_success')  # or wherever

    # For GET, render the checkout page template
    return render(request, 'checkout.html', {
        # any context variables you need; e.g. existing user info
    })


from django.shortcuts import redirect, render, get_object_or_404
from django.contrib import messages
from .models import Order, OrderItem, Product

def place_order(request):
    if request.method != 'POST':
        return redirect('checkout')

    # 1) Create the parent Order
    order = Order.objects.create(
        full_name = request.POST.get('full_name'),
        email     = request.POST.get('email'),
        phone     = request.POST.get('phone'),
        address   = request.POST.get('address'),
        payment_proof = request.FILES.get('payment_proof')
    )

    # 2) Extract all product_ids & quantities from POST
    product_ids = request.POST.getlist('product_id')
    quantities  = request.POST.getlist('quantity')

    # 3) Create one OrderItem per product
    for pid, qty_str in zip(product_ids, quantities):
        product = get_object_or_404(Product, pk=pid)
        qty     = int(qty_str)
        OrderItem.objects.create(
            order    = order,
            product  = product,
            quantity = qty,
            price    = product.price * qty
        )

    messages.success(request, 'Your order has been placed!')
    return redirect('order_success')


def order_success(request):
    # Render your thank‑you page template
    return render(request, 'ordersuccess.html')

from django.core.mail import send_mail
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test
from .models import Order  # adjust based on your model

def is_admin(user):
    return user.is_superuser

@user_passes_test(is_admin)
def send_shipment_email(request, order_id):
    order = get_object_or_404(Order, id=order_id)

    subject = f'Shipment Update for Your Order #{order.id}'
    message = f'Dear {order.user.username},\n\nYour order has been shipped!\nTracking ID: {order.tracking_number or "Not Available"}\n\nThank you for shopping with us.'
    recipient_email = order.user.email

    try:
        send_mail(
            subject,
            message,
            'yourstore@example.com',  # Replace with your "from" email
            [recipient_email],
            fail_silently=False,
        )
        messages.success(request, f"Shipment email sent to {recipient_email}.")
    except Exception as e:
        messages.error(request, f"Failed to send email: {str(e)}")

    return redirect('admin:app_order_change', order_id)  # Replace 'app' with your app name


# ecommerceapp/views.py
from django.shortcuts import render, redirect
# from .forms import ProfileForm
from django.contrib.auth.decorators import login_required

@login_required
def profile_view(request):
    profile = request.user.profile
    form = ProfileForm(request.POST or None, request.FILES or None, instance=profile)
    if form.is_valid():
        form.save()
        return redirect('profile')  # name of the URL pattern

    return render(request, 'profile.html', {
        'form': form,
        'user': request.user
    })


@login_required
def update_cart(request):
    if request.method == 'POST':
        user_email = request.user.email
        cart_order = Order.objects.filter(email=user_email, status='Pending').first()
        if not cart_order:
            # no cart/order found, redirect back
            return redirect('profile')

        selected_item_ids = request.POST.getlist('selected_items')

        # Update quantities and remove selected items
        for item in cart_order.items.all():
            qty_field = f'quantity_{item.id}'
            if qty_field in request.POST:
                try:
                    new_qty = int(request.POST[qty_field])
                    if new_qty > 0:
                        item.quantity = new_qty
                        item.save()
                except ValueError:
                    pass  # ignore invalid qty

            if str(item.id) in selected_item_ids:
                item.delete()

        # Optionally, update cart_order.total_price here or do it dynamically in views

    return redirect('profile')

from django.shortcuts import render

def profile_view(request):
    return render(request, 'profile.html')  # Make sure you have this template
