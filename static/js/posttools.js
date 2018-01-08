$(document).ready(function(){
	//bold
	$('#bold').click(function(){
		$('#boldModal').modal('show');
	});
	$('#boldButton').click(function(){
		var temp = $('#id_content').val();
		$('#id_content').val(temp + ' <b>' + $('#boldContent').val() + '</b> ');
		$('#boldContent').val('');
	});

	//line
	$('#line').click(function(){
		var temp = $('#id_content').val();
		$('#id_content').val(temp + "\n<hr>\n");
	})

	//url
	$('#url').click(function(){
		$('#urlModal').modal('show');
	});
	$('#urlButton').click(function(){
		var temp = $('#id_content').val();
		$('#id_content').val(
			temp + ' <a href="' + $('#urlContent').val() + '" target="_blank">' + $('#urlTitle').val() +'</a> '
			);
		$('#urlContent').val('');
		$('#urlTitle').val('');
	});

	//img
	$('#img').click(function(){
		$('#imgModal').modal('show');
	});
	$('#imgButton').click(function(){
		var temp = $('#id_content').val();
		$('#id_content').val(temp + '\n<img src="' + $('#imgContent').val() + '" class="img-thumbnail">\n');
		$('#imgContent').val('');
	})

	//kbd
	$('#kbd').click(function(){
		$('#kbdModal').modal('show');
	});
	$('#kbdButton').click(function(){
		var temp = $('#id_content').val();
		$('#id_content').val(temp + ' <code>' + $('#kbdContent').val() + '</code> ');
		$('#kbdContent').val('');
	});

	//snippet
	$('#snippet').click(function(){
		var editor = ace.edit('editor');
		var langSelect = document.getElementById('lang');
    	var snippetButton = document.getElementById('snippetButton')
    	editor.setTheme("ace/theme/clouds");
		$('#snippetModal').modal('show');
		editor.setValue('');
		
		function setLang(){
	    	var lang = this.value;
	    	var mode = 'ace/mode/' + lang;
	    	editor.getSession().setMode(mode);
	    	if(lang =='html'){
	    		
	    		$('#htmlEscape').toggleClass('d-none');
	    		$('#htmlEscape').toggleClass('d-inline-block');

    			$('#htmlEscape').click(function(){
    				editor.findAll('<');
    				editor.replaceAll('&lt;');
    				editor.findAll('>');
    				editor.replaceAll('&gt;');
    			});
    		} else {
    			$('#htmlEscape').removeClass('d-inline-block');
    			if($('#htmlEscape').hasClass('d-none') == false){
    				$('#htmlEscape').addClass('d-none')
    			}
    		};
    	};
    	
    	langSelect.addEventListener('change', setLang);
	});

	$('#snippetButton').click(function(){
		var editor = ace.edit("editor");
		var temp = $('#id_content').val();
		var code = editor.getValue();
		$('#id_content').val(temp + '\n<pre class="prettyprint">\n' + code + '\n</pre>\n');
	});
	
})