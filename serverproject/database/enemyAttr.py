# -*- coding: GBK -*-

class EnemyAttributes(object):
    def __init__(self):
        super(EnemyAttributes, self).__init__()
        self.enemyFilePath = './database/enemy-attr.txt'
        self.enemyAtrr = {}

        self._loadFileData(self.enemyFilePath)

        return

    def _loadFileData(self, path):

        f = open(path, 'r')

        try:
            data = {}
            for line in f:
                if line == '\n':
                    continue

                key,value = self._getKeyValue(line[0:-1])

                if key == 'EnemyID':
                    if len(data) != 0:
                        self.enemyAtrr[data['EnemyID']] = data
                        data = {}
                        data[key] = value
                    else:
                        data[key] = value
                else:
                    data[key] = value
            if len(data) != 0:
                self.enemyAtrr[data['EnemyID']] = data

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