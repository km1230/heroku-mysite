$(document).ready(function(){
	//Add and Remove .active to nav-link
	$('a.nav-link').removeClass('active');
	var title = $('title').text();
	var current = $(location).attr('href');
	if(current.search('post_tag') >= 0){
		$('#categories').addClass('active')
	} else if(current.search('archives')>=0){
		$('#archives').addClass('active')
	} else if(current.search('myaccount/') >= 0) {
		$('#myaccount').addClass('active')
	} else if(current.search('post/') >= 0){
		$('#postnew').addClass('active')
	} else if(current.search('register') >= 0){
		$('#signup').addClass('active')
	} else if(current.search('login') >= 0){
		$('#login').addClass('active')
	} else {
		$('#home').addClass('active')
	};
	;

	//Add .form-control to input
	$('input').addClass('form-control');
	$('input:file').addClass('form-control-file');
	$('input:checkbox').removeClass('form-control');
	$('input:checkbox').addClass('form-check-input');
	$('input:checkbox').parents('ul').addClass('tagfield');
	$('input:checkbox').parents('label').addClass('form-check-label');
	$('input:checkbox').parents('li').addClass('d-inline p-3');
	$('textarea').addClass('form-control');
	$('select').addClass('custom-select');
	$('#dob').children().addClass('col');

	//enable tooltip
	var tooltip = $('[data-toggle="tooltip"]');
	var tooltipTemplate = `<div class='tooltip'>
							<div class='tooltip-inner bg-secondary'>
							</div>
							</div>`;
	tooltip.attr('data-template',tooltipTemplate);
	tooltip.tooltip();

	//re-arrange col
	if($(document).width() < 992){
		$('.sidebar').addClass('order-first')
	}
	window.addEventListener('resize', ()=>{
		if($(document).width() > 992){
			$('.sidebar').removeClass('order-first')
		} else {
			$('.sidebar').addClass('order-first')
		};
	});

});