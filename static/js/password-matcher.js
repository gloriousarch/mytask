
window.onload = function(){ 
    document.querySelector('.btn').onclick = function(){
                                        
        var password = document.querySelector('.inputpass').value,
        confirmPassword = document.querySelector('.inputconf').value;

        if(password == ""){
                alert("Field cannot be empty.");
        }
        else if(password != confirmPassword){
                alert("passwords do not match.");
                return false
        }
    }
};
