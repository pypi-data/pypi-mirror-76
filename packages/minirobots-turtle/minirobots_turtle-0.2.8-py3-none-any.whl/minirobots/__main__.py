"""
Minirobots Python interface.

https://gitlab.com/minirobots/minirobots-python


Author: Leo Vidarte <https://minirobots.com.ar>

This is free software:
you can redistribute it and/or modify it
under the terms of the GPL version 3
as published by the Free Software Foundation.
"""


if __name__ == '__main__':
    import atexit
    import os
    import readline
    import rlcompleter
    from .turtle import Turtle

    history_path = os.path.expanduser(".minirobots-history")

    # readline.parse_and_bind('tab: menu-complete')
    readline.parse_and_bind('tab: complete')

    def save_history(history_path=history_path):
        import readline
        readline.write_history_file(history_path)

    if os.path.exists(history_path):
        readline.read_history_file(history_path)

    atexit.register(save_history)
    del os, atexit, readline, rlcompleter, save_history, history_path

    print("""
    Te damos la bienvenida a la interfaz interactiva de Minirobots!
    Desde aquí podrás programar tu tortuga en tiempo real 😀

    Para ver la ayuda completa escribí

        help(Turtle)⏎

    Si querés ver sólo la ayuda de alguna función específica,
    como por ejemplo 'forward', escribí

        help(Turtle.forward)⏎
    """)
