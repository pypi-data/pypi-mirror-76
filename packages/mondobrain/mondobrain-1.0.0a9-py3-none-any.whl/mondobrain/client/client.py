from .credentials import BasicCredentials
from .resources import APIResource, SolverAPIResource
from .sessions import APITokenSession, JWTSession


class Client:
    """
    The Client object enables API authentication in order to interface with the
    MondoBrain server-side services such as the MondoBrain Solver.

    **Parameters**

    apiKey: string, default=None
        The key or token will be provided by a MondoBrain representative

    username: string, default=None
        Authentication user name if needed
        ** Required if provided instead of apiKey **

    password: string, default=None
        Authentication password if needed
        ** Required if provided instead of apiKey **

    domain: string, default=None
        This will be the domain of the server stack that is provided with 
        your apiKey by a MondoBrain representative

    https: boolean, default=True
        Only set to False for local stack

    **Examples**

    >>> import mondobrain as mb
    >>> client = mb.Client(apiKey="<your-api-token-here>", domain="demo.mondobrain.com")
    """  # NOQA E501

    def __init__(
        self,
        apiKey=None,
        username=None,
        password=None,
        domain="staging.mondobrain.com",
        https=True,
    ):
        # endpoint configuration
        scheme = "https://" if https else "http://"
        base_url = scheme + domain + "/api/v0.2/"

        if username is not None and password is not None and apiKey is not None:
            raise ValueError(
                "`username` & `password` must be unset when `apiKey` is used"
            )

        session = None

        if apiKey is not None:
            session = APITokenSession(apiKey, base_url=base_url)

        if username is not None and password is not None:
            creds = BasicCredentials(username, password)
            session = JWTSession(creds, base_url=base_url)

        if session is None:
            raise TypeError(
                (
                    "Missing authorization arguments."
                    "Need `apiKey` or `username` & `password` arguments"
                )
            )

        self.session = session

        # setup resources
        # note: this is not end design yet
        self.portals = APIResource(self.session, "portals")

        # these ones are special... works still needed
        self._solver = SolverAPIResource(self.session, "sdk/process/solve")

    def request(self, method, url, **kwargs):
        return self.session.request(method, url, **kwargs)
