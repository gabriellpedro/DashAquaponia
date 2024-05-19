document.addEventListener('DOMContentLoaded', function() {
    // Seleciona os elementos pelo ID
    var checkboxAlface = document.getElementById("checkVendaAlface");
    var inputQtdeAlface = document.getElementById("qtdeVendaAlface");

    inputQtdeAlface.disabled = true;

    checkboxAlface.addEventListener('change', function() {

        if (checkboxAlface.checked) {
            inputQtdeAlface.disabled = false;
        } else {
            inputQtdeAlface.disabled = true;
        }
    });
});
