# -*- coding: utf-8 -*-
"""
Created on Sat Mar 23 13:09:07 2019

@author: shane

This file is part of nutra, a nutrient analysis program.
    https://github.com/nutratech/cli
    https://pypi.org/project/nutra/

nutra is an extensible nutraent analysis and composition application.
Copyright (C) 2018  Shane Jaroch

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""

import os

from colorama import Fore
from dotenv import load_dotenv

# Read in .env file if it exists locally, else look to env vars
load_dotenv(verbose=False)

# TODO: support more settings..
# 1) either with .env VARs, e.g. DEBUG=1
# 2) `~/.nutra/paramters.csv` file, or
# 3) split off into config.py?
NUTRA_DIR = os.path.join(os.path.expanduser("~"), ".nutra")

REMOTE_HOST = "https://nutra-server.herokuapp.com"
SERVER_HOST = os.getenv("NUTRA_OVERRIDE_LOCAL_SERVER_HOST", REMOTE_HOST)


TESTING = SERVER_HOST != REMOTE_HOST

# ---------------------------
# Colors and other settings
# ---------------------------

THRESH_WARN = 0.7
COLOR_WARN = Fore.YELLOW

THRESH_CRIT = 0.4
COLOR_CRIT = Fore.RED

THRESH_OVER = 1.9
# COLOR_OVER = Fore.LIGHTBLACK_EX
COLOR_OVER = Fore.LIGHTMAGENTA_EX

COLOR_DEFAULT = Fore.BLUE

SEARCH_LIMIT = 150


# ------------------------
# Nutrient IDs
# ------------------------
NUTR_ID_KCAL = 208

NUTR_ID_PROTEIN = 203

NUTR_ID_CARBS = 205
NUTR_ID_SUGAR = 269
NUTR_ID_FIBER = 291

NUTR_ID_FAT_TOT = 204
NUTR_ID_FAT_SAT = 606
NUTR_ID_FAT_MONO = 645
NUTR_ID_FAT_POLY = 646


NUTR_IDS_FLAVONES = [
    710,
    711,
    712,
    713,
    714,
    715,
    716,
    734,
    735,
    736,
    737,
    738,
    731,
    740,
    741,
    742,
    743,
    745,
    749,
    750,
    751,
    752,
    753,
    755,
    756,
    758,
    759,
    762,
    770,
    773,
    785,
    786,
    788,
    789,
    791,
    792,
    793,
    794,
]

NUTR_IDS_AMINOS = [
    501,
    502,
    503,
    504,
    505,
    506,
    507,
    508,
    509,
    510,
    511,
    512,
    513,
    514,
    515,
    516,
    517,
    518,
    521,
]
