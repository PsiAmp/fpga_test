## Build and program
Enable oss-cad-suite env by running start.bat in oss-cad-suite folder

run
```
python .\blinky2.py --build --load
```
## Fixing encoding error
There's a bug in litex\migen\migen\fhdl\conv_output.py in Windows

To fix add UTF-8 encoding to the 'open' functions in litex\migen\migen\fhdl\conv_output.py


```
def write(self, main_filename):
    with open(main_filename, "w", encoding="utf-8") as f:
        f.write(self.main_source)
    for filename, content in self.data_files.items():
        with open(filename, "w", encoding="utf-8") as f:
            f.write(content)
```