import sys
import unittest
from mock import patch, MagicMock, Mock

requesterMock = sys.modules['atrium.requester'] = MagicMock()

import pytest

from atrium import Api
from atrium.utils import storage

from atrium.errors import (
    BadRequestError,
    ConfigError,
    ConflictError,
    MaintenanceError,
    MethodNotAllowedError,
    NotAcceptable,
    NotFoundError,
    ServerError,
    UnauthorizedError,
    UnprocessableEntityError
)


class TestApiInit(unittest.TestCase):

    def test_init_no_key(self):
        with self.assertRaises(ConfigError):
            api = Api()

    def test_init_no_client(self):
        with self.assertRaises(ConfigError):
            api = Api(key="boo")

    def test_init_success(self):
        try:
            api = Api(key="foo", client_id="bar")
        except ConfigError:
            self.fail("init raised ConfigError unexpectedly")

    def test_root(self):
        api = Api(key="foo", client_id="bar")
        self.assertTrue(api.root)


class TestApiHeaders(unittest.TestCase):

    def setUp(self):
        self.api = Api(key="foo", client_id="bar")


    def test_buildHeaders(self):
        headers = self.api._buildHeaders("GET")
        self.assertEqual(headers, {
            "MX-API-KEY": "foo",
            "MX-CLIENT-ID": "bar",
            "Accept": "application/vnd.mx.atrium.v1+json"
        })

    def test_buildHeadersPost(self):
        headers = self.api._buildHeaders("POST")
        self.assertEqual(headers, {
            "MX-API-KEY": "foo",
            "MX-CLIENT-ID": "bar",
            "Accept": "application/vnd.mx.atrium.v1+json",
            "Content-Type": "application/json"
        })

    def test_buildHeadersPut(self):
        headers = self.api._buildHeaders("PUT")
        self.assertEqual(headers, {
            "MX-API-KEY": "foo",
            "MX-CLIENT-ID": "bar",
            "Accept": "application/vnd.mx.atrium.v1+json",
            "Content-Type": "application/json"
        })


class TestMakeRequest(unittest.TestCase):

    def setUp(self):
        self.api = Api(key="foo", client_id="bar")
        self.url = "foo"
        self.method = "bar"
        self.headers = {"foo": "bar"}
        requesterMock.request.return_value = storage({
            "status_code": 200
        })


    @patch('atrium.Api._parseResponse')
    @patch('atrium.Api._buildHeaders')
    def testRequestCall(self, mock_headers, parse_mock):
        mock_headers.return_value = self.headers

        self.api._makeRequest(self.url, self.method)

        self.assertTrue(mock_headers.called)
        self.assertTrue(parse_mock.called)
        requesterMock.request.assert_called_with(
            self.api.root + self.url,
            self.method,
            headers=self.headers,
            payload={}
        )

    def test400(self):
        with pytest.raises(BadRequestError):
            requesterMock.request.return_value = storage({
                "status_code": 400
            })
            self.api._makeRequest(self.url, self.method)


    def test401(self):
        with pytest.raises(UnauthorizedError):
            requesterMock.request.return_value = storage({
                "status_code": 401
            })
            self.api._makeRequest(self.url, self.method)

    def test404(self):
        with pytest.raises(NotFoundError):
            requesterMock.request.return_value = storage({
                "status_code": 404
            })
            self.api._makeRequest(self.url, self.method)

    def test405(self):
        with pytest.raises(MethodNotAllowedError) as e:
            requesterMock.request.return_value = storage({
                "status_code": 405
            })
            self.api._makeRequest(self.url, self.method)

    def test406(self):
        with pytest.raises(NotAcceptable) as e:
            requesterMock.request.return_value = storage({
                "status_code": 406
            })
            self.api._makeRequest(self.url, self.method)

    def test409(self):
        with pytest.raises(ConflictError):
            requesterMock.request.return_value = storage({
                "status_code": 409
            })
            self.api._makeRequest(self.url, self.method)

    def test422(self):
        with pytest.raises(UnprocessableEntityError):
            requesterMock.request.return_value = storage({
                "status_code": 422
            })
            self.api._makeRequest(self.url, self.method)

    def test500(self):
        with pytest.raises(ServerError):
            requesterMock.request.return_value = storage({
                "status_code": 500
            })
            self.api._makeRequest(self.url, self.method)

    def test503(self):
        with pytest.raises(MaintenanceError):
            requesterMock.request.return_value = storage({
                "status_code": 503
            })
            self.api._makeRequest(self.url, self.method)


class TestParseReponse(unittest.TestCase):

    def setUp(self):
        self.api = Api(key="foo", client_id="bar")

    def testWithJson(self):
        res = Mock(spec=["json", "status_code"])
        res.json.return_value = {"foo": "bar"}
        res.status_code.return_value = 200

        json = self.api._parseResponse(res)
        self.assertEqual(json, {"foo": "bar"})

    def testWithoutJson(self):
        with pytest.raises(ValueError):
            res = Mock(spec=["json", "status_code"])
            res.status_code = 500
            res.json.side_effect = ValueError('Kapow!')

            self.api._parseResponse(res)

    def testWithoutJson20x(self):
        '''
        It should not raise the exception if the status code is 202 or 204
        '''
        res = Mock(spec=["json", "status_code"])
        res.json.side_effect = ValueError('Kapow!')
        res.status_code = 204

        json = self.api._parseResponse(res)

        self.assertEqual(json, {})


class TestBuildQueryParams(unittest.TestCase):

    def setUp(self):
        self.api = Api(key="foo", client_id="bar")

    def testNoParams(self):
        """
        It should return just the standard URL with no params
        """
        res = self.api._buildQueryParams('foo', {})
        self.assertEqual(res, 'foo')

    def testWithParams(self):
        res = self.api._buildQueryParams('foo', {
            "foo": "bar",
            "baz": "bud"
        })
        # Python 3 doesn't return the args in the same order
        self.assertIn(res, ["foo?foo=bar&baz=bud", "foo?baz=bud&foo=bar"])


class TestUserCrudMethods(unittest.TestCase):

    def setUp(self):
        self.api = Api(key="foo", client_id="bar")

    @patch('atrium.Api._makeRequest')
    def testGetUsersNoParams(self, request_mock):
        self.api.getUsers()

        request_mock.assert_called_with("users", "GET")

    @patch('atrium.Api._makeRequest')
    def testGetUsersWithParams(self, request_mock):
        self.api.getUsers(queryParams={
            "foo": "bar"
        })

        request_mock.assert_called_with("users?foo=bar", "GET")

    @patch('atrium.Api._makeRequest')
    def testCreateUser(self, request_mock):
        payload={
            "foo": "bar"
        }
        self.api.createUser(payload=payload)

        request_mock.assert_called_with("users", "POST", payload={"user": payload})

    @patch('atrium.Api._makeRequest')
    def testReadUser(self, request_mock):
        self.api.readUser('userGuid')

        request_mock.assert_called_with("users/userGuid", "GET")

    @patch('atrium.Api._makeRequest')
    def testUpdateUser(self, request_mock):
        payload={
            "foo": "bar"
        }
        self.api.updateUser("userGuid", payload=payload)

        request_mock.assert_called_with("users/userGuid", "PUT", payload={"user": payload})

    @patch('atrium.Api._makeRequest')
    def testDeletedUser(self, request_mock):
        self.api.deleteUser('userGuid')

        request_mock.assert_called_with("users/userGuid", "DELETE")


class TestTransactionMethods(unittest.TestCase):

    def setUp(self):
        self.api = Api(key="foo", client_id="bar")

    @patch('atrium.Api._makeRequest')
    def testGetTransactionsNoParams(self, request_mock):
        self.api.getTransactions('userGuid')
        request_mock.assert_called_with("users/userGuid/transactions", "GET")

    @patch('atrium.Api._makeRequest')
    def testgetTransactionsWithParams(self, request_mock):
        self.api.getTransactions('userGuid', queryParams={
            "foo": "bar"
        })
        request_mock.assert_called_with("users/userGuid/transactions?foo=bar", "GET")

    @patch('atrium.Api._makeRequest')
    def testTransactionsByAccountNoParams(self, request_mock):
        self.api.getTransactionsByAccount(
            'userGuid',
            'accountGuid',
        )
        request_mock.assert_called_with(
            "users/userGuid/accounts/accountGuid/transactions",
            "GET"
        )

    @patch('atrium.Api._makeRequest')
    def testTransactionsByAccountWithParams(self, request_mock):
        self.api.getTransactionsByAccount(
            'userGuid',
            'accountGuid',
            queryParams={
                "foo": "bar"
            }
        )
        request_mock.assert_called_with(
            "users/userGuid/accounts/accountGuid/transactions?foo=bar",
            "GET"
        )

    @patch('atrium.Api._makeRequest')
    def testReadTransaction(self, request_mock):
        self.api.readTransaction('userGuid', 'transGuid')

        request_mock.assert_called_with(
            "users/userGuid/transactions/transGuid",
            "GET"
        )


class TestAccountMethods(unittest.TestCase):

    def setUp(self):
        self.api = Api(key="foo", client_id="bar")

    @patch('atrium.Api._makeRequest')
    def testGetAccountsNoParams(self, request_mock):
        self.api.getAccounts("userGuid")
        request_mock.assert_called_with("users/userGuid/accounts", "GET")

    @patch('atrium.Api._makeRequest')
    def testGetAccountsWithParams(self, request_mock):
        self.api.getAccounts("userGuid", queryParams={
            "foo": "bar"
        })
        request_mock.assert_called_with("users/userGuid/accounts?foo=bar", "GET")

    @patch('atrium.Api._makeRequest')
    def testReadAccounts(self, request_mock):
        self.api.readAccount("userGuid", "acctGuid")
        request_mock.assert_called_with("users/userGuid/accounts/acctGuid", "GET")


class TestInstitutionMethods(unittest.TestCase):

    def setUp(self):
        self.api = Api(key="foo", client_id="bar")

    @patch('atrium.Api._makeRequest')
    def testGetInstitutionsNoParams(self, request_mock):
        self.api.getInstitutions()
        request_mock.assert_called_with("institutions", "GET")

    @patch('atrium.Api._makeRequest')
    def testGetInstitutionsWithParams(self, request_mock):
        self.api.getInstitutions(queryParams={
            "foo": "bar"
        })
        request_mock.assert_called_with("institutions?foo=bar", "GET")

    @patch('atrium.Api._makeRequest')
    def testReadInstitution(self, request_mock):
        self.api.readInstitution('instGuid')
        request_mock.assert_called_with("institutions/instGuid", "GET")

    @patch('atrium.Api._makeRequest')
    def testGetCredentials(self, request_mock):
        self.api.getCredentials('instGuid')
        request_mock.assert_called_with("institutions/instGuid/credentials", "GET")


class TestMemberMethods(unittest.TestCase):

    def setUp(self):
        self.api = Api(key="foo", client_id="bar")

    @patch('atrium.Api._makeRequest')
    def testGetMembersNoParams(self, request_mock):
        self.api.getMembers("userGuid")
        request_mock.assert_called_with("users/userGuid/members", "GET")

    @patch('atrium.Api._makeRequest')
    def testGetMembersWithParams(self, request_mock):
        self.api.getMembers("userGuid", queryParams={
            "foo": "bar"
        })
        request_mock.assert_called_with("users/userGuid/members?foo=bar", "GET")

    @patch('atrium.Api._makeRequest')
    def testCreateMember(self, request_mock):
        payload={
            "foo": "bar"
        }
        self.api.createMember("userGuid", payload=payload)

        request_mock.assert_called_with(
            "users/userGuid/members",
            "POST",
            payload={"member": payload}
        )

    @patch('atrium.Api._makeRequest')
    def testReadMember(self, request_mock):
        self.api.readMember("userGuid", "memGuid")

        request_mock.assert_called_with(
            "users/userGuid/members/memGuid",
            "GET"
        )

    @patch('atrium.Api._makeRequest')
    def testUpdateMember(self, request_mock):
        payload={
            "foo": "bar"
        }
        self.api.updateMember("userGuid", "memGuid", payload=payload)

        request_mock.assert_called_with(
            "users/userGuid/members/memGuid",
            "PUT",
            payload={"member": payload}
        )

    @patch('atrium.Api._makeRequest')
    def testDeleteMember(self, request_mock):
        self.api.deleteMember("userGuid", "memGuid")

        request_mock.assert_called_with(
            "users/userGuid/members/memGuid",
            "DELETE"
        )

    @patch('atrium.Api._makeRequest')
    def testGetMemberStatus(self, request_mock):
        self.api.getMemberStatus('userGuid', 'memGuid')

        request_mock.assert_called_with(
            "users/userGuid/members/memGuid/status",
            "GET"
        )

    @patch('atrium.Api._makeRequest')
    def testGetMemberChallenges(self, request_mock):
        self.api.getMemberChallenges('userGuid', 'memGuid')

        request_mock.assert_called_with(
            "users/userGuid/members/memGuid/challenges",
            "GET"
        )

    @patch('atrium.Api._makeRequest')
    def testStartMemberAgg(self, request_mock):
        self.api.startMemberAgg('userGuid', 'memGuid')

        request_mock.assert_called_with (
            "users/userGuid/members/memGuid/aggregate",
            "POST"
        )

    @patch('atrium.Api._makeRequest')
    def testResumeMemberAgg(self, request_mock):
        payload={
            "foo": "bar"
        }
        self.api.resumeMemberAgg('userGuid', 'memGuid', payload=payload)

        request_mock.assert_called_with (
            "users/userGuid/members/memGuid/resume",
            "PUT",
            payload={"member": payload}
        )


class TestHoldingMethods(unittest.TestCase):

    def setUp(self):
        self.api = Api(key="foo", client_id="bar")

    @patch('atrium.Api._makeRequest')
    def testGetHoldingsNoParams(self, request_mock):
        self.api.getHoldings("userGuid")
        request_mock.assert_called_with("users/userGuid/holdings", "GET")

    @patch('atrium.Api._makeRequest')
    def testGetHoldingsWithParams(self, request_mock):
        self.api.getHoldings("userGuid", queryParams={
            "foo": "bar"
        })
        request_mock.assert_called_with("users/userGuid/holdings?foo=bar", "GET")

    @patch('atrium.Api._makeRequest')
    def testReadAccounts(self, request_mock):
        self.api.readHolding("userGuid", "holdGuid")
        request_mock.assert_called_with("users/userGuid/holdings/holdGuid", "GET")



if __name__ == '__main__':
    unittest.main()