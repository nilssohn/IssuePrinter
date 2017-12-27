# IssuePrinter
GitHub issue printer using GitHub API v3.

# Setup
The instructions can be found here: https://learn.adafruit.com/networked-thermal-printer-using-cups-and-raspberry-pi
It was successfully implemented in Raspberry Pi 3. It just has a different serial output, ttySAMA0.


# Usage
The printer should work with any printer as long as the "lpr" command exists. The setup for the printer was an extra step. If you have a serial output already, you can write to it like this: echo "Hello, World!" > ttySAMA0.
