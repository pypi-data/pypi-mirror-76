from SimpleDataQualityAnalyzer.DomainObjects.AnalyzeOptions import AnalyzeOptions
from SimpleDataQualityAnalyzer.DomainObjects.Column import Column
from SimpleDataQualityAnalyzer.DomainObjects.Report import Report

from collections import Counter
import inspect
from os import path
from pathlib import Path
from pyarrow import csv
from pyarrow.csv import ParseOptions, ConvertOptions


class Analyzer:
    __htmlTemplate = "Templates/template.html"
    __jsFunctions = "Templates/functions.js"
    __dataPlaceholder = "/*<<json_data>>*/"
    __functionsPlaceholder = "/*<<functions>>*/"

    _sourceFile:str = None
    _dataSetName:str = None
    _delimiter:str = None
    _analyzeOptions:AnalyzeOptions = None
    _report:Report = None


    @property
    def sourceFile(self) -> str:
        """Gets the path to the source file."""
        return self._sourceFile


    @property
    def dataSetName(self) -> str:
        """Gets the name of the dataset."""
        return self._dataSetName


    @property
    def analyzeOptions(self) -> AnalyzeOptions:
        """Gets the AnalyeOptions to help interprete the source file."""
        return self._analyzeOptions


    @analyzeOptions.setter
    def analyzeOptions(self, value:AnalyzeOptions):
        """Sets the AnalyeOptions to help interprete the source file."""
        self._analyzeOptions = value

       
    def __init__(self, sourceFile:str, analyzeOptions:AnalyzeOptions = None, dataSetName:str = None):
        """Creates a new Analyzer objects.
            sourceFile -- the path to the source file
            
            analyzeOptions -- the AnalyzeOptions object that is needed to interprete the source file (default None).
                              If None the default AnalyzeOptions are used.

            dataSetName -- The name of the dataset (default None).
                            If None the dataset name will be derived from the file name (without extension).
        """
        self._sourceFile = sourceFile
        self._analyzeOptions = analyzeOptions
        self._dataSetName = dataSetName

        if self._analyzeOptions is None:
            self._analyzeOptions = AnalyzeOptions() 

        if self._dataSetName is None:
            self._dataSetName = self.__extractDataSetName()


    def __extractDataSetName(self) -> str:
        fileName = path.basename(self.sourceFile)
        extension = Path(fileName).suffix
        dataSetName = fileName.replace(extension, "")
        return dataSetName


    def __getFolder(self) -> str:
        file = inspect.getabsfile(self.__class__)
        folder = path.dirname(file)
        return str(folder)


    def __getTemplate(self) -> str:
        folder = self.__getFolder()
        template = path.join(folder, self.__htmlTemplate)
        return template


    def __getFunctions(self) -> str:
        folder = self.__getFolder()
        functions = path.join(folder, self.__jsFunctions)
        return functions


    #TODO: how can we move this to a base object
    def __str__(self) -> str:
        returnValue = ""
        attributes = vars(self)
        for key, value in attributes.items():
            returnValue += str(key) + ": '" + str(value) + "'\r\n"
        return returnValue


    def __analyzeFile(self):
        rep = Report(self.dataSetName, self.sourceFile)
        parseOptions = self.analyzeOptions.parseOptions
        convertOptions = self.analyzeOptions.convertOptions
        table = csv.read_csv(rep.sourceFilePath, parse_options=parseOptions, convert_options=convertOptions)
        rep.records = table.num_rows 
        dict = table.to_pydict()
        colPosition = 0
        for colName in dict:
            dataType = str(table.schema.types[colPosition])
            valueCounts = Counter(dict[colName])
            col = Column(colPosition, colName, dataType, rep.records, valueCounts)
            rep.columns.append(col)
            colPosition += 1
        self._report = rep


    def __visualizeFile(self, exportFile:str):
        template = self.__getTemplate()
        functions = self.__getFunctions()
        
        templateContent = None
        with open(template) as f:
            templateContent = f.read()

        functionsContent = None
        with open(functions) as f:
            functionsContent = f.read()

        report = templateContent.replace(self.__functionsPlaceholder, functionsContent)
        report = report.replace(self.__dataPlaceholder, self._report.toJson())

        with open(exportFile, "w") as f:
            f.write(report)

    
    def generateReport(self, exportFile:str):
        self.__analyzeFile()
        self.__visualizeFile(exportFile)
