from SimpleDataQualityAnalyzer.DomainObjects.Column import Column

from datetime import datetime
import json
import os
from typing import List


class Report:
    _reportName:str = None
    _sourceFilePath:str = None
    _creationDate:datetime = None
    _records:int = None
    _columns:List[Column] = None
    __fileExtension:str = ".json"


    @property
    def reportName(self) -> str:
        return self._reportName


    @property
    def sourceFilePath(self) -> str:
        return self._sourceFilePath


    @property
    def creationDate(self) -> datetime:
        return self._creationDate


    @property
    def records(self) -> int:
        return self._records


    @records.setter
    def records(self, value:int):
        self._records = value


    @property
    def columns(self) -> List[Column]:
        return self._columns


    @columns.setter
    def columns(self, value:List[Column]):
        self._columns = value


    def __init__(self, reportName, sourceFilePath):
        self._reportName = reportName
        self._sourceFilePath = sourceFilePath
        self._records = 0
        self._creationDate = datetime.now()
        self._columns = []

        if not os.path.isfile(sourceFilePath):
            raise FileNotFoundError


    def toDict(self) -> dict:
        report = {}
        values = {}
        values["name"] = self.reportName
        values["file"] = self.sourceFilePath
        values["date"] = self.creationDate.isoformat()
        values["rows"] = self.records
        columns = []
        for col in self.columns:
            columns.append(col.toDict())
        values["columns"] = columns
        report["report"] = values
        return report


    def toJson(self) -> str:
        values = self.toDict()
        return json.dumps(values, indent=4, sort_keys=True)
        