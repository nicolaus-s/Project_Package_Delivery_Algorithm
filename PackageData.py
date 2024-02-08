import DataHandler
#PackageData class acts as a hash table for package data
class PackageData:
    #Create 10 buckets
    def __init__(self, size=10):
        self.size = size
        self.table=[]
        for i in range(size):
            self.table.append([])

    #Insert package object into a bucket based on package ID % 10
    def insert(self, id, package):
        bucket = int(id) % len(self.table)
        bucket_list = self.table[bucket]
        bucket_list.append([id, package])

    #Find package object in hash table
    def search(self, id):
        #Instantiate result variable
        result = None
        #Determine which bucket package object should be in
        bucket = int(id) % len(self.table)
        bucket_list = self.table[bucket]
        #For each package in bucket, check if package ID matches input ID
        for p in bucket_list:
            if p[0] == id:
                result = p[1]
        if result != None:
            return result
        #If no packages found, write message to console
        else:
            print('No package found')

    #Updates package by replacing package object with matching ID with the new package object
    #Since packages loaded into the HUB and onto Trucks are pointers to the hash table, this function is unnecessary
    def update(self, id, package):
        bucket = int(id) % len(self.table)
        bucket_list = self.table[bucket]
        for p in bucket_list:
            if p[0] == id:
                p[1] = package

    #Write package statuses to console; Message is formatted differently for each status type
    def allPackageReport(self):
        i = 0
        while i < 40:
            i = i+1
            p = DataHandler.packageHash.search(str(i))
            if p.Status == "delivered":
                print("Package ID: %s\n     Delivery Address: %s\n     Delivery Deadline: %s\n     Delivery City: %s\n     Delivery Zip Code: %s\n     Weight: %s\n     Delivery Status: %s\n     Delivery Time: %s" % (p.ID, p.Address, p.Deadline, p.City, p.Zip, p.Weight, p.Status, p.DeliveryTime))
            else:
                print("Package ID: %s\n     Delivery Address: %s\n     Delivery Deadline: %s\n     Delivery City: %s\n     Delivery Zip Code: %s\n     Weight: %s\n     Delivery Status: %s\n     Delivery Time: N/A" % (p.ID, p.Address, p.Deadline, p.City, p.Zip, p.Weight, p.Status))

    def singlePackageReport(self, id):
        p = self.search(id)
        if p.Status == "delivered":
            print("Package ID: %s\n     Delivery Address: %s\n     Delivery Deadline: %s\n     Delivery City: %s\n     Delivery Zip Code: %s\n     Weight: %s\n     Delivery Status: %s\n     Delivery Time: %s" % (p.ID, p.Address, p.Deadline, p.City, p.Zip, p.Weight, p.Status, p.DeliveryTime))
        else:
            print("Package ID: %s\n     Delivery Address: %s\n     Delivery Deadline: %s\n     Delivery City: %s\n     Delivery Zip Code: %s\n     Weight: %s\n     Delivery Status: %s\n     Delivery Time: N/A" % (p.ID, p.Address, p.Deadline, p.City, p.Zip, p.Weight, p.Status))