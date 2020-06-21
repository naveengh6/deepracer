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
    steering = abs(params['steering_angle'])
    progress = params['progress']

    # Initialize the reward with typical value 
    reward = 1.0

    # Set the speed threshold based your action space 
    SPEED_THRESHOLD = 2.0

    #Rewarding based on progress
    if progress == 100:
        reward += 100.0
    elif progress >= 90 and progress < 100:
        reward += 30.0
    elif progress >= 70 and progress < 90:
        reward += 10.0
    else:
        reward += 2.0

    # Calculate 3 markers that are increasingly further away from the center line
    marker_1 = 0.1 * track_width
    marker_2 = 0.25 * track_width
    marker_3 = 0.5 * track_width

    # Give higher reward if the car is closer to center line and vice versa
    if distance_from_center <= marker_1:
        reward += 10
    elif distance_from_center <= marker_2:
        reward += 5
    elif distance_from_center <= marker_3:
        reward += 1
    else:
        reward -= 10  # likely crashed/ close to off track

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
    if direction_diff > 5:
        if is_left_of_center:
            #Reward if on the left side
            reward += 1.0
        else:
            #Penalize if on the right side
            reward *= 0.3
    #Reward or penalize whether car is on right side of the track when turning right
    elif direction_diff < 5:
        if not is_left_of_center:
            #Reward if on the right side
            reward += 1.0
        else:
            #Penalize if on the left side
            reward *= 0.3
    else:
        if distance_from_border >= 0.05:
            #Reward if maintaining the distance from border
            reward += 2.0
        else:
            #Penalizing if too close to the border
            reward *= 0.3

    if not all_wheels_on_track:
        # Penalize if the car goes off track
        reward *= 0.35
    
    if speed < (SPEED_THRESHOLD * 0.8):
        # Penalize if the car goes too slow
        reward *= 0.5
    else:
        # High reward if the car stays on track and goes fast
        reward += 10.0

    # Penalize if car steer too much to prevent zigzag
    ABS_STEERING_THRESHOLD = 20.0
    if steering > ABS_STEERING_THRESHOLD:
        reward *= 0.8

    return reward