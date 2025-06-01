import pytest
from kawaiitb.utils.suggestions import osa_distance

_MOVE_COST = 1
_SUBSTITUTE_COST = 1
_TRANSPOSE_COST = 1

class TestOSADistance:
    def test_same_string(self):
        """测试相同字符串的情况"""
        assert osa_distance("hello", "hello", 10) == 0
        assert osa_distance("", "", 10) == 0

    def test_empty_string(self):
        """测试空字符串的情况"""
        assert osa_distance("", "hello", 10) == _MOVE_COST * 5  # _MOVE_COST * len("hello")
        assert osa_distance("world", "", 10) == _MOVE_COST * 5  # _MOVE_COST * len("world")

    def test_basic_operations(self):
        """测试基本操作(插入/删除/替换)"""
        # 替换 (h -> H)
        assert osa_distance("hello", "Hello", 10) == _SUBSTITUTE_COST
        # 删除 (去掉e)
        assert osa_distance("hello", "hllo", 10) == _MOVE_COST
        # 插入 (添加x)
        assert osa_distance("hello", "hellox", 10) == _MOVE_COST

    def test_transposition(self):
        """测试字符交换操作"""
        # 交换两个字符 (ab -> ba)
        assert osa_distance("ab", "ba", 10) == _TRANSPOSE_COST
        # 更长的字符串中的交换
        assert osa_distance("hello", "hlelo", 10) == _TRANSPOSE_COST
        # 非相邻字符交换不算作交换操作
        assert osa_distance("abcd", "badc", 10) == 2 * _TRANSPOSE_COST  # 交换两次

    def test_max_cost(self):
        """测试超过最大成本的情况"""
        # 距离为1但max_cost=1
        assert osa_distance("ab", "ba", 1) == _MOVE_COST
        # 距离为4但max_cost=3
        assert osa_distance("kitten", "sitting", 3) == 4  # max_cost + 1

    def test_max_string_size(self):
        """测试超过最大字符串长度的情况"""
        long_str = "a" * 41  # _MAX_STRING_SIZE = 40
        assert osa_distance(long_str, "a", 10) == 11  # max_cost + 1
        assert osa_distance("a", long_str, 10) == 11  # max_cost + 1

    def test_common_affixes(self):
        """测试公共前缀/后缀的处理"""
        # 公共前缀
        assert osa_distance("prehello", "preworld", 10) == osa_distance("hello", "world", 10)
        # 公共后缀
        assert osa_distance("hellopost", "worldpost", 10) == osa_distance("hello", "world", 10)
        # 公共前缀和后缀
        assert osa_distance("prehellopost", "preworldpost", 10) == osa_distance("hello", "world", 10)

    def test_case_sensitivity(self):
        """测试大小写敏感性"""
        # 大小写不同应视为替换
        assert osa_distance("Hello", "hello", 10) == _SUBSTITUTE_COST
        assert osa_distance("HELLO", "hello", 10) == 5 * _SUBSTITUTE_COST
