#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Parser module."""
from collections import defaultdict, namedtuple
import re

Operation = namedtuple('Operation', 'name, params, onto',
                       defaults=(None, None))
__prt_lvalue = r'(\w+(?:\s*,\s*\w*)*)'
__prt_op = r'\s*((?:\s\w+\s)|(?:[=~\\\*@\$<>\-]+\S*?))\s*'
__prt_rvalue = r'(\w[\w.]*(?:\s*\*\s*\w+)?(?:\s*\+\s*\w[\w.]*(?:\s*\*\s*\w+)?)*)'
PTRN_EFFECT = re.compile(__prt_lvalue + __prt_op + __prt_rvalue)
PTRN_OPERATION = re.compile(r'([A-Z][A-Z_]+(?:\(.*\))?)\s*([\w\s]+)*')
PTRN_RVALUE = re.compile(r'((\w[\w.]*\*)?\w+)')
PTRN_OP = re.compile(r'(\w+)(\(.*\))?')


def separate_token(token: str):
    """
    Test if token satisfies basic command semopy syntax and separates token.

    Parameters
    ----------
    token : str
        A text line with either effect command or operation command.

    Raises
    ------
    SyntaxError
        Token happens to be incorrect, i.e. it does not follows basic
        semopy command pattern.

    Returns
    -------
    bool
        True if token is an effect command.
    tuple
        A tuple of (lvalue, operation, rvalue) if command is effect or
        (operation, operands) if command is operation.

    """
    effect = PTRN_EFFECT.fullmatch(token)
    if effect:
        return True, effect.groups()
    operation = PTRN_OPERATION.fullmatch(token)
    if not operation:
        raise SyntaxError(f'Invalind syntax for line:\n{token}')
    return False, operation.groups()


def parse_rvalues(token: str):
    """
    Separate token by  '+' sign and parses expression "val*x" into tuples.

    Parameters
    ----------
    token : str
        Right values from operand.

    Raises
    ------
    Exception
        Rises when a certain rvalue can't be processed.

    Returns
    -------
    rvalues : dict
        A mapping Variable->Multiplicator.

    """
    token = token.replace(' ', '')
    rvalues = dict()
    for tok in token.split('+'):
        rval = PTRN_RVALUE.match(tok)
        if not rval:
            raise Exception(f'{rval} does not seem like a correct semopy \
                            expression')
        groups = rval.groups()
        name = groups[0].split('*')[-1]
        rvalues[name] = groups[1][:-1] if groups[1] else None
    return rvalues


def parse_operation(operation: str, operands: str):
    """
    Parse an operation according to semopy syntax.

    Parameters
    ----------
    operation : str
        Operation string with possible arguments.
    operands : str
        Variables/values that operation acts upon.

    Raises
    ------
    SyntaxError
        Rises when there is an error during parsing.

    Returns
    -------
    operation : Operation
        Named tuple containing information on operation.

    """
    oper = PTRN_OP.match(operation)
    if not oper:
        raise SyntaxError(f'Incorrect operation pattern: {operation}')
    operands = [op.strip() for op in operands.split()] if operands else list()
    groups = oper.groups()
    name = groups[0]
    params = groups[1]
    if params is not None:
        params = [t.strip() for t in params[1:-1].split(',')]
    operation = Operation(name, params, operands)
    return operation


def parse_desc(desc: str):
    """
    Parse a model description provided in semopy's format.

    Parameters
    ----------
    desc : str
        Model description in semopy format.

    Returns
    -------
    effects : defaultdict
        Mapping operation->lvalue->rvalue->multiplicator.
    operations : dict
        Mapping operationName->list[Operation type].

    """
    effects = defaultdict(lambda: defaultdict(dict))
    operations = defaultdict(list)
    for line in desc.splitlines():
        try:
            i = line.index('#')
            line = line[:i]
        except ValueError:
            pass
        line = line.strip()
        if line:
            is_effect, items = separate_token(line)
            if is_effect:
                lefts, op_symb, rights = items
                for left in lefts.split(','):
                    rvalues = parse_rvalues(rights)
                    effects[op_symb][left.strip()].update(rvalues)
            else:
                operation, operands = items
                t = parse_operation(operation, operands)
                operations[t.name].append(t)
    return effects, operations
