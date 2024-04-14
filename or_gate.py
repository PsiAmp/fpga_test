from migen import *

class ORGate(Module):
  def __init__(self):
    self.a = Signal()
    self.b = Signal()
    self.x = Signal()

    ###

    self.comb += self.x.eq(self.a | self.b)

dut = ORGate()

def testbench():
  yield dut.a.eq(0)
  yield dut.b.eq(0)
  yield
  assert (yield dut.x) == 0

  yield dut.a.eq(0)
  yield dut.b.eq(1)
  yield
  assert (yield dut.x) == 1

run_simulation(dut, testbench(), vcd_name="or_gate_test.vcd")