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
    def __init__(self, led):
        # self.clk = platform.request("clk25")
        counter = Signal(32)

        self.comb += led.eq(counter[25])
        self.sync += counter.eq(counter + 1)

# Build and program
if __name__ == "__main__":
    platform = Platform()
    led = platform.request("user_led")
    blinky = Blinky(led)
    platform.build(blinky)
    # platform.create_programmer().load_bitstream("build/top.bin")