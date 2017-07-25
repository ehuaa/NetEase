# -*- coding: GBK -*-

class ActorAttributes(object):
    def __init__(self):
        super(ActorAttributes, self).__init__()
        self.accoutFilePath = './database/actor-attr.txt'
        self.actorAtrr = {}

        self._loadFileData(self.accoutFilePath)

        return

    def _loadFileData(self, path):

        f = open(path, 'r')

        try:
            data = {}
            for line in f:
                if line == '\n':
                    continue

                key,value=self._getKeyValue(line[0:-1])

                if key == 'UserID':
                    if len(data) != 0:
                        self.actorAtrr[data['UserID']] = data
                        data = {}
                        data[key] = value
                    else:
                        data[key] = value
                else:
                    data[key] = value
            if len(data) != 0:
                self.actorAtrr[data['UserID']] = data

            f.close()

        except:
            f.close()
            raise


    def _getKeyValue(self, str):
        try:
            pos = str.index(':')
            return str[0:pos] , str[pos:]
        except:
            raise