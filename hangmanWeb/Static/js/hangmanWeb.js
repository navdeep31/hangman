$(document).ready(function(){

       $("#lengthButton").click(function(e){
            e.preventDefault()
			console.log('button clicked');
			$.ajax({
			    /*if ($('#lengthBox') < 3 || $('#lengthBox') > 10) {
			        alert('Enter Word Length between 3 and 10');
			    } else {*/
                    url: '/hangman/newgame',
                    data: $('#lengthBox').serialize(),
                    type: 'POST',
                    success: function(response) {
                        console.log(response);
                        $('body').html(response);
                        drawCanvas();
                    },
                    error: function(error) {
                        console.log(error);
                    }
                //}
            });
        });

        $('body').on('click', '#guessButton', function(e) {
            //alert("Clicked the guess! ");
            e.preventDefault()
            console.log('guess button clicked');
            $.ajax({
                url: '/hangman/guess',
                data: $('#guessBox').serialize(),
                type: 'POST',
                //dataType:'json',
                success: function(response) {
                    console.log(response);
                    $('body').html(response);
                    var livesRemaining = parseInt($('#livesRemaining').text());
                    console.log(livesRemaining)
                    drawCanvas(livesRemaining);
                },
                error: function(error) {
                    console.log(error);
                }
            });
        });
});

function drawCanvas(livesRemaining) {
  var canvas = document.getElementById("html-canvas");
  var context = canvas.getContext("2d");

  canvas.width = canvas.clientWidth;
  canvas.height = canvas.clientHeight;

  switch (livesRemaining){
    case 9:
        drawFrame(livesRemaining);
        break;
    case 8:
        drawFrame(livesRemaining);
        break;
    case 7:
        drawFrame(livesRemaining);
        break;
    case 6:
        drawFrame(livesRemaining);
        break;
    case 5:
        drawFrame(6);
        drawHead();
        break;
    case 4:
        drawFrame(6);
        drawHead();
        drawBody();
        break;
    case 3:
        drawFrame(6);
        drawHead();
        drawBody();
        drawLeftHand();
        break;
    case 2:
        drawFrame(6);
        drawHead();
        drawBody();
        drawLeftHand();
        drawRightHand();
        break;
    case 1:
        drawFrame(6);
        drawHead();
        drawBody();
        drawLeftHand();
        drawRightHand();
        drawLeftFoot();
        break;
    case 0:
        drawFrame(6);
        drawHead();
        drawBody();
        drawLeftHand();
        drawRightHand();
        drawLeftFoot();
        drawRightFoot();
        break;
    default:
        break;
    }

//  drawFrame();
//  drawHead();
//  drawBody();
//  drawRightHand();
//  drawLeftHand()
//  drawLeftFoot();
//  drawRightFoot();

  context.scale(0.5,0.5);

  function drawFrame(livesRemaining) {
  context.beginPath();
  context.moveTo(400,400);
  switch(livesRemaining){
    case (9):
        context.lineTo(100,400);
        break;
    case (8):
        context.lineTo(100,400);
        context.lineTo(100,100);
        break;
    case (7):
        context.lineTo(100,400);
        context.lineTo(100,100);
        context.lineTo(400,100);
        break;
    case (6):
        context.lineTo(100,400);
        context.lineTo(100,100);
        context.lineTo(400,100);
        context.lineTo(400,150);
        break;
  }

  context.lineWidth = 6;
  context.stroke();
};

function drawHead() {
  context.beginPath();
  context.arc(400, 175, 25, 0, Math.PI*2, true);
  context.closePath();
  context.lineWidth = 4;
  context.stroke();
};

function drawBody() {
  context.beginPath();
  context.moveTo(400, 200);
  context.lineTo(400, 300);
  context.lineWidth = 4;
  context.stroke();
};

function drawRightHand() {
  context.beginPath();
  context.moveTo(350, 240);
  context.lineTo(400, 220);
  context.lineWidth = 4;
  context.stroke();
};

function drawLeftHand() {
  context.beginPath();
  context.moveTo(450, 240);
  context.lineTo(400, 220);
  context.lineWidth = 4;
  context.stroke();
};

function drawRightFoot() {
  context.beginPath();
  context.moveTo(400, 300);
  context.lineTo(425, 380);
  context.lineWidth = 4;
  context.stroke();
};

function drawLeftFoot() {
  context.beginPath();
  context.moveTo(400, 300);
  context.lineTo(375, 380);
  context.lineWidth = 4;
  context.stroke();
};

};

//$("#guessButton").click(function(e){
//          e.preventDefault()
//			console.log('guess button clicked');
//			$.ajax({
//                url: '/hangman/guess',
//                data: $('#guessBox').serialize(),
//                type: 'POST',
//                //dataType:'json',
//                success: function(response) {
//                    console.log(response);
//                    $('body').html(response);
//                    drawCanvas();
//                },
//                error: function(error) {
//                    console.log(error);
//                }
//            });
//        });

//$('#body').on('click', '#guessButton', function(e) {
//    alert("Clicked the guess! ");
//    e.preventDefault()
//    console.log('guess button clicked');
//    $.ajax({
//        url: '/hangman/guess',
//        data: $('#guessBox').serialize(),
//        type: 'POST',
//        //dataType:'json',
//        success: function(response) {
//            console.log(response);
//            $('body').html(response);
//            drawCanvas();
//        },
//        error: function(error) {
//            console.log(error);
//        }
//    });
//});