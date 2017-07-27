$(document).ready(function(){
  $('.categories :checkbox').click(function(){
    $('.category_list').hide();
    $('.categories :checkbox:checked').each(function(){
      $('.' + $(this).val()).show();
    });
  });
});
