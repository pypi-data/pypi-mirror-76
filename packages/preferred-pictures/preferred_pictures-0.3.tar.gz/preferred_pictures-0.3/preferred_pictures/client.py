import hmac
import hashlib
import time
import uuid
import collections.abc
from typing import Iterable
from urllib.parse import urlencode

signature_field_order = [
    "choices_prefix",
    "choices_suffix",
    "choices[]",
    "choices",
    "destinations_prefix",
    "destinations_suffix",
    "destinations[]",
    "destinations",
    "expiration",
    "go",
    "json",
    "tournament",
    "ttl",
    "uid"
]


class Client:
    """
    A class to represent a PreferredPictures client

    Attributes
    ----------
    identity : str
        The identity that is used to generate requests

    secret_key: str
        The secret key associated with the identity to create
        signatures for requests.

    max_choices: int
        The maximum number of choices allowed in an API
        request.

        The default value is 35.

    endpoint: str
        The endpoint of the PreferredPictures API that
        should be used, by default this is

        https://api.preferred-pictures.com

    Methods
    -------
    create_choose_url(choices: Iterable[str], tournament: str, ttl=600, expiration_ttl=3600, prefix='', suffix='') -> str:
        Build a URL that calls the PreferredPictures API to select
        one choice from the list of choices available.
    """

    def __init__(self, identity: str, secret_key: str, max_choices=35, endpoint="https://api.preferred-pictures.com"):
        """
        Creates a new PreferredPictures client.

        Parameters:
        -----------

        identity : str
            The PreferredPictures identity to use when creating
            requests.

        secret_key : str
            The secret key associated with the passed identity

        Returns:

            A new PreferredPictures client instance
        """
        self.identity = identity
        self.secret_key = secret_key
        self.max_choices = max_choices
        self.endpoint = endpoint

    def create_choose_url(self,
                          choices: Iterable[str],
                          tournament: str,
                          ttl=600,
                          expiration_ttl=3600,
                          choices_prefix: str = '',
                          choices_suffix: str = '',
                          destinations: Iterable[str] = [],
                          destinations_prefix: str = '',
                          destinations_suffix: str = '',
                          go: bool = False,
                          json: bool = False
                          ) -> str:
        """
        Build a URL that calls the PreferredPictures API to select
        one choice from the list of choices available.

        Parameters:
        -----------

        choices : Iterable[str]
            A interable that returns the choices that should be sent
            to the api

        tournament: str
            The tournament in which this request participates.

        ttl: int, optional
            The time to live for an action to be recorded from
            this choice. Specified in seconds.

            Default: 600

        expiration_ttl: int, optional
            The time to live for the request signature. Specified
            in seconds.

            Default: 3600

        choices_prefix: str
            A prefix to apply to all of the choices

        choices_suffix: str
            A suffix to apply to all of the choices

        destinations : Iterable[Str]
            An optional iterable that return the destination URLs that
            will be paired with the choices.

        destinations_prefix: str
            A prefix to apply to all of the destination URLS

        destinations_suffix: str
            A suffix to apply to all of the destination URLS


        Returns:
        --------

        str - A signed URL that contains all of the specified
        parameters.

        """
        if ttl > expiration_ttl:
            raise ValueError("expiration_ttl must be >= ttl")

        if len(choices) == 0:
            raise ValueError("No choices were passed")

        if len(choices) > self.max_choices:
            raise ValueError(
                "Too many choices were passed the limit is " + str(self.max_choices))

        params = {
            "choices[]": choices,
            "tournament": tournament,
            "expiration": str(int(time.time()) + expiration_ttl),
            "uid": str(uuid.uuid4()),
            "ttl": str(ttl),
        }

        if choices_prefix != "":
            params['choices_prefix'] = choices_prefix

        if choices_suffix != "":
            params['choices_suffix'] = choices_suffix

        if len(destinations) > 0:
            params['destinations[]'] = destinations

        if destinations_prefix != "":
            params['destinations_prefix'] = destinations_prefix

        if destinations_suffix != "":
            params['destinations_suffix'] = destinations_suffix

        if json == True:
            params['json'] = 'true'

        if go == True:
            params['go'] = 'true'

        params['identity'] = self.identity

        included_fields = map(lambda name: params[name],
                              filter(lambda name: name in params, signature_field_order))

        signed_values = map(lambda v: ",".join(v) if isinstance(v, collections.abc.Iterable) and not isinstance(v, str) else v,
                            included_fields)

        signing_string = "/".join(signed_values)

        signature = hmac.new(
            bytearray(self.secret_key, 'utf8'),
            bytearray(signing_string, 'utf8'),
            hashlib.sha256).hexdigest()

        params['signature'] = signature

        return "{}/choose?{}".format(self.endpoint, urlencode(params, True))


if __name__ == "__main__":
    pp = Client("testidentity", "secret123456")
    url = pp.create_choose_url(["red", "green", "blue"], "test-tournament")
    print(url)
