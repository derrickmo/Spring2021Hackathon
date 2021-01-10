import http.client
import json
import Property
import math
from collections import defaultdict


class List:
    meta = []
    listProperty = []
    minScore = 8
    maxScore = 10
    priceScoreMin = 10000
    priceScoreMax = 0
    distanceScoreMin = 10000
    distanceScoreMax = 0
    usabilityScoreMin = 10000
    usabilityScoreMax = 0
    overallScoreList = []
    overallScoreSort = []

    def __init__(self, input, lat, lon, weight):
        metaTemp = Meta(input['meta'])
        self.meta.append(metaTemp)

        # This loop adds property object to the listProperty array
        for i in range(len(input['properties'])):
            proTemp = Property(input['properties'][i], lat, lon)
            self.listProperty.append(proTemp)

        # This loop collects individual scores
        for i in range(len(self.listProperty)):
            self.priceScoreMin = self.listProperty[i].priceScore if self.listProperty[
                                                                        i].priceScore < self.priceScoreMin else self.priceScoreMin
            self.priceScoreMax = self.listProperty[i].priceScore if self.listProperty[
                                                                        i].priceScore > self.priceScoreMax else self.priceScoreMax
            self.distanceScoreMin = self.listProperty[i].distanceScore if self.listProperty[
                                                                              i].distanceScore < self.distanceScoreMin else self.distanceScoreMin
            self.distanceScoreMax = self.listProperty[i].distanceScore if self.listProperty[
                                                                              i].distanceScore > self.distanceScoreMax else self.distanceScoreMax
            self.usabilityScoreMin = self.listProperty[i].usabilityScore if self.listProperty[
                                                                                i].usabilityScore < self.usabilityScoreMin else self.usabilityScoreMin
            self.usabilityScoreMax = self.listProperty[i].usabilityScore if self.listProperty[
                                                                                i].usabilityScore > self.usabilityScoreMax else self.usabilityScoreMax

        # This loop updates the the raw score to actual score using interpolation
        for i in range(len(self.listProperty)):
            self.listProperty[i].priceScore = self.minScore + abs(-(
                        (self.listProperty[i].priceScore - self.priceScoreMin) / (
                            self.priceScoreMax - self.priceScoreMin) * self.maxScore - self.maxScore)) * (
                                                          (self.maxScore - self.minScore) / self.maxScore)
            self.listProperty[i].distanceScore = self.minScore + abs(-(
                        (self.listProperty[i].distanceScore - self.distanceScoreMin) / (
                            self.distanceScoreMax - self.distanceScoreMin) * self.maxScore - self.maxScore)) * (
                                                             (self.maxScore - self.minScore) / self.maxScore)
            self.listProperty[i].usabilityScore = self.minScore + abs(
                (self.listProperty[i].usabilityScore - self.usabilityScoreMin) / (
                            self.usabilityScoreMax - self.usabilityScoreMin) * self.maxScore) * (
                                                              (self.maxScore - self.minScore) / self.maxScore)
            self.listProperty[i].overallScore = self.minScore + abs(
                self.listProperty[i].priceScore * weight[0] + self.listProperty[i].distanceScore * weight[1] +
                self.listProperty[i].usabilityScore * weight[2]) * ((self.maxScore - self.minScore) / self.maxScore)
            self.overallScoreList.append(self.listProperty[i].overallScore)

        # This equation is equivalent to Argsort using numpy package
        self.overallScoreSort = sorted(range(len(self.overallScoreList)), key=self.overallScoreList.__getitem__)
        self.overallScoreSort = self.overallScoreSort[::-1]

    def printScore(self):
        print("No.| Property ID | Price Score | Distance Score | Usability Score | Overall Score")
        for i in range(len(self.listProperty)):
            print(str(i + 1) + "   " + self.listProperty[self.overallScoreSort[i]].propertyId + "   " + str(
                round(self.listProperty[self.overallScoreSort[i]].priceScore, 1)) + "            " + str(
                round(self.listProperty[self.overallScoreSort[i]].distanceScore, 1)) + "               " + str(
                round(self.listProperty[self.overallScoreSort[i]].usabilityScore, 1)) + "                " + str(
                round(self.listProperty[self.overallScoreSort[i]].overallScore, 1)))

    # Get house information to be displayed {id: [location, score1:price, score2:dis, score3:use， score4:overall]}
    def getInfo(self):
        answer = defaultdict(list)
        for i in range(len(self.listProperty)):
            id = self.listProperty[self.overallScoreSort[i]].propertyId
            location = []
            if (isinstance(self.listProperty[self.overallScoreSort[i]].addressLat, float) and isinstance(self.listProperty[self.overallScoreSort[i]].addressLon,
                                                                                  float)):
                location.append(self.listProperty[self.overallScoreSort[i]].addressLat)
                location.append(self.listProperty[self.overallScoreSort[i]].addressLon)
            answer[id].append(location)
            price_score = round(self.listProperty[self.overallScoreSort[i]].priceScore, 1)
            answer[id].append(price_score)

            dis_score = round(self.listProperty[self.overallScoreSort[i]].distanceScore, 1)
            answer[id].append(dis_score)

            use_score = round(self.listProperty[self.overallScoreSort[i]].usabilityScore, 1)
            answer[id].append(use_score)

            overall = round(self.listProperty[self.overallScoreSort[i]].overallScore, 1)
            answer[id].append(overall)

        return answer

    # def toString(self):
    #     print("priceScoreMin:" + str(self.priceScoreMin))
    #     print("priceScoreMax:" + str(self.priceScoreMax))
    #     print("distanceScoreMin:" + str(self.distanceScoreMin))
    #     print("distanceScoreMax:" + str(self.distanceScoreMax))
    #     print("usabilityScoreMin:" + str(self.usabilityScoreMin))
    #     print("usabilityScoreMax:" + str(self.usabilityScoreMax))


class Meta:
    def __init__(self, input):
        self.channel = input['tracking_params']['channel'] if (
                    'tracking_params' in input and 'channel' in input['tracking_params']) else "unknown"
        self.siteSection = input['tracking_params']['siteSection'] if (
                    'tracking_params' in input and 'siteSection' in input['tracking_params']) else "unknown"
        self.city = input['tracking_params']['city'] if (
                    'tracking_params' in input and 'city' in input['tracking_params']) else "unknown"
        self.county = input['tracking_params']['county'] if (
                    'tracking_params' in input and 'county' in input['tracking_params']) else "unknown"
        self.neighborhood = input['tracking_params']['neighborhood'] if (
                    'tracking_params' in input and 'neighborhood' in input['tracking_params']) else "unknown"
        self.searchCityState = input['tracking_params']['searchCityState'] if (
                    'tracking_params' in input and 'searchCityState' in input['tracking_params']) else "unknown"
        self.state = input['tracking_params']['state'] if (
                    'tracking_params' in input and 'state' in input['tracking_params']) else "unknown"
        self.zip = input['tracking_params']['zip'] if (
                    'tracking_params' in input and 'zip' in input['tracking_params']) else "unknown"
        self.srpPropertyStatus = input['tracking_params']['srpPropertyStatus'] if (
                    'tracking_params' in input and 'srpPropertyStatus' in input['tracking_params']) else "unknown"
        self.listingActivity = input['tracking_params']['listingActivity'] if (
                    'tracking_params' in input and 'listingActivity' in input['tracking_params']) else "unknown"
        self.propertyStatus = input['tracking_params']['propertyStatus'] if (
                    'tracking_params' in input and 'propertyStatus' in input['tracking_params']) else "unknown"
        self.propertyType = input['tracking_params']['propertyType'] if (
                    'tracking_params' in input and 'propertyType' in input['tracking_params']) else "unknown"
        self.searchBedrooms = input['tracking_params']['searchBedrooms'] if (
                    'tracking_params' in input and 'searchBedrooms' in input['tracking_params']) else "unknown"
        self.searchMaxPrice = input['tracking_params']['searchMaxPrice'] if (
                    'tracking_params' in input and 'searchMaxPrice' in input['tracking_params']) else "unknown"
        self.searchMinPrice = input['tracking_params']['searchMinPrice'] if (
                    'tracking_params' in input and 'searchMinPrice' in input['tracking_params']) else "unknown"
        self.searchRadius = input['tracking_params']['searchRadius'] if (
                    'tracking_params' in input and 'searchRadius' in input['tracking_params']) else "unknown"
        self.searchHouseSqft = input['tracking_params']['searchHouseSqft'] if (
                    'tracking_params' in input and 'searchHouseSqft' in input['tracking_params']) else "unknown"
        self.searchLotSqft = input['tracking_params']['searchLotSqft'] if (
                    'tracking_params' in input and 'searchLotSqft' in input['tracking_params']) else "unknown"
        self.searchResults = input['tracking_params']['searchResults'] if (
                    'tracking_params' in input and 'searchResults' in input['tracking_params']) else "unknown"
        self.sortResults = input['tracking_params']['sortResults'] if (
                    'tracking_params' in input and 'sortResults' in input['tracking_params']) else "unknown"
        self.searchCoordinates = input['tracking_params']['searchCoordinates'] if (
                    'tracking_params' in input and 'searchCoordinates' in input['tracking_params']) else "unknown"
        self.searchBathrooms = input['tracking_params']['searchBathrooms'] if (
                    'tracking_params' in input and 'searchBathrooms' in input['tracking_params']) else "unknown"

    # def toString(self):
    #     print()
    #     print('Search Criteria')
    #     if (str(self.channel) != "unknown"): print("    Channel : " + str(self.channel))
    #     if (str(self.siteSection) != "unknown"): print("    siteSection : " + str(self.siteSection))
    #     if (str(self.city) != "unknown"): print("    city : " + str(self.city))
    #     if (str(self.county) != "unknown"): print("    county : " + str(self.county))
    #     if (str(self.neighborhood) != "unknown"): print("    neighborhood : " + str(self.neighborhood))
    #     if (str(self.searchCityState) != "unknown"): print("    searchCityState : " + str(self.searchCityState))
    #     if (str(self.state) != "unknown"): print("    state : " + str(self.state))
    #     if (str(self.zip) != "unknown"): print("    zip : " + str(self.zip))
    #     if (str(self.srpPropertyStatus) != "unknown"): print("    srpPropertyStatus : " + str(self.srpPropertyStatus))
    #     if (str(self.listingActivity) != "unknown"): print("    listingActivity : " + str(self.listingActivity))
    #     if (str(self.propertyStatus) != "unknown"): print("    propertyStatus : " + str(self.propertyStatus))
    #     if (str(self.propertyType) != "unknown"): print("    propertyType : " + str(self.propertyType))
    #     if (str(self.searchBedrooms) != "unknown"): print("    searchBedrooms : " + str(self.searchBedrooms))
    #     if (str(self.searchMaxPrice) != "unknown"): print("    searchMaxPrice : " + str(self.searchMaxPrice))
    #     if (str(self.searchMinPrice) != "unknown"): print("    searchMinPrice : " + str(self.searchMinPrice))
    #     if (str(self.searchRadius) != "unknown"): print("    searchRadius : " + str(self.searchRadius))
    #     if (str(self.searchHouseSqft) != "unknown"): print("    searchHouseSqft : " + str(self.searchHouseSqft))
    #     if (str(self.searchLotSqft) != "unknown"): print("    searchLotSqft : " + str(self.searchLotSqft))
    #     if (str(self.searchResults) != "unknown"): print("    searchResults : " + str(self.searchResults))
    #     if (str(self.sortResults) != "unknown"): print("    sortResults : " + str(self.sortResults))
    #     if (str(self.searchCoordinates) != "unknown"): print("    searchCoordinates : " + str(self.searchCoordinates))
    #     if (str(self.searchBathrooms) != "unknown"): print("    searchBathrooms : " + str(self.searchBathrooms))


class Property:
    def __init__(self, input, lat, lon):
        self.targetLat = lat
        self.targetLon = lon
        self.propertyId = input['property_id'] if 'property_id' in input else "N/A"
        self.listingId = input['listing_id'] if 'listing_id' in input else "N/A"
        self.webUrl = input['rdc_web_url'] if 'rdc_web_url' in input else "N/A"
        self.propertyType = input['prop_type'] if 'prop_type' in input else "N/A"
        self.propertySubType = input['prop_sub_type'] if 'prop_sub_type' in input else "N/A"
        self.tour = input['virtual_tour']['href'] if (
                    'virtual_tour' in input and 'href' in input['virtual_tour']) else "N/A"
        self.addressCity = input['address']['city'] if 'city' in input['address'] else "N/A"
        self.addressLine = input['address']['line'] if 'line' in input['address'] else "N/A"
        self.addressPostal = input['address']['postal_code'] if 'postal_code' in input['address'] else "N/A"
        self.addressState = input['address']['state'] if 'state' in input['address'] else "N/A"
        self.addressCounty = input['address']['county'] if 'county' in input['address'] else "N/A"
        self.addressFips = input['address']['fips_code'] if 'fips_code' in input['address'] else "N/A"
        self.addressLat = input['address']['lat'] if 'lat' in input['address'] else "N/A"
        self.addressLon = input['address']['lon'] if 'lon' in input['address'] else "N/A"
        self.addressNeighborhood = input['address']['neighborhood_name'] if 'neighborhood_name' in input[
            'address'] else "N/A"
        self.propertyStatus = input['prop_status'] if 'prop_status' in input else "N/A"
        self.price = input['price'] if 'price' in input else "N/A"
        self.bathsFull = input['baths_full'] if 'baths_full' in input else "N/A"
        self.baths = input['baths'] if 'baths' in input else "N/A"
        self.beds = input['beds'] if 'beds' in input else "N/A"
        self.buildingSize = input['building_size']['size'] if (
                    'building_size' in input and 'size' in input['building_size']) else "N/A"
        self.buildingSizeUnit = input['building_size']['units'] if (
                    'building_size' in input and 'units' in input['building_size']) else "N/A"
        self.lotSize = input['lot_size']['size'] if ('lot_size' in input and 'size' in input['lot_size']) else "N/A"
        self.lotSizeUnit = input['lot_size']['units'] if (
                    'lot_size' in input and 'units' in input['lot_size']) else "N/A"
        self.lastUpdate = input['last_update'] if 'last_update' in input else "N/A"
        self.photoCount = input['photo_count'] if 'photo_count' in input else "N/A"

        self.priceScore = self.calculatePriceScore()
        self.distanceScore = self.calculateDistanceScore()
        self.usabilityScore = self.calculateUsabilityScore()

    overallScore = 5

    # Price Score is calcualted based on price per building size and lot size with equal weight.
    # If any information is missing, scale the variable to full weight and discount for 20% otherwise 0.
    def calculatePriceScore(self):
        if (isinstance(self.price, int) and isinstance(self.buildingSize, int) and isinstance(self.lotSize, int)):
            return 0.5 * (self.price / self.buildingSize) + 0.5 * (self.price / self.lotSize)
        if (isinstance(self.price, int) and isinstance(self.buildingSize, int)):
            return 0.8 * (self.price / self.buildingSize)
        if (isinstance(self.price, int) and isinstance(self.lotSize, int)):
            return 0.8 * (self.price / self.lotSize)
        return 0

    # Distance score is calculated based on the property's location to the target location using latitude and longitude
    def calculateDistanceScore(self):
        if (isinstance(self.addressLat, float) and isinstance(self.addressLon, float)):
            return math.sqrt(
                math.pow(self.addressLat - self.targetLat, 2) + math.pow(self.addressLon - self.targetLon, 2))
        return 0

    # Usability score is calculated based on the number of bedrooms, full bathrooms and bathrooms
    def calculateUsabilityScore(self):
        score = 0
        score = score + 3 * self.beds if isinstance(self.beds, int) else score
        score = score + 2 * self.bathsFull if isinstance(self.bathsFull, int) else score
        score = score + 1 * self.baths if isinstance(self.baths, int) else score
        return score

    # Overall score is calculated based on the desired weight. This score has to be calculated after the loader is completed.
    def calculateOverallScore(self, weight):
        return self.priceScore * weight[0] + self.distanceScore * weight[1] + self.usabilityScore * weight[2]

    # def toString(self):
    #     print()
    #     print("Property ID: " +  str(self.propertyId))
    #     print("Listing ID: " +  str(self.listingId))
    #     print("Web URL: " +  str(self.webUrl))                              #
    #     print("Property Type: " +  str(self.propertyType))                  #
    #     print("Property Sub-type: " +  str(self.propertySubType))           #
    #     print("Tour URL: " +  str(self.tour))
    #     print("Address Line: " +  str(self.addressLine))                    #
    #     print("City: " +  str(self.addressCity))                            #
    #     print("Postal Code: " +  str(self.addressPostal))                   #
    #     print("State: " +  str(self.addressState))                          #
    #     print("County: " +  str(self.addressCounty))
    #     print("Fips: " +  str(self.addressFips))
    #     print("Latitude: " +  str(self.addressLat))                         #
    #     print("Longitude: " +  str(self.addressLon))                        #
    #     print("Neighborhood: " +  str(self.addressNeighborhood))
    #     print("Status: " +  str(self.propertyStatus))
    #     print("Price: " +  str(self.price))
    #     print("No. of Full Baths: " +  str(self.bathsFull))
    #     print("No. of Baths: " +  str(self.baths))
    #     print("No. of Beds: " +  str(self.beds))
    #     print("Building Size: " +  str(self.buildingSize))
    #     print("Building Size Unit: " +  str(self.buildingSizeUnit))
    #     print("Lot Size: " +  str(self.lotSize))
    #     print("Lot Size Unit: " +  str(self.lotSizeUnit))
    #     print("Last Update: " +  str(self.lastUpdate))
    #     print("No. of Photos: " +  str(self.photoCount))
    #     print("Building price per sqft: " + str(self.pricePerSqftBuilding))
    #     print("Price Score: " + str(self.PriceScore))
    #     print("Distance Score: " + str(self.distance))
    #     print("usability Score: " + str(self.usabilityScore))


def APIGenerator(city, state, ageMin=0, sqftMax=10000, bedsMin=0, priceMin=0, postalCode="", radius=100, priceMax=10000000, sqftMin=0, ageMax=100):
# def APIGenerator(city, state, ageMin="", sqftMax="", bedsMin="", priceMin="", postalCode="", radius="", priceMax="", sqftMin="", ageMax=""):
    # required: city, state, lat, lon, [weight 1-4]
    # optional: ageMin, sqftMax, bedsMin, priceMin, postalCode, radius, priceMax, sqftMin, ageMax
    ageMinString = "&age_min=" + str(ageMin) if isinstance(ageMin, int) else ""
    sqftMaxString = "&sqft_max=" + str(sqftMax) if isinstance(sqftMax, int) else ""
    bedsMinString = "&beds_min=" + str(bedsMin) if isinstance(bedsMin, int) else ""
    priceMinString = "&price_min=" + str(priceMin) if isinstance(priceMin, int) else ""
    postalCodeString = "&postal_code=" + str(postalCode) if isinstance(postalCode, int) else ""
    radiusString = "&radius=" + str(radius) if isinstance(radius, int) else ""
    priceMaxString = "&price_max=" + str(priceMax) if isinstance(priceMax, int) else ""
    sqftMinString = "&sqft_min=" + str(sqftMin) if isinstance(sqftMin, int) else ""
    ageMax = "&age_max=" + str(ageMax) if isinstance(ageMax, int) else ""

    requestString = "/properties/v2/list-for-sale?city=" + city + "&limit=5&offset=0&state_code=" + state + "&sort=relevance" + ageMinString + sqftMaxString + bedsMinString + priceMinString + postalCodeString + radiusString + priceMaxString + sqftMinString + ageMax
    print(requestString)

    conn = http.client.HTTPSConnection("realtor.p.rapidapi.com")
    headers = {
        'x-rapidapi-key': "5f13e17c76mshddb8f2e6b5ee988p1aec3bjsna33075e87baf",
        'x-rapidapi-host': "realtor.p.rapidapi.com"
    }
    conn.request("GET", requestString, headers=headers)
    return conn.getresponse()


def runner(city, state, lat, lng, w1, w2, w3):
    # # This block is to request a list of properties from API
    # # Method signature: APIGenerator(self, city, state, ageMin, sqftMax, bedsMin, priceMin, postalCode, radius, priceMax, sqftMin, ageMax):
    houses_from_api = APIGenerator(city, state, "", "", "", "", "", "", "", "")
    data = houses_from_api.read()
    rawData = json.loads(data)

    # priceFocused = [0.5,0.25,0.25]
    # distanceFocused = [0.25,0.5,0.25]
    # usabilityFocused = [0.25,0.25,0.50]
    # equalFocused = [0.33,0.33,0.33]
    w1 = float(w1)
    w2 = float(w2)
    w3 = float(w3)
    total = w1 + w2 + w3
    weight = [w2 / total, w2 / total, w3 / total]

    # Back-up option - This block reads from the source document
    # with open('source.txt') as input: # Pulling Json format txts from txt file for testing purposes
    #     rawData = json.load(input)       # Remember to comment this line too

    # print('*** Starting Point ***')

    H = List(rawData, lat, lng, weight)

    # Di wrote the function getInfo to obtain information could be used on front-end
    answer = H.getInfo()
    print(answer)
    H.printScore()
    return answer

    # return Data


if __name__ == "__main__":
    runner("Philadelphia", "PA", 35.95, 75.16, 0.33, 0.33, 0.33)

    # *** Request from API snippets ***
    # conn = http.client.HTTPSConnection("realtor.p.rapidapi.com")
    # headers = {
    #     'x-rapidapi-key': "5f13e17c76mshddb8f2e6b5ee988p1aec3bjsna33075e87baf",
    #     'x-rapidapi-host': "realtor.p.rapidapi.com"
    #     }
    # conn.request("GET", "/properties/v2/list-for-sale?city=Philadelphia&limit=10&offset=0&state_code=PA&sort=relevance", headers=headers)
    # res = conn.getresponse()
    # input = res.read()
    # print(input.decode("utf-8"))    # print the input data from the API
    # data = json.loads(input)       # Pulling Json format from the API
    # ********************