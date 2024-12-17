from playwright.sync_api import sync_playwright
from random import randint
from .headers import HEADERS

def get_random_headers():
    try:
        return HEADERS[randint(0, len(HEADERS) - 1)]
    except:
        return {}

# List of ad domains to block
AD_DOMAINS = [
    "ads.example.com",
    "adserver.example.com",
    "track.example.com",
    "offdeck.telkomsel.com",
    # Add more ad domains as needed
]

ALLOWED_DOMAINS = [
    "quotes.toscrape.com"
]

def block_unallowed(route, request):
    """Block unallowed domains"""
    # Check if the request URL matches any allowed domains
    if any(domain in request.url for domain in ALLOWED_DOMAINS):
        route.continue_()  # Allow the request
    else:
        print(f"Blocking request to: {request.url}")
        route.abort()  # Abort the request if it's not allowed the request if no allowed domains match

def block_ads(route, request):
    """Block requests to ad domains."""
    if any(ad_domain in request.url for ad_domain in AD_DOMAINS):
        print(f"Blocking request to: {request.url}")
        route.abort()  # Abort the request
    else:
        route.continue_()  # Continue the request

def extract_full_body_html(from_url : str, wait_for : str =None,) -> str:
    try:
        with sync_playwright() as p:
            # Define Browser object
            browser = p.chromium.launch(headless=False)
            # browser = p.firefox.launch(headless=False)
            # Create a new browser context
            context = browser.new_context()
            # Define Page object
            page = context.new_page()
            # # Intercept requests and block ads
            # page.route("**/*", block_ads)
            # Intercept requests and block unallowed domain
            page.route("**/*", block_unallowed)
            # Set Headers
            headers = get_random_headers()
            print("HEADERS : ", headers)
            if len(headers) != 0:
               page.set_extra_http_headers(get_random_headers())
            # Go to passed argument url
            page.goto(from_url)

            # Wait the pages
            # Wait until the page has no more than 2 active network connections for at least 500 milliseconds.
            page.wait_for_load_state("networkidle")
            # Trigger any lazy-loading or additional content loading that the page might be doing. 
            #   This helps ensure that all parts of the page are loaded for scraping.
            page.evaluate("() => window.scroll(0, document.body.scrollHeight)")
            # Wait until the initial HTML document has been completely loaded and parsed.
            page.wait_for_load_state("domcontentloaded")
            if wait_for:
                # Wait until specific selector appears
                page.wait_for_selector(wait_for)

            # Parsing HTML
            html = page.inner_html('body')

            # Close the browser
            browser.close()

            return html
    except Exception as e:
        print(f"An error occured: {e}")
        return ""
