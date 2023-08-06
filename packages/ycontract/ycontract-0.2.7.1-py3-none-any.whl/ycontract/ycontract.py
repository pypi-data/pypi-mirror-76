#!/usr/bin/env python
# -*- coding: utf-8 -*-

from dataclasses import dataclass


class ContractError(Exception):
    ...


@dataclass
class ContractState:
    is_enable: bool = True

    def disable(self) -> None:
        self.is_enable = False


DEFAULT_CONTRACT_STATE = ContractState()


def disable_contract(state: ContractState = DEFAULT_CONTRACT_STATE) -> None:
    state.disable()
