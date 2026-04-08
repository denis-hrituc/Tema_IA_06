

import random
import time
from enum import Enum
from coppeliasim_zmqremoteapi_client import RemoteAPIClient

V_FORWARD = 2.0
V_BACKWARD = -1.5
V_TURN = 2.0

STOP_DISTANCE = 0.45
FRONT_SENSORS = [2, 3, 4, 5]
SENSOR_MAX = 1.0

BACKWARD_TIME = 1.0
TURN_TIME = 1.5


class RobotState(Enum):
    FORWARD = "FORWARD"
    BACKWARD = "BACKWARD"
    TURNING = "TURNING"


def min_front_distance(sim, sensors):
    min_dist = SENSOR_MAX

    for idx in FRONT_SENSORS:
        result, dist, *_ = sim.readProximitySensor(sensors[idx])

        if result:
            min_dist = min(min_dist, dist)

    return min_dist


def set_speed(sim, left_motor, right_motor, vl, vr):
    sim.setJointTargetVelocity(left_motor, vl)
    sim.setJointTargetVelocity(right_motor, vr)


def next_state(state, dist_front, now, state_until):
    if state == RobotState.FORWARD:
        if dist_front < STOP_DISTANCE:
            return RobotState.BACKWARD, now + BACKWARD_TIME
        return RobotState.FORWARD, state_until

    elif state == RobotState.BACKWARD:
        if now >= state_until:
            return RobotState.TURNING, now + TURN_TIME
        return RobotState.BACKWARD, state_until

    elif state == RobotState.TURNING:
        if now >= state_until:
            return RobotState.FORWARD, state_until
        return RobotState.TURNING, state_until


def main():
    client = RemoteAPIClient()
    sim = client.require('sim')

    left_motor = sim.getObject('/PioneerP3DX/leftMotor')
    right_motor = sim.getObject('/PioneerP3DX/rightMotor')
    sensors = [sim.getObject(f'/PioneerP3DX/ultrasonicSensor[{i}]') for i in range(16)]

    state = RobotState.FORWARD
    state_until = 0.0
    turn_dir = 1

    sim.startSimulation()
    print("Tema A pornita. Ctrl+C pentru oprire.")

    try:
        while True:
            now = sim.getSimulationTime()
            dist_front = min_front_distance(sim, sensors)

           
            new_state, new_until = next_state(state, dist_front, now, state_until)

           
            if state != RobotState.TURNING and new_state == RobotState.TURNING:
                turn_dir = random.choice([-1, 1])

            state = new_state
            state_until = new_until

           
            if state == RobotState.FORWARD:
                set_speed(sim, left_motor, right_motor, V_FORWARD, V_FORWARD)

            elif state == RobotState.BACKWARD:
                set_speed(sim, left_motor, right_motor, V_BACKWARD, V_BACKWARD)

            elif state == RobotState.TURNING:
                if turn_dir > 0:
                    set_speed(sim, left_motor, right_motor, -V_TURN, +V_TURN)
                else:
                    set_speed(sim, left_motor, right_motor, +V_TURN, -V_TURN)

            print(f"state={state.value:<8} front={dist_front:.3f}m")

            time.sleep(0.05)

    except KeyboardInterrupt:
        print("\nOprire manuala.")
    finally:
        set_speed(sim, left_motor, right_motor, 0.0, 0.0)
        sim.stopSimulation()


if __name__ == '__main__':
    main()