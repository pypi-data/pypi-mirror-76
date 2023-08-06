"""
Minirobots Python interface.

https://gitlab.com/minirobots/minirobots-python


Author: Leo Vidarte <https://minirobots.com.ar>

This is free software:
you can redistribute it and/or modify it
under the terms of the GPL version 3
as published by the Free Software Foundation.
"""

import json
import random
import socket
import string
from datetime import datetime

import requests


DATETIME_FORMAT = '%Y-%m-%d %H:%M:%S'


class API:

    """
    Minirobots API class

    """

    API_URL = 'https://api.minirobots.com.ar'

    @staticmethod
    def get_robot_ip(robot_code):
        try:
            data = API.get_json(f'{API.API_URL}/robots/{robot_code}/ip')
            return data['robot']['ip'], data['robot']['created']
        except Exception:
            raise Exception(f'Robot `{robot_code}` not found')

    @staticmethod
    def send_program_to_robot(robot_ip, doc):
        return API.post_json(f'http://{robot_ip}/program', doc)

    @staticmethod
    def toggle_robot_debug(robot_ip):
        return API.post_json(f'http://{robot_ip}/debug', {})

    @staticmethod
    def get_robot_info(robot_ip):
        return API.get_json(f'http://{robot_ip}/')

    @staticmethod
    def get_robot_status(robot_ip):
        return API.get_json(f'http://{robot_ip}/status')

    @staticmethod
    def get_json(url):
        res = requests.get(url)
        assert res.status_code == 200, res.reason
        return res.json()

    @staticmethod
    def post_json(url, doc):
        data = json.dumps(doc, separators=(',', ':'))
        res = requests.post(url, data=data)
        assert res.status_code == 201, res.reason
        return res.json()


class IP:

    """
    Minirobots Turtle IP class

    """

    def __init__(self, address, created):
        self.address = address
        self.created = datetime.strptime(created, DATETIME_FORMAT)

    @property
    def age(self):
        seconds = (datetime.utcnow() - self.created).seconds
        if seconds < 60:
            return "less than 1 minute"
        if seconds < 3600:
            minutes = int(seconds/60)
            if minutes == 1:
                return "1 minute ago"
            return f"{minutes} minutes ago"
        hours = int(seconds/3600)
        if hours == 1:
            return "1 hour ago"
        return f"{hours} hours ago"

    def __repr__(self):
        return f"IP(address: '{self.address}', age: '{self.age}')"


class Turtle:

    """
    Minirobots Turtle class

    Minirobots Turtle is way for introducing programming to kids.
    It's based on the Logo programming language developed
    by Wally Feurzig and Seymour Papert in 1966.

    Example:
    >>> turtle = Turtle("15354b")
    >>> turtle.auto_send(False)
    >>> for _ in range(4):
    ...   turtle.forward(100)
    ...   turtle.right(90)
    ...
    >>> turtle.send()
    """

    LED_LEFT  = 0
    LED_RIGHT = 1
    LED_BOTH  = 2

    COLORS = (
        (('black', 'none'), (  0,   0,   0)),
        (('blue',),         (  0,   0, 255)),
        (('green',),        (  0, 255,   0)),
        (('cyan',),         (  0, 255, 255)),
        (('red',),          (255,   0,   0)),
        (('magenta',),      (255,   0, 255)),
        (('yellow',),       (255, 255,   0)),
        (('white',),        (255, 255, 255)),
    )

    NOTES = {
        'C1' :  262,
        'C#1':  277,
        'Db1':  277,
        'D1' :  294,
        'D#1':  311,
        'Eb1':  311,
        'E1' :  330,
        'F1' :  349,
        'F#1':  370,
        'Gb1':  370,
        'G1' :  392,
        'G#1':  415,
        'Ab1':  415,
        'A1' :  440,
        'A#1':  466,
        'Bb1':  466,
        'B1' :  494,
        'C2' :  523,
        'C#2':  554,
        'Db2':  554,
        'D2' :  587,
        'D#2':  622,
        'Eb2':  622,
        'E2' :  659,
        'F2' :  698,
        'F#2':  740,
        'Gb2':  740,
        'G2' :  784,
        'G#2':  831,
        'Ab2':  831,
        'A2' :  880,
        'A#2':  932,
        'Bb2':  932,
        'B2' :  988,
        'C3' : 1047,
        'C#3': 1109,
        'Db3': 1109,
        'D3' : 1175,
        'D#3': 1245,
        'Eb3': 1245,
        'E3' : 1319,
        'F3' : 1397,
        'F#3': 1480,
        'Gb3': 1480,
        'G3' : 1568,
        'G#3': 1661,
        'Ab3': 1661,
        'A3' : 1760,
        'A#3': 1865,
        'Bb3': 1865,
        'B3' : 1976,
        'C4' : 2093,
        'C#4': 2217,
        'Db4': 2217,
        'D4' : 2349,
        'D#4': 2489,
        'Eb4': 2489,
        'E4' : 2637,
        'F4' : 2794,
        'F#4': 2960,
        'Gb4': 2960,
        'G4' : 3136,
        'G#4': 3322,
        'Ab4': 3322,
        'A4' : 3520,
        'A#4': 3729,
        'Bb4': 3729,
        'B4' : 3951,
        'C5' : 4186,
    }

    def __init__(self, code, ip=None):
        """Create a Turtle instance

           Arguments:
           code -- a string, indicating the robot ID
           ip (optional) -- a string, with valid IP address

           The robot code is a 6 hexadecimal string

           Example:
           >>> turtle = Turtle("15354b")
        """
        self.code = code.lower()
        self._validate_code()
        self._get_robot_ip(ip)
        self._commands = []
        self._check_connection()

    def _validate_code(self):
        assert len(self.code) == 6, 'code must be 6 chars length'
        assert all(c in string.hexdigits for c in self.code), \
               'code must be hexadecimal'

    def _get_robot_ip(self, ip=None):
        if ip is None:
            address, created = API.get_robot_ip(self.code)
            self._ip = IP(address, created)
        else:
            assert socket.inet_aton(ip)
            self._ip = IP(ip, datetime.now().strftime(DATETIME_FORMAT))

    def _check_connection(self):
        self.debug(False)
        self.auto_send(False)
        self.leds(0, 0, 255)
        self.play_note('C1', 75)
        self.leds(0, 0, 127)
        self.play_note('C2', 75)
        self.send()
        self.auto_send(True)

    @property
    def ip(self):
        """Return the turtle's IP

           No arguments.

           Example (for a Turtle instance named turtle):
           >>> turtle.ip
           '192.168.1.107'
        """
        return self._ip.address

    @property
    def ip_age(self):
        """Return the age of the turtle's IP

           No arguments.

           Example (for a Turtle instance named turtle):
           >>> turtle.ip_age
           '1 hour ago'
        """
        return self._ip.age

    def auto_send(self, on=None):
        """Return/Set the turtle's auto send flag

           Argument:
           on (optional) -- a boolean

           Example (for a Turtle instance named turtle):
           >>> turtle.auto_send()
           True
           >>> turtle.auto_send(False)
           False
        """
        if isinstance(on, bool):
            self._auto_send = on
        return self._auto_send

    def debug(self, on=None):
        """Return/Set the turtle's debug flag

           Argument:
           on (optional) -- a boolean

           Example (for a Turtle instance named turtle):
           >>> turtle.debug()
           False
           >>> turtle.debug(True)
           True
        """
        self._debug = self.status()['debug']
        if isinstance(on, bool):
            if self._debug != on:
                res = API.toggle_robot_debug(self.ip)
                self._debug = res['debug']
        return self._debug

    def info(self):
        """Return the turtle's current info

           No arguments.

           Example (for a Turtle instance named turtle):
           >>> turtle.info()
           {'message': 'Welcome to Minirobots Turtle API! :)',
            'robot': {
                'id': 'minirobots-15354b',
                'ip': '192.168.1.107',
                'mac': '2c:3a:e8:15:35:4b',
                'firmware': '0.3.4',
                'config': {
                    'pen_up': 5,
                    'pen_down': 20,
                    'steps_per_degree': 7.5,
                    'steps_per_mm': 9.8284755764
           }}}
        """
        return API.get_robot_info(self.ip)

    def status(self):
        """Return the turtle's current status

           No arguments.

           Example (for a Turtle instance named turtle):
           >>> turtle.status()
           {'debug': False,
            'queue': {
                'lock': False,
                'size': 512,
                'left': 512
           }}
        """
        return API.get_robot_status(self.ip)

    def forward(self, distance):
        """Move the turtle forward by the specified distance.

           Argument:
           distance -- an integer, millimeters

           Move the turtle forward by the specified distance,
           in millimeters.

           Example (for a Turtle instance named turtle):
           >>> turtle.forward(25)
        """
        self._add(['FD', int(distance)])

    def backward(self, distance):
        """Move the turtle backward by distance.

           Argument:
           distance -- an integer, millimeters

           Move the turtle backward by distance,
           in millimeters.

           Example (for a Turtle instance named turtle):
           >>> turtle.backward(25)
        """
        self._add(['BD', int(distance)])

    def right(self, angle):
        """Turn turtle right by angle units.

           Argument:
           angle -- an integer

           Turn turtle right by angle units.

           Example (for a Turtle instance named turtle):
           >>> turtle.right(45)
        """
        self._add(['RT', int(angle)])

    def left(self, angle):
        """Turn turtle left by angle units.

           Argument:
           angle -- an integer

           Turn turtle left by angle units.

           Example (for a Turtle instance named turtle):
           >>> turtle.left(45)
        """
        self._add(['LT', int(angle)])

    def pen_up(self):
        """Pull the pen up -- no drawing when moving.

           No argument

           Example (for a Turtle instance named turtle):
           >>> turtle.pen_up()
        """
        self._add(['PN', 0])

    def pen_down(self):
        """Pull the pen down -- drawing when moving.

           No argument.

           Example (for a Turtle instance named turtle):
           >>> turtle.pen_down()
        """
        self._add(['PN', 1])

    def leds(self, red, green, blue, led=None):
        """Set the value for both or one of the robot leds.

           Arguments:
           red -- an integer, (0-255)
           green -- an integer, (0-255)
           blue -- an integer, (0-255)
           led (optional) -- an integer, indicating led or leds

           For the led value use the class constant or just an integer:
           Turtle.LED_LEFT or 0
           Turtle.LED_RIGHT or 1
           Turtle.LED_BOTH or 2

           Example (for a Turtle instance named turtle):
           >>> turtle.leds(127, 0, 0)
           >>> turtle.leds(0, 0, 0, Turtle.LED_LEFT)
           >>> color = (0, 127, 0)
           >>> turtle.leds(*color, Turtle.LED_RIGHT)
        """
        if led is None:
            led = Turtle.LED_BOTH
        self._add(['LD', [int(led), int(red), int(green), int(blue)]])

    def leds_color(self, color, led=None):
        """Set the color for both or one of the robot leds.

           Arguments:
           color -- a string, with the color name
           led (optional) -- an integer, indicating led or leds

           Allowed color names are defined in Turtle.COLORS:
           black, none, blue, green, cyan, red, magenta, yellow and white

           For the led value use the class constant or just an integer:
           Turtle.LED_LEFT or 0
           Turtle.LED_RIGHT or 1
           Turtle.LED_BOTH or 2

           Example (for a Turtle instance named turtle):
           >>> turtle.leds_color('red')
           >>> turtle.leds_color('blue', Turtle.LED_LEFT)
           >>> turtle.leds_color('none', Turtle.LED_RIGHT)
        """
        for colors, rgb in Turtle.COLORS:
            if color in colors:
                self.leds(*rgb, led)
                break

    def random_leds(self, led=None):
        """Set and return randomly the color for both or one of the robot leds.

           Arguments:
           led (optional) -- an integer, indicating led or leds

           For the led value use the class constant or just an integer:
           Turtle.LED_LEFT or 0
           Turtle.LED_RIGHT or 1
           Turtle.LED_BOTH or 2

           Example (for a Turtle instance named turtle):
           >>> turtle.random_leds()
           (71, 160, 233)
           >>> turtle.random_leds(Turtle.LED_LEFT)
           (51, 96, 199)
           >>> turtle.random_leds(Turtle.LED_RIGHT)
           (65, 66, 124)
        """
        color = Turtle.get_random_color()
        self.leds(*color, led)
        return color

    def random_led_right(self):
        """Set and return randomly the color for the right robot led.

           No arguments.

           Example (for a Turtle instance named turtle):
           >>> turtle.random_led_right()
           (71, 160, 233)
        """
        color = Turtle.get_random_color()
        self.leds(*color, self.LED_RIGHT)
        return color

    def random_led_left(self):
        """Set and return randomly the color for the left robot led.

           No arguments.

           Example (for a Turtle instance named turtle):
           >>> turtle.random_led_left()
           (71, 160, 233)
        """
        color = Turtle.get_random_color()
        self.leds(*color, self.LED_LEFT)
        return color

    def turn_off_leds(self, led=None):
        """Turn off both of one of the robot leds.

           Arguments:
           led (optional) -- an integer, indicating led or leds

           For the led value use the class constant or just an integer:
           Turtle.LED_LEFT or 0
           Turtle.LED_RIGHT or 1
           Turtle.LED_BOTH or 2

           Example (for a Turtle instance named turtle):
           >>> turtle.turn_off_leds()
           >>> turtle.turn_off_leds(Turtle.LED_RIGHT)
        """
        self.leds(0, 0, 0, led)

    def play_tone(self, frequency, duration=1000):
        """Play the sound according to tone frequency

           Arguments:
           frequency -- an integer, indicating the tone frequency
           duration (optional) -- an integer, indicating milliseconds

           For frecuency use values between (0 - 5000)

           Example (for a Turtle instance named turtle):
           >>> turtle.play_tone(2500)
           >>> turtle.play_tone(440, 250)
        """
        self._add(['TE', [int(frequency), int(duration)]])

    def play_note(self, note, duration=1000):
        """Play the sound according to note value,
           based on standard music notation

           Arguments:
           note -- a string, indicating name of the note
           duration (optional) -- an integer, indicating milliseconds

           For note use values defined in Turtle.NOTES
           Examples:
           C1, C#1, Db1, D1, Eb1... G#4, Ab4, A#4, Bb4, B4, C5

           Example (for a Turtle instance named turtle):
           >>> turtle.play_note('A2')
           >>> turtle.play_tone('Cb5', 1500)
        """
        self.play_tone(Turtle.get_frequency(note), duration)

    def play_random_note(self, duration=1000):
        """Play the sound of a random note and return the name

           Arguments:
           duration (optional) -- an integer, indicating milliseconds

           Example (for a Turtle instance named turtle):
           >>> turtle.play_random_note()
           'A2'
           >>> turtle.play_random_note(1500)
           'Cb5'
        """
        note = Turtle.get_random_note()
        self.play_note(note, duration)
        return note

    def sleep(self, duration=1000):
        """Pause the robot execution program

           Aliases: silence

           Arguments:
           duration (optional) -- an integer, indicating milliseconds

           Example (for a Turtle instance named turtle):
           >>> turtle.sleep()
           >>> turtle.sleep(5000)
        """
        self._add(['SP', int(duration)])

    def queue_lock(self):
        """Lock the robot queue and stop the execution of the program

           No arguments.

           Example (for a Turtle instance named turtle):
           >>> turtle.queue_lock()
        """
        self._add(['QE', 'lock'])

    def queue_unlock(self):
        """Unlock the robot queue and
           continue the execution of the program

           No arguments.

           Example (for a Turtle instance named turtle):
           >>> turtle.queue_lock()
        """
        self._add(['QE', 'unlock'])

    def queue_clear(self):
        """Remove all items in robot queue and
           stop the execution of the program

           No arguments.

           Example (for a Turtle instance named turtle):
           >>> turtle.queue_clear()
        """
        self._add(['QE', 'clear'])

    def send(self, commands=None):
        """Send the commands to robot

           Arguments:
           commands (optional), a list with the commands to execute

           If commands is not None
           the method will send the list of commands to the robot and
           will empty the current accumulated buffer of commands.

           If commands is None and auto_send is False
           the method will send the current buffer of commands and
           then it will empty the buffer.

           This command is useful when you set auto_send as False

           Example (for a Turtle instance named turtle):
           >>> turtle.auto_send(False)
           >>> # turtle actions here
           >>> turtle.send()
        """
        doc = None
        if commands is not None:
            doc = {'CMD': commands}
        elif self._commands and not self._auto_send:
            doc = {'CMD': self._commands}
        if doc is not None:
            if self._debug:
                print('Sending program to robot:', doc)
            API.send_program_to_robot(self.ip, doc)
            self._commands = []

    def stop(self):
        """Stop the robot and abort the execution of the program

           No arguments.

           Example (for a Turtle instance named turtle):
           >>> turtle.stop()
        """
        self.send([['QE', 'clear']])

    def _add(self, command):
        if self._auto_send:
            self.send([command])
        else:
            self._commands.append(command)

    def __repr__(self):
        return f"Turtle(code='{self.code}', ip='{self.ip}')"

    # Helpers

    @staticmethod
    def get_random_color():
        """Return a random color

           No arguments.

           Example (for a Turtle instance named turtle):
           >>> Turtle.get_random_color()
           (47, 104, 98)
        """
        return tuple(random.randrange(0, 256) for _ in range(3))

    @staticmethod
    def get_random_note():
        """Return a random note

           No arguments.

           Example (for a Turtle instance named turtle):
           >>> Turtle.get_random_note()
           'C1'
        """
        return random.choice(list(Turtle.NOTES.keys()))

    @staticmethod
    def get_frequency(note):
        """Return the frequency for a valid note

           Arguments:
           note -- a string, indicating name of the note

           For note use values defined in Turtle.NOTES
           Examples:
           C1, C#1, Db1, D1, Eb1... G#4, Ab4, A#4, Bb4, B4, C5

           Example (for a Turtle instance named turtle):
           >>> Turtle.get_frequency('A2')
           880
        """
        return Turtle.NOTES[note.capitalize()]

    # Aliases

    silence = sleep

    # Demo figures

    def star(self, n, side):
        for _ in range(n):
            self.forward(side)
            self.right(360 / n)
            self.forward(side)
            self.left(720 / n)


class Tortuga(Turtle):

    """
    Tortuga

    Versión español de la clase Turtle.
    """

    COLORS = (
        (('black', 'none', 'negro'), (  0,   0,   0)),
        (('blue',  'azul'),          (  0,   0, 255)),
        (('green', 'verde'),         (  0, 255,   0)),
        (('cyan', 'cian'),           (  0, 255, 255)),
        (('red', 'rojo'),            (255,   0,   0)),
        (('magenta',),               (255,   0, 255)),
        (('yellow', 'amarillo'),     (255, 255,   0)),
        (('white', 'blanco'),        (255, 255, 255)),
    )

    def __init__(self, *args, **kwargs):
        """Crea un objeto Robot para interactuar con un Minirobot"""
        super().__init__(*args, **kwargs)

    def adelante(self, distancia):
        """Mueve la tortuga hacia adelante según el valor de `distancia`
           (en mm)
        """
        self.forward(distancia)

    def atras(self, distancia):
        """Mueve la tortuga hacia atrás según el valor de `distancia`
           (en mm)
        """
        self.backward(distancia)

    def derecha(self, angulo):
        """Gira la tortuga hacia la derecha según el valor de `angulo`"""
        self.right(angulo)

    def izquierda(self, angulo):
        """Gira la tortuga hacia la izquierda según el valor de `angulo`"""
        self.left(angulo)

    def lapiz_arriba(self):
        """Levanta el lápiz"""
        self.pen_up()

    def lapiz_abajo(self):
        """Baja el lápiz"""
        self.pen_down()

    def leds(self, rojo, verde, azul, led=None):
        """Enciende uno o ambos leds del robot
           según el valor de `rojo`, `verde`, `azul`
        """
        super().leds(rojo, verde, azul, led)

    def leds_color(self, color, led=None):
        """Enciende uno o ambos leds del robot según el valor de `color`"""
        super().leds_color(color, led)

    def leds_al_azar(self, led=None):
        """Enciende ambos leds de la tortuga con un color al azar"""
        return self.random_leds(led)

    def led_derecho_al_azar(self):
        """Enciende el led derecho de la tortuga con un color al azar"""
        return self.random_led_right()

    def led_izquierdo_al_azar(self):
        """Enciende el led izquierdo de la tortuga con un color al azar"""
        return self.random_led_left()

    def apagar_leds(self, led=None):
        """Apaga uno o ambos leds del robot"""
        self.turn_off_leds(led)

    def tono(self, frecuencia, duracion=1000):
        """Reproduce la `frecuencia` durante `duracion` milisegundos"""
        self.play_tone(frecuencia, duracion)

    def nota(self, nota, duracion=1000):
        """Reproduce la `nota` durante `duracion` milisegundos"""
        self.play_note(nota, duracion)

    def nota_al_azar(self, duracion=1000):
        """Reproduce una `nota` al azar durante `duracion` milisegundos"""
        return self.play_random_note(duracion)

    def esperar(self, duracion=1000):
        """Detiene a la tortuga durante `duracion` milisegundos"""
        self.sleep(duracion)

    def auto_enviar(self, activado=None):
        """Activa y desactiva el envío automático de comandos a la tortuga.

        Si se usa sin parámetros devuelve el valor actual.

        Cuando el modo auto enviar está en True,
        se realiza un envío HTTP por cada comando que se procesa.
        Esto es útil para cuando estamos usando la consola,
        ya que escribimos una acción y esta se ejecuta inmediatamente.

        Cuando estamos haciendo un programa fuera de la consola,
        lo mejor puede ser procesar todos los comandos primero y finalmente
        enviar el programa completo a la tortuga. De esta manera evitaremos
        hacer muchos envíos HTTP.

        La forma de usarlo es:

            tortuga.auto_enviar(False)
            #
            # acciones
            #
            tortuga.enviar()
        """
        return self.auto_send(on=activado)

    def enviar(self):
        """Envía el programa a la tortuga"""
        self.send()

    def parar(self):
        """Detiene la ejecución del programa"""
        self.stop()

    def __repr__(self):
        return f"Tortuga(code='{self.code}', ip='{self.ip}')"

    # Aliases

    avanzar = adelante
    retroceder = atras
    subir_lapiz = lapiz_arriba
    bajar_lapiz = lapiz_abajo
    encender_leds = leds
    encender_leds_color = leds_color
    encender_leds_al_azar = leds_al_azar
    encender_led_derecho_al_azar = led_derecho_al_azar
    encender_led_izquierdo_al_azar = led_izquierdo_al_azar
    reproducir_tono = tono
    tocar_nota = nota
    tocar_nota_al_azar = nota_al_azar
    silencio = esperar
    obtener_color_al_azar = Turtle.get_random_color
    obtener_nota_al_azar = Turtle.get_random_note
    obtener_frecuencia = Turtle.get_frequency
