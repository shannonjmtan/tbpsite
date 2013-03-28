<!DOCTYPE html>
<html>
	<head>
		<title>Bootstrap 101 Template</title>
		<meta name="viewport" content="width=device-width, initial-scale=1.0">
		<!-- Bootstrap -->
		<link href="css/bootstrap.min.css" rel="stylesheet" media="screen">
	</head>
	<body>
	    <div class="navbar">
    <div class="navbar-inner">
    <a class="brand" href="#">UCLA Tau Beta Pi</a>
    <ul class="nav">
    <li class="active"><a href="#">Home</a></li>
    <li><a href="#">Events</a></li>
    <li><a href="#">Requirements</a></li>
    <li><a href="#">Tutoring</a></li>
    <li><a href="#">About Us</a></li>
    <li><a href="#">Houses</a></li>
    </ul>
    </div>
    </div>


		<!--  Carousel - consult the Twitter Bootstrap docs at
      http://twitter.github.com/bootstrap/javascript.html#carousel -->
<div id="this-carousel-id" class="carousel slide"><!-- class of slide for animation -->
  <div class="carousel-inner">
    <div class="item active"><!-- class of active since it's the first item -->
      <img src="img/pic1.jpg" alt="" />
      <div class="carousel-caption">
        <p>Caption text here</p>
      </div>
    </div>
    <div class="item">
      <img src="img/pic2.jpg" alt="" />
      <div class="carousel-caption">
        <p>Caption text here</p>
      </div>
    </div>
    <div class="item">
      <img src="img/pic3.jpg" alt="" />
      <div class="carousel-caption">
        <p>Caption text here</p>
      </div>
    </div>
    <div class="item">
      <img src="img/pic4.jpg" alt="" />
      <div class="carousel-caption">
        <p>Caption text here</p>
      </div>
    </div>
  </div><!-- /.carousel-inner -->
  <!--  Next and Previous controls below
        href values must reference the id for this carousel -->
    <a class="carousel-control left" href="#this-carousel-id" data-slide="prev">&lsaquo;</a>
    <a class="carousel-control right" href="#this-carousel-id" data-slide="next">&rsaquo;</a>
</div><!-- /.carousel -->
		<h1>Hello, world!</h1>
		<script src="http://code.jquery.com/jquery.js"></script>
	<script src="js/bootstrap.min.js"></script>
	</body>
</html>
