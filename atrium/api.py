from future.standard_library import install_aliases
install_aliases()

from urllib.parse import urlencode

from atrium.utils import cleanData
from atrium.requester import request
from atrium.errors import (
    BadRequestError,
    ConfigError,
    ConflictError,
    MaintenanceError,
    MethodNotAllowedError,
    NotFoundError,
    ServerError,
    UnauthorizedError,
    UnprocessableEntityError
)


class Api(object):
    """
      A python interface into the MX Atrium API
    """

    def __init__(self, **kwargs):

        self.key = kwargs.get('key')
        self.client_id = kwargs.get('client_id')

        if not self.key:
            raise ConfigError('Missing key (MX-API-KEY)')

        if not self.client_id:
            raise ConfigError('Missing client_id (MX-CLIENT-ID)')

        # self.root = "https://atrium.moneydesktop.com/api/"
        self.root = "https://qa-harvey.moneydesktop.com/api/"

    def _buildHeaders(self):
        return {
            "MX-API-KEY": self.key,
            "MX-CLIENT-ID": self.client_id,
            "Content-Type": "application/json"
        }

    def _makeRequest(self, endpoint, method, payload={}):
        full_url = self.root + endpoint
        headers = self._buildHeaders()

        r = request(full_url, method, headers=headers, payload=payload)

        status = r.status_code
        if status == 400:
            raise BadRequestError(payload)
        elif status == 401:
            raise UnauthorizedError()
        elif status == 404:
            raise NotFoundError(endpoint)
        elif status == 405:
            msg = '{} is not allowed on {}'.format(method, endpoint)
            raise MethodNotAllowedError(msg)
        elif status == 409:
            raise ConflictError()
        elif status == 422:
            raise UnprocessableEntityError()
        elif status == 500:
            raise ServerError()
        elif status == 503:
            raise MaintenanceError()

        return self._parseResponse(r)

    def _parseResponse(self, response):
        try:
            return response.json()
        except ValueError:
            if response.status_code in [202, 204]:
                return {}
            else:
                raise

    def _buildQueryParams(self, url, params):
        if params:
            return url + "?{}".format(urlencode(params))
        return url

    # --------------------------------------------------
    # USER
    # --------------------------------------------------
    # @cleanData('users')
    def getUsers(self, queryParams={}):
        url = "users"
        url = self._buildQueryParams(url, queryParams)

        return self._makeRequest(url, "GET")

    @cleanData('user')
    def createUser(self, payload={}):
        url = "users"

        return self._makeRequest(url, "POST", payload=payload)

    @cleanData('user')
    def readUser(self, guid):
        url = "users/{}".format(guid)

        return self._makeRequest(url, "GET")

    @cleanData('user')
    def updateUser(self, guid, payload={}):
        url = "users/{}".format(guid)

        return self._makeRequest(url, "PUT", payload=payload)

    def deleteUser(self, guid):
        url = "users/{}".format(guid)

        return self._makeRequest(url, "DELETE")

    # --------------------------------------------------
    # TRANSACTIONS
    # --------------------------------------------------
    # @cleanData('transactions')
    def getTransactions(self, userGuid, queryParams={}):
        url = "users/{}/transactions".format(userGuid)
        url = self._buildQueryParams(url, queryParams)

        return self._makeRequest(url, "GET")

    # @cleanData('transactions')
    def getTransactionsByAccount(self, userGuid, acctGuid, queryParams={}):
        url = "users/{}/accounts/{}/transactions".format(userGuid, acctGuid)
        url = self._buildQueryParams(url, queryParams)

        return self._makeRequest(url, "GET")

    def getTransactionsByDate(self, userGuid, dateStart, dateEnd):
        pass

    @cleanData('transaction')
    def readTransaction(self, userGuid, transGuid):
        url = "users/{}/transactions/{}".format(userGuid, transGuid)

        return self._makeRequest(url, "GET")

    # --------------------------------------------------
    # ACCOUNTS
    # --------------------------------------------------
    # @cleanData('accounts')
    def getAccounts(self, userGuid, queryParams={}):
        url = "users/{}/accounts".format(userGuid)
        url = self._buildQueryParams(url, queryParams)

        return self._makeRequest(url, "GET")

    @cleanData('account')
    def readAccount(self, userGuid, acctGuid):
        url = "users/{}/accounts/{}".format(userGuid, acctGuid)

        return self._makeRequest(url, "GET")

    # --------------------------------------------------
    # INSTITUTIONS
    # --------------------------------------------------
    # cleanData('institutions')
    def getInstitutions(self, queryParams={}):
        url = "institutions"
        url = self._buildQueryParams(url, queryParams)

        return self._makeRequest(url, "GET")

    @cleanData('institution')
    def readInstitution(self, instGuid):
        url = "institutions/{}".format(instGuid)

        return self._makeRequest(url, "GET")

    @cleanData('credentials')
    def getCredentials(self, instGuid):
        url = "institutions/{}/credentials".format(instGuid)

        return self._makeRequest(url, "GET")

    # --------------------------------------------------
    # MEMBERS
    # --------------------------------------------------
    def getMembers(self, userGuid, queryParams={}):
        url = "users/{}/members".format(userGuid)
        url = self._buildQueryParams(url, queryParams)

        return self._makeRequest(url, "GET")

    @cleanData('member')
    def createMember(self, userGuid, payload={}):
        url = "users/{}/members".format(userGuid)

        return self._makeRequest(url, "POST", payload=payload)

    @cleanData('member')
    def readMember(self, userGuid, memGuid):
        url = "users/{}/members/{}".format(userGuid, memGuid)

        return self._makeRequest(url, "GET")

    @cleanData('member')
    def updateMember(self, userGuid, memGuid, payload={}):
        url = "users/{}/members/{}".format(userGuid, memGuid)

        return self._makeRequest(url, "PUT", payload=payload)

    def deleteMember(self, userGuid, memGuid):
        url = "users/{}/members/{}".format(userGuid, memGuid)

        return self._makeRequest(url, "DELETE")

    @cleanData('member')
    def getMemberStatus(self, userGuid, memGuid):
        url = "users/{}/members/{}/status".format(userGuid, memGuid)

        return self._makeRequest(url, "GET")

    @cleanData('credentials')
    def getMemberChallenges(self, userGuid, memGuid):
        url = "users/{}/members/{}/challenges".format(userGuid, memGuid)

        return self._makeRequest(url, "GET")

    @cleanData('member')
    def startMemberAgg(self, userGuid, memGuid):
        url = "users/{}/members/{}/aggregate".format(userGuid, memGuid)

        return self._makeRequest(url, "POST")

    @cleanData('member')
    def resumeMemberAgg(self, userGuid, memGuid, payload={}):
        url = "users/{}/members/{}/resume".format(userGuid, memGuid)

        return self._makeRequest(url, "PUT", payload=payload)

    # --------------------------------------------------
    # HOLDINGS
    # --------------------------------------------------
    # @cleanData('holdings')
    def getHoldings(self, userGuid, queryParams={}):
        url = "users/{}/holdings".format(userGuid)
        url = self._buildQueryParams(url, queryParams)

        return self._makeRequest(url, "GET")

    @cleanData('holding')
    def readHolding(self, userGuid, holdGuid):
        url = "users/{}/holdings/{}".format(userGuid, holdGuid)

        return self._makeRequest(url, "GET")
