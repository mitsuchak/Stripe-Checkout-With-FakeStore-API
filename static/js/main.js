
// static/main.js
console.log("daccsd")
console.log("Sanity  vfvds !");

// Get Stripe publishable key

function myfunction(){
    console.log("Sanity check!");
    // Create an instance of the Stripe object with your publishable API key
    var stripe = Stripe('pk_test_51JAYouSIOIKz7cmfczeDN0rvHKakAERTCdfWb4dsAPjpz7otjndMXZSI54salmxBVWlTyXiUtDtFMsfizU7LBIsJ00v87dOvMs');
    
    // Gets all buy buttons
    var buttons = document.getElementsByClassName('button2');
    for (i = 0; i < buttons.length; i++) {
    
      // for every button we will add a Stripe POST request action
      buttons[i].addEventListener('click', function(event) {
        var targetElement = event.target || event.srcElement;
        var productName =  targetElement.value;
        console.log('Buying: ' + productName);
    
        // Our endpoint with the chosen product name
        var url = 'create-checkout-session/' + productName
    
        // Create a new Checkout Session
        fetch(url, {
          method: 'POST',
        })
        .then(function(response) {
          return response.json();
        })
        .then(function(session) {
          return stripe.redirectToCheckout({ sessionId: session.id });
        })
        .then(function(result) {
          // If `redirectToCheckout` fails due to a browser or network
          // error, you should display the localized error message to your
          // customer using `error.message`.
          if (result.error) {
            alert(result.error.message);
          }
        })
        .catch(function(error) {
          console.error('Error:', error);
        });
    
      });
    
    }

}