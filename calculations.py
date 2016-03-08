#-*- coding: utf-8 -*-

# 2015-2016 Complementos de Programacao
# Grupo 3
# 43134 Luís Filipe Leal Campos
# 48392 Mariana Vieira De Almeida Nave

# module with functions for specific calculations (in contrast with module timeTT, which contains functions
# for more general calculations)

from constants import *
from timeTT import *
from Time import Time


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
    delay = Time('00:00')

    if old_service.getServiceArrivalHour().diff(reservation.getReservRequestedStartHour()) > Time('00:00'):
        delay = old_service.getServiceArrivalHour().diff(reservation.getReservRequestedStartHour())

    startHour = reservation.getReservRequestedStartHour().add(delay)
    endHour = reservation.getReservRequestedEndHour().add(delay)

    return [startHour, endHour]


