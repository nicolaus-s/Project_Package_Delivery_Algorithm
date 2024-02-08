import csv
import os
import Package
import PackageData
import Address

#Returns distance between two addresses
def getDistance(addressA, addressB):
    key = createDistanceKey(addressA, addressB)
    return distanceData[key]


#Returns minimum distance between current Truck location and package addresses in the provided package data set.
def minDistance(currentLocation, currentPackages):
    minDist = 0
    nextStop = ""
    for package in currentPackages:
        thisAddress = currentPackages[package].AddressKey
        thisDist = getDistance(currentLocation, thisAddress)
        if minDist == 0 or thisDist < minDist:
            minDist = thisDist
            nextStop = thisAddress
    return [nextStop, minDist]


#Generates keys for two provided addresses for use in distanceData
def createAddressKey(a, b):
    subStr = a[0:5:1]
    return subStr + b


#Generates keys for 2 addresses to store their distance from each other.
def createDistanceKey(a, b):
    return str(a) + str(b)


os.chdir('data')

#Initialize address dictionary
addressData = {}

#Manually add the HUB address
addressData['HUB'] = Address.Address("HUB")

#Initialize package hash table using the PackageData class
packageHash = PackageData.PackageData()

#Extract package and address data from csv file
with open('WGUPS Package File.csv', newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        address = Address.Address(row['Address'], row['City '], row['State'], row['Zip'])
        addressKey = createAddressKey(address.ShortAddress, address.Zip)
        addressData[addressKey] = address
        package = Package.Package(row['Package\nID'], addressKey, addressData[addressKey].ShortAddress, row['Delivery\nDeadline'], addressData[addressKey].City, addressData[addressKey].Zip, row['Mass\nKILO'], row['page 1 of 1PageSpecial Notes'])
        packageHash.insert(package.ID, package)

#Initialize distance dictionary
distanceData = {}

#Extract distance data from csv file
with open('WGUPS Distance Table.csv', newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        #If statement handles the 1 instance of 'HUB'
        if str.strip(row['Short Address']) == 'HUB':
            addressData['HUB'].LongAddress = row['Long Address']
        #Else statement handles all other addresses
        else:
            #Parse address data and remove extra characters such as line breaks
            shortAddress = str.split(row['Short Address'], '\n')
            splitAddress = str.strip(shortAddress[0])
            splitZip = shortAddress[1].replace("(","")
            splitZip = splitZip.replace(")", "")
            splitZip = str.strip(splitZip)
            key = createAddressKey(splitAddress, splitZip)
            addressData[key].LongAddress = row['Long Address']
        for column in row:
            try:
                #Ignore distances of 0
                if float(row[column]) > 0.0:
                    addressKeyA = 0
                    addressKeyB = 0
                    #Extract two address values for distance data
                    for a in addressData:
                        if addressData[a].LongAddress == column:
                            addressKeyA = a
                        if addressData[a].LongAddress == row['Long Address']:
                            addressKeyB = a
                    #Create key using two addresses, store distance value
                    k = createDistanceKey(addressKeyA, addressKeyB)
                    distanceData[k] = float(row[column])
                    #Create second key using two addresses (input variables are reversed), store distance value again
                    k = createDistanceKey(addressKeyB, addressKeyA)
                    distanceData[k] = float(row[column])
            #Ignore any errors during data extraction
            except ValueError as e:
                pass
