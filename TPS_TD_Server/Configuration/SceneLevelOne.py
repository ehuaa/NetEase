configuration = {
	'scene_map_filename': "Configuration/SceneLevelOneMap.txt",
	'player_born_rotation': [0, 90, 0],
	'player_born_positions': [
		[10, 0, 5],
		[10, 0, 15],
		[10, 0, 25],
		[10, 0, 35],
		[10, 0, 45],
	],
	'target_position': [6, 0, 25],  # enemy target position

	'enemy_spawn_transforms': [
		[90, 0, 5, 0, -90, 0],  # position and rotation
		[90, 0, 15, 0, -90, 0],  # position and rotation
		[90, 0, 25, 0, -90, 0],  # position and rotation
		[90, 0, 35, 0, -90, 0],  # position and rotation
		[90, 0, 45, 0, -90, 0],  # position and rotation
	],
	'enemy_spawn_time': 1.5,  # spawn an enemy every 1 second
	'enemy_spawn_distribution': [0.4, 0.4, 0.2],
	'enemy_move_speed': 10,  # m/s
	'max_escape_enemies_num': 10,
	'enemy_escape_range': 1.5,

	'enemy_group_num': [3, 7, 10],
	'time_between_enemy_group': 5,  # in seconds

	# arrow
	'arrow_update_time': 0.005,  # update arrow behavior time

	# trap
	'trap_update_time': 0.05,  # update arrow behavior time

}
