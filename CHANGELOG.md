0.0.4.dev1
===
Added:
- Added file-based configuration for the parser.
- Added proper, file-based logging. Resolves https://github.com/Re-Volt-America/RVA-Points/issues/2
- Added a Console tab to display logs within the app.
- Added an update section which checks and allows for the installation of new parser & cars and tracks data versions from within the app.
- Added improvements for future multi-platform support.

Changed:
- cars/, tracks/, sessions/ & results/ directories are no longer shipped with the parser application, but rather created on execution time.
- cars/ & tracks/ directories in specific have been merged into a single data/ folder.
- Updated README.md to reflect the changes.
- Updated .gitignore to ignore configuration files and other data folders.

Fixed:
- Fixed one session row followed by another in RVGL session logs breaking the parser.
- Fixed tracks with similar names having one display over the other. (e.g. Botanical Garden & Botanical Garden EX would always display as 'BG').

0.0.2-alpha
===
Added:
- Added a few missing cars.
- Added a button to consider Mystery as a valid, playable car.

Changed:
- Updated to 2021-22 Season cars & tracks.

0.0.1-alpha
===
Initial release.
