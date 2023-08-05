#!/usr/bin/env python
# -*- coding: utf-8 -*-

import functools
from dataclasses import dataclass
from inspect import getcallargs, getfile, getsource, signature
from typing import Callable, Optional

__all__ = [
    'ContractError',
    'ContractState',
    'DEFAULT_CONTRACT_STATE',
    'disable_contract',
    'ContractException',
    'in_contract',
    'out_contract',
]


@dataclass
class ContractState:
    is_enable: bool = True

    def disable(self) -> None:
        self.is_enable = False


DEFAULT_CONTRACT_STATE = ContractState()


def disable_contract(state: ContractState = DEFAULT_CONTRACT_STATE) -> None:
    state.disable()


class ContractException(Exception):
    ...


class ContractError(Exception):
    ...


def new_contract_exception(
        cond_f: Callable[..., bool], contract_tag: Optional[str], *args,
        **kw) -> ContractException:
    contract_tag_msg = f"contract_tag={contract_tag}\n" if contract_tag else ""
    f_expr = get_func_expr(cond_f)
    return ContractException(
        f"Contract Error:\n{f_expr}\n    {contract_tag_msg}args={args},\n    kw={kw}")


def get_func_expr(f: Callable) -> str:
    if '<lambda>' in str(f):
        filename = getfile(f)
        lineno = f.__code__.co_firstlineno
        source = getsource(f)
        return f"{filename}:{lineno}:{source}"
    else:
        lineno = f.__code__.co_firstlineno
        return f"{f.__name__}:{lineno}"


def in_contract_callable_full_match_case(
        cond_f: Callable[..., bool], f: Callable, contract_tag: Optional[str],
        contract_state: ContractState, *args, **kw) -> bool:

    new_args = getcallargs(f, *args, **kw)
    values = list(new_args.values())
    return cond_f(*values)


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
        contract_state: ContractState, *args, **kw) -> Optional[ContractException]:
    if isinstance(varinfo, str):
        varinfo = varinfo.split("-")[0]
        res = in_contract_dict_match_varname_case(
            varinfo, cond_f, f, contract_tag, contract_state, *args, **kw)
        if res is not True:
            return new_contract_exception(cond_f, contract_tag, res)
    else:
        f_sig = signature(f)
        binded = f_sig.bind(*args, **kw)
        binded.apply_defaults()
        args, kw = binded.args, binded.kwargs
        keys_ = list(binded.arguments.keys())
        values = list(binded.arguments.values())
        inds = []
        for varname in varinfo:
            varname = varname.split("-")[0]
            inds.append(keys_.index(varname))
        cond_arguments = [values[ind] for ind in inds]
        if not cond_f(*cond_arguments):
            return new_contract_exception(cond_f, contract_tag, *cond_arguments)

    return None


def in_contract(
        *conds,
        contract_tag: Optional[str] = None,
        contract_state: ContractState = DEFAULT_CONTRACT_STATE,
        **cond_opts) -> Callable:

    def _in_contract(f: Callable) -> Callable:

        @functools.wraps(f)
        def wrapped(*args, **kw) -> Callable:
            if contract_state.is_enable:
                try:
                    for cond in conds:
                        if callable(cond):
                            if not in_contract_callable_one(cond, f, contract_tag, contract_state,
                                                            *args, **kw):
                                raise new_contract_exception(cond, contract_tag, *args, **kw)
                        else:
                            for varinfo, cond_f in cond.items():
                                ex = get_contract_exception_from_dict(
                                    cond_f, f, varinfo, contract_tag, contract_state, *args, **kw)
                                if ex is not None:
                                    raise ex

                    for varinfo, cond_f in cond_opts.items():
                        ex = get_contract_exception_from_dict(
                            cond_f, f, varinfo, contract_tag, contract_state, *args, **kw)
                        if ex is not None:
                            raise ex
                except (ValueError, TypeError) as err:
                    raise ContractError(*err.args)

            return f(*args, **kw)

        return wrapped

    return _in_contract


def out_contract(
        cond_f: Callable[..., bool],
        contract_tag: Optional[str] = None,
        contract_state: ContractState = DEFAULT_CONTRACT_STATE) -> Callable:

    def _out_contract(f: Callable) -> Callable:

        @functools.wraps(f)
        def wrapped(*args, **kw) -> Callable:
            result = f(*args, **kw)
            if contract_state.is_enable:
                try:
                    if not cond_f(result):
                        raise new_contract_exception(cond_f, contract_tag, result)
                except (ValueError, TypeError) as err:
                    raise ContractError(*err.args)
            return result

        return wrapped

    return _out_contract
