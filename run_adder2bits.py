#!/usr/bin/env python3

from myhdl import *
from ula_modules import adder2bits


@block
def runAdder2bits():
    x = Signal(intbv()[2:])
    y = Signal(intbv()[2:])

    x_ = [x(i) for i in range(2)]
    y_ = [y(i) for i in range(2)]
    s_ = [Signal(bool()) for i in range(2)]

    s = ConcatSignal(*reversed(s_))
    carry = Signal(bool(0))

    dut = adder2bits(x_, y_, s_, carry)

    @instance
    def stimulus():
        while True:
            x.next = int(input("x="))
            y.next = int(input("y="))
            yield delay(1)
            print("--------------------")
            print("--    results     --")
            print("--------------------")
            print(
                " x    : %s\n y    : %s\n soma : %s\n carry: %s"
                % (bin(x, 2), bin(y, 2), bin(s, 2), bin(carry))
            )
            print("--------------------")

    return instances()


tb = runAdder2bits()
tb.run_sim()
