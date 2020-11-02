[app]
title = Accelerometer
package.name = accelerometer
package.domain = org.kivy
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
version = 2.31
requirements = python3,kivy,plyer,numpy,oscpy,jnius
android.permissions = INTERNET, WRITE_EXTERNAL_STORAGE, READ_EXTERNAL_STORAGE
orientation = portrait
fullscreen = 0
android.arch = armeabi-v7a
services = Pong:service.py

[buildozer]
log_level = 2
warn_on_root = 1
