#!/usr/bin/env python
# -*- coding: utf-8 -*-

from dataclasses import dataclass


class ContractError(Exception):
    ...


class ContractException(Exception):
    ...


@dataclass
class ContractState:
    __is_enable: bool = True

    def enable(self) -> None:
        self.__is_enable = True

    def disable(self) -> None:
        self.__is_enable = False

    @property
    def is_enable(self) -> bool:
        return self.__is_enable

    @property
    def is_disable(self) -> bool:
        return not self.__is_enable

    def __str__(self) -> str:
        return f"ContractState<is_enable={self.__is_enable}>"

    def __repr__(self) -> str:
        return str(self)


DEFAULT_CONTRACT_STATE = ContractState()


def disable_contract(state: ContractState = DEFAULT_CONTRACT_STATE) -> None:
    state.disable()
