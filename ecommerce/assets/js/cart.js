
var updateBtns = document.getElementsByClassName('update-cart')

for(var i =0; i < updateBtns.length; i++ ){
    updateBtns[i].addEventListener('click', function(){
        var productId = this.dataset.product
        var action = this.dataset.action
        
        console.log('productId:',productId,'action:',action)

        // console.log('USER:', user)
            
        updateUserOrder(productId, action)
        
    })
}

function addCookieItem(productId, action){
   
    console.log('tiny')

    if(action == 'add'){
        if(cart[productId] == undefined){
            cart[productId] = {'quantity':1}
        }else{
            cart[productId]['quantity'] += 1
        }
    }

    if(action == 'remove'){
        cart[productId]['quantity'] -= 1

        if(cart[productId]['quantity'] <= 0){
            console.log('Remove Item')
            delete cart [productId]
        }
    }

    

    console.log('Cart:',cart)
    document.cookie ='cart=' + JSON.stringify(cart) + ";domain=;path=/"
    location.reload()
}



function updateUserOrder(productId, action){
    console.log('User is logged in, sending data...')
       
        var csrftoken =  $('input[name=csrfmiddlewaretoken]').val();
        console.log(csrftoken)

        $.ajax({
            type: "POST",
            url: "/update_item/",
            data: {
                'productId':productId,
                'action':action,
                csrfmiddlewaretoken : csrftoken
            },
            success: function (response) {
               
                console.log(response.itemTotal)
                console.log(response.itemQty)
                alertify.success(response.messages);
                

                let cartqty = document.getElementsByClassName('cartqty')
                for (var i=0; i < cartqty.length; i++){

                    cartqty[i].innerHTML = response.cartItems
                    // cartqty.innerHTML = response.cartItems
                }

                

                let cartotal = document.getElementsByClassName('cartotal')
                for (var i=0; i < cartotal.length; i++){

                    cartotal[i].innerHTML = '&#8377; ' + response.cartTotal
                    // cartqty.innerHTML = response.cartItems
                }

                console.log(productId)
                console.log(action)
            
                

                //try and catch because of the problem, when adding items in the store page. 

                try{

                    document.getElementById(productId+'total').innerHTML = '&#8377; ' + response.itemTotal
                    
                }catch(e){
                    
                    }
                

                try{

                    document.getElementById(productId+'qty').value = response.itemQty

                }catch(e){
                    
                    }

               if (action == 'delete'){
                document.getElementById(productId+'row').innerHTML = ''
               }
               
            }
        });
        
   
    
    
}




var updateWishlist = document.getElementsByClassName('addToWishlist')

for(var i =0; i < updateWishlist.length; i++ ){

    updateWishlist[i].addEventListener('click', function(){
        var productId = this.dataset.product
        
        console.log('productId:',productId)
        // console.log('USER:', user)

        addToWishlist(productId)

    })
}

function addToWishlist(productId){
    console.log('User is logged in, sending wishlist...')
     
    var csrftoken =  $('input[name=csrfmiddlewaretoken]').val();
    console.log(csrftoken)
    
    $.ajax({
        method: "POST",
        url: "/add_to_wishlist/",
        data: {
            'productId':productId,
            csrfmiddlewaretoken : csrftoken
        },
        
        success: function (response) {
            if (response.wishlistcount){
                document.getElementById("wishlistcount").innerHTML = response.wishlistcount
            }
                
            alertify.success(response.status);

        }
    });
}

