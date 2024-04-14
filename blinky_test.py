from migen import *

from blinky import Blinky

led = Signal(name='led')
counter = Signal(32, name='counter')
dut = Blinky(led, counter)

def testbench():
    # yield dut.led.eq(0)
    # yield dut.counter.eq(0)
    # assert (yield led) == 0
    # assert (yield counter) == 0
    # yield
    # assert (yield led) == 0
    # assert (yield counter) == 0
    # yield

    yield dut.counter.eq(int(25e6 - 4))

    for count in range(32):
        yield

    yield dut.counter.eq(int(25e6 - 4))

    for count in range(32):
        yield


run_simulation(dut, testbench(), vcd_name="blinky_test.vcd")