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
    def __init__(self, led):
        # self.clk = platform.request("clk25")
        counter = Signal(32)

        # self.comb += led.eq(counter[24])
        self.sync += [
            counter.eq(counter + 1),
            If(counter == int(25e6), led.eq(~led), counter.eq(0))
        ]

# Build and program
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--build",       action="store_true",      help="Build bitstream")
    parser.add_argument("--load",        action="store_true",      help="Load bitstream")
    parser.add_argument("--flash",       action="store_true",      help="Flash bitstream")
    parser.add_argument("--ip",          default="192.168.1.20",   help="Ethernet IP address of the board (default: 192.168.1.20).")
    parser.add_argument("--mac-address", default="0x726b895bc2e2", help="Ethernet MAC address of the board (defaullt: 0x726b895bc2e2).")
    parser.add_argument("--port",        default="5678",           help="Port to send UDP data over (default: 5678)")
    parser.add_argument("--host-ip",     default="192.168.1.1",    help="IP to send UDP data to (default: 192.168.1.1)")

    args = parser.parse_args()

    platform = Platform()
    led = platform.request("user_led")
    blinky = Blinky(led)
    platform.build(blinky)
    # platform.create_programmer().load_bitstream("build/top.bin")

    if args.load:
        prog = platform.create_programmer()
        prog.load_bitstream(builder.get_bitstream_filename(mode="sram"))