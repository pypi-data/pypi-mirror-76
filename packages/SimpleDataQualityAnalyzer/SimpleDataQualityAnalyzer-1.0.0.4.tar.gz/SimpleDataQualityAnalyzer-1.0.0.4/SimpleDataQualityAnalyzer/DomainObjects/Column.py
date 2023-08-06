class Column:
    __position:int = None
    __name:str = None
    __dataType:str = None
    __domain:str = None
    __nonNullValues:int = None
    __nullValues:int = None
    __uniqueValues:int = None
    __nonUniqueValues:int = None
    __distinctValues:int = None
    __duplicateValues:int = None
    __records:int = None
    __minValue:str = None
    __medianValue:str = None
    __maxValue:str = None
    __minValueFrequency:int = None
    __medianValueFrequency:int = None
    __maxValueFrequency:int = None
    __minLength:int = None
    __medianLength:int = None
    __maxLength:int = None
    __averageLength:float = None
    __valueCounts:dict = None
    __lengthCounts:dict = None


    def __getPosition(self) -> int:
        return self.__position


    def __getName(self) -> str:
        return self.__name


    def __getRecords(self) -> int:
        return self.__records


    def __getDataType(self) -> str:
        return self.__dataType


    def __getDomain(self) -> str:
        return self.__domain


    def __getNonNullValues(self) -> int:
        if self.__nonNullValues is None:
            self.__nonNullValues = self.__countNumberOfNonNullValues()
        return self.__nonNullValues


    def __getNullValues(self) -> int:
        if self.__nullValues is None:
            self.__nullValues = self.__countNumberOfNullValues()
        return self.__nullValues


    def __getUniqueValues(self) -> int:
        if self.__uniqueValues is None:
            self.__uniqueValues = self.__countNumberOfUniqueValues()
        return self.__uniqueValues


    def __getNonUniqueValues(self) -> int:
        if self.__nonUniqueValues is None:
            self.__nonUniqueValues = self.__getDistinctValues() - self.__getUniqueValues()
        return self.__nonUniqueValues


    def __getDistinctValues(self) -> int:
        if self.__distinctValues is None:
            self.__distinctValues = self.__countNumberOfDistinctValues()
        return self.__distinctValues


    def __geDuplicateValues(self) -> int:
        if self.__duplicateValues is None:
            self.__duplicateValues = self.__getNonNullValues() - self.__getDistinctValues()
        return self.__duplicateValues


    def __getMinValue(self) -> str:
        if self.__minValue is None:
            self.__minValue, self.__minValueFrequency = self.__extractMinValueAndFrequency()
        return self.__minValue


    def __getMedianValue(self) -> str:
        if self.__medianValue is None:
            self.__medianValue, self.__medianValueFrequency = self.__extractMedianValueAndFrequency()
        return self.__medianValue


    def __getMaxValue(self) -> str:
        if self.__maxValue is None:
            self.__maxValue, self.__maxValueFrequency = self.__extractMaxValueAndFrequency()
        return self.__maxValue


    def __getMinLength(self) -> int:
        if self.__minLength is None:
            self.__minLength = self.__extractMinLength()
        return self.__minLength


    def __getMedianLength(self) -> int:
        if self.__medianLength is None:
            self.__medianLength = self.__extractMedianLength()
        return self.__medianLength


    def __getMaxLength(self) -> int:
        if self.__maxLength is None:
            self.__maxLength = self.__extractMaxLength()
        return self.__maxLength


    def __getAverageLength(self) -> float:
        if self.__averageLength is None:
            self.__averageLength = self.__extractAverageLength()
        return self.__averageLength


    position = property(__getPosition)
    name = property(__getName)
    records = property(__getRecords)
    dataType = property(__getDataType)
    domain = property(__getDomain)
    nonNullValues = property(__getNonNullValues)
    nullValues = property(__getNullValues)
    uniqueValues = property(__getUniqueValues)
    nonUniqueValues = property(__getNonUniqueValues)
    distinctValues = property(__getDistinctValues)
    duplicateValues = property(__geDuplicateValues)
    minValue = property(__getMinValue)
    medianValue = property(__getMedianValue)
    maxValue = property(__getMaxValue)
    minLength = property(__getMinLength)
    medianLength = property(__getMedianLength)
    maxLength = property(__getMaxLength)
    averageLength = property(__getAverageLength)


    def __init__(self, position:int, name:str, dataType:str, records: int, valueCounts:dict):
        self.__position = position
        self.__name = name
        self.__dataType = dataType
        self.__records = records
        self.__valueCounts = valueCounts
        self.__lengthCounts = self.__extractLengthCounts()


    def __str__(self):
        val = "Pos: " + str(self.position) + "\r\n"
        val += "Name: " + self.name + "\r\n"
        val += "DataType: " + self.dataType + "\r\n"
        val += "Non-Null: " + str(self.nonNullValues) + "\r\n"
        val += "Null: " + str(self.nullValues) + "\r\n"
        val += "Unique: " + str(self.uniqueValues) + "\r\n"
        val += "Distinct: " + str(self.distinctValues) + "\r\n"
        val += "Min: " + self.minValue + "\r\n"
        val += "Medain: " + self.medianValue + "\r\n"
        val += "Max: " + self.maxValue
        return val


    def __countNumberOfNonNullValues(self) -> int:
        nonNullValues = 0
        for key in self.__valueCounts:
            if key != None and key != "":
                nonNullValues += self.__valueCounts[key]
        return nonNullValues


    def __countNumberOfNullValues(self) -> int:
        nullValues = 0
        nullValues += self.__valueCounts[None]
        nullValues += self.__valueCounts[""]
        return nullValues


    def __countNumberOfUniqueValues(self) -> int:
        uniqueValues = 0
        for key in self.__valueCounts:
            if key != None and key != "" and self.__valueCounts[key] == 1:
                uniqueValues += 1
        return uniqueValues


    def __countNumberOfDistinctValues(self) -> int:
        distinctValues = 0
        for key in self.__valueCounts:
            if key != None and key != "":
                distinctValues += 1
        return distinctValues


    def __extractMinValueAndFrequency(self) -> (str, int):
        valueList = set(self.__valueCounts)
        if None in valueList:
            valueList.remove(None)
        if "" in valueList:
            valueList.remove("")

        valueList = sorted(valueList)
        return str(valueList[0]), self.__valueCounts[valueList[0]]


    def __extractMaxValueAndFrequency(self) -> (str, int):
        valueList = set(self.__valueCounts)
        if None in valueList:
            valueList.remove(None)
        if "" in valueList:
            valueList.remove("")

        valueList = sorted(valueList)
        return str(valueList[-1]), self.__valueCounts[valueList[-1]]


    def __extractMedianValueAndFrequency(self) -> (str, int):
        valueCounts = self.__valueCounts
        if None in valueCounts:
            del valueCounts[None]
        if "" in valueCounts:
            del valueCounts[""]

        valueList = set(valueCounts)
        valueList = sorted(valueList)
        pos = round(self.nonNullValues / 2)
        posCounter = 1
        for key in valueList:
            posCounter += valueCounts[key]
            if posCounter >= pos:
                return str(key), valueCounts[key]


    def __extractLengthCounts(self) -> dict:
        lengthDict = {}
        valueCounts = self.__valueCounts
        if None in valueCounts:
            del valueCounts[None]
        if "" in valueCounts:
            del valueCounts[""]
        
        valueList = set(valueCounts)
        for val in valueList:
            length = len(str(val))
            if length in lengthDict:
                lengthDict[length] += valueCounts[val]
            else:
                lengthDict[length] = valueCounts[val]
        return lengthDict


    def __extractMinLength(self) -> int:
        lenList = set(self.__lengthCounts)
        lenList = sorted(lenList)
        return str(lenList[0])


    def __extractMaxLength(self) -> int:
        lenList = set(self.__lengthCounts)
        lenList = sorted(lenList)
        return str(lenList[-1])


    def __extractMedianLength(self) -> int:
        lenCounts = self.__lengthCounts
        lenList = set(lenCounts)
        lenList = sorted(lenList)

        pos = round(self.nonNullValues / 2)
        posCounter = 1
        for key in lenList:
            posCounter += lenCounts[key]
            if posCounter >= pos:
                return str(key)


    def __extractAverageLength(self) -> float:
        lenCounts = self.__lengthCounts
        lenList = set(lenCounts)
        lenList = sorted(lenList)

        totLen = 0
        totFreq = 0
        for key in lenList:
            totLen += (key * lenCounts[key])
            totFreq += lenCounts[key]
        avg = totLen / totFreq
        return avg


    def toDict(self):
        values = {}
        values["position"] = self.position
        values["name"] = self.name
        values["dataType"] = self.dataType
        values["records"] = self.records
        values["nonNullValues"] = self.nonNullValues
        values["nullValues"] = self.nullValues
        values["uniqueValues"] = self.uniqueValues
        values["nonUniqueValues"] = self.nonUniqueValues
        values["distinctValues"] = self.distinctValues
        values["duplicateValues"] = self.duplicateValues
        values["minValue"] = self.minValue
        values["medianValue"] = self.medianValue
        values["maxValue"] = self.maxValue
        values["minValueFrequency"] = self.__minValueFrequency
        values["medianValueFrequency"] = self.__medianValueFrequency
        values["maxValueFrequency"] = self.__maxValueFrequency
        values["minLength"] = self.minLength
        values["medianLength"] = self.medianLength
        values["maxLength"] = self.maxLength
        values["averageLength"] = self.averageLength
        values["valueCounts"] = self.__valueCounts
        return values
