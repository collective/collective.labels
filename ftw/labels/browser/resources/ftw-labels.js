$(document).ready(function(){

  $('.colorBox').click(function() {
    // reset all selected
    $(this).closest('form').find('.colorBox').removeClass('selected');
    $(this).toggleClass('selected');
    $(this).closest('form').find('input[name=color]').val($(this).data("color"));
  });

  $('.labelItem').click(function() {
    if(typeof(tabbedview) == undefined) {
      return;
    }

    $(this).toggleClass('selected');
    $(this).toggleClass(
      'labelcolor-' + $(this).find('.labelColor').data('color'));

    var labels_prop;
    if (tabbedview.prop('labels')) {
      labels_prop = tabbedview.prop('labels').split(',');
    } else {
      labels_prop = [];
    }

    if($(this).hasClass('selected')) {
      labels_prop.push($(this).data('label-id'));
    } else {
      labels_prop.remove($(this).data('label-id'));
    }

    tabbedview.prop('labels', labels_prop.join(','));
    // tabbedview.prop('labels', $(this).data('label-id'));
    tabbedview.reload_view();
  });

  $('.labelListing .edit-label-link').prepOverlay({
    subtype: 'ajax',
    width: '235px',
    noform: function(el) {return $.plonepopups.noformerrorshow(el, 'close');}
  });

  $('.toggleManageLabeling').click(function() {
    $('.updateLabeling').slideToggle();
    $('.activeLabels').slideToggle();
  });

});
