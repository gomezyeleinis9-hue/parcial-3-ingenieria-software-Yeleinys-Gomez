# Changelog

All notable changes to this project are documented in this file.

## [2.0.0] - 2026-11-11

### Added
- Insular shipping zone for San Andrés with a 70% surcharge and no promotional coupon.

### Changed
- Replaced the legacy calc interface with calculate_shipping_cost.
- Extracted validation, tariff calculation, discount handling, rounding, and zone strategies.

### Fixed
- Corrected weight error message, zone and day validation, Saturday surcharge, half-up rounding, and non-numeric weight handling.

### Removed
- Removed the diagnostic flag argument and console output.

## [1.0.0] - 2026-11-11
- Added the inherited shipping calculator used as the starting point for the assignment.
