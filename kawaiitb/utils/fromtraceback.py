"""
本模块从traceback中复制了一些函数，用于格式化异常信息
"""

# noinspection PyUnresolvedReferences, PyProtectedMember
from traceback import (
    walk_stack,
    walk_tb,
    _sentinel as sentinel,
    _parse_value_tb as parse_value_tb,
    _walk_tb_with_full_positions as walk_tb_with_full_positions,
    _get_code_position as get_code_position,
    _byte_offset_to_character_offset as byte_offset_to_character_offset,
    _ExceptionPrintContext as ExceptionPrintContext,
    _levenshtein_distance as levenshtein_distance,
    _compute_suggestion_error as compute_suggestion_error,
    _substitution_cost as substitution_cost,
    _display_width as display_width,
)

# noinspection PyUnresolvedReferences
__all__ = [
    "sentinel",
    "parse_value_tb",
    "walk_stack",
    "walk_tb",
    "walk_tb_with_full_positions",
    "get_code_position",
    "byte_offset_to_character_offset",
    "ExceptionPrintContext",
    "levenshtein_distance",
    "compute_suggestion_error",
    "substitution_cost",
    "display_width",
]
