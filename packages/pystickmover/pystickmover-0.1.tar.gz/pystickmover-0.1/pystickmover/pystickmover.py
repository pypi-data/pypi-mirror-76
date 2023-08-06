#!/usr/bin/env python3

import serial
import sys


class StickMover:
    AXIS_MIN_OUTPUT = 1000
    AXIS_MAX_OUTPUT = 2000
    AXIS_BYTES = 2
    AXIS_MIN_INPUT = 0.0
    AXIS_MAX_INPUT = 1.0
    AXIS_CENTER_INPUT = 0.5
    AXIS_EXP_MIN_OUTPUT = -100
    AXIS_EXP_MAX_OUTPUT = 100
    AXIS_EXP_BYTES = 1
    AXIS_EXP_INVERT_INPUT = -1.0
    AXIS_EXP_MIN_INPUT = -1.0
    AXIS_EXP_MAX_INPUT = 1.0
    AXIS_EXP_OFF_INPUT = 0.0
    CHECKSUM_BYTES = 1
    RX_BYTES = 100
    ENDIANNESS = 'big'
    BAUD_RATE = 57600
    ACK_TIMEOUT = 0.01

    @staticmethod
    def sanitize_axis(axis_input):
        axis_output = (axis_input - StickMover.AXIS_MIN_INPUT) / (StickMover.AXIS_MAX_INPUT - StickMover.AXIS_MIN_INPUT) * \
            (StickMover.AXIS_MAX_OUTPUT - StickMover.AXIS_MIN_OUTPUT) + \
            StickMover.AXIS_MIN_OUTPUT
        if axis_output > StickMover.AXIS_MAX_OUTPUT:
            axis_output = StickMover.AXIS_MAX_OUTPUT
        elif axis_output < StickMover.AXIS_MIN_OUTPUT:
            axis_output = StickMover.AXIS_MIN_OUTPUT
        return int(axis_output).to_bytes(StickMover.AXIS_BYTES, byteorder=StickMover.ENDIANNESS)

    @staticmethod
    def sanitize_exp(exp_input):
        exp_output = StickMover.AXIS_EXP_INVERT_INPUT * ((exp_input - StickMover.AXIS_EXP_MIN_INPUT) / (StickMover.AXIS_EXP_MAX_INPUT - StickMover.AXIS_EXP_MIN_INPUT) * (
            StickMover.AXIS_EXP_MAX_OUTPUT - StickMover.AXIS_EXP_MIN_OUTPUT) + StickMover.AXIS_EXP_MIN_OUTPUT)
        if exp_output > StickMover.AXIS_EXP_MAX_OUTPUT:
            exp_output = StickMover.AXIS_EXP_MAX_OUTPUT
        elif exp_output < StickMover.AXIS_EXP_MIN_OUTPUT:
            exp_output = StickMover.AXIS_EXP_MIN_OUTPUT
        else:
            return int(exp_output).to_bytes(StickMover.AXIS_EXP_BYTES, byteorder=StickMover.ENDIANNESS, signed=True)

    @staticmethod
    def generate_payload(axis1_input=0.5, axis2_input=0.5, axis3_input=0.5, axis4_input=0.5, axis1_exp=0.0, axis2_exp=0.0, axis3_exp=0.0, axis4_exp=0.0):
        mode_bytes = b'\x02'
        axis1_bytes = StickMover.sanitize_axis(axis1_input)
        axis2_bytes = StickMover.sanitize_axis(axis2_input)
        axis3_bytes = StickMover.sanitize_axis(axis3_input)
        axis4_bytes = StickMover.sanitize_axis(axis4_input)
        axis1_exp_bytes = StickMover.sanitize_exp(axis1_exp)
        axis2_exp_bytes = StickMover.sanitize_exp(axis2_exp)
        axis3_exp_bytes = StickMover.sanitize_exp(axis3_exp)
        axis4_exp_bytes = StickMover.sanitize_exp(axis4_exp)
        partial_payload = mode_bytes + axis1_bytes + axis2_bytes + axis3_bytes + \
            axis4_bytes + axis1_exp_bytes + axis2_exp_bytes + \
            axis3_exp_bytes + axis4_exp_bytes
        check_bytes = (sum(partial_payload) & 0xff).to_bytes(
            StickMover.CHECKSUM_BYTES, byteorder=StickMover.ENDIANNESS)
        return partial_payload + check_bytes

    def __init__(self, serial_port, debug=False):
        self.serial_connection = serial.Serial(
            serial_port, baudrate=StickMover.BAUD_RATE, timeout=StickMover.ACK_TIMEOUT)
        self.axis1 = StickMover.AXIS_CENTER_INPUT
        self.axis2 = StickMover.AXIS_CENTER_INPUT
        self.axis3 = StickMover.AXIS_CENTER_INPUT
        self.axis4 = StickMover.AXIS_CENTER_INPUT
        self.axis1_exp = StickMover.AXIS_EXP_OFF_INPUT
        self.axis2_exp = StickMover.AXIS_EXP_OFF_INPUT
        self.axis3_exp = StickMover.AXIS_EXP_OFF_INPUT
        self.axis4_exp = StickMover.AXIS_EXP_OFF_INPUT
        self.debug = debug

    def __del__(self):
        try:
            self.serial_connection.close()
        except AttributeError:
            pass

    def update(self):
        payload = StickMover.generate_payload(
            self.axis1, self.axis2, self.axis3, self.axis4, self.axis1_exp, self.axis2_exp, self.axis3_exp, self.axis4_exp)
        if self.debug:
            print('Writing:', payload)
        self.serial_connection.write(payload)
        repsonse = self.serial_connection.read(StickMover.RX_BYTES)
        if self.debug:
            print('Reading:', repsonse)


if __name__ == '__main__':
    if len(sys.argv) > 1:
        try:
            stickmover = StickMover(serial_port=sys.argv[1], debug=True)
            stickmover.axis1 = 0.0
            stickmover.axis2 = 0.5
            stickmover.axis3 = 0.5
            stickmover.axis4 = 1.0
            stickmover.axis1_exp = 1.0
            stickmover.axis2_exp = -1.0
            stickmover.axis3_exp = 0.0
            stickmover.axis4_exp = 0.5
            axis1_step = 0.01
            axis2_step = 0.01
            axis3_step = 0.01
            axis4_step = 0.01
            while True:
                stickmover.update()
                if stickmover.axis1 > StickMover.AXIS_MAX_INPUT or stickmover.axis1 < StickMover.AXIS_MIN_INPUT:
                    axis1_step *= -1.0
                if stickmover.axis2 > StickMover.AXIS_MAX_INPUT or stickmover.axis2 < StickMover.AXIS_MIN_INPUT:
                    axis2_step *= -1.0
                if stickmover.axis3 > StickMover.AXIS_MAX_INPUT or stickmover.axis3 < StickMover.AXIS_MIN_INPUT:
                    axis3_step *= -1.0
                if stickmover.axis4 > StickMover.AXIS_MAX_INPUT or stickmover.axis4 < StickMover.AXIS_MIN_INPUT:
                    axis4_step *= -1.0
                stickmover.axis1 += axis1_step
                stickmover.axis2 += axis2_step
                stickmover.axis3 += axis3_step
                stickmover.axis4 += axis4_step
        except KeyboardInterrupt:
            exit(0)
        except FileNotFoundError:
            print('Invalid serial port.')
            exit(1)
        except serial.serialutil.SerialException:
            print('Serial port disconnected.')
            exit(1)
    else:
        print('Usage: ./pystickmover <device>')
        exit(1)
