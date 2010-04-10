# Module for handeling CSV files. It's a nicer interface to the
# builtin scv module. Methods natilvly supports unicode.
import csv, codecs

# Reads a csv file and returns a 2d iterator.
def read(file, delimiter=',', quotechar='"'):
    reader = _unicode_csv_reader(codecs.open(file, 'r', 'utf-8'), delimiter=delimiter, quotechar=quotechar)
    return tuple([tuple(row) for row in reader])

# Writes a 2d iterator to a csv file.
def write(file, data, delimiter=',', quotechar='"'):
    file = codecs.open(file, 'w', 'utf-8')

    for row in data:
        file.write(delimiter.join(['%s%s%s' % (quotechar, _escape(col, quotechar), quotechar) for col in row]))
        file.write('\r\n')
    file.flush()
    file.close()

def _unicode_csv_reader(unicode_csv_data, dialect=csv.excel, delimiter=',', quotechar='"', **kwargs):
    # csv.py doesn't do Unicode; encode temporarily as UTF-8:
    csv_reader = csv.reader(_utf_8_encoder(unicode_csv_data),
                            dialect=dialect, delimiter=delimiter, 
                            quotechar=quotechar, **kwargs)
    for row in csv_reader:
        # decode UTF-8 back to Unicode, cell by cell:
        yield [unicode(cell, 'utf-8') for cell in row]

def _utf_8_encoder(unicode_csv_data):
    for line in unicode_csv_data:
        yield line.encode('utf-8')

def _escape(obj, char):
    return obj.replace(char, char*2) if isinstance(obj, basestring) else obj

