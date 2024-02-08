import DataHandler

class Truck:
    def __init__(self, id, driving=False, capacity=16):
        self.ID = id
        self.IsDriving = driving
        self.Capacity = capacity
        self.Packages = {}
        self.Location = 'HUB'
        self.Speed = 18
        self.ArrivalTime = None

    def loadSpecialPackages (self, packages):
        specialPackages = {}
        pLoaded = []
        #Truck 1 loads no specific packages
        if self.ID == 1:
            pass
        #Truck 2 loads required packages, packages to be delivered together, and packages with a deadline
        elif self.ID == 2:
            pLoaded = ['3', '18', '36', '38', '13', '14', '15', '16', '19', '20', '1', '30', '31', '34', '37', '40']
            for p in pLoaded:
                specialPackages[p] = packages[p]
            # Specified packages are loaded in order to reduce mileage
            self.loadTruckEfficiently(specialPackages)
            for p in pLoaded:
                #Any package loaded on the truck is popped from the input package data set (HUB packages)
                packages.pop(p)
        #Truck 3 loads delayed packages, and the package with an incorrect address
        else:
            pLoaded = ['9', '6', '25', '28', '32']
            for p in pLoaded:
                specialPackages[p] = packages[p]
            #Specified packages are loaded in order to reduce mileage
            self.loadTruckEfficiently(specialPackages)
            #Any package loaded on the truck is popped from the input package data set (HUB packages)
            for p in pLoaded:
                packages.pop(p)

    #Efficiently load Truck object with Package objects
    def loadTruckEfficiently(self, packages):
        #Instantiate nextStop variable with Truck's current location (HUB by default)
        nextStop = self.Location
        #While Truck isn't full, and packages remain in the input package data set (HUB packages)
        while (len(self.Packages) < self.Capacity) and (len(packages) > 0):
            pLoaded = []
            minDist = 0
            #Determine next closest address among available packages
            for p in packages:
                fromAddress = str(nextStop)
                if packages[p].AddressKey != nextStop:
                    thisDist = DataHandler.getDistance(fromAddress, packages[p].AddressKey)
                    if minDist == 0 or thisDist < minDist:
                        minDist = thisDist
                        nextStop = packages[p].AddressKey
            #If truck has capacity, load one package for the next closest address
            if len(self.Packages) < self.Capacity:
                for p in packages:
                    if packages[p].AddressKey == nextStop:
                        self.Packages[p] = packages[p]
                        pLoaded.append(p)
                        #If Truck is driving, set package status to 'en route'
                        if self.IsDriving == True:
                            self.Packages[p].Status = "en route"
                        break
                #Any package loaded on the truck is popped from the input package data set (HUB packages)
                for p in pLoaded:
                    packages.pop(p)

    #Deliver packages
    def deliverPackages(self, t):
        deliverPackages = []
        for p in self.Packages:
            #If package address is the current Truck location, update package status to 'delivered', and update package delivery time.
            if self.Packages[p].AddressKey == self.Location:
                deliverPackages.append(p)
                self.Packages[p].Status = "delivered"
                self.Packages[p].DeliveryTime = str(t)
        for k in deliverPackages:
            #Unload package from Truck
            self.Packages.pop(k)

    #Put driver in Truck, set Truck package statuses to 'en route'
    def startTruck(self):
        self.IsDriving = True
        for p in self.Packages:
            self.Packages[p].Status = "en route"

    #Remove driver from Truck, set Truck package statuses to 'at the hub'
    def stopTruck(self):
        self.IsDriving = False
        for p in self.Packages:
            self.Packages[p].Status = "at the hub"