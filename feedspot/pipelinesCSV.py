# -*- coding: utf-8 -*-
import csv
from scrapy.exporters import CsvItemExporter
from scrapy.utils.project import get_project_settings
from .helper.customLogger import customLogger

settings = get_project_settings()
idColumn = settings.get('ID_COLUMN')
csvFileName = settings.get('CSV_FILENAME')

columns = ['urls', 'location']

class PipelineCSV(object):
    rows = []
    rowsId = []
    no_added_rows = 0
    no_updated_rows = 0
    def __init__(self):
        try:
            with open(csvFileName, 'r', encoding="utf8", errors='ignore') as file:
                reader = csv.reader(file)
                self.getAllData(reader)
                if len(self.rows) == 0:
                    self.rows.append(columns)
                    self.rowsId.append('0')
                file.close()
        except Exception as e:
            customLogger.error("Pipeline CSV " + str(e))
            print("Pipeline CSV " + str(e))

    def close_spider(self, spider):
        try:
            self.writeCSV(self.rows)
            customLogger.info(str(self.no_added_rows) + ' Information added at ' + csvFileName)
            customLogger.info(str(self.no_updated_rows) + ' Information updated at ' + csvFileName)
        except Exception as e:
            customLogger.error("Pipeline CSV Exception@@@\n\n\n" + str(e))

    def process_item(self, item, spider):
        try:
            self.updateRows(self.getRow(item))
        except Exception as e:
            customLogger.error("Pipeline CSV Exception@@@\n\n\n" + item[idColumn][0] + e)
        return item

    def getAllData(self, reader):
        for row in reader:
            self.rows.append(row)
            self.rowsId.append(row[0])

    def writeCSV(self, rows):
        with open(csvFileName, 'w', encoding="utf8", errors='ignore') as csvoutput:
            writer = csv.writer(csvoutput, lineterminator='\n')
            writer.writerows(rows)

    def getRow(self, item):
        row = []
        for column in columns:
            if column in item:
                row.append(str(item[column][0]))
            else:
                row.append('NOT AVAILABLE')
        return row

    def updateRows(self, newRow):
        try:
            index = self.rowsId.index(newRow[0])
        except ValueError:
            index = -1
        if index == -1:
            self.rows.append(newRow)
            self.rowsId.append(newRow[0])
            self.no_added_rows += 1
        elif ','.join(newRow[:-1]) != ','.join(self.rows[index][:-1]):
            self.rows[index] = newRow
            self.no_updated_rows += 1
