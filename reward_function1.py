import math

def reward_function(params):
    
    # Read input variables
    waypoints = params['waypoints']
    closest_waypoints = params['closest_waypoints']
    heading = params['heading']
    is_left_of_center = params['is_left_of_center']
    distance_from_center = params['distance_from_center']
    track_width = params['track_width']
    speed = params['speed']
    all_wheels_on_track = params['all_wheels_on_track']


    # Initialize the reward with typical value 
    reward = 1.0

    # Set the speed threshold based your action space 
    SPEED_THRESHOLD = 1.0 

    # Calculate the direction of the center line based on the closest waypoints
    next_point = waypoints[closest_waypoints[1]]
    prev_point = waypoints[closest_waypoints[0]]

    # Calculate the direction in radius, arctan2(dy, dx), the result is (-pi, pi) in radians
    track_direction = math.atan2(next_point[1] - prev_point[1], next_point[0] - prev_point[0]) 
    # Convert to degree
    track_direction = math.degrees(track_direction)

    # Calculate the distance from each border
    distance_from_border = 0.5 * track_width - distance_from_center

    #Calculate the direction difference between track and car
    direction_diff = track_direction - heading if heading > 0 else (360 + heading)

    # Calculate the absolute difference between the track direction and the heading direction of the car
    abs_direction_diff = abs(track_direction - heading)
    if abs_direction_diff > 180:
        abs_direction_diff = 360 - abs_direction_diff

    # Penalize the reward if the difference is too large
    DIRECTION_THRESHOLD = 10.0
    if abs_direction_diff > DIRECTION_THRESHOLD:
        reward *= 0.5
    
    #Reward or penalize whether car is on left side of the track when turning left
    if direction_diff > 10:
        if is_left_of_center:
            reward += 1.0
        else:
            reward *= 0.3
    elif direction_diff < 10:
        #Reward or penalize whether car is on right side of the track when turning right
        if not is_left_of_center:
            reward += 1.0
        else:
            reward *= 0.3
    else:
        if distance_from_border >= 0.05:
            reward += 1.0
        else:
            reward -= 1e-3

    if not all_wheels_on_track:
        # Penalize if the car goes off track
        reward -= 1e-3
    elif speed < (SPEED_THRESHOLD * 0.8):
        # Penalize if the car goes too slow
        reward = 0.5
    else:
        # High reward if the car stays on track and goes fast
        reward += 1.0

    return reward