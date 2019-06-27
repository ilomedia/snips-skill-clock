#!/usr/bin/env python2
# -*- coding: utf-8 -*-

from hermes_python.hermes import Hermes
from datetime import datetime
from pytz import timezone

MQTT_IP_ADDR = "localhost"
MQTT_PORT = 1883
MQTT_ADDR = "{}:{}".format(MQTT_IP_ADDR, str(MQTT_PORT))


def verbalise_hour(i):
    if i == 0:
        return "minuit"
    elif i == 1:
        return "une heure"
    elif i == 12:
        return "midi"
    elif i == 21:
        return "vingt et une heures"
    else:
        return "{0} heures".format(str(i))


def verbalise_minute(i):
    if i == 0:
        return ""
    elif i == 1:
        return "une"
    elif i == 21:
        return "vingt et une"
    elif i == 31:
        return "trente et une"
    elif i == 41:
        return "quarante et une"
    elif i == 51:
        return "cinquante et une"
    elif i == 15:
        return "et quart"
    elif i == 30:
        return "et demi"
    elif i == 40:
        return "moins vingt"
    elif i == 45:
        return "moins le quart"
    elif i == 50:
        return "moins dix"
    elif i == 50:
        return "moins cinq"
    else:
        return "{0}".format(str(i))


def intent_received(hermes, intent_message):

    if intent_message.intent.intent_name == 'duch:askTime':

        sentence = 'Il est '
        print(intent_message.intent.intent_name)

        now = datetime.now(timezone('Europe/Paris'))

        minute = verbalise_minute(now.minute)

        if now.hour > 12:
            heure = "{0} heure".format(str(now.hour - 12)) + " " + minute + " de l'apres-midi"
        else:
            heure = verbalise_hour(now.hour) + " " + minute

        sentence += heure

        print(sentence)

        hermes.publish_end_session(intent_message.session_id, sentence.decode("latin-1"))


with Hermes(MQTT_ADDR) as h:
    h.subscribe_intents(intent_received).start()