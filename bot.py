#!/usr/bin/python
from telebot.async_telebot import AsyncTeleBot
import telebot
import logging

import config

bot = AsyncTeleBot(config.TOKEN)
logger = telebot.logger
telebot.logger.setLevel(logging.DEBUG)  # Outputs debug messages to console.
