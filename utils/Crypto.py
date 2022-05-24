#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# File name          : EthereumCtfTool.py
# Author             : Wlayzz (@wlayzz)
# Date created       : 21 May 2022
# Python Version     : 3.*

from web3 import Web3

class Crypto:
    def __init__(self, logger):
        self.logger = logger

    def calcule_keccak256(self, n, ntype):
        n = int(n)
        if ntype == "uint8":
            if n < 0 and n > 255:
                self.logger.error("uint8 must be in 0 and 255 range ")
        w3 = Web3()
        return w3.solidityKeccak([ntype], [n]).hex()

    def get_keccak_value(self, n, ntype):
        h = self.calcule_keccak256(n, ntype)
        self.logger.success(f"Result of keccak256({n}): {h}")

    def bf_keccak256(self, bf_range, bf_value, ntype):
        min = int(bf_range.split('-')[0])
        max = int(bf_range.split('-')[1])

        for i in range(min, max):
            h = self.calcule_keccak256(i, ntype)
            if bf_value == h:
                self.logger.success(f"Brute force success the value for {bf_value} is {i}")
                break

