class SimpleDataQualtyAnalyzerReport {
    constructor(id, data) {
        this._basicAnalysis = $("#basicAnalysisCard");
        this._columnTableDom = $("#columns_table");
        this._columnTableBodyDom = $("#columns_table tbody");
        this._tableBasicCountsDom = $("#tableBasicCounts");
        this._tableColumnFrequencyDom = $("#columnFrequencyTable");
        this._tableBodyColumnFrequencyId = "columnFrequencyTableBody";
        this._tableBodyColumnFrequencyDom = $("#" + this._tableBodyColumnFrequencyId);
        this._columnFrequencyTable = null;
        this._columnChartId = "columnChart";
        this._columnChartDom = $("#" + this._columnChartId);
        this._columnTable = null;
        this._columnTableColPrefixId = "column_pos_";
        this._columnTableRowClass = "columns_column_row";
        this._columnTableColRowActiveClass = "table-primary";
        this._reportNameValueDom = $("#report_name_value");
        this._reportFileValueDom = $("#report_file_value");
        this._reportDateValueDom = $("#report_date_value");
        this._reportRowsValueDom = $("#report_rows_value");
        this._columnMinValue = $("#columnMinValue");
        this._columnMedianValue = $("#columnMedianValue");
        this._columnMaxValue = $("#columnMaxValue");
        this._columnMinFrequency = $("#columnMinFrequency");
        this._columnMedianFrequency = $("#columnMedianFrequency");
        this._columnMaxFrequency = $("#columnMaxFrequency");
        this._columnMinLength = $("#columnMinLength");
        this._columnMedianLength = $("#columnMedianLength");
        this._columnAvgLength = $("#columnAvgLength");
        this._columnMaxLength = $("#columnMaxLength");
        this._columnNullValues = $("#columnNullValues");
        this._columnNonNullValues = $("#columnNonNullValues");
        this._columnDuplicateValues = $("#columnDuplicateValues");
        this._columnDistinctValues = $("#columnDistinctValues");
        this._columnNonUniqueValues = $("#columnNonUniqueValues");
        this._columnUniqueValues = $("#columnUniqueValues");
        this._columnNullPercent = $("#columnNullPercent");
        this._columnNonNullPercent = $("#columnNonNullPercent");
        this._columnDuplicatePercent = $("#columnDuplicatePercent");
        this._columnDistinctPercent = $("#columnDistinctPercent");
        this._columnNonUniquePercent = $("#columnNonUniquePercent");
        this._columnUniquePercent = $("#columnUniquePercent");
        this.id = id;
        this.data = data;
        this.init();
    }
    init() {
        this.bindFileOverview();
        this.bindDataSetOverview();
    }
    bindFileOverview() {
        this._reportNameValueDom.html(this.data.report.name);
        this._reportFileValueDom.html(this.data.report.file);
        this._reportDateValueDom.html(this.data.report.date);
        this._reportRowsValueDom.html(this.data.report.rows);
    }
    bindDataSetOverview() {
        let self = this;
        if (self._columnTable != null) {
            self._columnTable.destroy();
        }
        $(self.data.report.columns).each(function (pos, col) {
            let html = "<tr class='" + self._columnTableRowClass + "' id='" +
                self._columnTableColPrefixId + "" + col.position + "'>" +
                "<th scope='row'>" + col.position + "</td>" +
                "<td>" + col.name + "</td>" +
                "<td>" + col.dataType + "</td>" +
                "<td>" + col.nonNullValues + "</td>" +
                "<td>" + col.nullValues + "</td>" +
                "<td>" + col.uniqueValues + "</td>" +
                "<td>" + col.distinctValues + "</td>" +
                "<td>" + col.minValue + "</td>" +
                "<td>" + col.medianValue + "</td>" +
                "<td>" + col.maxValue + "</td></tr>";
            self._columnTableBodyDom.append(html);
        });
        self._columnTableBodyDom.on("click", "." + self._columnTableRowClass, (evt) => self.columnRowClickEventHandler(evt, self));
        $("#" + self._columnTableColPrefixId + "0").children().first().trigger("click");
        self._columnTable = self._columnTableDom.DataTable();
    }
    columnRowClickEventHandler(evt, self) {
        let row = $(evt.target).parent();
        if (!row.hasClass(self._columnTableColRowActiveClass)) {
            row.addClass(self._columnTableColRowActiveClass).siblings().removeClass(self._columnTableColRowActiveClass);
            let colPos = parseInt($(row).children().first().html());
            let colData = self.data.report.columns[colPos];
            self.bindBasicColumnValuesTable(colData);
            self.bindBasicColumnValuesChart(colData);
            self.bindFrequencyColumnValuesTable(colData);
            self.bindBasicColumnFrequencyTable(colData);
            self.bindBasicColumnLengthTable(colData);
            $("html, body").animate({ scrollTop: self._basicAnalysis.offset().top });
        }
    }
    bindBasicColumnValuesTable(colData) {
        this._columnMinValue.html(colData.minValue);
        this._columnMedianValue.html(colData.medianValue);
        this._columnMaxValue.html(colData.maxValue);
        this._columnMinFrequency.html(colData.minValueFrequency);
        this._columnMedianFrequency.html(colData.medianValueFrequency);
        this._columnMaxFrequency.html(colData.maxValueFrequency);
    }
    bindBasicColumnValuesChart(colData) {
        let self = this;
        let labels = [];
        let data = [];
        if (colData.nullValues > 0) {
            labels.push("Null");
            data.push(colData.nullValues);
        }
        if (colData.duplicateValues > 0) {
            labels.push("Duplicate");
            data.push(colData.duplicateValues);
        }
        if (colData.nonUniqueValues > 0) {
            labels.push("Non-Unique");
            data.push(colData.nonUniqueValues);
        }
        if (colData.uniqueValues > 0) {
            labels.push("Unique");
            data.push(colData.uniqueValues);
        }
        let chartOptions = {
            type: 'bar',
            data: {
                labels: labels,
                datasets: [
                    {
                        label: "Records",
                        backgroundColor: ["#3e95cd", "#8e5ea2", "#3cba9f", "#e8c3b9", "#c45850"],
                        data: data
                    }
                ]
            },
            options: {
                legend: { display: false },
                maintainAspectRatio: false,
                onResize: (chart, size) => self.changeChartSizeEventHandler(chart, self),
                title: {
                    display: true,
                    text: 'Records'
                }
            }
        };
        this._columnChartDom.replaceWith($("<canvas id='" + this._columnChartId + "'></canvas>"));
        let chart = new Chart(this._columnChartId, chartOptions);
        self.changeChartSizeEventHandler(chart, self);
    }
    changeChartSizeEventHandler(chart, self) {
        chart.canvas.parentNode.style.height = self._tableBasicCountsDom.height();
    }
    bindFrequencyColumnValuesTable(colData) {
        var accuracy = 10000;
        this._columnNullValues.html(colData.nullValues);
        this._columnNonNullValues.html(colData.nonNullValues);
        this._columnDuplicateValues.html(colData.duplicateValues);
        this._columnDistinctValues.html(colData.distinctValues);
        this._columnNonUniqueValues.html(colData.nonUniqueValues);
        this._columnUniqueValues.html(colData.uniqueValues);
        let val = this._columnNullPercent.html(SimpleDataQualtyAnalyzerReport.changeAccuracy(colData.nullValues / colData.records * 100));
        this._columnNonNullPercent.html(SimpleDataQualtyAnalyzerReport.changeAccuracy(colData.nonNullValues / colData.records * 100));
        this._columnDuplicatePercent.html(SimpleDataQualtyAnalyzerReport.changeAccuracy(colData.duplicateValues / colData.records * 100));
        this._columnDistinctPercent.html(SimpleDataQualtyAnalyzerReport.changeAccuracy(colData.distinctValues / colData.records * 100));
        this._columnNonUniquePercent.html(SimpleDataQualtyAnalyzerReport.changeAccuracy(colData.nonUniqueValues / colData.records * 100));
        this._columnUniquePercent.html(SimpleDataQualtyAnalyzerReport.changeAccuracy(colData.uniqueValues / colData.records * 100));
    }
    bindBasicColumnLengthTable(colData) {
        this._columnMinLength.html(colData.minLength);
        this._columnMedianLength.html(colData.medianLength);
        let avgLen = SimpleDataQualtyAnalyzerReport.changeAccuracy(colData.averageLength);
        this._columnAvgLength.html(avgLen.toString());
        this._columnMaxLength.html(colData.maxLength);
    }
    bindBasicColumnFrequencyTable(colData) {
        let self = this;
        if (self._columnFrequencyTable != null) {
            self._columnFrequencyTable.destroy();
            self._tableBodyColumnFrequencyDom.replaceWith($("<tbody id='columnFrequencyTableBody'></tbody>"));
            self._tableBodyColumnFrequencyDom = $("#" + self._tableBodyColumnFrequencyId);
        }
        $.each(colData.valueCounts, (index, value) => self.generateColumnFrequencyTableRow(index, value, colData.records, self));
        self._columnFrequencyTable = self._tableColumnFrequencyDom.DataTable();
    }
    generateColumnFrequencyTableRow(index, value, total, self) {
        let percent = SimpleDataQualtyAnalyzerReport.changeAccuracy(value / total * 100);
        let rowHtml = "<tr><th scope='row'>" + index + "</th><td>" + value + "</td><td>" + percent + "</td>";
        self._tableBodyColumnFrequencyDom.append(rowHtml);
    }
    static changeAccuracy(value, factor = 10000) {
        let newValue = Math.round((value + Number.EPSILON) * factor) / factor;
        return newValue;
    }
}
//# sourceMappingURL=functions.js.map