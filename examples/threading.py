"""
Multi-threading examples with tqdm_rich.

This module demonstrates how tqdm_rich handles concurrent progress tracking
across multiple threads safely.
"""

import threading
import time

from tqdm_rich import tqdm, track


def example_simple_threading():
    """
    Example 1: Simple multi-threaded usage.

    Multiple threads can create progress bars independently
    and they will display correctly.
    """
    print("Example 1: Simple multi-threading")
    print("-" * 50)

    def worker(worker_id):
        for item in tqdm(range(30), desc=f"Worker {worker_id}"):
            time.sleep(0.02)

    threads = [threading.Thread(target=worker, args=(i,)) for i in range(3)]

    for t in threads:
        t.start()

    for t in threads:
        t.join()

    print("✓ All workers completed\n")


def example_producer_consumer():
    """
    Example 2: Producer-consumer pattern with progress tracking.

    One thread produces items, another consumes them,
    each with its own progress bar.
    """
    print("Example 2: Producer-consumer pattern")
    print("-" * 50)

    items = []
    items_lock = threading.Lock()

    def producer():
        for i in tqdm(range(50), desc="Producing"):
            time.sleep(0.01)
            with items_lock:
                items.append(i)

    def consumer():
        processed = 0
        while processed < 50:
            with items_lock:
                if items:
                    items.pop(0)
                    processed += 1
            time.sleep(0.01)

        # Show completion
        for _ in tqdm(range(50), desc="Consuming"):
            pass

    prod_thread = threading.Thread(target=producer)
    cons_thread = threading.Thread(target=consumer)

    prod_thread.start()
    cons_thread.start()

    prod_thread.join()
    cons_thread.join()

    print("✓ Producer-consumer completed\n")


def example_thread_pool_simulation():
    """
    Example 3: Thread pool pattern simulation.

    Multiple worker threads processing tasks with progress tracking.
    """
    print("Example 3: Thread pool pattern")
    print("-" * 50)

    def task_worker(worker_id, task_count):
        for task in tqdm(
            range(task_count), desc=f"Worker {worker_id}", leave=False
        ):
            time.sleep(0.01)

    # Create a pool of workers
    num_workers = 4
    tasks_per_worker = 25

    threads = [
        threading.Thread(target=task_worker, args=(i, tasks_per_worker))
        for i in range(num_workers)
    ]

    for t in threads:
        t.start()

    for t in threads:
        t.join()

    print(
        f"✓ {num_workers} workers completed {num_workers * tasks_per_worker} tasks\n"
    )


def example_synchronized_progress():
    """
    Example 4: Synchronized progress tracking across threads.

    Threads synchronize their progress with a shared counter.
    """
    print("Example 4: Synchronized progress")
    print("-" * 50)

    shared_progress = {"completed": 0}
    progress_lock = threading.Lock()
    total_items = 100

    def synchronized_worker(worker_id):
        local_items = list(range(25))
        for item in tqdm(local_items, desc=f"Worker {worker_id}", leave=False):
            time.sleep(0.01)
            with progress_lock:
                shared_progress["completed"] += 1

    threads = [
        threading.Thread(target=synchronized_worker, args=(i,))
        for i in range(4)
    ]

    for t in threads:
        t.start()

    for t in threads:
        t.join()

    print(f"✓ Total completed: {shared_progress['completed']}/{total_items}\n")


def example_parallel_file_processing():
    """
    Example 5: Simulated parallel file processing.

    Multiple threads processing "files" with progress tracking.
    """
    print("Example 5: Parallel file processing")
    print("-" * 50)

    files = [f"file_{i}.txt" for i in range(20)]
    files_lock = threading.Lock()

    def process_file(worker_id):
        processed = []
        while True:
            with files_lock:
                if not files:
                    break
                file_name = files.pop(0)

            # Simulate file processing
            for _ in tqdm(
                range(10), desc=f"Processing {file_name}", leave=False
            ):
                time.sleep(0.01)

            processed.append(file_name)

        print(f"  Worker {worker_id}: Processed {len(processed)} files")

    threads = [
        threading.Thread(target=process_file, args=(i,)) for i in range(4)
    ]

    for t in threads:
        t.start()

    for t in threads:
        t.join()

    print("✓ All files processed\n")


def example_track_with_threading():
    """
    Example 6: Using track() in multi-threaded environment.

    The track() function works seamlessly with threading.
    """
    print("Example 6: track() with threading")
    print("-" * 50)

    def worker(worker_id):
        for item in track(range(40), description=f"Task {worker_id}"):
            time.sleep(0.01)

    threads = [threading.Thread(target=worker, args=(i,)) for i in range(3)]

    for t in threads:
        t.start()

    for t in threads:
        t.join()

    print("✓ All tasks completed\n")


def example_stress_test():
    """
    Example 7: Stress test with many concurrent threads.

    This demonstrates thread safety with high concurrency.
    """
    print("Example 7: Stress test (10 concurrent threads)")
    print("-" * 50)

    def stress_worker(worker_id):
        for _ in tqdm(range(50), desc=f"Stress {worker_id}", leave=False):
            time.sleep(0.005)

    threads = [
        threading.Thread(target=stress_worker, args=(i,)) for i in range(10)
    ]

    start_time = time.time()

    for t in threads:
        t.start()

    for t in threads:
        t.join()

    elapsed = time.time() - start_time
    print(f"✓ Stress test completed in {elapsed:.2f}s\n")


def example_mixed_progress_modes():
    """
    Example 8: Mixing tqdm and track in threads.

    Demonstrates that both APIs work correctly together in threads.
    """
    print("Example 8: Mixed progress modes")
    print("-" * 50)

    def tqdm_worker(worker_id):
        for item in tqdm(range(25), desc=f"tqdm {worker_id}", leave=False):
            time.sleep(0.01)

    def track_worker(worker_id):
        for item in track(range(25), description=f"track {worker_id}"):
            time.sleep(0.01)

    threads = [
        threading.Thread(target=tqdm_worker, args=(0,)),
        threading.Thread(target=track_worker, args=(1,)),
        threading.Thread(target=tqdm_worker, args=(2,)),
        threading.Thread(target=track_worker, args=(3,)),
    ]

    for t in threads:
        t.start()

    for t in threads:
        t.join()

    print("✓ Mixed modes completed\n")


if __name__ == "__main__":
    print("\n" + "=" * 50)
    print("tqdm_rich Threading Examples")
    print("=" * 50 + "\n")

    example_simple_threading()
    example_producer_consumer()
    example_thread_pool_simulation()
    example_synchronized_progress()
    example_parallel_file_processing()
    example_track_with_threading()
    example_stress_test()
    example_mixed_progress_modes()

    print("=" * 50)
    print("All threading examples completed! ✨")
    print("=" * 50)
