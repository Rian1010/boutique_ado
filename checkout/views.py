from django.shortcuts import render, redirect, reverse, get_object_or_404, HttpResponse
from django.views.decorators.http import require_POST
from django.contrib import messages
from django.conf import settings

from .forms import OrderForm
from .models import Order, OrderLineItem
from products.models import Product
from bag.contexts import bag_contents

import stripe
import json

@require_POST
def cache_checkout_data(request):
    try:
        pid = request.POST.get('client_secret').split('_secret')[0]
        stripe.api_key = settings.STRIPE_SECRET_KEY
        stripe.PaymentIntent.modify(pid, metadata={
            'bag': json.dumps(request.session.get('bag', {})),
            # Check if user wants to save their information 
            'save_info': request.POST.get('save_info'),
            'username': request.user,
        })
        return HttpResponse(status=200)
    except Exception as e:
        messages.error(request, 'Sorry, your payment cannot be \
            processed right now. Please try again later.')
        return HttpResponse(content=e, status=400)

def checkout(request):
    # Create the payment intent
    stripe_public_key = settings.STRIPE_PUBLIC_KEY
    stripe_secret_key = settings.STRIPE_SECRET_KEY

    if request.method == "POST":
        # Use the shopping-bag
        bag = request.session.get('bag', {})

        # Put the form data into a dictionary
        form_data = {
            'full_name': request.POST['full_name'],
            'email': request.POST['email'],
            'phone_number': request.POST['phone_number'],
            'country': request.POST['country'],
            'postcode': request.POST['postcode'],
            'town_or_city': request.POST['town_or_city'],
            'street_address1': request.POST['street_address1'],
            'street_address2': request.POST['street_address2'],
            'county': request.POST['county'],
        }
        order_form = OrderForm(form_data)
        # Get the client secret if the form is valid
        if order_form.is_valid():
            # Add it to the model
            # As a quick optimization, prevent multiple save events from being executed on the database, use
            # commit=False to prevent the first one from happening
            order = order_form.save(commit=False)
            pid = request.POST.get('client_secret').split('_secret')[0]
            order.stripe_pid = pid
            # Dump it to a JSON string and set it on the order
            order.original_bag = json.dumps(bag)
            order.save()
        # Save the order, if the form is valid
        if order_form.is_valid():
            # Save the order to get the order number argument and other order information
            order = order_form.save()
            for item_id, item_data in bag.items():
                try:
                    # Take a product out of the shopping-bag
                    product = Product.objects.get(id=item_id)
                    # If the value is an integer, the product does not have a size
                    if isinstance(item_data, int):
                        order_line_item = OrderLineItem(
                            order=order,
                            product=product,
                            # Since the product does not have sizes, the quantity is just the item data
                            quantity=item_data,
                        )
                        order_line_item.save()
                    else:
                        # If the product does have sizes, iterate through each size and create a line item accordingly
                        for size, quantity in item_data['items_by_size'].items():
                            order_line_item = OrderLineItem(
                                order=order,
                                product=product,
                                quantity=quantity,
                                product_size=size,
                            )
                            order_line_item.save()
                except Product.DoesNotExist:
                    # If product is not found, add an error message, delete the empty order and return to the bag page
                    messages.error(request, (
                        "One of the products in your bag wasn't found in our database. "
                        "Please call us for assistance!")
                    )
                    order.delete()
                    return redirect(reverse('view_bag'))
            # Saves user information to the session, if user wants
            request.session['save_info'] = 'save-info' in request.POST
            # redirect to checkout_success and pass it the order number as an argument
            return redirect(reverse('checkout_success', args=[order.order_number]))
        else:
            # Error message, if the form is not valid
            messages.error(request, 'There was an error with your form. \
                Please double check your information.')
    else:
        # Handle GET requests
        bag = request.session.get('bag', {})
        if not bag:
            messages.error(request, "There's nothing in your bag at the moment")
            return redirect(reverse('products'))

        # Create the current_bag variable, making sure not to overwrite the bag variable that already exists
        current_bag = bag_contents(request)
        total = current_bag['grand_total']
        # Stripe requires the amount as an integer
        stripe_total = round(total * 100)
        # Set the secret key on stripe after creating the payment intent at the top of the function
        stripe.api_key = stripe_secret_key
        # Create the payment intent with stripe.payment.intent.create, giving it the amount and the currency
        intent = stripe.PaymentIntent.create(
            amount=stripe_total,	
            currency=settings.STRIPE_CURRENCY,
        )

        print(intent)

        order_form = OrderForm()

    if not stripe_public_key:
        messages.warning(request, 'Stripe public key is missing. \
            Did you forget to set it in the environment')

    template = 'checkout/checkout.html'
    context = {
        'order_form': order_form,
        'stripe_public_key': stripe_public_key,
        'client_secret': intent.client_secret,
    }

    return render(request, template, context)


def checkout_success(request, order_number):
    """
    Handle successful checkouts
    """
    # save_info for user profile
    save_info = request.session.get('save_info')
    order = get_object_or_404(Order, order_number=order_number)
    # send an email to inputted email
    messages.success(request, f'Order successfully processed! \
        Your order number is {order_number}. A confirmation \
        email will be sent to {order.email}.')
    # the bag session is not needed
    if 'bag' in request.session:
        del request.session['bag']

    template = 'checkout/checkout_success.html'
    context = {
        'order': order,
    }

    return render(request, template, context)
