# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).

## [unreleased]
### Added
### Changed
### Fixed
### Removed
### Deprecated

## [v2.3.0] - 2023-09-05
### Fixed
- Prevent crash when reading from empty log file at very first invocation.
### Removed
- Remove Python 3.7 support.

## [v2.2.0] - 2023-02-07
### Added
- Fallback to using system media player if `simpleaudio` not available (configurable by environment variable `PYDARTZ_MEDIA_PLAYER`).
### Removed
- Remove Python 3.6 support.

## [v2.1.1] - 2023-01-08
### Changed
- Update suggestions for finishes.
- Officially support Python 3.11.

## [v2.1.0] - 2023-01-01
### Added
- Handle keyboard interrupt.
### Changed
- Display smaller banner for narrow terminals.
