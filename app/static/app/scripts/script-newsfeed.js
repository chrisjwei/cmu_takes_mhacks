function readInput(){
	var inputMsg = $('#robot-input').val();
	$('#robot-input').val('');
	parseInput(inputMsg);
}

function parseInput(msg){
	msg = cleanMsg(msg)
	var keyword = ''; // only relevant for commandType 2
	var arr = msg.split(" ");
	var commandType = getCommandType(arr); // 0 - unknown command, 1 - refresh, 2 - filter
	if (commandType == 2 || commandType == 3){
		keyword = getKeyword(arr);
	}
	execute(commandType,keyword);
}

function cleanMsg(msg){
	var msg1 = msg.replace(/[.,-\/#!$%\^&\*;:{}=\-_`~()]/g,""); // remove punctuation
	return msg1;
}

function getCommandType(arr){
	var i;
	var prevWord;
	var word;
	for (i = 0; i < arr.length; i++){
		word = arr[i].toLowerCase();
		/* here are some definitively refresh based words*/
		if (word == 'refresh' || word == 'reload' || word == 'update' || word == 'restock'){
			return 1;
		}
		if (word == 'new' || word == 'update' || word == 'updates' && i > 0){
			prevWord = arr[i-1].toLowerCase();
			if (prevWord == 'load' || prevWord == 'show' || prevWord == 'get' || prevWord == 'display' || prevWord == 'me'){
				return 1;
			}
			if (i > 1){
				prevWord = arr[i-2].toLowerCase();
				if (prevWord == 'give'){
					return 1;
				}
			}
		}
		if (word == 'remove' && i < arr.length-1 && arr[i+1].toLowerCase() == 'filter'){
			return 3;
		}
		if (word == 'filter' || word == 'where' || word == 'by'){
			return 2;
		}
		if (i > 0 ) {
			prevWord = arr[i-1].toLowerCase();
			if (prevWord == 'load' || prevWord == 'show' || prevWord == 'get' || prevWord == 'display'){
				if (word != 'new'){
					if (word != 'me'){
						return 2;
					}
				}
			}
		}
	}
	return 0;
}

function getKeyword(arr){
	var keywordArr=[];
	for (i = 0; i < arr.length-1; i++){
		word = arr[i].toLowerCase();
		if (word == 'about' || word == 'by' || word == 'to'
			|| word == 'for' || word == 'at' || word == 'in' 
			|| word == 'from' || word == 'like' || word == 'on' 
			|| word == 'with'){
			keywordArr = arr.slice(i+1);
		}
	}
	return keywordArr.join(" ");
}

function execute(commandType,keyword){
	var output = $('#robot-output');
	switch(commandType){
		case 0:
			output.html("I don't understand your command :(");
			break;
		case 1:
			output.html("Fetching new stories for you");
			refresh();
			break;
		case 2:
			output.html("Applying filter: " + keyword);
			applyFilter(keyword);
			break;
		case 3:
			output.html("Removing filter: " + keyword);
			removeFilter(keyword);
			break;
		default: throw 'Unsupported commandType';
	}
}

function refresh(){
	return;
}

function applyFilter(keyword){
	return;
}

function removeFilter(keyword){
	return;
}