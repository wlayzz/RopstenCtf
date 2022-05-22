#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# File name          : EthereumCtfTool.py
# Author             : Wlayzz (@wlayzz)
# Date created       : 21 May 2022
# Python Version     : 3.*

class Logger:
    def __init__(self, console, verbosity=0):
        self.verbosity = verbosity
        self.console = console
    def success(self, message):
        self.console.print("{}[+]{} {}".format("[bold green]", "[/bold green]", message), highlight=False)

    def error(self, message):
        self.console.print("{}[ERROR] {}{}".format("[bold red]", message, "[/bold red]"), highlight=False)

    def info(self, message):
        self.console.print("{}[INFO]{} {}".format("[bold blue]", "[/bold blue]", message), highlight=False)

    def list(self, message):
        self.console.print("\t{}[*]{} {}".format("[bold blue]", "[/bold blue]", message), highlight=False)

    def debug(self, message):
        if self.verbosity:
            self.console.print("{}[DEBUG]{} {}".format("[bold magenta]", "[/bold magenta]", message), highlight=False)