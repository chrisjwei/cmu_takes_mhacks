var $win = $(window);

function resize_main_box(){
	var box = $("#main-box")
	box.css('position', 'relative');
	box.css('top', $win.height()*(3/8));
}

$( document ).ready(function() {
  resize_main_box();
  $(".selector").select2({
  	placeholder: "Select an organization",
  	allowClear: true
  });
});

$win.on('resize',function(){
	resize_main_box();
});