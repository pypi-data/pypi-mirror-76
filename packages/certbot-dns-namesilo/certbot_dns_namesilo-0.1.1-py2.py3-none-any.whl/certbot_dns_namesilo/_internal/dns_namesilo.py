"""DNS Authenticator for Namesilo DNS."""
import logging

from lexicon.providers import namesilo
import zope.interface

from certbot import errors
from certbot import interfaces
from certbot.plugins import dns_common
from certbot.plugins import dns_common_lexicon

logger = logging.getLogger(__name__)

ACCOUNT_URL = 'https://namesilo.com/user'


@zope.interface.implementer(interfaces.IAuthenticator)
@zope.interface.provider(interfaces.IPluginFactory)
class Authenticator(dns_common.DNSAuthenticator):
    """DNS Authenticator for Namesilo

    This Authenticator uses the Namesilo API to fulfill a dns-01 challenge.
    """

    description = 'Obtain certificates using a DNS TXT record (if you are using Namesilo for DNS).'
    ttl = 3600

    def __init__(self, *args, **kwargs):
        super(Authenticator, self).__init__(*args, **kwargs)
        self.credentials = None

    @classmethod
    def add_parser_arguments(cls, add):  # pylint: disable=arguments-differ
        super(Authenticator, cls).add_parser_arguments(add, default_propagation_seconds=1800)
        add('credentials', help='Namesilo credentials INI file.')

    def more_info(self):  # pylint: disable=missing-function-docstring
        return 'This plugin configures a DNS TXT record to respond to a dns-01 challenge using ' + \
               'the Namesilo API.'

    def _setup_credentials(self):
        self.credentials = self._configure_credentials(
            'credentials',
            'Namesilo credentials INI file',
            {
                'token': 'User access token for Namesilo API. (See {0}.)'.format(ACCOUNT_URL)
            }
        )

    def _perform(self, domain, validation_name, validation):
        self._get_namesilo_client().add_txt_record(domain, validation_name, validation)

    def _cleanup(self, domain, validation_name, validation):
        self._get_namesilo_client().del_txt_record(domain, validation_name, validation)

    def _get_namesilo_client(self):
        return _NamesiloLexiconClient(self.credentials.conf('token'), self.ttl)


class _NamesiloLexiconClient(dns_common_lexicon.LexiconClient):
    """
    Encapsulates all communication with the Namesilo via Lexicon.
    """

    def __init__(self, token, ttl):
        super(_NamesiloLexiconClient, self).__init__()

        config = dns_common_lexicon.build_lexicon_config('namesilo', {
            'ttl': ttl,
        }, {
            'auth_token': token,
        })

        self.provider = namesilo.Provider(config)

    def _handle_general_error(self, e, domain_name):
        if "Invalid Domain Syntax" in str(e):
            return None

        if str(e).startswith('No domain found'):
            return None

        return errors.PluginError('Unexpected error determining zone identifier for {0}: {1}'
                                    .format(domain_name, e))

