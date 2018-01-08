$(document).ready(function(){
	//Add and Remove .active to nav-link
	$('a.nav-item').removeClass('active');
	var title = $('title').text();
	var current = $(location).attr('href');
	if(title.search('-') < 0 || current.search('blog/') >= 0){
		$('#home').addClass('active');
	} else if(current.search('myaccount/') >= 0) {
		$('#myaccount').addClass('active');
	} else if(current.search('post/') >= 0){
		$('#postnew').addClass('active');
	};

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
	$('[data-toggle=tooltip]').tooltip();
});