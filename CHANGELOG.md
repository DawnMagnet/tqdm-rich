# Changelog

All notable changes to the tqdm-rich project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Planned Features
- Custom column configuration
- Progress persistence/resumption
- Batch progress bar mode
- Integration with async/await patterns

## [0.1.0] - 2025-01-15

### Added
- Initial release
- `tqdm()` function for tqdm-compatible progress bars using Rich backend
- `TqdmRich` class for class-based progress tracking
- `track()` generator function for elegant progress tracking
- Thread-safe progress management with internal locking
- Automatic color indication:
  - White for running progress
  - Green for successful completion
  - Red for errors or interruption
- Support for known and unknown total lengths
- Logarithmic progress mode for generators and unknown totals
- Transient mode for cleaner output
- Full tqdm API compatibility for easy migration
- Comprehensive documentation and examples
- Extensive test suite with 100+ tests covering:
  - Basic functionality
  - Edge cases (empty, single item iterables)
  - Error handling
  - Context manager usage
  - Multi-threaded concurrent access
  - Generator and custom iterable support

### Features
- **Beautiful Progress Bars**: Renders gorgeous terminal progress bars using Rich
- **Thread-Safe**: Fully thread-safe with RLock-protected access
- **tqdm Compatible**: Drop-in replacement with familiar API
- **Smart Coloring**: Automatic state-based color changes
- **Flexible Modes**: Linear and logarithmic progress tracking
- **Rich Integration**: Leverages Rich's powerful formatting
- **Generator Support**: Elegant generator-based progress tracking

### Dependencies
- rich >= 10.0.0: Core rendering engine

### Development Dependencies
- pytest >= 7.0.0: Testing framework
- pytest-cov >= 4.0.0: Coverage reporting
- black >= 23.0.0: Code formatting
- ruff >= 0.1.0: Linting
- mypy >= 1.0.0: Type checking

### Documentation
- Comprehensive README with quick start guide
- API reference for all public functions and classes
- Thread safety documentation
- Multi-task progress examples
- Error handling examples
- Configuration guide

### Testing
- 50+ tests for tqdm() and TqdmRich class
- 40+ tests for track() function
- 30+ tests for multi-threading and concurrency
- Edge case coverage (empty iterables, single items, large iterables)
- Exception and error state handling tests
- Context manager tests
- Type preservation tests

## Notes for Future Releases

### v0.2.0 (Planned)
- Custom progress column configuration
- Support for progress bar presets (fancy, simple, minimal)
- Better logging integration
- Performance optimizations

### v0.3.0 (Planned)
- Async/await support with AsyncTrack
- Progress bar persistence (save/restore state)
- Integration with multiprocessing
- Advanced statistics and metrics

### v1.0.0 (Planned)
- Stable API guarantee
- Complete feature parity with major tqdm features
- Performance benchmarks
- Official 3.8 - 3.13 support guarantee
