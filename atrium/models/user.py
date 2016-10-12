class User(object):

    def __init__(self, api, guid):
        self.api = api
        self.guid = guid

    def getUser(self):
        return self.api.readUser(self.guid)

    # --------------------------------
    # ACCOUNTS
    # --------------------------------
    def getAccounts(self, queryParams={}):
        return self.api.getAccounts(self.guid, queryParams=queryParams)

    def readAccount(self, acctGuid):
        return self.api.readAccount(self.guid, acctGuid)

    # --------------------------------
    # MEMBERS
    # --------------------------------
    def getMembers(self, queryParams={}):
        return self.api.getMembers(self.guid, queryParams=queryParams)

    def readMember(self, memGuid):
        return self.api.readMember(self.guid, memGuid)

    def createMember(self, payload):
        return self.api.createMember(self.guid, payload=payload)

    def getMemberStatus(self, memGuid):
        return self.api.getMemberStatus(self.guid, memGuid)

    def getMemberChallenges(self, memGuid):
        return self.api.getMemberChallenges(self.guid, memGuid)

    def aggregateMember(self, memGuid):
        return self.api.startMemberAgg(self.guid, memGuid)

    def resumeAggregation(self, memGuid, payload):
        return self.api.resumeMemberAgg(self.guid, memGuid, payload=payload)

    # --------------------------------
    # TRANSACTIONS
    # --------------------------------
    def getTransactions(self, queryParams={}):
        return self.api.getTransactions(self.guid, queryParams=queryParams)

    def getTransactionsByAccount(self, acctGuid, queryParams={}):
        return self.api.getTransactionsByAccount(
            self.guid,
            acctGuid,
            queryParams=queryParams
        )

    def readTransaction(self, transGuid):
        return self.api.readTransaction(self.guid, transGuid)

    # --------------------------------
    # HOLDINGS
    # --------------------------------
    def getHoldings(self, queryParams={}):
        return self.api.getHoldings(self.guid, queryParams=queryParams)

    def readHolding(self, holdGuid):
        return self.api.readHolding(self.guid, holdGuid)

