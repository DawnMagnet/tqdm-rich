"""
Comprehensive tests for the track() function.

This test suite covers:
- Basic track functionality
- Generator tracking
- Logarithmic mode
- Transient mode
- Error handling in track()
"""

import pytest

from tqdm_rich import track


class TestTrackBasic:
    """Test basic track() functionality."""

    def test_track_list(self):
        """Test track with a simple list."""
        items = []
        for item in track(range(10), description="Test"):
            items.append(item)

        assert len(items) == 10
        assert items == list(range(10))

    def test_track_iteration(self):
        """Test basic iteration with track."""
        count = 0
        for _ in track(range(100), description="Count"):
            count += 1

        assert count == 100

    def test_track_with_description(self):
        """Test track with custom description."""
        items = list(track(range(5), description="Custom"))
        assert len(items) == 5

    def test_track_default_description(self):
        """Test track with default description."""
        items = list(track(range(5)))
        assert len(items) == 5


class TestTrackWithTotal:
    """Test track with explicit total."""

    def test_track_with_explicit_total(self):
        """Test track with explicit total parameter."""
        items = []
        for item in track(range(10), total=10):
            items.append(item)

        assert len(items) == 10

    def test_track_total_detection(self):
        """Test track auto-detects total from list."""
        items = list(track([1, 2, 3, 4, 5]))
        assert len(items) == 5

    def test_track_total_mismatch(self):
        """Test track with incorrect total."""
        # Should still iterate all items even if total is wrong
        items = list(track(range(10), total=5))
        assert len(items) == 10


class TestTrackGenerator:
    """Test track with generators."""

    def test_track_generator(self):
        """Test track with a generator function."""

        def gen():
            for i in range(10):
                yield i

        items = list(track(gen()))
        assert len(items) == 10
        assert items == list(range(10))

    def test_track_generator_expression(self):
        """Test track with a generator expression."""
        gen_expr = (i for i in range(10))
        items = list(track(gen_expr))
        assert len(items) == 10

    def test_track_generator_without_total(self):
        """Test track with generator without total."""

        def gen():
            for i in range(5):
                yield i

        items = list(track(gen(), description="Generator"))
        assert len(items) == 5


class TestTrackLogarithmicMode:
    """Test track's logarithmic progress mode."""

    def test_track_log_mode_explicit(self):
        """Test track with explicit log parameter."""

        def slow_gen():
            for i in range(100):
                yield i

        items = list(track(slow_gen(), log=20))
        assert len(items) == 100

    def test_track_log_mode_default(self):
        """Test track with default log mode for generators."""

        def gen():
            for i in range(50):
                yield i

        # Generator without total should use log mode
        items = list(track(gen()))
        assert len(items) == 50

    def test_track_log_mode_float(self):
        """Test track with float log parameter."""
        items = list(track(range(100), log=15.5))
        assert len(items) == 100

    def test_track_log_mode_large(self):
        """Test track with large log parameter."""
        items = list(track(range(100), log=100))
        assert len(items) == 100


class TestTrackTransient:
    """Test track's transient mode."""

    def test_track_transient_true(self):
        """Test track with transient=True."""
        items = list(track(range(10), transient=True))
        assert len(items) == 10

    def test_track_transient_false(self):
        """Test track with transient=False (default)."""
        items = list(track(range(10), transient=False))
        assert len(items) == 10

    def test_track_transient_default(self):
        """Test track with default transient (should be False)."""
        items = list(track(range(10)))
        assert len(items) == 10


class TestTrackErrorHandling:
    """Test error handling in track()."""

    def test_track_exception_during_iteration(self):
        """Test that exceptions during iteration are propagated."""
        with pytest.raises(ValueError):
            for item in track(range(100)):
                if item == 50:
                    raise ValueError("Test error")

    def test_track_exception_in_generator(self):
        """Test track with generator that raises exception."""

        def failing_gen():
            for i in range(100):
                if i == 30:
                    raise RuntimeError("Generator failed")
                yield i

        with pytest.raises(RuntimeError):
            list(track(failing_gen()))

    def test_track_keyboard_interrupt(self):
        """Test handling of KeyboardInterrupt in track."""
        with pytest.raises(KeyboardInterrupt):
            for item in track(range(100)):
                if item == 25:
                    raise KeyboardInterrupt()

    def test_track_break_iteration(self):
        """Test breaking out of track iteration."""
        count = 0
        for item in track(range(100)):
            count += 1
            if item == 10:
                break

        assert count == 11


class TestTrackEmptyIterables:
    """Test track with empty iterables."""

    def test_track_empty_list(self):
        """Test track with empty list."""
        items = list(track([], description="Empty"))
        assert items == []

    def test_track_empty_range(self):
        """Test track with empty range."""
        items = list(track(range(0)))
        assert items == []

    def test_track_empty_generator(self):
        """Test track with empty generator."""

        def empty_gen():
            return
            yield  # Never reached

        items = list(track(empty_gen()))
        assert items == []


class TestTrackSingleItem:
    """Test track with single items."""

    def test_track_single_item_list(self):
        """Test track with single item list."""
        items = list(track([42]))
        assert items == [42]

    def test_track_single_item_range(self):
        """Test track with single item range."""
        items = list(track(range(1)))
        assert items == [0]


class TestTrackLargeIterables:
    """Test track with large iterables."""

    def test_track_large_range(self):
        """Test track with large range."""
        count = 0
        for _ in track(range(10000), description="Large"):
            count += 1
            if count >= 100:
                break
        assert count == 100

    def test_track_large_with_log(self):
        """Test track with large range in log mode."""

        def large_gen():
            for i in range(10000):
                yield i

        count = 0
        for _ in track(large_gen(), log=50):
            count += 1
            if count >= 100:
                break
        assert count == 100


class TestTrackDescriptions:
    """Test track description handling."""

    def test_track_custom_description(self):
        """Test track with custom description."""
        items = list(track(range(5), description="Processing items"))
        assert len(items) == 5

    def test_track_empty_description(self):
        """Test track with empty description."""
        items = list(track(range(5), description=""))
        assert len(items) == 5

    def test_track_long_description(self):
        """Test track with very long description."""
        long_desc = "This is a very long description " * 10
        items = list(track(range(5), description=long_desc))
        assert len(items) == 5

    def test_track_unicode_description(self):
        """Test track with unicode description."""
        items = list(track(range(5), description="处理中 🚀"))
        assert len(items) == 5

    def test_track_special_chars_description(self):
        """Test track with special characters in description."""
        items = list(track(range(5), description="[Progress] 50%"))
        assert len(items) == 5


class TestTrackTypePreservation:
    """Test that track preserves item types."""

    def test_track_string_items(self):
        """Test track with string items."""
        items = list(track(["a", "b", "c"]))
        assert items == ["a", "b", "c"]
        assert all(isinstance(i, str) for i in items)

    def test_track_mixed_types(self):
        """Test track with mixed types."""
        data = [1, "two", 3.0, None, [5]]
        items = list(track(data))
        assert items == data

    def test_track_tuple_items(self):
        """Test track with tuple items."""
        tuples = [(1, 2), (3, 4), (5, 6)]
        items = list(track(tuples))
        assert items == tuples

    def test_track_dict_items(self):
        """Test track with dict items."""
        dicts = [{"a": 1}, {"b": 2}]
        items = list(track(dicts))
        assert items == dicts


class TestTrackCombinations:
    """Test track with various parameter combinations."""

    def test_track_all_parameters(self):
        """Test track with all parameters specified."""
        items = list(
            track(
                range(10),
                description="Full",
                total=10,
                log=None,
                transient=False,
            )
        )
        assert len(items) == 10

    def test_track_log_with_explicit_total(self):
        """Test track with both log and total specified."""
        items = list(track(range(10), total=10, log=20))
        assert len(items) == 10

    def test_track_log_and_transient(self):
        """Test track with log mode and transient."""

        def gen():
            for i in range(50):
                yield i

        items = list(track(gen(), log=20, transient=True))
        assert len(items) == 50


class TestTrackIterableVariations:
    """Test track with various iterable types."""

    def test_track_tuple(self):
        """Test track with tuple."""
        data = (1, 2, 3, 4, 5)
        items = list(track(data))
        assert items == list(data)

    def test_track_set(self):
        """Test track with set."""
        data = {1, 2, 3, 4, 5}
        items = list(track(data))
        assert len(items) == 5
        assert set(items) == data

    def test_track_dict_keys(self):
        """Test track with dict keys."""
        data = {"a": 1, "b": 2, "c": 3}
        items = list(track(data.keys()))
        assert set(items) == set(data.keys())

    def test_track_dict_values(self):
        """Test track with dict values."""
        data = {"a": 1, "b": 2, "c": 3}
        items = list(track(data.values()))
        assert sorted(items) == sorted(data.values())

    def test_track_enumerate(self):
        """Test track with enumerate."""
        data = ["a", "b", "c"]
        items = list(track(enumerate(data)))
        assert items == list(enumerate(data))

    def test_track_zip(self):
        """Test track with zip."""
        data1 = [1, 2, 3]
        data2 = ["a", "b", "c"]
        items = list(track(zip(data1, data2)))
        assert items == list(zip(data1, data2))


class TestTrackYield:
    """Test that track properly yields all items."""

    def test_track_yields_in_order(self):
        """Test that track yields items in correct order."""
        data = list(range(20))
        items = list(track(data))
        assert items == data

    def test_track_generator_yields_once(self):
        """Test that generator items are yielded only once."""

        def gen():
            for i in range(10):
                yield i

        items1 = list(track(gen()))
        items2 = list(gen())

        assert items1 == items2


class TestTrackNesting:
    """Test nested track calls."""

    def test_nested_track(self):
        """Test nested track calls."""
        count = 0
        for i in track(range(5)):
            for j in track(range(5), transient=True):
                count += 1

        assert count == 25

    def test_track_in_function(self):
        """Test track inside a function."""

        def process(items):
            results = []
            for item in track(items, description="Processing"):
                results.append(item * 2)
            return results

        results = process(range(5))
        assert results == [0, 2, 4, 6, 8]
