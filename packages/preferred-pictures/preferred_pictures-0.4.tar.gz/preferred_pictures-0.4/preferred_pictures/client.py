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
    """This class is a PreferredPictures client

    :param identity:
        The PreferredPictures identity to use when creating
        requests.
    :type identity: str

    :param secret_key:
        The secret key associated with the passed identity
    :type secret_key: str

    :returns: A new PreferredPictures client instance
    :rtype: PreferredPictures.Client

    :Example:

    >>> import preferred_pictures
    >>> pp_client = preferred_pictures.Client(identity, secret_key)

    """

    def __init__(self, identity: str, secret_key: str, max_choices=35, endpoint="https://api.preferred-pictures.com"):
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
                          json: bool = False,
                          uid: str = ''
                          ) -> str:
        """
        Build a URL that calls the PreferredPictures API to select
        one choice from the list of choices available.

        :param choices: A interable that returns the choices that
            should be sent to the api
        :type choices: Iterable[str]

        :param tournament:
            The tournament in which this request participates.
        :type tournament: str

        :param ttl:
            The time to live for an action to be recorded from
            this choice. Specified in seconds.
            Default: 600
        :type ttl: int, optional

        :param expiration_ttl:
            The time to live for the request signature. Specified
            in seconds.
            Default: 3600
        :type expiration_ttl: int, optional

        :param choices_prefix:
            A prefix to apply to all of the choices
        :type choices_prefix: str

        :param choices_suffix:
            A suffix to apply to all of the choices
        :type choices_suffix: str

        :param destinations:
            An optional iterable that return the destination URLs that
            will be paired with the choices.
        :type destinations: Iterable[Str]

        :param destinations_prefix:
            A prefix to apply to all of the destination URLS
        :type destinations_prefix: str

        :param destinations_suffix:
            A suffix to apply to all of the destination URLS
        :type destinations_suffix: str

        :param uid:
            An optional unique identifier that is used to correlate
            choices and actions. If it is not specified a UUID v4
            will be generated.
        :type uid: str

        :return: A signed URL that contains all of the specified
            parameters.
        :rtype: str

        :Examples:

        >>> # The simpliest example of choosing between
        >>> # three URLs.
        >>> #
        >>> import preferred_pictures
        >>> pp_client = preferred_pictures.Client(identity, secret_key)
        >>> url = pp_client.create_choose_url(
        >>>     choices=[
        >>>         'https://example.com/color-red.jpg',
        >>>         'https://example.com/color-green.jpg',
        >>>         'https://example.com/color-blue.jpg',
        >>>     ],
        >>>     tournament: 'test-tournament',
        >>> )
        "https://api.preferred-pictures.com/...."

        >>> # Different Example using prefix and suffix for choices.
        >>> url = pp_client.create_choose_url(
        >>>     choices=['red', 'green', 'blue'],
        >>>     tournament: 'test-tournament',
        >>>     choices_prefix: 'https://example.com/color-',
        >>>     choices_suffix: '.jpg',
        >>> )
        "https://api.preferred-pictures.com/...."

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
            "ttl": str(ttl),
        }

        if uid != "":
            params['uid'] = uid
        else:
            params['uid'] = str(uuid.uuid4())

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
