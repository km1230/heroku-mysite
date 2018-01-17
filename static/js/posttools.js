$(document).ready(function(){
	//bold
	$('#bold').click(function(){
		$('#boldModal').modal('show');
	});
	$('#boldButton').click(function(){
		var temp = $('#id_content').val();
		$('#id_content').val(temp + ' `bold`' + $('#boldContent').val() + '`endbold` ');
		$('#boldContent').val('');
	});

	//line
	$('#line').click(function(){
		var temp = $('#id_content').val();
		$('#id_content').val(temp + "\n`line`\n");
	})

	//url
	$('#url').click(function(){
		$('#urlModal').modal('show');
	});
	$('#urlButton').click(function(){
		var temp = $('#id_content').val();
		$('#id_content').val(
			temp + ' `url`' + $('#urlContent').val() + '`midurl`' + $('#urlTitle').val() +'`endurl` '
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
		$('#id_content').val(temp + '\n`img`' + $('#imgContent').val() + '`endimg`\n');
		$('#imgContent').val('');
	})

	//kbd
	$('#kbd').click(function(){
		$('#kbdModal').modal('show');
	});
	$('#kbdButton').click(function(){
		var temp = $('#id_content').val();
		$('#id_content').val(temp + ' `kbd`' + $('#kbdContent').val() + '`endkbd` ');
		$('#kbdContent').val('');
	});

	//snippet
	$('#snippet').click(function(){
		var editor = ace.edit('editor');
		ace.config.set('basePath', 'http://www.devjunior.com/static/js/ace/src-noconflict');
		ace.config.set('modePath', 'http://www.devjunior.com/static/js/ace/src-noconflict');
		ace.config.set('themePath', 'http://www.devjunior.com/static/js/ace/src-noconflict');
		var langSelect = document.getElementById('lang');
    	var snippetButton = document.getElementById('snippetButton')
    	editor.setTheme("ace/theme/clouds");
		$('#snippetModal').modal('show');
		editor.setValue('');
		
		function setLang(){
	    	var lang = this.value;
	    	var mode = 'ace/mode/' + lang;
	    	editor.getSession().setMode(mode);
    	};
    	
    	langSelect.addEventListener('change', setLang);
	});

	$('#snippetButton').click(function(){
		var editor = ace.edit("editor");
		var temp = $('#id_content').val();
		var code = editor.getValue();
		$('#id_content').val(temp + '\n`snippet`\n' + code + '\n`endsnippet`\n');
	});

	//delete
	$('#delete').click(function(){
		$('#deleteModal').modal('show');
	})	
})