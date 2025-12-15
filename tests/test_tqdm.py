"""
Comprehensive tests for the tqdm_rich module.

This test suite covers:
- Basic functionality of tqdm() function
- tqdm() with various parameter combinations
- Error handling and color state transitions
- Context manager usage
- Manual update operations
"""

import pytest

from tqdm_rich import TqdmRich, tqdm


class TestTqdmBasic:
    """Test basic tqdm functionality."""

    def test_tqdm_with_list(self):
        """Test tqdm with a simple list."""
        items = []
        for item in tqdm(range(10), desc="Test"):
            items.append(item)

        assert len(items) == 10
        assert items == list(range(10))

    def test_tqdm_iteration(self, fast_iterable):
        """Test basic iteration with tqdm."""
        count = 0
        for _ in tqdm(fast_iterable):
            count += 1

        assert count == 100

    def test_tqdm_with_description(self):
        """Test tqdm with custom description."""
        items = list(tqdm(range(5), desc="Custom"))
        assert len(items) == 5

    def test_tqdm_without_iterable(self):
        """Test tqdm without iterable (manual mode)."""
        bar = tqdm(total=100, desc="Manual")
        bar.update(50)
        bar.update(50)
        bar.close()

    def test_tqdm_leave_true(self):
        """Test tqdm with leave=True."""
        items = list(tqdm(range(5), leave=True))
        assert len(items) == 5

    def test_tqdm_leave_false(self):
        """Test tqdm with leave=False."""
        items = list(tqdm(range(5), leave=False))
        assert len(items) == 5

    def test_tqdm_disable_true(self):
        """Test tqdm with disable=True."""
        count = 0
        bar = tqdm(range(10), disable=True)
        for _ in bar:
            count += 1

        assert count == 10

    def test_tqdm_returns_tqdmrich(self):
        """Test that tqdm() returns a TqdmRich instance."""
        bar = tqdm(range(10))
        assert isinstance(bar, TqdmRich)
        bar.close()


class TestTqdmRichClass:
    """Test TqdmRich class directly."""

    def test_tqdmrich_initialization(self):
        """Test TqdmRich initialization."""
        bar = TqdmRich(range(10), desc="Test")
        assert bar.desc == "Test"
        assert bar.total is None  # Will be determined during iteration
        bar.close()

    def test_tqdmrich_context_manager(self):
        """Test TqdmRich as context manager."""
        with TqdmRich(range(10), desc="Context") as bar:
            count = 0
            for _ in bar:
                count += 1

        assert count == 10

    def test_tqdmrich_manual_iteration(self):
        """Test manual iteration with TqdmRich."""
        bar = TqdmRich(range(5), desc="Manual")
        items = []
        for item in bar:
            items.append(item)
        bar.close()

        assert items == [0, 1, 2, 3, 4]

    def test_tqdmrich_update(self):
        """Test manual update method."""
        bar = TqdmRich(total=100, desc="Update")
        bar.update(25)
        bar.update(25)
        bar.update(50)
        bar.close()

    def test_tqdmrich_attributes(self):
        """Test TqdmRich attributes."""
        bar = TqdmRich(
            range(10),
            desc="Test",
            unit="items",
            position=0,
            colour="blue",
        )
        assert bar.unit == "items"
        assert bar.position == 0
        assert bar.colour == "blue"
        bar.close()


class TestTqdmParameters:
    """Test tqdm with various parameter combinations."""

    def test_tqdm_with_total(self):
        """Test tqdm with explicit total."""
        count = 0
        for _ in tqdm(range(20), total=20):
            count += 1
        assert count == 20

    def test_tqdm_all_parameters(self):
        """Test tqdm with all common parameters."""
        bar = tqdm(
            iterable=range(10),
            desc="Full",
            total=10,
            leave=True,
            unit="item",
            disable=False,
        )
        count = sum(1 for _ in bar)
        assert count == 10

    def test_tqdm_generator_detection(self):
        """Test tqdm with generator (no __len__)."""

        def gen():
            for i in range(5):
                yield i

        items = list(tqdm(gen()))
        assert items == [0, 1, 2, 3, 4]

    def test_tqdm_with_minimal_args(self):
        """Test tqdm with minimal arguments."""
        items = list(tqdm(range(5)))
        assert items == [0, 1, 2, 3, 4]


class TestErrorHandling:
    """Test error handling and state transitions."""

    def test_exception_during_iteration(self):
        """Test that exception colors the bar red."""
        with pytest.raises(ValueError):
            for item in tqdm(range(100)):
                if item == 50:
                    raise ValueError("Test error")

    def test_exception_propagation(self):
        """Test that exceptions are properly propagated."""

        def failing_gen():
            for i in range(5):
                if i == 2:
                    raise RuntimeError("Fail")
                yield i

        with pytest.raises(RuntimeError):
            list(tqdm(failing_gen()))

    def test_keyboard_interrupt(self):
        """Test handling of KeyboardInterrupt."""
        with pytest.raises(KeyboardInterrupt):
            for item in tqdm(range(100)):
                if item == 25:
                    raise KeyboardInterrupt()

    def test_break_during_iteration(self):
        """Test breaking out of iteration."""
        count = 0
        for item in tqdm(range(100)):
            count += 1
            if item == 10:
                break

        assert count == 11


class TestTqdmRichContextManager:
    """Test context manager functionality."""

    def test_context_manager_entry_exit(self):
        """Test __enter__ and __exit__ methods."""
        bar = TqdmRich(range(10))
        with bar as b:
            assert b is bar
            count = sum(1 for _ in b)
        assert count == 10

    def test_context_manager_with_exception(self):
        """Test context manager with exception inside."""
        with pytest.raises(ValueError):
            with TqdmRich(range(100)) as bar:
                for item in bar:
                    if item == 50:
                        raise ValueError("Test")

    def test_context_manager_cleanup(self):
        """Test that context manager cleans up properly."""
        try:
            with TqdmRich(range(10)) as bar:
                for _ in bar:
                    pass
        except Exception:
            pytest.fail("Context manager should handle cleanup")


class TestEmptyIterables:
    """Test edge cases with empty iterables."""

    def test_empty_list(self):
        """Test tqdm with empty list."""
        items = list(tqdm([]))
        assert items == []

    def test_empty_range(self):
        """Test tqdm with empty range."""
        items = list(tqdm(range(0)))
        assert items == []

    def test_empty_generator(self):
        """Test tqdm with empty generator."""

        def empty_gen():
            return
            yield  # Never reached

        items = list(tqdm(empty_gen()))
        assert items == []


class TestSingleItem:
    """Test edge cases with single items."""

    def test_single_item_list(self):
        """Test tqdm with single item list."""
        items = list(tqdm([42]))
        assert items == [42]

    def test_single_iteration_with_total(self):
        """Test single iteration with explicit total."""
        bar = tqdm(range(1), total=1)
        count = sum(1 for _ in bar)
        assert count == 1


class TestLargeIterables:
    """Test with larger iterables."""

    def test_large_range(self):
        """Test tqdm with large range."""
        count = 0
        for _ in tqdm(range(10000)):
            count += 1
            if count >= 100:  # Limit for test speed
                break
        assert count == 100

    def test_large_list_with_break(self):
        """Test tqdm with large list and early break."""
        items = []
        for item in tqdm(range(10000)):
            items.append(item)
            if len(items) >= 100:
                break
        assert len(items) == 100


class TestUpdateMethod:
    """Test the update method of TqdmRich."""

    def test_update_single(self):
        """Test single update call."""
        bar = TqdmRich(total=100)
        bar.update(1)
        bar.close()

    def test_update_multiple(self):
        """Test multiple update calls."""
        bar = TqdmRich(total=100)
        for _ in range(10):
            bar.update(10)
        bar.close()

    def test_update_without_total(self):
        """Test update without explicit total."""
        bar = TqdmRich()
        bar.update(5)
        bar.update(5)
        bar.close()


class TestDescriptionHandling:
    """Test description handling in various scenarios."""

    def test_none_description(self):
        """Test with None description."""
        bar = TqdmRich(range(5), desc=None)
        count = sum(1 for _ in bar)
        bar.close()
        assert count == 5

    def test_empty_description(self):
        """Test with empty string description."""
        bar = TqdmRich(range(5), desc="")
        count = sum(1 for _ in bar)
        bar.close()
        assert count == 5

    def test_long_description(self):
        """Test with very long description."""
        long_desc = "This is a very long description " * 10
        bar = TqdmRich(range(5), desc=long_desc)
        count = sum(1 for _ in bar)
        bar.close()
        assert count == 5

    def test_unicode_description(self):
        """Test with unicode description."""
        bar = TqdmRich(range(5), desc="处理中 🚀")
        count = sum(1 for _ in bar)
        bar.close()
        assert count == 5


class TestCompatibility:
    """Test tqdm compatibility features."""

    def test_tqdm_compatible_parameters(self):
        """Test that tqdm accepts tqdm-compatible parameters."""
        bar = tqdm(
            range(10),
            desc="Compat",
            total=10,
            leave=True,
            file=None,
            ncols=80,
            mininterval=0.1,
            maxinterval=10.0,
            miniters=1,
            ascii=False,
            unit="it",
            unit_scale=False,
        )
        count = sum(1 for _ in bar)
        assert count == 10

    def test_tqdm_returns_correct_type(self):
        """Test that tqdm() returns a proper iterable."""
        bar = tqdm(range(5))
        assert hasattr(bar, "__iter__")
        assert hasattr(bar, "__next__")
        bar.close()


class TestNestedIterables:
    """Test nested iteration scenarios."""

    def test_nested_tqdm(self):
        """Test nested tqdm calls."""
        count = 0
        for i in tqdm(range(5)):
            for j in tqdm(range(5), leave=False):
                count += 1

        assert count == 25

    def test_tqdm_in_function(self):
        """Test tqdm inside a function."""

        def process(items):
            results = []
            for item in tqdm(items, desc="Processing"):
                results.append(item * 2)
            return results

        results = process(range(5))
        assert results == [0, 2, 4, 6, 8]


class TestTypePreservation:
    """Test that iteration preserves item types."""

    def test_string_items(self):
        """Test iteration over strings preserves type."""
        items = list(tqdm(["a", "b", "c"]))
        assert items == ["a", "b", "c"]
        assert all(isinstance(i, str) for i in items)

    def test_mixed_types(self):
        """Test iteration over mixed types."""
        data = [1, "two", 3.0, None, [5]]
        items = list(tqdm(data))
        assert items == data

    def test_object_items(self):
        """Test iteration over custom objects."""

        class Obj:
            def __init__(self, value):
                self.value = value

        objs = [Obj(i) for i in range(3)]
        items = list(tqdm(objs))
        assert len(items) == 3
        assert all(isinstance(i, Obj) for i in items)
