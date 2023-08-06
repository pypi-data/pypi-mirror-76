#!/usr/bin/env python
# -*- coding: utf-8 -*-
import functools
from inspect import getcallargs
from typing import Callable, Optional, TypeVar

from .ycontract import DEFAULT_CONTRACT_STATE, ContractError, ContractException, ContractState


class OutContractException(ContractException):
    ...


T = TypeVar('T')


def new_out_contract_exception(
        f: Callable[..., T], f_args: list, f_kw: dict, cond_f: Callable[..., bool], result: T,
        contract_tag: Optional[str]) -> OutContractException:
    callargs = getcallargs(f, *f_args, **f_kw)

    f_filename = f.__code__.co_filename
    f_lineno = f.__code__.co_firstlineno
    cond_f_filename = cond_f.__code__.co_filename
    cond_f_lineno = cond_f.__code__.co_firstlineno

    msg = "\n"
    if contract_tag:
        msg += f"    tag:       {contract_tag}\n"
    msg += f"    function:  {f.__name__} at {f_filename}:{f_lineno}\n"
    msg += f"    condition: {cond_f.__name__} at {cond_f_filename}:{cond_f_lineno}\n"
    arguments_str = ", ".join(f"{key}={value}" for key, value in callargs.items())
    msg += f"    arguments: {arguments_str}\n"
    msg += f"    result:    {result}"

    return OutContractException(msg)


def out_contract(
        *conds,
        contract_tag: Optional[str] = None,
        contract_state: ContractState = DEFAULT_CONTRACT_STATE) -> Callable:

    def _out_contract(f: Callable) -> Callable:

        if contract_state.is_disable:
            return f

        @functools.wraps(f)
        def wrapped(*args, **kw) -> Callable:
            result = f(*args, **kw)
            try:
                for cond_f in conds:
                    if not cond_f(result):
                        raise new_out_contract_exception(
                            f, list(args), kw, cond_f, result, contract_tag)
            except (ValueError, TypeError) as err:
                raise ContractError(*err.args)
            return result

        return wrapped

    return _out_contract
