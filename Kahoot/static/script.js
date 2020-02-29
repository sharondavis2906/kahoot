$(document).ready(function() {

// Index page

    var socket = io.connect('http://127.0.0.1:5000');

// Message to Flask when button is pressed

// Game 1 button pressed

    $('#game1').on('click', function() {
		
		/*
        var message = $('#message').val();
       */

        socket.emit('game selected', "Politics Trivia");

    });


// Game 2 button pressed

    $('#game2').on('click', function() {
		
		/*
        var message = $('#message').val();
       */

        socket.emit('game selected', "Animal Trivia");

    });


// Game 3 button pressed

    $('#game3').on('click', function() {
		
		/*
        var message = $('#message').val();
       */

        socket.emit('game selected', "Sports Trivia");

    });


// Game 4 button pressed

    $('#game4').on('click', function() {
		
		/*
        var message = $('#message').val();
       */

        socket.emit('game selected', "Music Trivia");

    });





// Message from Flask

socket.on('redirect from flask to index', function (data) {

	// Change page to "Start Page" after game selection
	
	//alert(data.url);
	
    window.location = data.url;
 
  
   /*window.location.href = "http://www.w3schools.com";*/
});


// -------------------------------------------------------------------------
// Start page

   var socket_start = io.connect('http://127.0.0.1:5000/start');


    $('#gamestart').on('click', function() {
        
		//var message = $('#message').val();

        socket_start.emit('gamestart', "Game Start");

    });


    $('#gameexit').on('click', function() {
        
		//var message = $('#message').val();

        console.log(3);

        socket_start.emit('gameexit', "Game Exit");

    });


socket_start.on('redirect from flask to start', function (data) {

	// Change page to "Start Page" after game selection
	
   
	
    window.location = data.url;

    //alert("bla");

    console.log(100);
 
  
   /*window.location.href = "http://www.w3schools.com";*/
});



// -------------------------------------------------------------------------
// Join page (enter PIN)

   var socket_join = io.connect('http://127.0.0.1:5000/join');


    $('#gamepin').on('click', function() {
        
		console.log(101);
		
		var message = $('#message').val();

        socket_join.emit('gamepin', message);

    });


 
// Message from Flask

socket_join.on('redirect from flask', function (data) {

	// Change page to "Name" if correct PIN was entered or stay on "Join" and print "wrong PIN"
	
		console.log(100);
	
    window.location = data.url;
 
  
   /*window.location.href = "http://www.w3schools.com";*/
});




// -------------------------------------------------------------------------
// Nickname page (enter name and wait for game to start)

   var socket_nickname = io.connect('http://127.0.0.1:5000/nickname');


    $('#nickname').on('click', function() {
        
		console.log(102);
		
		var message = $('#message').val();

        socket_nickname.emit('nickname', message);

    });


 
// Message from Flask

socket_nickname.on('redirect from flask', function (data) {

	// Change page to "active" once game starts or print error
	
		console.log(103);
	
    window.location = data.url;
 
  
   /*window.location.href = "http://www.w3schools.com";*/
});







    

});