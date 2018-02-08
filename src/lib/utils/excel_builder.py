import io
from datetime import datetime

from django.http import HttpResponse
from xlsxwriter.workbook import Workbook


class ExcelBuilder:
    def __init__(self):
        self.output = io.BytesIO()
        self.workbook = Workbook(self.output)
        self.worksheet = self.workbook.add_worksheet()

        self.row_count = 0

    def append(self, data):
        for row in data:
            col_count = 0
            for col in row:
                self.worksheet.write(self.row_count, col_count, col)
                col_count += 1
            self.row_count += 1

    def export(self):
        self.close()
        return self.output

    def close(self):
        self.workbook.close()
        self.output.seek(0)

    def get_response(self, filename=''):
        self.close()

        if filename == '':
            filename = 'tmp'
        filename = filename + datetime.now().strftime('_%Y_%m_%d_%H_%M_%S') + '.xlsx'

        response = HttpResponse(
            self.output.read(),
            content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
        response['Content-Disposition'] = 'attachment; filename=' + filename

        return response
