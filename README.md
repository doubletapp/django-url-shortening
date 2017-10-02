django-url-shortening
=====================
A custom URL shortening app for Django with API.

Usage
=====
1. Add ``urlshortening`` app to your ``INSTALLED_APPS`` and do ``migrate``

2. Wire up the redirect view by adding to your URLconf
    ```
    ('^linkshortening/', include('urlshortening.urls'))
    ```

3. Add settings (more about parameters further)
    ```
    INITIAL_URL_LEN = 6
    RETRY_COUNT = 5
    SHORT_URL_PATH = 'http://example.com/short-prefix/'
    REDIRECT_PREFIX = 'r'
    ```

4. Now you can use API to make short links
    
    ``POST linkshortening/short/``
    
    With json data ``{"full_url": "http://example.com/a/b/c/d/e"}``

    And get response
    ```
    {"data": {
        "short_id": "123456",
        "short_url_path": "http://example.com/short-prefix/"
     }, "error": ""}
    ```

5. You could also use ``urlshortening`` right from code
    ```
    from urlshortening.models import get_short_url, invalidate_url, get_full_url
    ```
    ```
    url = "http://example.com/a/b/c/d/e"
    short_url = get_short_url(url) # Url object
    print(short_url.short_id) # id for short url
    ```
    ```
    full_url = get_full_url(short_url.short_id) # Url object
    print(full_url.url) # "http://example.com/a/b/c/d/e"
    ```
    ```
    # You could also invalidate url
    invalidate_url(full_url.short_id)
    ```


API
===
**Get short link**

- **URL**
    ```
    /short/
    ```

- **Method:** `POST`

- **Data Params**
    - full_url

- **Success Response:**
    - **Code:** 200 <br />
      **Content:** `{ data: { "short_url_path": "000001" }, error: "" }`
 
- **Error Response:**

    - **Code:** 400 <br />
      **Content:** `{ error : "full_url is empty" }`

    - **Code:** 400 <br />
      **Content:** `{ error : "full_url is too long" }`
    
**Get full link**

- **URL**
    ```
    /expand/:short_id/
    ```

- **Method:** `GET`
  
- **URL Params**
    ```
    short_id=[string]
    ```

- **Success Response:**

    - **Code:** 200 <br />
      **Content:** `{ error : "", data: { full_url: "http://example.com/to-000001" }}`
 
- **Error Response:**

    - **Code:** 404 <br />
      **Content:** `{ error : "Link is expired" }`

    - **Code:** 404 <br />
      **Content:** `{ error : "Url doesn\'t exist" }`
    
**Get redirect**

- **URL**
    ```
    /REDIRECT_PREFIX/expand/:short_id/
    ```

- **Method:** `GET`
  
- **URL Params**
    ```
    short_id=[string]
    ```

- **Success Response:**

    - **Code:** 302 <br />
 
- **Error Response:**

    - **Code:** 404 <br />
      **Content:** `{ error : "Link is expired" }`

    - **Code:** 404 <br />
      **Content:** `{ error : "Url doesn\'t exist" }`
    
**Invalidate url**

- **URL**
    ```
    /invalidate/
    ```

- **Method:** `POST`
  
- **Data Params**

    - short_id
  
- **Success Response:**

    - **Code:** 200 <br />
      **Content:** `{ error : "", data: { "short_id": "000001", "invalidated": "true" } }`
 
- **Error Response:**

    - **Code:** 400 <br />
      **Content:** `{ error : "short_id is empty" }`

    - **Code:** 400 <br />
      **Content:** `{ error : "Link is already expired" }`
    
    - **Code:** 404 <br />
      **Content:** `{ error : "Url doesn\'t exist" }`

        
Settings
========

Available settings are:

- ``INITIAL_URL_LEN``
    
    Initial length of short id for url. Once you get more short id's than is possible in all combinations of ``INITIAL_URL_LEN`` symbols it will increase by one

- ``RETRY_COUNT``
    
    How many times do we to check before increasing ``INITIAL_URL_LEN``.

- ``SHORT_URL_PATH``
    
    Url that will be returned with ``short_id`` on ``POST linkshortening/short/`` request. It might help you to construct full url.
    
- ``REDIRECT_PREFIX``

    Select prefix to use redirect links. For example ``REDIRECT_PREFIX="r"`` and we get redirect links with format  ``/r/expand/{short_id}/``
   
