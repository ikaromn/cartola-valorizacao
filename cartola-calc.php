<?php
	$name = $_GET['name-player'];
	$valuePlayer = $_GET['coust-value'];
	$lastPont = $_GET['last-pontuation'];

	function valorizationPlayer($player_name, $player_price,$player_pontuation){
		$y = ($player_price / 100) * 37;
		$z = $y * 2;
		$total_points = $z - $player_pontuation;
		return 'O jogador ' . $player_name . ' precisa fazer ' . $total_points . ' para valorizar';
	}
	$value = valorizationPlayer($name,$valuePlayer,$lastPont);
	echo $value;
?>