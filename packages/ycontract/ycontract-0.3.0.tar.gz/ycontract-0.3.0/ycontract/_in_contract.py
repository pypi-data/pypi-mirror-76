#!/usr/bin/env python
# -*- coding: utf-8 -*-

import functools
from inspect import getcallargs, signature
from typing import Any, Callable, Dict, Optional, Sequence, Union

from .ycontract import DEFAULT_CONTRACT_STATE, ContractError, ContractException, ContractState

__all__ = ['InContractException', 'in_contract']

VARINFO = Union[str, Sequence[str]]
CONDINFO = Union[Callable[..., bool], Sequence[Callable[..., bool]]]


class InContractException(ContractException):
    ...


def new_in_contract_exception(
        f: Callable, f_args: Sequence, f_kw: dict, cond_f: Callable[..., bool],
        contract_tag: Optional[str]) -> InContractException:
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
    msg += f"    arguments: {arguments_str}"

    return InContractException(msg)


def in_contract_callable_full_match_case(
        cond_f: Callable[..., bool], f: Callable, contract_tag: Optional[str],
        contract_state: ContractState, *args, **kw) -> bool:
    new_values = list(getcallargs(f, *args, **kw).values())
    return cond_f(*new_values)


def in_contract_callable_partial_match_case(
        cond_f: Callable[..., bool], f: Callable, contract_tag: Optional[str],
        contract_state: ContractState, *args, **kw) -> bool:
    f_sig = signature(f)
    f_varnames = list(f_sig.parameters)
    cond_sig = signature(cond_f)
    cond_varnames = list(cond_sig.parameters)
    varname_indexes = {v: f_varnames.index(v) for v in cond_varnames}

    def get_arg(v: str):
        if varname_indexes[v] < len(args):
            return args[varname_indexes[v]]
        elif v in kw:
            return kw[v]
        else:
            return f_sig.parameters[v].default

    var_args = {v: get_arg(v) for v in cond_sig.parameters.keys()}

    return cond_f(**var_args)


def in_contract_callable_one(
        cond_f: Callable[..., bool], f: Callable, contract_tag: Optional[str],
        contract_state: ContractState, *args, **kw) -> bool:
    try:
        return in_contract_callable_full_match_case(
            cond_f, f, contract_tag, contract_state, *args, **kw)
    except TypeError:
        return in_contract_callable_partial_match_case(
            cond_f, f, contract_tag, contract_state, *args, **kw)


def check_in_contract_dict(
        cond: Dict[VARINFO, Callable[..., bool]], f: Callable, contract_tag: Optional[str],
        contract_state: ContractState, args: Sequence,
        kw: Dict[str, Any]) -> Optional[InContractException]:
    for varinfo, cond_info in cond.items():
        cond_fs = []
        if callable(cond_info):
            cond_fs = [cond_info]
        else:
            cond_fs = list(cond_info)

        for cond_f in cond_fs:
            ex = get_contract_exception_from_dict(
                cond_f, f, varinfo, contract_tag, contract_state, *args, **kw)
            if ex is not None:
                return ex

    return None


def in_contract_dict_match_varname_case(
        varname: str, cond_f: Callable[..., bool], f: Callable, contract_tag: Optional[str],
        contract_state: ContractState, *args, **kw):
    sig = signature(f)
    binded = sig.bind(*args, **kw)
    binded.apply_defaults()
    keys_ = list(binded.arguments.keys())
    values = list(binded.arguments.values())
    ind = keys_.index(varname)
    is_ok = cond_f(values[ind])
    if is_ok:
        return True
    else:
        return values[ind]


def get_contract_exception_from_dict(
        cond_f: Callable[..., bool], f: Callable, varinfo, contract_tag: Optional[str],
        contract_state: ContractState, *args, **kw) -> Optional[InContractException]:
    if isinstance(varinfo, str):
        res = in_contract_dict_match_varname_case(
            varinfo, cond_f, f, contract_tag, contract_state, *args, **kw)
        if res is not True:
            return new_in_contract_exception(f, list(args), kw, cond_f, contract_tag)
    else:
        f_sig = signature(f)
        binded = f_sig.bind(*args, **kw)
        binded.apply_defaults()
        keys_ = list(binded.arguments.keys())
        values = list(binded.arguments.values())
        inds = []
        for varname in varinfo:
            inds.append(keys_.index(varname))
        cond_arguments = [values[ind] for ind in inds]
        if not cond_f(*cond_arguments):
            return new_in_contract_exception(f, list(args), kw, cond_f, contract_tag)

    return None


def in_contract(
        *conds,
        contract_tag: Optional[str] = None,
        contract_state: ContractState = DEFAULT_CONTRACT_STATE,
        **cond_opts) -> Callable:

    def _in_contract(f: Callable) -> Callable:

        @functools.wraps(f)
        def wrapped(*args, **kw) -> Callable:
            if contract_state.is_disable:
                return f(*args, **kw)

            try:
                for cond in conds:
                    if callable(cond):
                        if not in_contract_callable_one(cond, f, contract_tag, contract_state, *
                                                        args, **kw):
                            raise new_in_contract_exception(f, list(args), kw, cond, contract_tag)
                    else:
                        ex = check_in_contract_dict(
                            cond, f, contract_tag, contract_state, args, kw)
                        if ex is not None:
                            raise ex

                ex = check_in_contract_dict(
                    cond_opts, f, contract_tag, contract_state, args, kw)  # type: ignore
                if ex is not None:
                    raise ex
            except (ValueError, TypeError) as err:
                raise ContractError(*err.args)

            return f(*args, **kw)

        return wrapped

    return _in_contract
