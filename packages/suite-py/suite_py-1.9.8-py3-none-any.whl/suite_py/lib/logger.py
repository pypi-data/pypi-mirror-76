# -*- encoding: utf-8 -*-
from termcolor import colored


def info(message):
    print(colored(message, "green"))


def warning(message):
    print(colored(message, "yellow"))


def error(message):
    print(colored(message, "red"))
