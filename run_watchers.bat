@echo off
start /B python watcher\watcher.py
start /B python action_watcher.py
echo Watcher scripts started in the background.
echo You can close this window.
