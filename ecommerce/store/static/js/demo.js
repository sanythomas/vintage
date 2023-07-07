
function submitFormData(){
    console.log('payment button clicked')

    var userFormData = {
        'name': null,
        'email':null,
        'total':total,
        

    }
    var shippingInfo = {
        
        'address': null,
        'city':null,
        'state':null,
        'zipcode':null,
        'shippingaddressId':null,

    }

    shippingInfo.address = shippingform.address.value
    shippingInfo.city = shippingform.city.value
    shippingInfo.state = shippingform.state.value
    shippingInfo.zipcode = shippingform.zipcode.value
    shippingInfo.shippingaddressId = shippingform.shippingaddressId.value

    if (user == 'AnonymousUser'){
        userFormData.name = shippingform.name.value
        userFormData.email = shippingform.email.value
        
    }

    var url = '/process_order/'
    fetch (url, {
        method: 'POST',
        headers:{
            'Content-Type': 'application/json',
            'X-CSRFToken':csrftoken,
        },
        body:JSON.stringify({'form':userFormData, 'shipping':shippingInfo})
    })

    .then((response) => response.json())
    .then((data) => {
       
        //console.log('Success:', data);
        alert('Transaction completed')
        //swal("Success", "Thank you for buying with us!", "success");

        cart = {}
        document.cookie ='cart=' + JSON.stringify(cart) + ";domain=;path=/"  

        window.location.href = "{% url 'home' %}"
        
        
        
    })

}