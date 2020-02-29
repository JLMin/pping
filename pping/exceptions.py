# -*- coding: utf-8 -*-


def _int_positive(name, value):
    # value : int > 0
    is_int = isinstance(value, int) and not isinstance(value, bool)
    if not (is_int and value > 0):
        error = (
            f'Expect the "{name}" to be a positive integer, get'
            f': <{type(value).__name__}> \'{value}\''
        )
        raise ValueError(error)


def _int_positive_or_zero(name, value):
    # value : int >= 0
    is_int = isinstance(value, int) and not isinstance(value, bool)
    if not (is_int and value >= 0):
        error = (
            f'Expect the "{name}" to be a non-negative interger, get'
            f': <{type(value).__name__}> \'{value}\''
        )
        raise ValueError(error)


def _num_positive(name, value):
    # value : int | float > 0
    is_num = isinstance(value, (int, float)) and not isinstance(value, bool)
    if not (is_num and value > 0):
        error = (
            f'Expect the "{name}" to be a positive number, get'
            f': <{type(value).__name__}> \'{value}\''
        )
        raise ValueError(error)


def _num_positive_or_zero(name, value):
    # value : int | float >= 0
    is_num = isinstance(value, (int, float)) and not isinstance(value, bool)
    if not (is_num and value >= 0):
        error = (
            f'Expect the "{name}" to be a non-negative number, get'
            f': <{type(value).__name__}> \'{value}\''
        )
        raise ValueError(error)
