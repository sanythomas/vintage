
var updateBtns = document.getElementsByClassName('update-cart')

for(var i =0; i < updateBtns.length; i++ ){
    updateBtns[i].addEventListener('click', function(){
        var productId = this.dataset.product
        var action = this.dataset.action
        
        var size_variant = this.dataset.size_variant
        console.log(size_variant)
        

        // if (size_id == undefined){
        //     var size_id = 3
        // }

        if (size_variant == undefined){
            var size_variant = 'S'
        }
        
        
        
        console.log('productId:',productId,'action:',action)

        // console.log('USER:', user)
            
        updateUserOrder(productId, action, size_variant)
        
    })
}





function updateUserOrder(productId, action, size_variant){
    console.log('User is logged in, sending data...')
       
        var csrftoken =  $('input[name=csrfmiddlewaretoken]').val();
        console.log(csrftoken)

        $.ajax({
            type: "POST",
            url: "/update_item/",
            data: {
                'productId':productId,
                'action':action,
                'size_variant':size_variant,
              
                csrfmiddlewaretoken : csrftoken
            },
            success: function (response) {
               
                console.log(response.itemTotal)
                console.log(response.itemQty)
                console.log(size_variant)
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
                console.log(size_variant)
               
                

                //try and catch because of the problem, when adding items in the store page. 

                try{

                    document.getElementById(productId+'total'+size_variant).innerHTML = '&#8377; ' + response.itemTotal
                    
                }catch(e){
                    
                    }
                

                try{

                    document.getElementById(productId+'qty'+size_variant).value = response.itemQty
                    

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

