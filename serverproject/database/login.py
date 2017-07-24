# -*- coding: GBK -*-

class loginServer(object):
    def __init__(self):
        super(loginServer, self).__init__()
        self.usersData ={}
        self.accoutFilePath = './database/account-info.txt'
        self.MAX_USER_ID = -1

        self._loaddata(self.accoutFilePath)

        return

    def _loaddata(self, path):
        f = open(path, 'r')

        try:
            data = []
            for line in f:
                if line != '\n':
                    data.append(line[0:len(line)-1])
                    continue
                else:
                    self._parseLine(data)
                    data=[]

            self._parseLine(data)
        except:
            f.close()
            raise

        f.close()

    def _parseLine(self, data):
        userID = int(data[0])
        userName = data[1]
        userPassword=data[2]

        if userID > self.MAX_USER_ID:
            self.MAX_USER_ID = userID

        self.usersData[userName] = [userID, userName, userPassword]

    def userPasswordConfirm(self, userName, userPassword):
        try:
            if userPassword == self.usersData[userName][2]:
                return 1,self.usersData[userName][0] # return userID
            else:
                return 0,-1
        except:
            return -1,-1 #Illegal user name

    def createAccount(self, userName, passwrod):
        try:
            cell = None
            cell = self.usersData[userName]
            return 0,-1; #userName conflict
        except:
            f = open(self.accoutFilePath, 'a')

            try:
                f.write('\n\n')
                f.writelines(repr(self.MAX_USER_ID + 1))
                f.write('\n')
                f.writelines(userName)
                f.write('\n')
                f.writelines(passwrod)

                self.usersData[userName] = [self.MAX_USER_ID + 1, userName, passwrod]
                self.MAX_USER_ID += 1
                f.close()
                return 1, self.usersData[userName][0]  # return userID
            except:
                f.close();
                return -1, -1