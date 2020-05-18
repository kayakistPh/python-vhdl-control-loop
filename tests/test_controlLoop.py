# Simple tests for an adder module
import cocotb
from cocotb.clock import Clock
from cocotb.decorators import coroutine
from cocotb.triggers import Timer, RisingEdge, ReadOnly
from cocotb.monitors import Monitor
from cocotb.drivers import BitDriver
from cocotb.binary import BinaryValue
from cocotb.regression import TestFactory
from cocotb.scoreboard import Scoreboard
from cocotb.result import TestFailure, TestSuccess

import math

@cocotb.test()
def test_controlLoop(dut):
    # Set up the clock
    fs = 2e6  # Hz

    # Generate the test waveforms
    sineFrq = 50e3  # Hz The frequency of the excitation wave
    cycles = 3  # The number of waves to use
    # timebase = np.arange(0, (cycles * (1 / sineFrq)), (1 / fs))
    # Stimulus = (2 ** 17) * (np.sin(2 * np.pi * sineFrq * timebase))

    # START Test
    dut.controlInput_i.value = 0
    dut.kp_i = 24
    dut.ki_i = 26

    # Create a clock from which we start everything
    c = Clock(dut.clock_i, 500, "ns")
    cocotb.fork(c.start())

    clkedge = RisingEdge(dut.clock_i)

    timebase = []
    stimulus = []

    inputSignal = []
    controllerError = []
    feedback = []
    plantOut = []
    Output = []

    controllerError.append(0)
    feedback.append(0)
    plantOut.append(0)
    controllerError.append(0)
    feedback.append(0)
    plantOut.append(0)

    # open file and read the content in a list
    with open("timebase.txt", "r") as filehandle:
        for line in filehandle:
            # remove linebreak which is the last character of the string
            currentPlace = line[:-1]

            # add item to the list
            timebase.append(currentPlace)

    with open("input.txt", "r") as filehandle:
        for line in filehandle:
            # remove linebreak which is the last character of the string
            currentPlace = line[:-1]

            # add item to the list
            stimulus.append(currentPlace)

    yield clkedge
    yield clkedge
    for i in range(1, len(timebase)):
        yield clkedge

        inputSignal.append(stimulus[i])
        controllerError.append(float(stimulus[i]) - float(feedback[i - 1]))
        # The plant is a sine wave
        plantOut.append(math.sin(controllerError[i]) * (2 ** 17))
        dut.controlInput_i.value = int(plantOut[i])
        Output.append(dut.feedback_o.value.signed_integer)
        feedback.append((dut.feedback_o.value.signed_integer) / (2 ** 17))

    controllerErrorList = list(controllerError)
    feedbackList = list(feedback)
    plantOutList = list(plantOut)

    with open("controllerError.txt", "w") as filehandle:
        for listitem in controllerErrorList:
            filehandle.write("%s\n" % listitem)

    with open("feedback.txt", "w") as filehandle:
        for listitem in feedbackList:
            filehandle.write("%s\n" % listitem)

    with open("plantOut.txt", "w") as filehandle:
        for listitem in plantOutList:
            filehandle.write("%s\n" % listitem)
