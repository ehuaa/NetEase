# -*- coding: GBK -*-
class ActorData(object):
    def __init__(self, data):
        self.userID = int(data['UserID'])
        self.bood = int(data['Blood'])
        self.money = int(data['Money'])
        self.attack = int(data['Attack'])
        self.shootdistance = int(data['ShootDistance'])
        self.speed = int(data['Speed'])
        self.experience = int(data['Experience'])


class ActorAttributes(object):
    def __init__(self):
        super(ActorAttributes, self).__init__()
        self.actorFilePath = './database/actor-attr.txt'
        self.actorAttr = {}

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
                        cell = ActorData(data)
                        self.actorAttr[cell.userID] = cell
                        data = {}
                        data[key] = value
                    else:
                        data[key] = value
                else:
                    data[key] = value
            if len(data) != 0:
                cell = ActorData(data)
                self.actorAttr[cell.userID] = cell

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