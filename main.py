#!python3
# -*- coding: UTF-8 -*-

"""
Compilation possible avec java 8 et non avec 11
sudo update-alternatives --config java
java -version
export JAVA_HOME=/usr/lib/jvm/adoptopenjdk-8-hotspot-amd64

Le service s'appelle Pong

Ne pas oublier d'autoriser les droits d'écriture dans Paramètres/Applications
sur Android.
"""

import os
from time import sleep
from runpy import run_path
from threading import Thread

import kivy
kivy.require('1.11.1')

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.clock import Clock
from kivy.properties import NumericProperty

from plyer import utils

from oscpy.client import OSCClient
from oscpy.server import OSCThreadServer

print("Platform =", utils.platform)
ANDROID = utils.platform._platform_android  # retourne True ou False
print("Android =", ANDROID)
if not ANDROID:
    from kivy.core.window import Window
    # Simulation de l'écran de mon tél: 1280*720
    k = 1.0
    WS = (int(720*k), int(1280*k))
    Window.size = WS
    os.environ['JAVA_HOME'] = '/usr/lib/jvm/adoptopenjdk-8-hotspot-amd64'

from jnius import autoclass
"""
Dans buildozer.spec
package.name = accelerometer
package.domain = org.kivy
services = Pong:service.py

SERVICE_NAME = u'{packagename}.Service{servicename}'.format(
    packagename=u'org.kivy.accelerometer',
    servicename=u'ServicePong')

Structure = package.domain.package.name.ServiceToto
package.domain = org.kivy
package.name = accelerometer
soit
org.kivy.accelerometer.ServicePong
"""

SERVICE_NAME = 'org.kivy.accelerometer.ServicePong'
print("SERVICE_NAME:", SERVICE_NAME)


class Accelerometer(BoxLayout):

    activity = NumericProperty(-1)

    def __init__(self, app):

        super().__init__()
        self.app = app
        freq = 50
        self.sensor_status = 0
        Clock.schedule_interval(self.update_display, 1/freq)

    def on_sensor_enable(self):
        """Envoi au service de l'info sensor enable or not"""

        r = self.app.get_running_app()
        if self.sensor_status == 0:
            self.sensor_status = 1
            self.ids.acceleromer_status.text = "Stop Accelerometer"
        elif self.sensor_status == 1:
            self.sensor_status = 0
            self.ids.acceleromer_status.text = "Start Accelerometer"
        print("Envoi de sensor_status:", self.sensor_status)
        r.client.send_message(b'/sensor_enable', [self.sensor_status])

    def on_activity(self, act):
        r = self.app.get_running_app()
        r.client.send_message(b'/activity', [act])

    def update_display(self, dt):
        root = self.app.get_running_app()
        a, b, c, activity, num =    (root.display_list[0],
                                    root.display_list[1],
                                    root.display_list[2],
                                    root.display_list[3],
                                    root.display_list[4])
        self.ids.x_label.text = "X: " + str(a)
        self.ids.y_label.text = "Y: " + str(b)
        self.ids.z_label.text = "Z: " + str(c)
        self.ids.activity_label.text = "Activité: " + str(activity)
        self.ids.number.text = "Indice de boucle: " + str(num)
        self.ids.file_saved.text = root.file
        self.ids.activ_sensor.text = f"Capteur actif: {root.sensor}"

    def do_quit(self):
        self.app.get_running_app().do_quit()


class AccelerometerApp(App):

    def build(self):
        self.display_list = [0]*5
        self.file = ""
        self.sensor = ""
        self.service = None

        self.server = OSCThreadServer()
        self.server.listen( address=b'localhost',
                            port=3003,
                            default=True)
        self.server.bind(b'/acc', self.on_message)
        self.server.bind(b'/file', self.on_file)
        self.server.bind(b'/sensor', self.on_sensor)
        self.client = OSCClient(b'localhost', 3001)

        self.start_service()
        return Accelerometer(App)

    def start_service(self):
        if ANDROID:
            self.service = autoclass(SERVICE_NAME)
            self.m_activity = autoclass(u'org.kivy.android.PythonActivity').mActivity
            argument = ''
            self.service.start(self.m_activity, argument)
        else:
            # Equivaut à:
            # run_path('./service.py', {'run_name': '__main__'}, daemon=True)
            self.service = Thread(  target=run_path,
                                    args=('service.py',),
                                    kwargs={'run_name': '__main__'},
                                    daemon=True)
            self.service.start()
            print("Thread lancé.")

    def on_sensor(self, sens):
        self.sensor = sens.decode('utf-8')

    def on_file(self, f):
        # acc_2020_11_01_14_26_46/acc_2020_11_01_14_29_53.npz
        self.file = f.decode('utf-8')[-51:]

    def on_message(self, *args):
        self.display_list = args

    def on_pause(self):
        print("on_pause")
        return True

    def on_resume(self):
        print("on_resume")

    def do_quit(self):
        if ANDROID:
            self.service.stop(self.m_activity)
            self.service = None
        else:
            self.client.send_message(b'/stop', [1])
            sleep(1)

        AccelerometerApp.get_running_app().stop()


if __name__ == '__main__':
    AccelerometerApp().run()
