$(document).ready(function(){
  $('.categories :checkbox').click(function(){
    $('.category_list').hide();
    $('.categories :checkbox:checked').each(function(){
        console.log($('.categories :checkbox:checked').val())
      $('.' + $(this).val()).show();
    });
  });
  $('.categories :checkbox').click(function(){
  if ($('.categories :checkbox').filter(':checked').length === 0){
    $('.category_list').show();
  }});
});
