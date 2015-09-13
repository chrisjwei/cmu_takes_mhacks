$(window).scroll(function() {
	var scrollTop = $(this).scrollTop();
	var newTop = Math.max(scrollTop,50)
	var currTop = $('.robot').position().top;
	var time = 50;
	$('.robot').animate({ top: newTop }, time);
});

$( document ).ready(function() {
	$("a.article-title").click(function() {
		$(this).parent().parent().addClass("read");
	});
});

$.ajaxSetup({
   contentType: "application/json; charset=utf-8"
});

function updateScrollLocation(){
	$('#robot-output').scrollTop($('#robot-output')[0].scrollHeight);
}

function readInput(){
	var inputMsg = $('#robot-input').val();
	$('#robot-input').val('');
	//parseInput(inputMsg);
	mlParseInput(inputMsg);
}

function mlParseInput(msg){
	var token;
	msg = cleanMsg(msg);
	var arr = msg.split(" ");
	var tokens = ["label", "giggles", "filtering", "information", "is", "results", "related", "Content", "have", "data", "information", "hackathons", "no", "friends", "update", "undo", "content", "to", "hi", "news", "articles", "on", "i", "refresh", "hey", "reload", "stories", "remove", "new", "news", "with", "hello", "delete", "articles", "about", "tired", "of", "get", "bot", "filter", "erase", "charlie", "where"];
	var flags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0];
	for (var i = 0; i < tokens.length; i++){
		token = tokens[i];
		if (arr.indexOf(token) != -1){
			flags[i] = 1;
		}
	}
	var postData = {
  Inputs: {
    input1: {
      ColumnNames: [
        "label",
        "giggles",
        "filtering",
        "Information",
        "is",
        "results",
        "related",
        "Content",
        "have",
        "data",
        "information",
        "hackathons",
        "no",
        "friends",
        "Update",
        "Undo",
        "content",
        "to",
        "Hi",
        "News",
        "Articles",
        "on",
        "I",
        "Refresh",
        "Hey",
        "Reload",
        "Stories",
        "Remove",
        "new",
        "news",
        "with",
        "Hello",
        "Delete",
        "articles",
        "about",
        "Tired",
        "of",
        "Get",
        "bot",
        "filter",
        "Erase",
        "charlie",
        "where"
      ],
      Values: [
        [
          "0",
          "0",
          "0",
          "0",
          "0",
          "0",
          "0",
          "0",
          "0",
          "0",
          "0",
          "0",
          "0",
          "0",
          "0",
          "0",
          "0",
          "0",
          "0",
          "0",
          "0",
          "0",
          "0",
          "0",
          "0",
          "0",
          "0",
          "0",
          "0",
          "0",
          "0",
          "0",
          "0",
          "0",
          "0",
          "0",
          "0",
          "0",
          "0",
          "0",
          "0",
          "0",
          "0"
        ]
      ]
    }
  },
  GlobalParameters: {}
};
	var request = new XMLHttpRequest();
	request.onreadystatechange= function () {
	    if (request.readyState==4) {
	        console.log(request)
	    }
	}

	request.open("POST", secret, true);
	request.setRequestHeader("Authorization", "Bearer "+secret2);
	request.setRequestHeader("Content-Type","application/json");
	request.setRequestHeader("Accept","application/json");
	request.send(JSON.stringify(postData));

	/*var commandType = getWhatIWant(jsonCallback); // 0 - unknown command, 1 - refresh, 2 - filter, 3 -remove filter
	if (commandType == 2 || commandType == 3){
		keyword = getKeyword(arr);
	}
	execute(commandType,keyword);*/
}









function parseInput(msg){
	msg = cleanMsg(msg)
	var keyword = ''; // only relevant for commandType 2
	var arr = msg.split(" ");
	var commandType = getCommandType(arr); // 0 - unknown command, 1 - refresh, 2 - filter, 3 -remove filter
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
		if (word == 'filter' || word == 'by'){
			return 2;
		}
		if (word == 'where') {
			return 4;
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
		case 4:
			output.html("Finding incidents you can help");
			$.ajax({
				  url: '/filter',
				  data: {'type_of_filter' : 'incidents'},
				  success: function(response) {
				  		var newDoc = document.open("text/html", "replace");
				  		console.log(response)
						newDoc.write(response);
						newDoc.close();
				  }
				});
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