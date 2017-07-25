# -*- coding: GBK -*-

class ActorAttributes(object):
    def __init__(self):
        super(ActorAttributes, self).__init__()
        self.actorFilePath = './database/actor-attr.txt'
        self.actorAtrr = {}

        self._loadFileData(self.actorFilePath)

        return

    def _loadFileData(self, path):

        f = open(path, 'r')

        try:
            data = {}
            for line in f:
                if line == '\n':
                    continue

                key,value = self._getKeyValue(line[0:-1])

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
            key = str[0:pos]
            value = str[pos+1:]

            if value[0] == '{':
                value = self._parseSubAttr(value)

            return key, value
        except:
            raise

    def _parseSubAttr(self, str):
        str = str.strip('{}')
        retVal = {}
        data = {}
        try:
            index = str.find(',')
            while index != -1:
                key,value = self._getKeyValue(str[0:index])
                str = str[index+1:]
                index = str.find(',')

                if key == 'trapID':
                    if len(data) != 0:
                        retVal[data['trapID']] = data
                        data = {}
                        data[key] = value
                    else:
                        data[key] = value
                else:
                    data[key] = value

            key,value = self._getKeyValue(str)
            data[key] = value

            retVal[data['trapID']] = data

            return retVal
        except:
            raise