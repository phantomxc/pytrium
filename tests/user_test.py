from atrium import User, Api

from mock import MagicMock
import pytest
import unittest


class TestUser(unittest.TestCase):

    def setUp(self):

        self.apiMock = MagicMock(spec=Api)
        self.user = User(self.apiMock, 'userGuid')
        self.params = {
            "foo": "bar"
        }
        self.payload = {
            "bar": "baz"
        }

    def testGetUser(self):
        self.user.getUser()
        self.apiMock.readUser.assert_called_with("userGuid")

    def testGetAccounts(self):
        self.user.getAccounts(queryParams=self.params)
        self.apiMock.getAccounts.assert_called_with("userGuid", queryParams=self.params)

    def testReadAccount(self):
        self.user.readAccount("acctGuid")
        self.apiMock.readAccount.assert_called_with("userGuid", "acctGuid")

    def testGetMembers(self):
        self.user.getMembers(queryParams=self.params)
        self.apiMock.getMembers.assert_called_with("userGuid", queryParams=self.params)

    def testReadMember(self):
        self.user.readMember("memGuid")
        self.apiMock.readMember.assert_called_with("userGuid", "memGuid")

    def testCreateMember(self):
        self.user.createMember(self.payload)
        self.apiMock.createMember.assert_called_with("userGuid", payload=self.payload)

    def testGetMemberStatus(self):
        self.user.getMemberStatus("memGuid")
        self.apiMock.getMemberStatus.assert_called_with("userGuid", "memGuid")

    def testGetMemberChallenges(self):
        self.user.getMemberChallenges("memGuid")
        self.apiMock.getMemberChallenges.assert_called_with("userGuid", "memGuid")

    def testAggregateMember(self):
        self.user.aggregateMember("memGuid")
        self.apiMock.startMemberAgg.assert_called_with("userGuid", "memGuid")

    def testResumeAggregration(self):
        self.user.resumeAggregation("memGuid", self.payload)
        self.apiMock.resumeMemberAgg.assert_called_with(
            "userGuid",
            "memGuid",
            payload=self.payload
        )

    def testGetTransactions(self):
        self.user.getTransactions(queryParams=self.params)
        self.apiMock.getTransactions.assert_called_with("userGuid", queryParams=self.params)

    def testGetTransactionsByAccount(self):
        self.user.getTransactionsByAccount("acctGuid", queryParams=self.params)
        self.apiMock.getTransactionsByAccount.assert_called_with(
            "userGuid",
            "acctGuid",
            queryParams=self.params
        )

    def testReadTransaction(self):
        self.user.readTransaction("transGuid")
        self.apiMock.readTransaction.assert_called_with("userGuid", "transGuid")

    def getHoldings(self):
        self.user.getHoldings(queryParams=self.params)
        self.apiMock.getHoldings.assert_called_with("userGuid", queryParams=self.params)

    def readHolding(self):
        self.user.readHolding("holdGuid")
        self.apiMock.readHolding.assert_called_with("userGuid", "holdGuid")

