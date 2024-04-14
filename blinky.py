import argparse

from migen import *
from litex.build.generic_platform import *
from litex.build.lattice import LatticeECP5Platform
from litex.build.lattice.programmer import EcpprogProgrammer

# Platform definition
_io = [
    ("clk25", 0, Pins("P3"), IOStandard("LVCMOS33")),
    ("user_led", 0, Pins("U16"), IOStandard("LVCMOS33")),
]

class Platform(LatticeECP5Platform):
    default_clk_name   = "clk25"
    default_clk_period = 1e9/25e6

    def __init__(self, board="i5", revision="7.0", toolchain="trellis"):
        self.revision = revision

        device     = {"7.0": "LFE5U-25F-6BG381C"}[revision]
        io         = {"7.0": _io}[revision]

        LatticeECP5Platform.__init__(self, device, io, toolchain=toolchain)

    def create_programmer(self):
        return EcpprogProgrammer()


# Blinky design
class Blinky(Module):
    def __init__(self, led, counter):
        # self.clk = platform.request("clk25")
        self.led = led
        self.counter = Signal(32)

        # self.comb += led.eq(counter[24])
        self.sync += [
            self.counter.eq(self.counter + 1),
            
            If(self.counter == int(25e6),
               self.led.eq(~self.led),
               self.counter.eq(0)
               )
        ]

# Build and program
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--build",       action="store_true",      help="Build bitstream")
    parser.add_argument("--load",        action="store_true",      help="Load bitstream")
    parser.add_argument("--flash",       action="store_true",      help="Flash bitstream")
    args = parser.parse_args()

    platform = Platform()
    blinky = Blinky(platform.request("user_led"), Signal(32))
    platform.build(blinky)

    if args.load:
        platform.create_programmer().load_bitstream("build/top.bin")