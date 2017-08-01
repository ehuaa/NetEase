configuration = {
	'enemy_prefab': [
		# attack_mode: 0->near attack 1-> remote attack
		{  # bear
			'etype': 0,
			'health': 100,
			'damage': 10,
			'attack_mode': 0,
			'time_between_attack': 1.0,  # in seconds
			'visible_range': 15,
			'attack_stop_distance': 1.5,
			'height': 2.25,
			'body_radius': 0.5,
			'kill_reward': 50,
		},
		{  # bunny
			'etype': 1,
			'health': 100,
			'damage': 10,
			'attack_mode': 0,
			'time_between_attack': 1.0,  # in seconds
			'visible_range': 15,
			'attack_stop_distance': 1.5,
			'height': 2.5,
			'body_radius': 0.6,
			'kill_reward': 50,
		},
		{  # elephant
			'etype': 2,
			'health': 200,
			'damage': 15,
			'attack_mode': 1,
			'time_between_attack': 5,  # in seconds
			'visible_range': 23,
			'attack_stop_distance': 10,
			'height': 3,
			'body_radius': 1,
			'kill_reward': 100,
		},
	],
}
