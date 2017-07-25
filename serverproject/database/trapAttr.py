# -*- coding: GBK -*-

class TrapAttributes(object):
    def __init__(self):
        super(TrapAttributes, self).__init__()
        self.trapFilePath = './database/trap-attr.txt'
        self.trapAtrr = {}

        self._loadFileData(self.trapFilePath)

        return

    def _loadFileData(self, path):

        f = open(path, 'r')

        try:
            data = {}
            for line in f:
                if line == '\n':
                    continue

                key,value = self._getKeyValue(line[0:-1])

                if key == 'TrapID':
                    if len(data) != 0:
                        self.trapAtrr[data['TrapID']] = data
                        data = {}
                        data[key] = value
                    else:
                        data[key] = value
                else:
                    data[key] = value
            if len(data) != 0:
                self.trapAtrr[data['TrapID']] = data

            f.close()

        except:
            f.close()
            raise

    def _getKeyValue(self, str):
        try:
            pos = str.index(':')
            key = str[0:pos]
            value = str[pos+1:]

            return key, value
        except:
            raise