#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Blocos combinacionais de somadores em MyHDL.

Este modulo declara implementacoes de:
- meio somador (half adder),
- somador completo (full adder),
- somador de 2 bits,
- somador generico por encadeamento,
- somador vetorial comportamental.
"""

from myhdl import *


@block
def halfAdder(a, b, soma, carry):
    """Meio somador de 1 bit.

    Args:
        a: Entrada de 1 bit.
        b: Entrada de 1 bit.
        soma: Saida de soma.
        carry: Saida de carry.
    """
    @always_comb
    def comb():
        soma.next = a ^ b
        carry.next = a & b
    return instances()


@block
def fullAdder(a, b, c, soma, carry):
    """Somador completo de 1 bit.

    Args:
        a: Primeira entrada de 1 bit.
        b: Segunda entrada de 1 bit.
        c: Carry de entrada.
        soma: Saida de soma.
        carry: Carry de saida.
    """
    #apenas para a solução com dois half adder
    #s1 = Signal(bool(0)) # (1)
    #s2 = Signal(bool(0)) 
    #s3 = Signal(bool(0))

    #uma forma de melhorar é ao invés de escrever os sinais dessa forma, colocar num vetor:
    s = [Signal(bool(0)) for i in range(3)]

    #half_1 = halfAdder(a, b, s[0], s[1]) 
    #half_2 = halfAdder(c, s[0], soma, s[2])

    #vetor
    haList = [None for i in range(2)]  # (1)

    haList[0] = halfAdder(a, b, s[0], s[1]) 
    haList[1] = halfAdder(c, s[0], soma, s[2])

    @always_comb
    def comb():
        #solução padrão
        #carry.next = (a & b) or (a & c) or (c & b)
        #soma.next = ((not a) & (not b) & c) or ((not a) & b & (not c)) or (a & (not b) & (not c)) or (a & b & c)

        #solução com dois halfAdder
        carry.next = s[1] | s[2]
    return instances()


@block
def adder2bits(x, y, soma, carry):
    """Somador de 2 bits.

    Implementacao esperada com dois full adders, gerando
    uma soma de 2 bits e carry final.

    Args:
        x: Vetor de entrada de 2 bits.
        y: Vetor de entrada de 2 bits.
        soma: Vetor de saida de 2 bits.
        carry: Carry de saida.
    """
    c_int = Signal(bool(0))

    full1 = fullAdder(x[0], y[0], 0, soma[0], c_int)

    full2 = fullAdder(x[1], y[1], c_int, soma[1], carry)

    return instances()


@block
def adder(x, y, soma, carry):
    """Somador generico para vetores de mesmo tamanho.

    Implementacao esperada por ripple-carry (encadeamento de carries)
    usando celulas de full adder.

    Args:
        x: Vetor de entrada.
        y: Vetor de entrada.
        soma: Vetor de saida com mesma largura de x/y.
        carry: Carry de saida mais significativo.
    """
    n = len(x)
    faList = [None for i in range(n)]

    carry_int_list = [Signal(bool(0)) for j in range(n)]



    for k in range(n):
        if k == 0:
            c_in = Signal(bool(0))
        else:
            c_in = carry_int_list[k-1]
        
        c_out = carry_int_list[k]

        faList[k] = fullAdder(x[k], y[k], c_in, soma[k], c_out)
    return instances()


@block
def addervb(x, y, soma, carry):
    """Somador vetorial em estilo comportamental.

    Versao combinacional que pode usar operacoes aritmeticas diretas
    sobre os vetores para gerar soma e carry.

    Args:
        x: Vetor de entrada.
        y: Vetor de entrada.
        soma: Vetor de saida.
        carry: Carry de saida.
    """
    n = len(x)

    @always_comb
    def comb():
        result = intbv(x + y)[n+1:] 

        soma.next = result[n:0]
        carry.next = result[n]

    return instances()
