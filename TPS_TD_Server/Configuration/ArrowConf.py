configuration = {
	'arrow_prefab': [
		{
			'damage': {
				'health_dec': 35,
			},
			'speed': 50,  # m/s
			'duration': 2,
			'arrow_length': 2.5,
		},
		{
			'damage': {
				'health_dec': 50,
				'stun': 5,  # in seconds
			},
			'speed': 30,  # m/s
			'duration': 5,
			'arrow_length': 9,
			'attack_range': 5,
		},
	],

	'max_arrow_id_num': 100000,

	'enemy_arrow_prefab': {
		'damage': {
			'health_dec': 15,
		},
		'speed': 10,  # m/s
		'duration': 10,
		'arrow_length': 2,
	}
}
