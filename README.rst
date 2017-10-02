django-url-shortening
================
A custom URL shortening app for Django with API.

Usage
=====
1. Add ``urlshortening`` app to your ``INSTALLED_APPS`` and do ``migrate``

2. Wire up the redirect view by adding to your URLconf
        .. code-block:: python

          ('^linkshortening/', include('urlshortening.urls'))

3. Add settings (more about parameters further)
        .. code-block:: python

            INITIAL_URL_LEN = 6
            RETRY_COUNT = 5
            SHORT_URL_PATH = 'http://example.com/short-prefix/'

4. Now you can use API to make short links
        - ``POST linkshortening/short/``

        With json data ``{"full_url": "http://example.com/a/b/c/d/e"}``

        And get response

        .. code-block:: python

          {"data": {
              "short_id": "123456",
              "short_url_path": "http://example.com/short-prefix/"
           }, "error": ""}

        Possible errors:
        ``{"error": "full_url is empty", "data": ""}, status=400`` if you will send empty ``full_url``


        - ``GET linkshortening/expand/123456``

        And get response ``{"error": "", "data": {"full_url": "http://example.com/a/b/c/d/e"}}``

        Possible errors:
        ``{"error": "Link is expired", "data": ""}, status=404`` if is_expired flag set to true
        ``{"error": "Url doesn\'t exist", "data": ""}, status=404`` if given short_id doesn't exist

5. You could also use ``urlshortening`` right from code
       .. code-block:: python

        from urlshortening.models import get_short_url, invalidate_url, get_full_url

        url = "http://example.com/a/b/c/d/e"
        short_url = get_short_url(url) # Url object
        print(short_url.short_id) # id for short url

        full_url = get_full_url(short_url.short_id) # Url object
        print(full_url.url) # "http://example.com/a/b/c/d/e"

        # You could also invalidate url
        invalidate_url(full_url.short_id)

Settings
========

Available settings are:

``INITIAL_URL_LEN``
    Initial length of short id for url. Once you get more short id's than is possible in all combinations of ``INITIAL_URL_LEN`` symbols it will increase by one

``RETRY_COUNT``
    How many times do we to check before increasing ``INITIAL_URL_LEN``.

``SHORT_URL_PATH``
    Url that will be returned with ``short_id`` on ``POST linkshortening/short/`` request. It might help you to construct full url.
