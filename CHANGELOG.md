# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

## Unreleased

### Added

- Support for Python 3.13.

### Removed

- Support for Python 3.8.

## [0.3.0] - 2023-08-30

### Changed

- The output will not be different between regular and dry-run mode.

  Prior to this, when the tool was run in dry-run mode, it would output "would
  write" and "would overwrite" instead of "writing" and "overwriting". The tool
  will now always output "writing" and "overwriting". To indicate that dry-run
  mode is active, a new message ("dry-run: no files will be written") is shown
  before the regular output.

### Fixed

- Files will not be overwritten if there is no change to be made.

## [0.1.0] - 2023-08-09

Initial release.
