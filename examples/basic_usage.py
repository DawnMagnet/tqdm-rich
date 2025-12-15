"""
Basic usage examples of tqdm_rich.

This module demonstrates the three main ways to use tqdm_rich:
1. Using the tqdm() function (tqdm-compatible)
2. Using the track() generator function
3. Using the TqdmRich class directly
"""

import time
from tqdm_rich import tqdm, track, TqdmRich


def example_tqdm_basic():
    """
    Example 1: Basic tqdm usage with a list.
    
    This is the most familiar interface for users coming from tqdm.
    """
    print("Example 1: Basic tqdm() usage")
    print("-" * 50)
    
    for item in tqdm(range(100), desc="Processing items"):
        time.sleep(0.01)
    
    print("✓ Completed\n")


def example_tqdm_with_generator():
    """
    Example 2: Using tqdm with a generator.
    
    tqdm will automatically enter logarithmic mode for generators
    without a known length.
    """
    print("Example 2: tqdm() with generator")
    print("-" * 50)
    
    def data_generator():
        """Generate data items one at a time."""
        for i in range(50):
            time.sleep(0.02)
            yield f"Item {i}"
    
    for item in tqdm(data_generator(), desc="Generating data"):
        pass
    
    print("✓ Completed\n")


def example_track_function():
    """
    Example 3: Using the track() function.
    
    track() is the recommended way for generator-based progress tracking.
    It provides an elegant, functional API.
    """
    print("Example 3: track() function")
    print("-" * 50)
    
    for item in track(range(100), description="Processing"):
        time.sleep(0.01)
    
    print("✓ Completed\n")


def example_track_with_log_mode():
    """
    Example 4: Using track() with logarithmic progress.
    
    Logarithmic mode shows gradual progress for long operations
    with unknown completion time.
    """
    print("Example 4: track() with logarithmic mode")
    print("-" * 50)
    
    def long_running_generator():
        """Simulate a long operation."""
        for i in range(200):
            time.sleep(0.01)
            yield i
    
    for item in track(long_running_generator(), log=20):
        pass
    
    print("✓ Completed\n")


def example_tqdmrich_class():
    """
    Example 5: Using the TqdmRich class directly.
    
    For more control, you can instantiate TqdmRich directly.
    """
    print("Example 5: TqdmRich class")
    print("-" * 50)
    
    bar = TqdmRich(range(50), desc="Custom progress")
    for item in bar:
        time.sleep(0.02)
    bar.close()
    
    print("✓ Completed\n")


def example_context_manager():
    """
    Example 6: Using TqdmRich as a context manager.
    
    Context manager automatically handles cleanup.
    """
    print("Example 6: Context manager usage")
    print("-" * 50)
    
    with TqdmRich(range(75), desc="Context manager") as bar:
        for item in bar:
            time.sleep(0.015)
    
    print("✓ Completed\n")


def example_manual_update():
    """
    Example 7: Manual progress updates.
    
    Sometimes you need to manually update progress instead of
    iterating over items.
    """
    print("Example 7: Manual updates")
    print("-" * 50)
    
    bar = TqdmRich(total=100, desc="Manual progress")
    
    for i in range(10):
        time.sleep(0.05)
        bar.update(10)  # Advance by 10
    
    bar.close()
    
    print("✓ Completed\n")


def example_transient_mode():
    """
    Example 8: Transient mode.
    
    When transient=True, the progress bar disappears after completion,
    keeping the output clean.
    """
    print("Example 8: Transient mode")
    print("-" * 50)
    
    for i in range(3):
        for item in track(range(20), description=f"Task {i+1}", transient=True):
            time.sleep(0.01)
    
    print("✓ All tasks completed\n")


def example_nested_progress():
    """
    Example 9: Nested progress bars.
    
    Multiple progress bars can be nested and will display correctly.
    """
    print("Example 9: Nested progress bars")
    print("-" * 50)
    
    for i in tqdm(range(5), desc="Outer"):
        for j in tqdm(range(5), desc=f"Inner {i}", leave=False):
            time.sleep(0.02)
    
    print("✓ Completed\n")


def example_error_handling():
    """
    Example 10: Error handling.
    
    The progress bar will turn red when an error occurs.
    """
    print("Example 10: Error handling")
    print("-" * 50)
    
    try:
        for item in tqdm(range(100), desc="Processing"):
            time.sleep(0.01)
            if item == 50:
                raise ValueError("Error at item 50!")
    except ValueError as e:
        print(f"✗ Error caught: {e}\n")


def example_different_sizes():
    """
    Example 11: Working with different iterable sizes.
    
    tqdm automatically adapts to different sizes.
    """
    print("Example 11: Different iterable sizes")
    print("-" * 50)
    
    print("Small iteration (10 items):")
    list(tqdm(range(10), leave=False))
    
    print("Medium iteration (50 items):")
    list(tqdm(range(50), leave=False))
    
    print("Large iteration (100 items):")
    list(tqdm(range(100), leave=False))
    
    print("✓ Completed\n")


def example_with_custom_descriptions():
    """
    Example 12: Various description styles.
    """
    print("Example 12: Custom descriptions")
    print("-" * 50)
    
    descriptions = [
        "Loading data...",
        "🚀 Processing files",
        "📊 Analyzing results",
        "✨ Finalizing output",
    ]
    
    for desc in descriptions:
        list(tqdm(range(30), desc=desc, leave=False))
        time.sleep(0.1)
    
    print("✓ Completed\n")


if __name__ == "__main__":
    print("\n" + "=" * 50)
    print("tqdm_rich Usage Examples")
    print("=" * 50 + "\n")
    
    # Run all examples
    example_tqdm_basic()
    example_tqdm_with_generator()
    example_track_function()
    example_track_with_log_mode()
    example_tqdmrich_class()
    example_context_manager()
    example_manual_update()
    example_transient_mode()
    example_nested_progress()
    example_error_handling()
    example_different_sizes()
    example_with_custom_descriptions()
    
    print("=" * 50)
    print("All examples completed successfully! ✨")
    print("=" * 50)
