# Changelog

All notable changes to this project are documented in this file.

## [Unreleased]

### Added
- Insular shipping zone for San Andrés with a 70% surcharge and no promotional coupon.

### Changed
- Replaced the legacy calc interface with calculate_shipping_cost.
- Extracted validation, tariff calculation, discount handling, rounding, and zone strategies.
- Removed the diagnostic flag and console output.

### Fixed
- Corrected weight error message, zone and day validation, Saturday surcharge, half-up rounding, and non-numeric weight handling.

### Removed
- Removed the legacy flag argument.

## [1.0.0] - Baseline
- Added the inherited shipping calculator used as the starting point for the assignment.
