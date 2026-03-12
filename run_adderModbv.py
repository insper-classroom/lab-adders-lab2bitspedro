#!/usr/bin/env python3

from myhdl import *
from ula_modules import *


@block
def runAdderModbv():
    x = Signal(modbv()[2:])
    y = Signal(modbv()[2:])
    s = Signal(modbv()[2:])
    c = Signal(bool())

    dut = addervb(x, y, s, c)

    @instance
    def stimulus():
        while True:
            x.next = modbv(int(input("x=")))
            y.next = modbv(int(input("y=")))
            yield delay(1)
            print("--------------------")
            print("--    results     --")
            print("--------------------")
            print(
                " x    : %s\n y    : %s\n soma : %s\n carry: %s"
                % (bin(x, len(x)), bin(y, len(x)), bin(s, len(x)), bin(c))
            )
            print("--------------------")

    return instances()


@block
def runBcd():
    x0 = Signal(modbv(6)[8:])
    y0 = Signal(modbv(8)[8:])
    x1 = Signal(modbv(0)[8:])
    y1 = Signal(modbv(0)[8:])
    dut = addBcd(x1, x0, y1, y0)

    @instance
    def stimulus():
        yield delay(1)
        print("--------------------")
        print("--    results     --")
        print("--------------------")
        print("%s%s" % (bin(x1, 8), bin(x0, 8)))
        print("%s%s" % (bin(y1, 8), bin(y0, 8)))
        yield delay(1)
        yield delay(1)

    return instances()


tb = runAdderModbv()
tb.run_sim()
