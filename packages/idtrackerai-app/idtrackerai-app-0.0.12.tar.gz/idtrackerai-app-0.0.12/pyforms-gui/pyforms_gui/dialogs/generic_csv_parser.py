import csv
from pyforms_gui.basewidget import BaseWidget
from pyforms_gui.allcontrols import ControlText
from pyforms_gui.allcontrols import ControlButton
from pyforms_gui.allcontrols import ControlFile
from pyforms_gui.allcontrols import ControlList
from pyforms_gui.allcontrols import ControlNumber
from pyforms_gui.allcontrols import ControlCombo


class GenericCsvParserDialog(BaseWidget):
    def __init__(self, columns, parent=None):
        super(GenericCsvParserDialog, self).__init__('CSV Choose the columns', parent_win=parent)

        self._filename = None
        self._columns = columns
        self._columns_indexes = []
        self._rownum = 0

        # Definition of the forms fields
        self._filename      = ControlFile('CSV File')
        self._separator     = ControlCombo('Separator', default='auto')
        self._startingrow   = ControlNumber('Starting row', default=0)

        for index, column in enumerate(columns):
            setattr(self, '_col_{0}'.format(index), ControlNumber(column, default=index, minimum=-1, maximum=1000))

        self._filePreview = ControlList('Preview')
        self._loadButton  = ControlButton('Load')

        form_row = ['_separator'] + ['_col_{0}'.format(index) for index, column in enumerate(columns)] + ['_loadButton']

        self._formset = [
            ('_filename', '_startingrow'),
            tuple(form_row),
            '_filePreview'
        ]
        self._separator.changed_event = self.__refreshPreview
        self._filename.changed_event = self.__refreshPreview
        self._startingrow.changed_event = self.__refreshPreview
        self._loadButton.value = self.load

        self._load_event = None

        self._separator.add_item('auto', 'auto')
        self._separator.add_item(';', ';')
        self._separator.add_item(',', ',')
        self._separator.add_item('TAB', '\t')
        self._separator.add_item('Excel', csv.excel)
        self._separator.add_item('Excel TAB', csv.excel_tab)

    @property
    def load_file_event(self):
        return self._load_event

    @load_file_event.setter
    def load_file_event(self, value):
        self._load_event = value

    def __iter__(self):

        if self._filename.value != None and self._filename.value != '':
            csvfile = open(self._filename.value, 'U')
            if self.delimiter in ['auto',  csv.excel,  csv.excel_tab]:
                try:
                    dialect = csv.Sniffer().sniff(csvfile.read(1024))
                    csvfile.seek(0)
                    self._spamreader = csv.reader(csvfile, dialect)
                except:
                    self._spamreader = None
                    return self
            else:
                self._spamreader = csv.reader(csvfile, delimiter=self.delimiter)
            for i in range(int(self._startingrow.value)): next(self._spamreader, None)  # skip the headers
        else:
            self._spamreader = None

        return self

    # For compatibility with python 3
    def __next__(self):
        return self.next()

    def next(self):
        if self._spamreader != None:
            row = next(self._spamreader)
            res = []
            for col in self._columns_indexes:
                if col == -1:
                   res.append(self._rownum)
                else:
                    if row[col].lower() == 'nan':
                        res.append('None')
                    else:
                        res.append(row[col])

            self._rownum +=1

            return res
        else:
            raise StopIteration()

    def __refreshPreview(self):
        if self._filename.value != None and self._filename.value != '':
            with open(self._filename.value, 'U') as csvfile:
                if self.delimiter in ['auto',  csv.excel,  csv.excel_tab]:
                    try:
                        dialect = csv.Sniffer().sniff(csvfile.read(1024))
                        csvfile.seek(0)
                        spamreader = csv.reader(csvfile, dialect)
                    except:
                        self.message('Error when reading the file.')
                        return
                else:
                    spamreader = csv.reader(csvfile, delimiter=self.delimiter)

                for i in range(int(self._startingrow.value)): next(spamreader, None)  # skip the headers
                self._filePreview.value = []
                self._filePreview.horizontalHeaders = map(str, range(1000))
                for i, row in enumerate(spamreader):
                    self._filePreview += row
                    if i >= 10:
                        break

    @property
    def delimiter(self):
        return self._separator.value

    def load(self):
        self.__refreshPreview()
        self._columns_indexes = []
        for index, column in enumerate(self._columns):
            self._columns_indexes.append(int(getattr(self, '_col_{0}'.format(index)).value))
        if self._load_event is not None: self._load_event()


##################################################################################################################
##################################################################################################################
##################################################################################################################

# Execute the application
if __name__ == "__main__":
    import pyforms

    pyforms.start_app(GenericCsvParserDialog, geometry=(0, 0, 600, 400))