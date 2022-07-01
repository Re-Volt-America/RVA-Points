0.0.2.1.dev3
===
Changed:
- Car names are now ignored for results in the Randoms class.

0.0.2.1.dev2
===
Added:
- INFO message box for tracks missing a short name.
- ERROR message box for racers with no team parsed on teams results.
- 1st, 2nd and 3rd places are now colour highlighted at the Preview tab(gold, silver and bronze respectively).

Changed:
- Cleaned up some Console logs.
- Scrollbars are now seamlessly restored when resizing the app's window.
- Refactored internal colour constants.
- Changed cell highlight colour to yellow at the Preview tab.

Fixed:
- Fixed scrollbars disappearing at Preview tab.

0.0.2.0
===
Added:
- Cap to the maximum multiplier to 4.0 (including bonus).

Changed:
- Rename macOS to macos internally.
- Now scoring is determined for each individual race.
- Updated build.sh.

Fixed:
- Fixed file dialogs ignoring files being opened.

0.0.1.5.dev6
===
Added:
- Added a full deployment pipeline via GitHub Actions.
- Added Full support for Linux platforms. (Compiling against Ubuntu 18.04)
- Added partial Beta support for MacOS Intel & Apple Silicon platforms. (Compiling against MacOS 10.15) (needs testing)

Changed:
- The parser will now only auto-exit after update if on Windows.
- Update setup.py to include missing dependencies.
- Changed automatic updates to reflect deploy changes.
- Changed version format.
  - Previously: x.x.x.devx.
  - Now: x.x.x.x.devx.
- Changed RVA-Data distribute paths for fetching.

Fixed:
- Fixed Fatal IO error 11 on Linux when updating.
- Fixed OSError: [Errno 26] Text file busy on Linux when updating.
- Fixed file contents being altered when fetching from distribute.
- Fixed [Linux] Pango:ERROR:pango-layout.c:3871.
- Fixed files not opening on linux & macOS platforms.

0.1.4.dev1
===
Changed:
- When parsing team sessions, players display without their team prefix next to their names on preview and exported results.
- Moved Open Parser Folder button to the bottom of the Quick Access box.
- Changed Teams Session checkbox's selection status to be persistent.

Fixed:
- Fixed exporting results always saving result files to results/ regardless of the selected directory via dialog.
- Fixed version having changed to 0.1.0.dev0.

0.0.4.dev3
===
Fixed:
- Fixed some track names not being correctly encoded and decoded.

0.0.4.dev2
===
Fixed:
- Fixed [WinError 5] Access Denied when trying to update.
- Fixed reverse track names not displaying in results.

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
