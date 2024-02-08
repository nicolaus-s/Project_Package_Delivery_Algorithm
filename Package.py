#Package class stores all package data
class Package:
    def __init__(self, packageID="", addressKey="", address="", deliveryDeadline="", city="", zip="", mass=0, specialNotes=""):
        self.ID = packageID
        self.AddressKey = addressKey
        self.Address = address
        self.Deadline = deliveryDeadline
        self.City = city
        self.Zip = zip
        self.Weight = mass
        self.Notes = specialNotes
        self.Status = "Not shipped."
        self.DeliveryTime = None