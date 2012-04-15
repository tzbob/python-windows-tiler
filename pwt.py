import re #CX_Freeze throws up errors without it

from pwt.controller import Controller
from singleinstance import Singleinstance

import sys

import logging
logging.basicConfig(filename="errors.log"
        , level=logging.DEBUG
        , format="%(asctime)s - %(levelname)s - %(message)s"
)

if __name__ == "__main__":

    #way to assure a singleinstance
    this = Singleinstance()

    if not this.alreadyrunning():

        #initialization

        controller = Controller("Python Windows Tiler")

        logging.info("START controller")

        controller.start()


