# -*- coding: GBK -*-
class TrapData(object):
    def __init__(self, data):
        self.trapID = int(data['TrapID'])
        self.attack = int(data['Attack'])
        self.price = int(data['Price'])
        self.speed = int(data['Speed'])

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
                        cell = TrapData(data)
                        self.trapAtrr[cell.trapID] = cell
                        data = {}
                        data[key] = value
                    else:
                        data[key] = value
                else:
                    data[key] = value
            if len(data) != 0:
                cell = TrapData(data)
                self.trapAtrr[cell.trapID] = cell

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