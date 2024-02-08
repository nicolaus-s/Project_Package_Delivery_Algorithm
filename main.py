#Nicolaus Shaffer, 001097144
import datetime
import Truck
import DataHandler

#Function is called when the program accepts user input
def truckRoutes(hour, minute, reportType, pId = 0):

    #Instantiate variable to store user input for hour and minute
    timeInput = datetime.datetime(100, 1, 1, hour, minute, 00)

    # Initialize Trucks into a dictionary. Trucks 1 and 2 start with drivers (the 'True' value); Truck 3 starts with no driver.
    allTrucks = {}
    allTrucks['1'] = Truck.Truck(1, True, 8)
    allTrucks['2'] = Truck.Truck(2, True)
    allTrucks['3'] = Truck.Truck(3, False)

    # Initialize hub using Truck class.
    hub = Truck.Truck('Hub', False, 40)

    # Load Hub with all packages from PackageHash table, set package status to 'at the hub'
    i = 0
    while len(hub.Packages) < hub.Capacity:
        i = i + 1
        hub.Packages[str(i)] = DataHandler.packageHash.search(str(i))
        hub.Packages[str(i)].Status = 'at the hub'

    # Load each Truck with specific packages truck
    for t in allTrucks:
        allTrucks[t].loadSpecialPackages(hub.Packages)

    # Finish loading trucks 1 and 3 with remaining packages
    allTrucks['1'].loadTruckEfficiently(hub.Packages)
    allTrucks['3'].loadTruckEfficiently(hub.Packages)

    # Set clock to 8:00AM
    clock = datetime.datetime(100, 1, 1, 8, 00, 00)

    # Initialize variable to be used as 1 second increment
    oneSecond = datetime.timedelta(seconds=1)

    # Initialize mileage counter
    totalMileage = 0

    #Instantiate variable to check if package report has been written to the console for the user
    reportSent = False

    #Loop until end of the business day at 17:00
    while clock.hour <= 17:
        #Send user report if clock is equal to user's input time
        if (clock.time() == timeInput.time()) and (reportSent == False) and (reportType == 1):
            reportSent = True
            print("\n----------------%s Status Report for All Packages--------------------" % str(timeInput.time()))
            DataHandler.packageHash.allPackageReport()
        if (clock.time() == timeInput.time()) and (reportSent == False) and (reportType == 2):
            reportSent = True
            print("\n----------------%s Status Report for Package ID %s--------------------" % ((str(timeInput.time())),pId))
            DataHandler.packageHash.singlePackageReport(pId)
        if (clock.time() == timeInput.time()) and (reportSent == False) and (reportType == 3):
            reportSent = True
            print("\n----------------%s Truck Mileage Report--------------------" % str(timeInput.time()))
            print("Total Truck Mileage: % d" % totalMileage)
        #Handle package 9's address correction at 10:20
        if (clock.time() == datetime.time(10, 20, 00)) and ('9' in allTrucks[t].Packages and (allTrucks[t].Packages['9'].Address != '410 S State St')):
            updatedAddressKey = [k for k, v in DataHandler.addressData.items() if v.ShortAddress == '410 S State St'].pop()
            allTrucks[t].Packages['9'].AddressKey = updatedAddressKey
            allTrucks[t].Packages['9'].Address = DataHandler.addressData[updatedAddressKey].ShortAddress
            allTrucks[t].Packages['9'].City = DataHandler.addressData[updatedAddressKey].City
            allTrucks[t].Packages['9'].Zip = DataHandler.addressData[updatedAddressKey].Zip
        #For each Truck
        for t in allTrucks:
            #If Truck is driving
            if allTrucks[t].IsDriving == True:
                #Check Truck for priority packages
                priorityPackageCount = [k for k, v in allTrucks[t].Packages.items() if v.Deadline != 'EOD']
                #Set first destination and leave HUB
                if allTrucks[t].ArrivalTime == None:
                    #Identify next closest address, travel distance, travel time for priority packages
                    if len(priorityPackageCount) > 0:
                        priorityPackages = {}
                        for p in priorityPackageCount:
                            priorityPackages[p] = allTrucks[t].Packages[p]
                        travelDistance = float(DataHandler.minDistance(allTrucks[t].Location, priorityPackages)[1])
                        travelTime = datetime.timedelta(minutes=(travelDistance / allTrucks[t].Speed * 60))
                        allTrucks[t].ArrivalTime = clock + travelTime
                        allTrucks[t].Location = DataHandler.minDistance(allTrucks[t].Location, priorityPackages)[0]
                        totalMileage += travelDistance
                    #Identify next closest address, travel distance, and travel time
                    else:
                        travelDistance = float(DataHandler.minDistance(allTrucks[t].Location, allTrucks[t].Packages)[1])
                        travelTime = datetime.timedelta(minutes=(travelDistance/allTrucks[t].Speed*60))
                        allTrucks[t].ArrivalTime = clock + travelTime
                        allTrucks[t].Location = DataHandler.minDistance(allTrucks[t].Location, allTrucks[t].Packages)[0]
                        totalMileage += travelDistance
                #Arrive at destination, deliver packages
                elif (allTrucks[t].ArrivalTime <= clock) and (len(allTrucks[t].Packages) > 0):
                    #Deliver packages to this address
                    allTrucks[t].deliverPackages(clock.time())
                    #Check Truck for priority packages
                    priorityPackageCount = [k for k, v in allTrucks[t].Packages.items() if v.Deadline != 'EOD']
                    #Identify next closest address, travel distance, travel time for priority packages
                    if len(priorityPackageCount) > 0:
                        priorityPackages = {}
                        for p in priorityPackageCount:
                            priorityPackages[p] = allTrucks[t].Packages[p]
                        travelDistance = float(DataHandler.minDistance(allTrucks[t].Location, priorityPackages)[1])
                        travelTime = datetime.timedelta(minutes=(travelDistance / allTrucks[t].Speed * 60))
                        allTrucks[t].ArrivalTime = clock + travelTime
                        allTrucks[t].Location = DataHandler.minDistance(allTrucks[t].Location, priorityPackages)[0]
                        totalMileage += travelDistance
                    #If any packages remain on the Truck, identify next closest address, travel distance, and travel time
                    elif (len(allTrucks[t].Packages) > 0) and (len(priorityPackageCount) == 0):
                        travelDistance = float(DataHandler.minDistance(allTrucks[t].Location, allTrucks[t].Packages)[1])
                        travelTime = datetime.timedelta(minutes=(travelDistance / allTrucks[t].Speed * 60))
                        allTrucks[t].ArrivalTime = clock + travelTime
                        allTrucks[t].Location = DataHandler.minDistance(allTrucks[t].Location, allTrucks[t].Packages)[0]
                        totalMileage += travelDistance
                    #Return to HUB if no packages remain on the truck, and another loaded truck is at the hub
                    elif len([k for k, v in allTrucks.items() if (v.Packages.__len__() > 0) and (v.IsDriving == False)]):
                        if len([k for k, v in allTrucks.items() if v.Location == 'HUB']) < 2:
                            #Set destination, travel time, and travel distance to HUB
                            if allTrucks[t].Location != 'HUB':
                                travelDistance = float(DataHandler.getDistance(allTrucks[t].Location, 'HUB'))
                                travelTime = datetime.timedelta(minutes=(travelDistance / allTrucks[t].Speed * 60))
                                allTrucks[t].ArrivalTime = clock + travelTime
                                allTrucks[t].Location = 'HUB'
                    else:
                        pass
                #Arrive at HUB at arrival time and release the remaining loaded truck
                elif allTrucks[t].Location == 'HUB':
                            if allTrucks[t].ArrivalTime <= clock:
                                allTrucks[t].stopTruck()
                                for t in allTrucks:
                                    if (allTrucks[t].IsDriving == False) and (len(allTrucks[t].Packages) > 0):
                                        allTrucks[t].startTruck()
                else:
                    pass
        #Add 1 second to clock
        clock += oneSecond

#Prompts user for hour and minute, and runs the algorithm to output a package status report for the user's requested time.
def userInput():
    print("\nPlease select a report to generate.")
    print("1: All package statuses at a given time.")
    print("2: Status of a specific package at a given time.")
    print("3: Total mileage of all trucks at a given time.")
    print("4: Exit program.")
    menuSelect = int(input(""))
    if menuSelect == 1:
        hourInput = int(input("Please enter an hour between 8 and 17: "))
        minInput = int(input("Please enter a minute between 00 and 59: "))
        if (hourInput >= 8) and (hourInput <= 17):
            if (minInput >= 0) and (minInput <= 59):
                truckRoutes(hourInput, minInput, 1)
                userInput()
            else:
                print("Invalid entry for 'minute'")
                userInput()
        else:
            print("Invalid entry for 'hour'")
            userInput()

    elif menuSelect == 2:
        packageID = input("Please enter a package ID: ")
        hourInput = int(input("Please enter an hour between 8 and 17: "))
        minInput = int(input("Please enter a minute between 00 and 59: "))
        if (hourInput >= 8) and (hourInput <= 17):
            if (minInput >= 0) and (minInput <= 59):
                truckRoutes(hourInput, minInput, 2, packageID)
                userInput()
            else:
                print("Invalid entry for 'minute'")
                userInput()
        else:
            print("Invalid entry for 'hour'")
            userInput()

    elif menuSelect == 3:
        hourInput = int(input("Please enter an hour between 8 and 17: "))
        minInput = int(input("Please enter a minute between 00 and 59: "))
        if (hourInput >= 8) and (hourInput <= 17):
            if (minInput >= 0) and (minInput <= 59):
                truckRoutes(hourInput, minInput, 3)
                userInput()
            else:
                print("Invalid entry for 'minute'")
                userInput()
        else:
            print("Invalid entry for 'hour'")
            userInput()

    elif menuSelect == 4:
        exit()

    else:
        print("Please make a valid selection for report generation.")
        userInput()

#Requests user input
userInput()