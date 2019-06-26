#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import ConfigParser
from hermes_python.hermes import Hermes
from hermes_python.ffi.utils import MqttOptions
from hermes_python.ontology import *
from datetime import datetime
from pytz import timezone
import io
import subprocess

CONFIGURATION_ENCODING_FORMAT = "utf-8"
CONFIG_INI = "config.ini"

class SnipsConfigParser(ConfigParser.SafeConfigParser):
    def to_dict(self):
        return {section : {option_name : option for option_name, option in self.items(section)} for section in self.sections()}


def read_configuration_file(configuration_file):
    try:
        with io.open(configuration_file, encoding=CONFIGURATION_ENCODING_FORMAT) as f:
            conf_parser = SnipsConfigParser()
            conf_parser.readfp(f)
            return conf_parser.to_dict()
    except (IOError, ConfigParser.Error) as e:
        return dict()


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

def subscribe_intent_callback(hermes, intentMessage):
    conf = read_configuration_file(CONFIG_INI)
    action_wrapper(hermes, intentMessage, conf)


def action_wrapper(hermes, intentMessage, conf):
    if intentMessage.intent.intent_name == 'Joseph:askTime':

        sentence = 'Il est '
        print(intentMessage.intent.intent_name)

        now = datetime.now(timezone('Europe/Paris'))

        minute = verbalise_minute(now.minute)

        if now.hour > 12:
            heure = "{0} heure".format(str(now.hour - 12)) + " de l'après-midi" + " " + minute
        else:
            heure = verbalise_hour(now.hour) + " " + minute

        sentence += heure

        print(sentence)

        # hermes.publish_continue_session(intent_message.session_id, sentence, ["Joseph:greetings"])
        hermes.publish_end_session(intentMessage.session_id, sentence)


if __name__ == "__main__":
    mqtt_opts = MqttOptions()
    with Hermes(mqtt_options=mqtt_opts) as h:
        h.subscribe_intents(subscribe_intent_callback).start()
