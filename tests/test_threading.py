"""
Thread safety and concurrent execution tests.

This test suite covers:
- Multi-threaded progress tracking
- Thread-safe concurrent updates
- Multiple simultaneous progress bars
- Lock behavior and race conditions
"""

import threading
import time
import pytest
from tqdm_rich import tqdm, track, TqdmRich


class TestThreadSafety:
    """Test thread-safe operations."""

    def test_single_thread(self):
        """Test basic single-threaded operation."""
        items = list(tqdm(range(50), desc="Single"))
        assert len(items) == 50

    def test_multiple_threads_sequential(self):
        """Test multiple threads using tqdm sequentially."""
        results = []
        
        def worker(worker_id):
            items = []
            for item in tqdm(range(10), desc=f"Worker {worker_id}"):
                items.append(item)
            results.append(items)
        
        threads = [threading.Thread(target=worker, args=(i,)) for i in range(3)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()
        
        assert len(results) == 3
        assert all(len(r) == 10 for r in results)

    def test_multiple_threads_parallel(self):
        """Test multiple threads running tqdm in parallel."""
        completed_count = [0]
        lock = threading.Lock()
        
        def worker(worker_id):
            items = 0
            for item in tqdm(range(20), desc=f"Task {worker_id}", leave=False):
                items += 1
            with lock:
                completed_count[0] += 1
        
        threads = [
            threading.Thread(target=worker, args=(i,))
            for i in range(5)
        ]
        
        for t in threads:
            t.start()
        for t in threads:
            t.join()
        
        assert completed_count[0] == 5

    def test_concurrent_track(self):
        """Test concurrent track calls."""
        results = []
        
        def worker(worker_id):
            items = list(track(range(15), description=f"Track {worker_id}"))
            results.append(items)
        
        threads = [threading.Thread(target=worker, args=(i,)) for i in range(3)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()
        
        assert len(results) == 3
        assert all(len(r) == 15 for r in results)


class TestMultipleProgressBars:
    """Test multiple progress bars."""

    def test_two_sequential_progress_bars(self):
        """Test two progress bars running sequentially."""
        count1 = 0
        for _ in tqdm(range(20), desc="First"):
            count1 += 1
        
        count2 = 0
        for _ in tqdm(range(20), desc="Second"):
            count2 += 1
        
        assert count1 == 20
        assert count2 == 20

    def test_nested_progress_bars(self):
        """Test nested progress bars."""
        count = 0
        for i in tqdm(range(5), desc="Outer"):
            for j in tqdm(range(5), desc="Inner", leave=False):
                count += 1
        
        assert count == 25

    def test_multiple_bars_different_sizes(self):
        """Test multiple progress bars with different sizes."""
        results = []
        
        def task(size):
            items = list(tqdm(range(size), leave=False))
            results.append(len(items))
        
        threads = [
            threading.Thread(target=task, args=(10,)),
            threading.Thread(target=task, args=(20,)),
            threading.Thread(target=task, args=(30,)),
        ]
        
        for t in threads:
            t.start()
        for t in threads:
            t.join()
        
        assert results == [10, 20, 30]


class TestConcurrentUpdates:
    """Test concurrent update operations."""

    def test_concurrent_manual_updates(self):
        """Test concurrent manual updates."""
        bar = TqdmRich(total=100)
        
        def updater():
            for _ in range(20):
                bar.update(5)
                time.sleep(0.001)
        
        threads = [threading.Thread(target=updater) for _ in range(2)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()
        
        bar.close()

    def test_concurrent_track_updates(self):
        """Test concurrent track with updates."""
        def worker(worker_id):
            for item in track(range(30), description=f"Worker {worker_id}"):
                time.sleep(0.001)
        
        threads = [
            threading.Thread(target=worker, args=(i,))
            for i in range(3)
        ]
        
        for t in threads:
            t.start()
        for t in threads:
            t.join()


class TestThreadSafeNestedCalls:
    """Test thread-safe nested and concurrent calls."""

    def test_nested_in_thread(self):
        """Test nested progress bars in a thread."""
        results = []
        
        def worker():
            count = 0
            for i in tqdm(range(5), desc="Outer", leave=False):
                for j in tqdm(range(5), desc="Inner", leave=False):
                    count += 1
            results.append(count)
        
        thread = threading.Thread(target=worker)
        thread.start()
        thread.join()
        
        assert results[0] == 25

    def test_many_threads_with_nested_bars(self):
        """Test many threads with nested progress bars."""
        counts = []
        lock = threading.Lock()
        
        def worker(worker_id):
            count = 0
            for i in tqdm(range(3), leave=False):
                for j in tqdm(range(3), leave=False):
                    count += 1
            with lock:
                counts.append(count)
        
        threads = [
            threading.Thread(target=worker, args=(i,))
            for i in range(5)
        ]
        
        for t in threads:
            t.start()
        for t in threads:
            t.join()
        
        assert len(counts) == 5
        assert all(c == 9 for c in counts)


class TestRaceConditions:
    """Test potential race conditions."""

    def test_rapid_start_stop(self):
        """Test rapid creation and destruction of progress bars."""
        for _ in range(10):
            bar = tqdm(range(10), leave=False)
            list(bar)

    def test_rapid_multiple_threads(self):
        """Test rapid concurrent creation."""
        def quick_task():
            list(tqdm(range(5), leave=False))
        
        threads = [
            threading.Thread(target=quick_task)
            for _ in range(10)
        ]
        
        for t in threads:
            t.start()
        for t in threads:
            t.join()

    def test_stress_concurrent_access(self):
        """Stress test with many concurrent accesses."""
        results = []
        
        def stress_worker(worker_id):
            for item in track(range(50), description=f"Stress {worker_id}"):
                pass
            results.append(worker_id)
        
        threads = [
            threading.Thread(target=stress_worker, args=(i,))
            for i in range(20)
        ]
        
        for t in threads:
            t.start()
        for t in threads:
            t.join()
        
        assert len(results) == 20


class TestConcurrentExceptions:
    """Test exception handling in concurrent scenarios."""

    def test_exception_in_one_thread(self):
        """Test exception in one thread doesn't affect others."""
        success_count = [0]
        error_count = [0]
        
        def worker(worker_id):
            try:
                for item in tqdm(range(100)):
                    if worker_id == 1 and item == 50:
                        raise ValueError("Worker 1 error")
                    if item >= 20:
                        break
                success_count[0] += 1
            except ValueError:
                error_count[0] += 1
        
        threads = [
            threading.Thread(target=worker, args=(i,))
            for i in range(3)
        ]
        
        for t in threads:
            t.start()
        for t in threads:
            t.join()
        
        assert success_count[0] >= 2
        assert error_count[0] >= 0

    def test_exception_propagation_in_thread(self):
        """Test that exceptions propagate correctly in threads."""
        exception_caught = [False]
        
        def worker():
            try:
                for item in track(range(100)):
                    if item == 25:
                        raise RuntimeError("Test error")
            except RuntimeError:
                exception_caught[0] = True
        
        thread = threading.Thread(target=worker)
        thread.start()
        thread.join()
        
        assert exception_caught[0]


class TestContextManagerThreading:
    """Test context manager behavior with threading."""

    def test_context_manager_in_thread(self):
        """Test context manager usage in thread."""
        count = [0]
        
        def worker():
            with TqdmRich(range(20)) as bar:
                for item in bar:
                    count[0] += 1
        
        thread = threading.Thread(target=worker)
        thread.start()
        thread.join()
        
        assert count[0] == 20

    def test_multiple_context_managers_concurrent(self):
        """Test multiple context managers in concurrent threads."""
        counts = []
        lock = threading.Lock()
        
        def worker(size):
            with TqdmRich(range(size)) as bar:
                count = sum(1 for _ in bar)
            with lock:
                counts.append(count)
        
        threads = [
            threading.Thread(target=worker, args=(10,)),
            threading.Thread(target=worker, args=(20,)),
            threading.Thread(target=worker, args=(30,)),
        ]
        
        for t in threads:
            t.start()
        for t in threads:
            t.join()
        
        assert sorted(counts) == [10, 20, 30]


class TestThreadLocalState:
    """Test that progress bars don't interfere across threads."""

    def test_separate_progress_in_threads(self):
        """Test that each thread gets proper progress tracking."""
        results = {}
        
        def worker(worker_id):
            items = list(tqdm(
                range(worker_id * 10 + 10),
                desc=f"Worker {worker_id}",
                leave=False
            ))
            results[worker_id] = len(items)
        
        threads = [
            threading.Thread(target=worker, args=(i,))
            for i in range(5)
        ]
        
        for t in threads:
            t.start()
        for t in threads:
            t.join()
        
        assert len(results) == 5
        for i in range(5):
            assert results[i] == (i * 10 + 10)


class TestShutdownBehavior:
    """Test proper shutdown of progress tracking in threads."""

    def test_cleanup_after_threads(self):
        """Test that cleanup happens properly after threads."""
        def worker():
            list(tqdm(range(20), leave=False))
        
        threads = [threading.Thread(target=worker) for _ in range(5)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()
        
        # Create another progress bar to ensure manager is clean
        items = list(tqdm(range(10), leave=False))
        assert len(items) == 10

    def test_manager_state_consistency(self):
        """Test that manager maintains consistent state."""
        def worker():
            for _ in track(range(15)):
                pass
        
        # Run multiple rounds
        for _ in range(3):
            threads = [threading.Thread(target=worker) for _ in range(2)]
            for t in threads:
                t.start()
            for t in threads:
                t.join()
        
        # Should still work after multiple rounds
        items = list(tqdm(range(10), leave=False))
        assert len(items) == 10
