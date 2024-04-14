import argparse

from litex.build.generic_platform import *
from litex.build.lattice import LatticeECP5Platform
from litex.build.lattice.programmer import EcpDapProgrammer
from litex.soc.cores.clock import ECP5PLL
from litex.soc.cores.led import LedChaser
from litex.soc.integration.builder import Builder
from litex.soc.integration.soc_core import SoCMini
from migen import *

# Platform definition
_io = [
    ("clk25", 0, Pins("P3"), IOStandard("LVCMOS33")),
    ("user_led", 0, Pins("U16"), IOStandard("LVCMOS33")),
]

class _CRG(Module):
    def __init__(self, platform, sys_clk_freq):
        self.clock_domains.cd_sys = ClockDomain(name="cd_sys")

        # Clk / Rst.
        clk25 = platform.request("clk25")

        # PLL.
        self.submodules.pll = pll = ECP5PLL()
        pll.register_clkin(clk25, 25e6)
        pll.create_clkout(self.cd_sys, sys_clk_freq)


class Platform(LatticeECP5Platform):
    default_clk_name   = "clk25"
    default_clk_period = 1e9/25e6

    def __init__(self, board="i5", revision="7.0", toolchain="trellis"):
        self.revision = revision

        device     = {"7.0": "LFE5U-25F-6BG381C"}[revision]
        io         = {"7.0": _io}[revision]

        LatticeECP5Platform.__init__(self, device, io, toolchain=toolchain)

    def create_programmer(self):
        return EcpDapProgrammer()


class BlinkySoC(SoCMini):

    def __init__(self, platform, sys_clk_freq=int(50e6)):
        self.platform = platform

        # CRG --------------------------------------------------------------------------------------
        self.submodules.crg = _CRG(platform=platform, sys_clk_freq=sys_clk_freq)

        # SoCMini ----------------------------------------------------------------------------------
        SoCMini.__init__(self, platform, clk_freq=sys_clk_freq)

        self.submodules.led = Blinky(platform.request('user_led'), Signal(32), sys_clk_freq=sys_clk_freq)

        # self.add_csr('leds')


# Blinky design
class Blinky(Module):

    def __init__(self, led, counter, sys_clk_freq):
        self.submodules.leds = LedChaser(
            sys_clk_freq=sys_clk_freq,
            pads=led,
            period=0.25
        )

        # self.led = led
        # self.counter = counter
        #
        # self.sync += [
        #     self.counter.eq(self.counter + 1),
        #
        #     If(self.counter == int(25e6),
        #        self.led.eq(~self.led),
        #        self.counter.eq(0)
        #        )
        # ]

# Build and program
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--build",       action="store_true",      help="Build bitstream")
    parser.add_argument("--load",        action="store_true",      help="Load bitstream")
    parser.add_argument("--flash",       action="store_true",      help="Flash bitstream")
    args = parser.parse_args()

    platform = Platform()
    # blinky = Blinky(platform.request("user_led"), Signal(32))
    blinky_soc = BlinkySoC(platform=platform, sys_clk_freq=int(50e6))

    if args.build:
        builder = Builder(blinky_soc, output_dir="build", csr_csv="scripts/csr.csv")
        builder.build(build_name="blinky2", run=args.build)

    if args.load:
        platform.create_programmer().load_bitstream("build/gateware/blinky2.bit")

