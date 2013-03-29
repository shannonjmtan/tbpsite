<?php if (!isset($_POST['email'])) header('Location: http://tbp.seas.ucla.edu/index.php'); ?>
<!DOCTYPE html>
<meta charset="utf-8">
<title>UCLA Tau Beta Pi</title>
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<!-- Bootstrap -->
<link href="css/bootstrap.min.css" rel="stylesheet" media="screen">

<?php include('php/navbar.php'); ?>
<div class="container">
<?php echo "Welcome " + strip_tags($_POST['email']); ?>
</div>
<script src="http://code.jquery.com/jquery.js"></script>
<script src="js/bootstrap.min.js"></script>
