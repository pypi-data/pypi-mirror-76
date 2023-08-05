from openpyxl import load_workbook
from .ImageWriter import ImageWriter

class TemplateWriter:
    def __init__(self, template_path, output_dir):
        self.writer = ImageWriter(template_path, output_dir)

    def map_dimensions(self, workbook_path, dimensions):
        workbook = load_workbook(workbook_path)
        worksheet = workbook.active
        entries = tuple(worksheet.values)
        if len(entries[0]) != len(dimensions): 
            raise Exception("Error: Workbook and dimensions are not compatible!")
        self.datalist = []
        for entry in entries:
            if entry is None: break
            data = {}
            for index in range(len(dimensions)):
                if entry[index] is None: break
                data[str(entry[index])] = dimensions[index]
            self.datalist.append(data)


    def write_templates(self):
        for index in range(len(self.datalist)):
            self.writer.write(index, self.datalist[index])
    