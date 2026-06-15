[app]
title = Dead Pixel
package.name = deadpixel
package.domain = com.deadpixel.game
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
source.exclude_dirs = __pycache__,.git,.pytest_cache,.mypy_cache
source.exclude_patterns = */__pycache__/*,*.pyc,assets/player.png,assets/ships_ascii/*
version = 0.6

requirements = python3,kivy==2.3.1,esper==3.7

orientation = portrait
fullscreen = 1

android.permissions = VIBRATE,WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE

android.api = 33
android.minapi = 21
android.ndk = 25b
android.archs = arm64-v8a
android.accept_sdk_license = True

[buildozer]
log_level = 2
warn_on_root = 1
