var please = {
    hidenow: function() {
        return this.hide;
    }
}

$(document).ready(function () {
    $(document).off('click', '.order_button').on('click', '.order_button', function () {
        var amount = prompt("Please enter amount of orders", "0");
        if (parseInt(amount) <= 0 /* || amount === null */) {
            alert("Please enter integer greater than 0");
        } else if (parseInt(amount) > 0) {
            var link = $(this).attr('href');
            console.log(link);
            $.ajax({
                url: link,
                data: {
                    'amount': amount
                },
                dataType: 'json',
                success: function (data) {
                    if (data.success) {
                        alert("Order successful");
                        location.reload();
                    }
                }
            });
        }
        return false;
    });
    $(document).off('click', '.rating').on('click', '.rating', function () {
        var rating = prompt("Please enter amount of orders", "0");
        if (parseInt(rating) <= 0 || parseInt(rating) >= 6) {
            alert("Please enter integer between 1 and 5");
        } else if (parseInt(rating) > 0) {
            var link = $(this).attr('href');
            console.log(link);
            console.log(rating);
            $.ajax({
                url: link,
                data: {
                    'rating': rating
                },
                dataType: 'json',
                success: function (data) {
                    if (data.success) {
                        alert("Rating successful");
                        location.reload();
                    } else {
                        alert(data.error);
                    }
                }
            });
        }
    });
    // $.fn.stars = function() {
    //     return this.each(function(i,e){$(e).html($('<span/>').width($(e).text()*16));});
    // };

    $('.stars').click(function () {
        please.hidenow.call(this);
    });
});