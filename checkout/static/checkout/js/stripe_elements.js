/*
    Core logic/payment flow for this comes from here:
    https://stripe.com/docs/payments/accept-a-payment
    CSS from here: 
    https://stripe.com/docs/stripe-js
*/

// Get stripe public key and client secret
var stripePublicKey = $('#id_stripe_public_key').text().slice(1, -1);
var clientSecret = $('#id_client_secret').text().slice(1, -1);
// Create a stripe variable, through the stripe js used in the base template, using the public key
var stripe = Stripe(stripePublicKey);
// Use the stripe variable to create an instance of a stripe element and use it to create a card element
var elements = stripe.elements();
// The card element can also accept a style argument (Got these styles from the stripe JS docs)
var style = {
    base: {
        color: '#000',
        fontFamily: '"Helvetica Neue", Helvetica, sans-serif',
        fontSmoothing: 'antialiased',
        fontSize: '16px',
        '::placeholder': {
            color: '#aab7c4'
        }
    },
    invalid: {
        color: '#dc3545',
        iconColor: '#dc3545'
    }
};
var card = elements.create('card', {style: style});
// Mount the card element to the div created before 
card.mount('#card-element');

card.addEventListener('change', function() {
    var errorDiv = document.getElementById("card-errors");
    if (event.error) {
        var html = `
            <span class='icon' role='alert'>
                <i class='fas fa times'></i>
            </span>
            <span>${event.error.message}</span>
        `;
        $(errorDiv).html(html);
    } else {
        errorDiv.textContent = '';
    }
})

// Handle form submit
var form = document.getElementById('payment-form');

form.addEventListener('submit', function(ev) {
    // prevent default to prevent POST 
    ev.preventDefault();
    // Disable the card element and submit button, before calling out to stripe, 
    // so that multiple submissions are prevented
    card.update({ 'disabled': true});
    $('#submit-button').attr('disabled', true);
    $('#payment-form').fadeToggle(100);
    $('#loading-overlay').fadeToggle(100);
    // Send the card information securely to stripe
    stripe.confirmCardPayment(clientSecret, {
        payment_method: {
            card: card,
        }
    }).then(function(result) {
        if (result.error) {
            // If statement for errors
            var errorDiv = document.getElementById('card-errors');
            var html = `
                <span class="icon" role="alert">
                <i class="fas fa-times"></i>
                </span>
                <span>${result.error.message}</span>`;
            $(errorDiv).html(html);
            $('#payment-form').fadeToggle(100);
            $('#loading-overlay').fadeToggle(100);
            // If there is an error, allow the user to fix it by enabling the card element and submit button
            card.update({ 'disabled': false});
            $('#submit-button').attr('disabled', false);
        } else {
            // Submit the form, if successful
            if (result.paymentIntent.status === 'succeeded') {
                form.submit();
            }
        }
    });
});