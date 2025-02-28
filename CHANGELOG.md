# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1/1.1.0/), and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.1.0] 2025-02-28

### Added

- All functions should now provide logging capabilites (with various degrees of usefulness)
- This CHANGELOG
- Command line flag to change buffersize (may be deprecated in future releases once a sane default is determine)
- "logs" directory for printing of logfile(s)
- logger.py module for handling logging setup
- "utils" directory now contains helper functions for setting up logging

### Changed

- Logging configuration setup now exists in its own separate file
- Print carriage return character instead of newline character to refresh screen (hopefully)
- Versioning in pyproject.toml
- Logfile now writes to "logs" dir instead of "."

