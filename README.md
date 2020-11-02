# Kivy Accelerometer Service OSC

### Contexte
* Debian 10 Buster
* Kivy 1.11.1

### Principes

* Cette application enregistre les accélérations du téléphone dans des fichiers,
périodiquement, et tourne en background.
* La communication entre main.py et service.py se fait en OSC.
* Le script service.py continue à tourner même lorsque l'application est en pause/réduite.

### La documentation sur le wiki ressources.labomedia.org

* [Kivy: Android Service](https://ressources.labomedia.org/kivy_android_service)
* [Kivy: Les pages Kivy en détails](https://ressources.labomedia.org/les_pages_kivy_en_details)
* [Kivy: oscpy](https://ressources.labomedia.org/kivy_oscpy)
* [Kivy: jnius](https://ressources.labomedia.org/kivy_jnius)
* [Kivy: plyer](https://ressources.labomedia.org/kivy_plyer)


### Merci à

* [Labomedia](https://labomedia.org/)
* [tshirtman kivy_service_osc](https://github.com/tshirtman/kivy_service_osc)
