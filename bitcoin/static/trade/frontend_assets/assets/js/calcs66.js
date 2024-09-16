$(function() {
    $('#calc_plan').on('change', calc);
    $('#inv_amount').bind('change keyup', calc).on('keypress', isNumberKey);

});

function isNumberKey(evt) {
    var charCode = (evt.which) ? evt.which : event.keyCode;
    if (charCode != 46 && charCode > 31 && (charCode < 48 || charCode > 57))
        return false;
    return true;
}

$('#total_return').val('Select Plan And Enter Amount');
$('#assign_per').val('Select Plan And Enter Amount');
function calc() {

    var calUrl = $('#calc_url').val();
    var plan = parseInt($('#calc_plan').val());
    var amount = parseFloat($('#inv_amount').val());
    var percent;
    var min;
    var max;
    var days;
    $.ajax({

        url: calUrl,
        type: 'POST',
        dataType: 'json',
        //cache: false,
        data: {id: plan},
        //contentType: false,
       // processData: false,
        success: function(results) {
           // let result = JSON.parse(results);
            console.log(results);
            min = parseFloat(results.min_price);
            max = parseFloat(results.max_price);
            percent = parseFloat(results.increment_amount);
            days = parseFloat(results.expiration);
            if(amount < min){
                percent = " Min $" + min;
                $('#total_return').val('Enter right figure');
                $('#assign_per').val(percent);
            }else if(amount <= max){
                $('#assign_per').val(percent + '%');
                var total = amount + ((days * amount * percent) / 100);
                $('#total_return').val('$'+total);
                $('#net_profit').val((total - amount).toFixed(2) + '$');
            }else if(amount > max){
                percent = " Max $" + max;
                $('#total_return').val('Enter right figure');
                $('#assign_per').val(percent);
            }
        }
    });
    
    


}

function limitText(limitField, limitCount, limitNum) {
    if (limitField.value.length > limitNum) {
        limitField.value = limitField.value.substring(0, limitNum);
    } else {
        limitCount.value = limitNum - limitField.value.length;
    }
}