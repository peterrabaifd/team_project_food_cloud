$(document).ready(function() {
    $(document).off('click', '.order_button').on('click', '.order_button', function() {
        var amount = prompt("Please enter amount of orders" ,"0");
        if (parseInt(amount) <= 0 /* || amount === null */) {
            alert("Please enter integer greater than 0")
        } else if (parseInt(amount) > 0) {
            Cookies.set('amount', amount)
            console.log(document.cookie)
            var link = $(this).find('a');
            console.log(link.attr('href'));
            window.location.href=link.attr('href');
            console.log("OK");
        }
        return false;
    });
});