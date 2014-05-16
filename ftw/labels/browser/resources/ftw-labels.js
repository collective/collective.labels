$(document).ready(function(){

    $('.colorBox').click(function() {
        // reset all selected
        $(this).closest('form').find('.colorBox').removeClass('selected')
        $(this).toggleClass('selected');
        $(this).closest('form').find('input[name=color]').val($(this).attr("color-picker"))
     });

});
