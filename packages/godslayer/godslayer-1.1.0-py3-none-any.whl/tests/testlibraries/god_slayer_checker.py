"""Test library for check GodSlayer."""
from dataclasses import dataclass
from typing import Iterator, List, Optional

import pytest

from godslayer.csv.god_slayer import GodSlayer


@dataclass
class GodSlayerCheckState:
    iterator_actual: Iterator
    length_record: int = 0
    gap: bool = False
    last_index: Optional[int] = None


class GodSlayerChecker:
    """Test library for check GodSlayer."""

    @staticmethod
    def assert_god_slayer(god_slayer: GodSlayer, expected_index_start: int, expected: List[List[str]]):
        """checks GodSlayer."""
        god_slayer_check_state = GodSlayerCheckState(god_slayer.__iter__())
        # Order of argument for zip() is important.
        # First argument should be "expected"
        # to confirm that next iteration of actual raises StopIteration,
        # since zip() iterates first argument even if second argument is empty.
        for index, (expected_record, actual) in enumerate(zip(expected, god_slayer_check_state.iterator_actual)):
            assert god_slayer.index == expected_index_start + index
            assert actual == expected_record
            god_slayer_check_state.length_record += 1
        GodSlayerChecker.assert_length(expected, god_slayer_check_state)

    @staticmethod
    def assert_god_slayer_partition(god_slayer: GodSlayer, expected: List[List[str]]):
        god_slayer_check_state = GodSlayerCheckState(god_slayer.__iter__())
        GodSlayerChecker._assert_god_slayer_partition(expected, god_slayer, god_slayer_check_state)
        GodSlayerChecker.assert_length(expected, god_slayer_check_state)
        assert god_slayer_check_state.gap

    @staticmethod
    def _assert_god_slayer_partition(
        expected: List[List[str]], god_slayer: GodSlayer, god_slayer_check_state: GodSlayerCheckState
    ):
        for expected_record, actual in zip(expected, god_slayer_check_state.iterator_actual):
            if (
                god_slayer_check_state.last_index is not None
                and god_slayer.index - god_slayer_check_state.last_index > 1
            ):
                god_slayer_check_state.gap = True
            god_slayer_check_state.last_index = god_slayer.index
            assert actual == expected_record
            god_slayer_check_state.length_record += 1
        return god_slayer_check_state.length_record

    @staticmethod
    def assert_length(expected: List[List[str]], god_slayer_check_state: GodSlayerCheckState):
        assert god_slayer_check_state.length_record == len(expected)
        with pytest.raises(StopIteration):
            next(god_slayer_check_state.iterator_actual)
