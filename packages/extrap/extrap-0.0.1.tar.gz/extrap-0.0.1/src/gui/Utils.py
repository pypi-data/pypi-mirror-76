"""
This file is part of the Extra-P software (http://www.scalasca.org/software/extra-p)

Copyright (c) 2020,
Technische Universitaet Darmstadt, Germany
 
This software may be modified and distributed under the terms of
a BSD-style license.  See the COPYING file in the package base
directory for details.
"""


def makeExponent(exponent):
    exponent = exponent.replace('0', 'â�°')
    exponent = exponent.replace('1', 'Â¹')
    exponent = exponent.replace('2', 'Â²')
    exponent = exponent.replace('3', 'Â³')
    exponent = exponent.replace('4', 'â�´')
    exponent = exponent.replace('5', 'â�µ')
    exponent = exponent.replace('6', 'â�¶')
    exponent = exponent.replace('7', 'â�·')
    exponent = exponent.replace('8', 'â�¸')
    exponent = exponent.replace('9', 'â�¹')
    exponent = exponent.replace('-', 'â�»')
    exponent = exponent.replace('.', 'â‹…')
    return exponent


def makeBase(base):
    base = base.replace('0', 'â‚€')
    base = base.replace('1', 'â‚�')
    base = base.replace('2', 'â‚‚')
    base = base.replace('3', 'â‚ƒ')
    base = base.replace('4', 'â‚„')
    base = base.replace('5', 'â‚…')
    base = base.replace('6', 'â‚†')
    base = base.replace('7', 'â‚‡')
    base = base.replace('8', 'â‚ˆ')
    base = base.replace('9', 'â‚‰')
    base = base.replace('e', 'â‚‘')
    return base


def replace_substr(formula, begin, end, substr):
    if begin > 0:
        new_formula = formula[:begin] + substr
    else:
        new_formula = substr
    if end < len(formula):
        new_formula = new_formula + formula[end:]
    return new_formula


def formatNumber(value_str, precision=3):

    # try to convert long 0.00000 prefixes to 10^-x
    if value_str.find('.') != -1 and value_str.find('e') == -1:
        splitted_value = value_str.split('.')
        if (splitted_value[0] == '0'):
            zero_count = 0
            while len(splitted_value[1]) > zero_count:
                if splitted_value[1][zero_count] == '0':
                    zero_count += 1
                else:
                    break
            if splitted_value[1][zero_count:] and zero_count > 1:
                value_str = '{:.{}e}'.format(float(value_str), len(
                    splitted_value[1][zero_count:]) - 1)
                value_str = value_str.replace("+", "")

        elif(len(splitted_value[0]) > 4):
            count_digits_before_decimal = len(splitted_value[0])-1
            while splitted_value[0][count_digits_before_decimal] == '0':
                count_digits_before_decimal = count_digits_before_decimal-1
            value_str = '{:.{}e}'.format(float(value_str), len(
                splitted_value[0][:count_digits_before_decimal]))
            value_str = value_str.replace("+", "")
            # value_str=self.reduce_length(value_str)

    # Adjust the precision
    if value_str.find('e') != -1:
        splitted_value = value_str.split('e')
        if splitted_value[1].find('+') != -1:
            value_after_e = splitted_value[1].replace("+", "")
        else:
            value_after_e = splitted_value[1]
        value_str = '{:.{}f}'.format(
            float(splitted_value[0]), precision)+"e" + ''.join(value_after_e)
    else:
        value_str = '{:.{}f}'.format(float(value_str), precision)

    # Convert scientific exponent notation into 10^
    value_str = value_str.replace('e', 'x10^')

    # Convert exponents with ^ to real smaller numbers
    if value_str.find('^') != -1:
        split_value_str = value_str.split('^')
        value_after = makeExponent(split_value_str[1])
        value_str = split_value_str[0]+(value_after)
    return value_str


def isnumber(c):
    return c == '0' or \
        c == '1' or \
        c == '2' or \
        c == '3' or \
        c == '4' or \
        c == '5' or \
        c == '6' or \
        c == '7' or \
        c == '8' or \
        c == '9'


def formatFormula(formula):

    end = 0
    # Set logarithm base
    while formula.find('log', end) != -1:
        begin = formula.find('log', end) + 3
        end = begin
        while formula[end].isdigit():
            end = end + 1
        base = makeBase(formula[begin:end])
        formula = replace_substr(formula, begin, end, base)

    # Make exponents
    end = 0
    while formula.find('^', end) != -1:
        begin = formula.find('^', end)
        end = begin+1
        if formula[end] == '-':
            end = end + 1
        while formula[end].isdigit() or formula[end] == '.':
            end = end + 1
        exponent = formula[begin+1:end]
        # Skip exponent 1
        if exponent == '1':
            exponent = exponent.replace('1', '')
        else:
            exponent = makeExponent(exponent)
        formula = replace_substr(formula, begin, end, exponent)

    # Replace '+-'
    formula = formula.replace('+-', '-')

    # Format numbers
    # last to get exponenten and base out of the way

    # MODES
    # 0 = search start of new number
    # 1 = search end of new number before exponent
    # 2 = after e for exponent
    mode = 0
    i = 0
    while i < len(formula):
        if mode == 0 and isnumber(formula[i]):
            begin = i
            mode = 1
        elif mode == 1 and formula[i] == 'e':
            mode = 2
        elif mode == 1 and not isnumber(formula[i]) and not formula[i] == '.':
            end = i
            number = formatNumber(formula[begin:end])
            formula = replace_substr(formula, begin, end, number)
            i = begin + len(number)
            mode = 0
        elif mode == 2:
            if isnumber(formula[i]) or formula[i] == '+' or formula[i] == '-':
                mode = 1
            else:
                end = i-1
                number = formatNumber(formula[begin:end])
                formula = replace_substr(formula, begin, end, number)
                i = begin + len(number)
                mode = 0
        i = i + 1
    return formula

