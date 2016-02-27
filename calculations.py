#-*- coding: utf-8 -*-

# 2015-2016 Complementos de Programacao
# Grupo 3
# 43134 Luís Filipe Leal Campos
# 48392 Mariana Vieira De Almeida Nave

# module with functions for specific calculations (in contrast with module timeTT, which contains functions
# for more general calculations)

from constants import *
from timeTT import *


def calculateDelay(old_service, reservation):
    """Calculates start and end times of the new_service, with delay, if that's the case.

    Requires:
    reservation is a sublist of a list with the structure as in the output of
    consultStatus.readReservationsFile; service is a sublist of a list with
    the structure as in the output of consultStatus.waiting4ServicesList.
    Ensures:
    A two-element list in which the first element is the starting time of the service
    with or without delay and the second element is the end time of the service with
    or without delay.
    """
    delay = '00:00'

    if diff(old_service[INDEXArrivalHour], reservation[INDEXRequestedStartHour]) > '00:00':
        delay = diff(old_service[INDEXArrivalHour], reservation[INDEXRequestedStartHour])

    startHour = add(reservation[INDEXRequestedStartHour], delay)
    endHour = add(reservation[INDEXRequestedEndHour], delay)

    return [startHour, endHour]


def kmsLeftVehicle(service):
    """Calculates how many kilometers a vehicle can still do.

    Requires:
    service is a sublist of a list with the structure as in the output of
    consultStatus.waiting4ServicesList.
    Ensures:
    An int corresponding to the number of km a vehicle can still make.
    """

    return int(service[INDEXINDEXVehicAutonomy]) - int(service[INDEXAccumulatedKms])
