const area = document.querySelector('#id_content');
let start = area.selectionStart;
let end = area.selectionEnd;
const editor = ace.edit('editor');
ace.config.set('basePath', 'https://devjunior.com/static/js/ace/src-noconflict');
ace.config.set('modePath', 'https://devjunior.com/static/js/ace/src-noconflict');
ace.config.set('themePath', 'https://devjunior.com/static/js/ace/src-noconflict');
let langSelect = document.querySelector('#lang');
editor.setTheme("ace/theme/clouds");

function getPos(){
	start = area.selectionStart;
	end = area.selectionEnd;
	return start, end;
};

area.addEventListener('mouseup', getPos);
area.addEventListener('keyup', getPos);

$('#bold').click(function(){
	if(start==end){
		area.value = area.value.slice(0,start) + '[b][/b]' + area.value.slice(start,area.value.length);
	} else {
		area.value = area.value.slice(0,start) + '[b]' + area.value.slice(start,end) + '[/b]' + area.value.slice(end,area.value.length);
	};
});

$('#line').click(function(){
	if(start==end){
		area.value = area.value.slice(0,start) + '\n[line]\n' + area.value.slice(start,area.value.length);
	} else {
		area.value = area.value.slice(0,start) + '\n[line]\n' + area.value.slice(end,area.value.length);
	};
});

$('#url').click(function(){
	if(start==end){
		area.value = area.value.slice(0,start) + '[url][/url]' + area.value.slice(start,area.value.length);
	} else {
		area.value = area.value.slice(0,start) + '[url]' + area.value.slice(start,end) + '[/url]' + area.value.slice(end,area.value.length);
	};
});

$('#img').click(function(){
	if(start==end){
		area.value = area.value.slice(0,start) + '\n[img][/img]\n' + area.value.slice(start,area.value.length);
	} else {
		area.value = area.value.slice(0,start) + '\n[img]' + area.value.slice(start,end) + '[/img]\n' + area.value.slice(end,area.value.length);
	};
});

$('#kbd').click(function(){
	if(start==end){
		area.value = area.value.slice(0,start) + '[kbd][/kbd]' + area.value.slice(start,area.value.length);
	} else {
		area.value = area.value.slice(0,start) + '[kbd]' + area.value.slice(start,end) + '[/kbd]' + area.value.slice(end,area.value.length);
	}
});

$('#snippet').click(function(){
	editor.setValue('');
	$('#snippetModal').modal('show');

	function setLang(){
    	let lang = this.value;
    	editor.getSession().setMode('ace/mode/'+lang);
    	if(lang=='html'){
    		$('#htmlEscape').removeClass('d-none');
    		$('#htmlEscape').click(function(){
    			let temp = editor.getValue();
    			tempList = temp.split('\n');
    			let newTemp = [];
    			let line;
    			for(i=0;i<tempList.length;i++){
	    			tempList[i] = tempList[i].replace(/</g, '&lt;');
	    			tempList[i] = tempList[i].replace(/>/g, '&gt;');
	    			newTemp.push(tempList[i]);
    			};
    			editor.setValue(newTemp.join('\n'));
    		});
    	} else {
    		$('#htmlEscape').addClass('d-none');
    	};
	};
	
	langSelect.addEventListener('change', setLang);

});

$('#snippetButton').click(function(){
	area.value += '\n[snippet]' + editor.getValue() + '\n[/snippet]\n';
});

$('#delete').click(function(){
	$('#deleteModal').modal('show');
});

$('#photo_upload-clear_id').addClass('ml-1');
$('[for=photo_upload-clear_id]').addClass('ml-4');