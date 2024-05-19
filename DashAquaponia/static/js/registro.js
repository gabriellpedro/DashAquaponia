
var input = document.getElementById("checkVenda");
var input2 = document.querySelector("#qtdeVendaPeixe");
input2.disabled = true
input.addEventListener('click', function(){

    var input2 = document.querySelector("#qtdeVendaPeixe");

    input2.classList.toggle('active');

    if (input2.classList.contains('active')){
        input2.disabled = false;
    }
    else{
        input2.disabled = true
    }
})