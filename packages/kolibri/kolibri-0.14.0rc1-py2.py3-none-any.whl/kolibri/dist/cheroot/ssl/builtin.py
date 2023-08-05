"""
A library for integrating Python's builtin ``ssl`` library with Cheroot.

The ssl module must be importable for SSL functionality.

To use this module, set ``HTTPServer.ssl_adapter`` to an instance of
``BuiltinSSLAdapter``.
"""

try:
    import ssl
except ImportError:
    ssl = None

try:
    from _pyio import DEFAULT_BUFFER_SIZE
except ImportError:
    try:
        from io import DEFAULT_BUFFER_SIZE
    except ImportError:
        DEFAULT_BUFFER_SIZE = -1

from . import Adapter
from .. import errors
from ..makefile import MakeFile


def _assert_ssl_exc_contains(exc, *msgs):
    """Check whether SSL exception contains either of messages provided."""
    if len(msgs) < 1:
        raise TypeError(
            '_assert_ssl_exc_contains() requires '
            'at least one message to be passed.'
        )
    err_msg_lower = exc.args[1].lower()
    return any(m.lower() in err_msg_lower for m in msgs)


class BuiltinSSLAdapter(Adapter):
    """A wrapper for integrating Python's builtin ssl module with Cheroot."""

    certificate = None
    """The filename of the server SSL certificate."""

    private_key = None
    """The filename of the server's private key file."""

    certificate_chain = None
    """The filename of the certificate chain file."""

    context = None
    """The ssl.SSLContext that will be used to wrap sockets."""

    ciphers = None
    """The ciphers list of SSL."""

    def __init__(
            self, certificate, private_key, certificate_chain=None,
            ciphers=None):
        """Set up context in addition to base class properties if available."""
        if ssl is None:
            raise ImportError('You must install the ssl module to use HTTPS.')

        super(BuiltinSSLAdapter, self).__init__(
            certificate, private_key, certificate_chain, ciphers)

        self.context = ssl.create_default_context(
            purpose=ssl.Purpose.CLIENT_AUTH,
            cafile=certificate_chain
        )
        self.context.load_cert_chain(certificate, private_key)
        if self.ciphers is not None:
            self.context.set_ciphers(ciphers)

    def bind(self, sock):
        """Wrap and return the given socket."""
        return super(BuiltinSSLAdapter, self).bind(sock)

    def wrap(self, sock):
        """Wrap and return the given socket, plus WSGI environ entries."""
        try:
            s = self.context.wrap_socket(
                sock, do_handshake_on_connect=True, server_side=True,
            )
        except ssl.SSLError as ex:
            EMPTY_RESULT = None, {}
            if ex.errno == ssl.SSL_ERROR_EOF:
                # This is almost certainly due to the cherrypy engine
                # 'pinging' the socket to assert it's connectable;
                # the 'ping' isn't SSL.
                return EMPTY_RESULT
            elif ex.errno == ssl.SSL_ERROR_SSL:
                if _assert_ssl_exc_contains(ex, 'http request'):
                    # The client is speaking HTTP to an HTTPS server.
                    raise errors.NoSSLError

                # Check if it's one of the known errors
                # Errors that are caught by PyOpenSSL, but thrown by
                # built-in ssl
                _block_errors = (
                    'unknown protocol', 'unknown ca', 'unknown_ca',
                    'unknown error',
                    'https proxy request', 'inappropriate fallback',
                    'wrong version number',
                    'no shared cipher', 'certificate unknown',
                    'ccs received early',
                )
                if _assert_ssl_exc_contains(ex, *_block_errors):
                    # Accepted error, let's pass
                    return EMPTY_RESULT
            elif _assert_ssl_exc_contains(ex, 'handshake operation timed out'):
                # This error is thrown by builtin SSL after a timeout
                # when client is speaking HTTP to an HTTPS server.
                # The connection can safely be dropped.
                return EMPTY_RESULT
            raise
        return s, self.get_environ(s)

    # TODO: fill this out more with mod ssl env
    def get_environ(self, sock):
        """Create WSGI environ entries to be merged into each request."""
        cipher = sock.cipher()
        ssl_environ = {
            'wsgi.url_scheme': 'https',
            'HTTPS': 'on',
            'SSL_PROTOCOL': cipher[1],
            'SSL_CIPHER': cipher[0]
            # SSL_VERSION_INTERFACE     string  The mod_ssl program version
            # SSL_VERSION_LIBRARY   string  The OpenSSL program version
        }
        return ssl_environ

    def makefile(self, sock, mode='r', bufsize=DEFAULT_BUFFER_SIZE):
        """Return socket file object."""
        return MakeFile(sock, mode, bufsize)
