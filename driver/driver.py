from tmc_driver.tmc_2209 import *

# TMC2209 config
UART_PORT = "/dev/serial0"
ENABLE_PIN = 21
MOTION_CONTROL_PIN0 = 16
MOTION_CONTROL_PIN1 = 20

# Starter code from
# https://github.com/Chr157i4n/PyTmcStepper
def main():
    tmc = Tmc2209(TmcEnableControlPin(ENABLE_PIN), TmcMotionControlStepDir(MOTION_CONTROL_PIN0, MOTION_CONTROL_PIN1), TmcComUart(UART_PORT))

    tmc.set_direction_reg(False)
    tmc.set_current(300)
    tmc.set_interpolation(True)
    tmc.set_spreadcycle(False)
    tmc.set_microstepping_resolution(2)
    tmc.set_internal_rsense(False)

    tmc.set_acceleration(2000)
    tmc.set_max_speed(500)

    tmc.set_motor_enabled(True)

    tmc.run_to_position_steps(400)
    tmc.run_to_position_steps(0)

    tmc.set_motor_enabled(False)

if __name__ == "__main__":
    main()