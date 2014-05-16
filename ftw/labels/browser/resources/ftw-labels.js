$(document).ready(function(){

    $('.colorBox').click(function() {
        // reset all selected
        $(this).closest('form').find('.colorBox').removeClass('selected');
        $(this).toggleClass('selected');
        $(this).closest('form').find('input[name=color]').val($(this).attr("data-color"));
     });

    $('.labelItem').click(function() {
        $(this).toggleClass('selected');
        $(this).toggleClass(
            'labelcolor-' + $(this).find('.labelColor').attr('data-color'));

     });

    $('.labelListing .edit-label-link').prepOverlay({
        subtype: 'ajax',
        width: '500px',
        noform: function(el) {return $.plonepopups.noformerrorshow(el, 'close');}
    });

    $('.toggleManageLabeling').click(function() {
        $('.updateLabeling').slideToggle()
        $('.activeLabels').slideToggle()
     });

});
