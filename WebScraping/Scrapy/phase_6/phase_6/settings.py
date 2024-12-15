# Scrapy settings for phase_6 project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://docs.scrapy.org/en/latest/topics/settings.html
#     https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://docs.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = "phase_6"

SPIDER_MODULES = ["phase_6.spiders"]
NEWSPIDER_MODULE = "phase_6.spiders"

FEEDS = { 'booksdata.json': 
            {
                'format': 'json',
                'encoding': 'utf8',
                'store_empty': False,
                'fields': None,
                'indent': 4,
            },
        }

SCRAPEOPS_API_KEY=''
SCRAPEOPS_FAKE_USER_AGENT_ENDPOINT='https://headers.scrapeops.io/v1/user-agents'
SCRAPEOPS_FAKE_USER_AGENT_ENABLED=True
SCRAPEOPS_NUM_RESULTS=50
SCRAPEOPS_FAKE_BROWSER_HEADER_ENDPOINT = 'http://headers.scrapeops.io/v1/browser-headers'
SCRAPEOPS_FAKE_BROWSER_HEADER_ENABLED = True

USER_AGENTS_SETTINGS = ['Opera/7.11 (Windows NT 5.1; U) [en]', 
        'Mozilla/5.0 (Windows NT 6.0; rv:32.0) Gecko/20100101 Firefox/32.0', 
        'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.75 Safari/537.36 Vivaldi/1.0.219.50',]

ROTATING_PROXY_LIST = [
    '20.210.113.32',
    '20.206.106.192',
    '50.207.199.81',
    '68.185.57.66',
    '50.172.75.122',
]

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = "phase_6 (+http://www.yourdomain.com)"

# Obey robots.txt rules
ROBOTSTXT_OBEY = True

# Configure maximum concurrent requests performed by Scrapy (default: 16)
#CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See https://docs.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
#DOWNLOAD_DELAY = 3
# The download delay setting will honor only one of:
#CONCURRENT_REQUESTS_PER_DOMAIN = 16
#CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
#COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
#DEFAULT_REQUEST_HEADERS = {
#    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
#    "Accept-Language": "en",
#}

# Enable or disable spider middlewares
# See https://docs.scrapy.org/en/latest/topics/spider-middleware.html
#SPIDER_MIDDLEWARES = {
#    "phase_6.middlewares.Phase6SpiderMiddleware": 543,
#}

# Enable or disable downloader middlewares
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#DOWNLOADER_MIDDLEWARES = {
#    "phase_6.middlewares.Phase6DownloaderMiddleware": 543,
#}
DOWNLOADER_MIDDLEWARES = {
   "phase_6.middlewares.FakeUserAgentMiddleware": 300,
    # "rotating_proxies.middlewares.RotatingProxyMiddleware": 610,
    # "rotating_proxies.middlewares.BanDetectionMiddleware": 620,
    # "phase_6.middlewares.ScrapeOpsFakeUserAgentMiddleware": 400,
    # "phase_6.middlewares.ScrapeOpsFakeBrowserHeaderAgentMiddleware": 400,
}

# Enable or disable extensions
# See https://docs.scrapy.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    "scrapy.extensions.telnet.TelnetConsole": None,
#}

# Configure item pipelines
# See https://docs.scrapy.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
   "phase_6.pipelines.BookScraperPipeline": 300,
#    "phase_6.pipelines.PostgresDemoPipeline": 400,
}

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/autothrottle.html
#AUTOTHROTTLE_ENABLED = True
# The initial download delay
#AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
#AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
#AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
#AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = "httpcache"
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = "scrapy.extensions.httpcache.FilesystemCacheStorage"

# Set settings whose default value is deprecated to a future-proof value
REQUEST_FINGERPRINTER_IMPLEMENTATION = "2.7"
TWISTED_REACTOR = "twisted.internet.asyncioreactor.AsyncioSelectorReactor"
FEED_EXPORT_ENCODING = "utf-8"
