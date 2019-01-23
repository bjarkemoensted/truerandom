$(function(){
    
    var twoToneButton = document.querySelector('.twoToneButton');
    const loader = document.getElementById("loadanim");
    const volatiles = document.querySelectorAll('.volatile');

    
    twoToneButton.addEventListener("click", function() {
        twoToneButton.innerHTML = "doing stuff";
        loader.hidden = false;
        for (const volatile of volatiles) {
            volatile.hidden = true;
    }
        
        
      setTimeout( 
            function  (){  
                twoToneButton.innerHTML = "Again!";
                loader.hidden = true;
                for (const volatile of volatiles) {
                    volatile.hidden = false;
                }
                

                
            }, 6000);
    }, false);
    
});