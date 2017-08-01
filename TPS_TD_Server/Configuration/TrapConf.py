configuration = {
	'trap_prefabs': [
		{
			'attack_size_length': 6,
			'damage': {
				'health_dec': 60,
			},
			'trigger_times': 3,
			'time_between_trigger': 5,
			'trigger_range': 3,
			'cost': 100,
		},

		{
			'attack_size_length': 6,
			'damage': {
				'health_dec': 40,
				'speed_slow': 0.2,  # percentage
				'speed_slow_time': 5,
			},
			'trigger_times': 5,
			'time_between_trigger': 5,
			'trigger_range': 3,
			'cost': 150,
		}
	],
	'max_trap_id_num': 100000,

}
