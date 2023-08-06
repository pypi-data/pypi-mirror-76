from typing import List
from pyarrow.csv import ParseOptions, ConvertOptions


class AnalyzeOptions:
    _delimiter:str = ","
    _ignoreEmptyLines:bool = True
    _emptyStringIsNull:bool = True
    _placeholderNull:List[str] = ["", " "]
    _placeholderTrue:List[str] = ["Y", "y"]
    _placeholderFalse:List[str] = ["N", "n"]


    @property
    def delimiter(self) -> str:
        """Gets the str that separates the columns within a source file"""
        return self._delimiter


    @delimiter.setter
    def delimiter(self, value:str):
        """Sets the str that separates the columns within a source file."""
        self._delimiter = value


    @property
    def ignoreEmptyLines(self) -> bool:
        """Gets whether or not empty lines within a source file shall be ignored."""
        return self._ignoreEmptyLines


    @ignoreEmptyLines.setter
    def ignoreEmptyLines(self, value:bool):
        """Sets whether or not empty lines within a source file shall be ignored."""
        self._ignoreEmptyLines = value


    @property
    def emptyStringIsNull(self) -> bool:
        """Gets whether or not empty strings shall be interpreted as null."""
        return self._emptyStringIsNull


    @emptyStringIsNull.setter
    def emptyStringIsNull(self, value:bool):
        """Sets whether or not empty strings shall be interpreted as null."""
        self._emptyStringIsNull = value


    @property
    def placeholderNull(self) -> List[str]:
        """Gets a list with all the str that represent a null value within a source file."""
        return self._placeholderNull


    @placeholderNull.setter
    def placeholderNull(self, value:List[str]):
        """Sets a list with all the str that represent a null value within a source file."""
        self._placeholderNull = value


    @property
    def placeholderTrue(self) -> List[str]:
        """Gets a list with all the str that represent a true value within a source file."""
        return self._placeholderTrue


    @placeholderTrue.setter
    def placeholderTrue(self, value:List[str]):
        """Sets a list with all the str that represent a true value within a source file."""
        self._placeholderTrue = value


    @property
    def placeholderFalse(self) -> List[str]:
        """Gets a list with all the str that represent a false value within a source file."""
        return self._placeholderFalse


    @placeholderFalse.setter
    def placeholderFalse(self, value:List[str]):
        """Sets a list with all the str that represent a false value within a source file."""
        self._placeholderFalse = value


    @property
    def parseOptions(self) -> ParseOptions:
        options = ParseOptions()
        options.delimiter = self.delimiter
        options.ignore_empty_lines = self.ignoreEmptyLines
        return options


    @property
    def convertOptions(self) -> ConvertOptions:
        options = ConvertOptions()
        if self.emptyStringIsNull:
            options.strings_can_be_null = True
        options.false_values = self.placeholderFalse
        options.true_values = self.placeholderTrue
        options.null_values = self.placeholderNull
        return options


    #TODO: how can we move this to a base object
    def __str__(self) -> str:
        returnValue = ""
        attributes = vars(self)
        for key, value in attributes.items():
            returnValue += str(key) + ": '" + str(value) + "'\r\n"
        return returnValue
