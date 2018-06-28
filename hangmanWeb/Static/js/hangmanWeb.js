$(document).ready(function(){

       $("#lengthButton").click(function(e){
            e.preventDefault()
			console.log('button clicked');
			$.ajax({
                url: '/hangman/newgame',
                data: $('form').serialize(),
                type: 'POST',
                success: function(response) {
                    console.log(response);
                    $('body').html(response);
                    drawCanvas();
                },
                error: function(error) {
                    console.log(error);
                }
            });
        });

        $("#guessButton").click(function(e){
            e.preventDefault()
			console.log('guess button clicked');
			$.ajax({
                url: '/hangman/guess',
                data: $('form').serialize(),
                type: 'POST',
                //dataType:'json',
                success: function(response) {
                    console.log(response);
                    $('body').html(response);
                    drawCanvas();
                },
                error: function(error) {
                    console.log(error);
                }
            });
        });
});

function drawCanvas() {
  var canvas = document.getElementById("html-canvas");
  var context = canvas.getContext("2d");

  canvas.width = canvas.clientWidth;
  canvas.height = canvas.clientHeight;
  drawFrame();
  drawHead();
  drawBody();
  drawRightHand();
  drawLeftHand()
  drawLeftFoot();
  drawRightFoot();

  context.scale(0.5,0.5);

  function drawFrame() {
  context.beginPath();
  context.moveTo(500,500);
  context.lineTo(100,500);
  context.lineTo(100,100);
  context.lineTo(500,100);
  context.lineTo(500,150);
  context.lineWidth = 6;
  context.stroke();
};

function drawHead() {
  context.beginPath();
  context.arc(500, 175, 25, 0, Math.PI*2, true);
  context.closePath();
  context.lineWidth = 4;
  context.stroke();
};

function drawBody() {
  context.beginPath();
  context.moveTo(500, 200);
  context.lineTo(500, 300);
  context.lineWidth = 4;
  context.stroke();
};

function drawRightHand() {
  context.beginPath();
  context.moveTo(450, 240);
  context.lineTo(500, 220);
  context.lineWidth = 4;
  context.stroke();
};

function drawLeftHand() {
  context.beginPath();
  context.moveTo(550, 240);
  context.lineTo(500, 220);
  context.lineWidth = 4;
  context.stroke();
};

function drawRightFoot() {
  context.beginPath();
  context.moveTo(500, 300);
  context.lineTo(525, 380);
  context.lineWidth = 4;
  context.stroke();
};

function drawLeftFoot() {
  context.beginPath();
  context.moveTo(500, 300);
  context.lineTo(475, 380);
  context.lineWidth = 4;
  context.stroke();
};

};