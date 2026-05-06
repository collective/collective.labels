from functools import wraps
from plone.app.testing import TEST_USER_ID
from plone.app.testing import TEST_USER_NAME
from plone.app.testing import TEST_USER_PASSWORD
from plone.testing import z2
import base64
import lxml.html
import re
import threading
import transaction
import urllib.error
import urllib.parse


_local = threading.local()


def get_current_browser():
    return getattr(_local, 'browser', None)


def browsing(func):
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        app = self.layer['app']
        transaction.commit()
        browser = Browser(app)
        _local.browser = browser
        try:
            return func(self, browser, *args, **kwargs)
        finally:
            _local.browser = None
    return wrapper


class NodeList:

    def __init__(self, elements):
        self._elements = elements

    def __bool__(self):
        return bool(self._elements)

    def __len__(self):
        return len(self._elements)

    def __iter__(self):
        return (Node(el) for el in self._elements)

    @property
    def first(self):
        return Node(self._elements[0])

    @property
    def first_or_none(self):
        if self._elements:
            return Node(self._elements[0])
        return None

    @property
    def text(self):
        return [el.text_content().strip() for el in self._elements]


class Node:

    def __init__(self, element):
        self._el = element

    def __bool__(self):
        return True

    def css(self, selector):
        return NodeList(self._el.cssselect(selector))

    @property
    def text(self):
        return self._el.text_content().strip()

    @property
    def attrib(self):
        return self._el.attrib

    def parent(self):
        return Node(self._el.getparent())

    @property
    def inputs(self):
        return [Node(el) for el in self._el.cssselect('input')]

    @property
    def label(self):
        el_id = self._el.attrib.get('id')
        if not el_id:
            return None
        root = self._el.getroottree().getroot()
        matches = root.cssselect(f'label[for="{el_id}"]')
        if matches:
            return Node(matches[0])
        return None


class FormFiller:

    def __init__(self, zope_browser, fields, form=None, browser_wrapper=None):
        self._browser = zope_browser
        self._fields = fields
        self._form = form
        self._browser_wrapper = browser_wrapper

    def submit(self, label=None):
        form = self._form if self._form is not None else self._browser.getForm()
        for name, value in self._fields.items():
            try:
                ctrl = form.getControl(name=name)
            except Exception:
                try:
                    ctrl = form.getControl(name)
                except Exception:
                    continue
            ctrl.value = value
        if label:
            form.getControl(label).click()
        else:
            form.submit()
        if self._browser_wrapper is not None:
            self._browser_wrapper._parse_response()


class FormWrapper:

    def __init__(self, zope_browser, form, browser_wrapper=None):
        self._browser = zope_browser
        self._form = form
        self._browser_wrapper = browser_wrapper

    def fill(self, fields):
        return FormFiller(self._browser, fields, form=self._form,
                          browser_wrapper=self._browser_wrapper)

    def submit(self):
        self._form.submit()
        if self._browser_wrapper is not None:
            self._browser_wrapper._parse_response()


class FormCollection:

    def __init__(self, browser_wrapper):
        self._browser_wrapper = browser_wrapper
        self._browser = browser_wrapper._zope_browser

    def __getitem__(self, form_id):
        form = self._browser.getForm(id=form_id)
        return FormWrapper(self._browser, form, self._browser_wrapper)

    def get(self, key):
        if isinstance(key, str) and key.startswith('form-'):
            index = int(key.split('-', 1)[1])
            form = self._browser.getForm(index=index)
        else:
            form = self._browser.getForm(id=key)
        return FormWrapper(self._browser, form, self._browser_wrapper)


class _ExpectHTTPError:

    def __init__(self, codes):
        self._codes = codes

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is None:
            raise AssertionError(
                f'Expected HTTP error {self._codes} but no exception was raised')
        if exc_type is urllib.error.HTTPError:
            if exc_val.code in self._codes:
                return True
            raise AssertionError(
                f'Expected HTTP error {self._codes}, got {exc_val.code}')
        try:
            from webtest.app import AppError
            if issubclass(exc_type, AppError):
                match = re.search(r'\b(\d{3})\b', str(exc_val))
                code = int(match.group(1)) if match else 0
                if code in self._codes:
                    return True
                raise AssertionError(
                    f'Expected HTTP error {self._codes}, got {code}: {exc_val}')
        except ImportError:
            pass
        try:
            from ZODB.POSException import ConnectionStateError
            if issubclass(exc_type, ConnectionStateError):
                return True
        except ImportError:
            pass
        try:
            from zExceptions import HTTPException
            if issubclass(exc_type, HTTPException):
                code = getattr(exc_val, 'status', None)
                if code is not None and int(code) in self._codes:
                    return True
                raise AssertionError(
                    f'Expected HTTP error {self._codes}, got {code}: {exc_val}')
        except ImportError:
            pass
        return False


class Browser:

    def __init__(self, app):
        self._zope_browser = z2.Browser(app)
        self._zope_browser.handleErrors = False
        self._tree = None
        self._auth_username = None

    def login(self, user=None):
        if user is None:
            username = TEST_USER_NAME
            password = TEST_USER_PASSWORD
            # getUserName() for the test user returns TEST_USER_NAME
            self._auth_username = TEST_USER_NAME
        else:
            username = user.getId()
            password = 'secret123'
            # For plone.api-created users, getUserName() == getId()
            self._auth_username = username
        credentials = base64.b64encode(
            f'{username}:{password}'.encode()).decode()
        self._zope_browser.addHeader('Authorization', f'Basic {credentials}')
        return self

    def _get_authenticator_token(self):
        if self._auth_username is None:
            return None
        try:
            from hashlib import sha1 as sha
            from plone.protect.authenticator import _getKeyring
            from plone.keyring.interfaces import IKeyManager
            from zope.component import getUtility
            import hmac as _hmac

            manager = getUtility(IKeyManager)
            ring = _getKeyring(self._auth_username, manager=manager)
            secret = ring.random()
            return _hmac.new(
                secret.encode('utf-8'),
                self._auth_username.encode('utf-8'),
                sha,
            ).hexdigest()
        except Exception:
            return None

    def open(self, obj_or_url, view=None, data=None):
        if isinstance(obj_or_url, str):
            url = obj_or_url
        else:
            url = obj_or_url.absolute_url()
        if view:
            url = f'{url}/{view}'
        if data is not None:
            post_data = dict(data)
            if '_authenticator' not in post_data:
                token = self._get_authenticator_token()
                if token:
                    post_data['_authenticator'] = token
            encoded = urllib.parse.urlencode(post_data, doseq=True)
            self._zope_browser.post(url, encoded)
        else:
            self._zope_browser.open(url)
        self._parse_response()
        return self

    def visit(self, obj=None):
        if obj is None:
            self._zope_browser.open(
                self._zope_browser.getLink('').url
                if False else 'http://nohost/plone')
        else:
            self._zope_browser.open(obj.absolute_url())
        self._parse_response()
        return self

    def _parse_response(self):
        contents = self._zope_browser.contents
        if isinstance(contents, bytes):
            contents = contents.decode('utf-8', errors='replace')
        self._tree = lxml.html.fromstring(contents)

    def css(self, selector):
        if self._tree is None:
            return NodeList([])
        try:
            return NodeList(self._tree.cssselect(selector))
        except Exception:
            return NodeList([])

    def fill(self, fields):
        return FormFiller(self._zope_browser, fields, browser_wrapper=self)

    @property
    def forms(self):
        return FormCollection(self)

    def find(self, text):
        try:
            ctrl = self._zope_browser.getControl(text)
            return _ControlProxy(ctrl, self._zope_browser)
        except Exception:
            pass
        try:
            ctrl = self._zope_browser.getControl(name=text)
            return _ControlProxy(ctrl, self._zope_browser)
        except Exception:
            pass
        if self._tree is not None:
            for el in self._tree.iter():
                content = (el.text or '').strip()
                if content == text:
                    return Node(el)
        return None

    def expect_unauthorized(self):
        return _ExpectHTTPError([401, 403])

    def expect_http_error(self, reason=None):
        codes = list(range(400, 600))
        return _ExpectHTTPError(codes)


class _ControlProxy:

    def __init__(self, control, zope_browser):
        self._control = control
        self._browser = zope_browser

    @property
    def value(self):
        return self._control.value

    @value.setter
    def value(self, v):
        self._control.value = v

    def click(self):
        self._control.click()


def assert_message(text):
    browser = get_current_browser()
    contents = browser._zope_browser.contents
    if isinstance(contents, bytes):
        contents = contents.decode('utf-8', errors='replace')
    tree = lxml.html.fromstring(contents)
    messages = [
        el.text_content().strip()
        for el in tree.cssselect('dl.portalMessage dd, .portalMessage dd, .alert')
    ]
    assert any(text in m for m in messages), (
        f'Status message {text!r} not found. Found: {messages}')
