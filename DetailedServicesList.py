from UserList import UserList
from DetailedService import DetailedService
from copy import deepcopy
from ServicesList import ServicesList
from constants import *
from Time import Time
from operator import attrgetter

class DetailedServicesList(UserList):

    def __init__(self, drivers_p=None, vehicles_p=None, services_p=None):
        UserList.__init__(self)

        if (drivers_p is not None) and (vehicles_p is not None) and (services_p is not None):

            serviceList = deepcopy(services_p)
            serviceList.reverse()

            driversInWaitingList = []
            detailedWaitingList = ServicesList()

            # Obtains sublist SL
            for service in serviceList:
                driver = service.getServiceDriver()
                driverTerminated = service.getServiceDriverStatus() == STATUSTerminated
                if (driver not in driversInWaitingList) and (not driverTerminated):
                    if service.getServiceDriverStatus() == STATUSCharging:
                        service.resetVehic()
                    driversInWaitingList.append(driver)
                    detailedWaitingList.append(service)

            # Creates a list of services with further data items
            for service in detailedWaitingList:
                drivername = service.getServiceDriver()
                driver = drivers_p[drivername]
                vehicleplate = service.getServicePlate()
                vehicle = vehicles_p[vehicleplate]
                detailedService = DetailedService(driver, vehicle, service)
                self.append(detailedService)

            # Sorting according to increasing availability time,
            # untying with drivers's names

            self.sort()

    def addNoServiceDriver(self, waiting4ServicesList):
        """Adds the drivers/vehicles that had no service in the current period to the list
        of new services.

        Requires:
        new_services is a list of lists with the structure of the output of
        consultStatus.readServicesFile although not necessarily ordered;
        waiting4Services is a list of lists with the structure of
        consultStatus.waiting4ServicesList
        Ensures:
        a list of lists similar to new_services but with list(s), corresponding
        to drivers/vehicles which had no service in the current, appended to it.
        """
        # list of names of drivers with services
        names_of_drivers_with_services = [service.getServiceDriver() for service in self]

        # services of the previous period of the drivers which got no services in this period
        ex_services_of_drivers_with_no_services = []
        for service in waiting4ServicesList:
            if service.getServiceDriver() not in names_of_drivers_with_services:
                ex_services_of_drivers_with_no_services.append(service)

        for service in ex_services_of_drivers_with_no_services:
            service.noService()
            self.append(service)

    def nextDriver(self, reservation):
        """Returns the index of the driver/vehicle to work on the reservation.

        Requires:
        reservation is a Reservation object.
        self is a ServiceList object containing Services with the detailed attributes defined.
        Ensures:

        """
        i = 0

        # checks if reservation would pass km limit of vehicle or time limit of driver and chooses another driver if that's the case
        # while cycle stops also when all the drivers were checked
        while i < len(self) and \
                (int(reservation.getReservCircuitKms()) >= self[i].calculateKmsLeft() or
                         reservation.duration() >= Time(TIMELimit).diff(self[i].getAccumTime())):
            i += 1

        return i

    def writeServicesFile(services_p, file_name_p, header_p):
        """Writes a collection of services into a file.

        Requires:
        services_p is a list with the structure as in the output of
        updateServices representing the services in a period p;
        file_name_p is a str with the name of a .txt file whose end (before
        the .txt suffix) indicates the period p, as in the examples provided in
        the general specification (omitted here for the sake of readability);
        and header is a string with a header concerning period p, as in
        the examples provided in the general specification (omitted here for
        the sake of readability).
        Ensures:
        writing of file named file_name_p representing the collection of
        services in services_p and organized as in the examples provided in
        the general specification (omitted here for the sake of readability);
        in the listing in this file keep the ordering of services in services_p.
        """

        f = open(file_name_p + '.txt', 'w')

        h = header_p.split(',')

        for line in h:
            f.write(line + '\n')

        services_p = sorted(services_p, key=attrgetter('_servArrivalHour', '_servDriver'))

        for service in services_p:
            line = service.getServiceDriver() + ", " + service.getServicePlate() + ", " + service.getServiceClient() + ", " + \
                   str(service.getServiceDepartHour()) + ", " + str(service.getServiceArrivalHour()) + ", " + service.getServiceCircuit() + ", " + \
                   service.getServiceCircuitKms() + ", " + service.getServiceDriverStatus()
            f.write(line + '\n')

        f.close()





