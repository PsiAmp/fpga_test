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
    default_clk_name = "clk25"
    default_clk_period = 25.0

    def __init__(self, board="i5", revision="7.0", toolchain="trellis"):
        self.revision = revision
        device     = {"7.0": "LFE5U-25F-6BG381C"}[revision]
        io         = {"7.0": _io}[revision]
        LatticeECP5Platform.__init__(self, device, io, toolchain=toolchain)

    def create_programmer(self):
        return EcpprogProgrammer()


# Blinky design
class Blinky(Module):
    def __init__(self, platform):
        self.clk = platform.request("clk25")
        self.led = platform.request("user_led")
        self.counter = Signal(32)

        platform.add_period_constraint(self.clk, 1e9 / 25e6)

        self.clock_domains.cd_sys = ClockDomain()
        self.comb += self.cd_sys.clk.eq(self.clk)

        self.sync += self.counter.eq(self.counter + 1)
        self.comb += self.led.eq(self.counter[16])

# Build and program
if __name__ == "__main__":
    platform = Platform()
    blinky = Blinky(platform)
    platform.build(blinky)
    # platform.create_programmer().load_bitstream("build/top.bin")