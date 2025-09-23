import asyncio, aiohttp
from urllib.parse import urlparse
import sys

from vocab_management import *

##### IMP: How to use MODE and DPV_VERSION #####
# When testing whether urls resolve correctly, we want to check:
# 1) default purl resolves to w3id version i.e. 2.1 (-P flag)
# 2) versioned urls resolve to latest version i.e. 2.2 (-L flag)
# 3) dev urls resolve to dev server i.e. 2.3-dev on dpvcg.org (-D flag)
# When the w3id and latest version urls are different (1 and 2 above)
# The _DPV_VERSION_override in __init__ should be set to the latest
# version (the trailing slash is important to keep).
# The _DPV_VERSION_w3id param specifies which version is set as the 
# latest version / default version in the w3id config.
##### END #####

MODE = None
URL_BASE = None
URLS = []
_DPV_VERSION_override = None
_DPV_VERSION_w3id = '2.2'


def clean_path(path: str) -> str:
    """remove unwanted elements from the path 
    as these are relevant for the RDF files and we want urls"""
    path = path.replace('../', '').replace(f'{DPV_VERSION}/', _DPV_VERSION_override)
    path = '/'.join(path.split('/')[:-1])
    return path


def init_URLS():
    """populate the URLS list from vocab_management metadata"""
    for vocab, data in RDF_VOCABS.items():
        path = clean_path(data['vocab'])
        if vocab != "dpv":  # dpv has special url with no vocab suffix
            URLS.append(f'{URL_BASE["purl"]}{path}')
        elif MODE == "live": # only relevant when testing w3id
            URLS.append(f'{URL_BASE["purl"]}')


def get_expected_url(original_url):
    """for a given url, what should it get resolved to"""
    expected_url = original_url.replace(URL_BASE['purl'], URL_BASE['live'])
    if original_url == f"{URL_BASE['purl']}":
        return f"{URL_BASE['live']}{_DPV_VERSION_w3id}/dpv/"
    return expected_url


async def resolve_url(session, url, timeout=10, max_redirects=15):
    """resolve given url and note its final url and status code"""
    try:
        timeout_obj = aiohttp.ClientTimeout(total=timeout)
        
        async with session.get(
            url,
            timeout=timeout_obj,
            allow_redirects=True,
            max_redirects=max_redirects,
        ) as response:
            final_url = str(response.url)
            status_code = response.status            
            return final_url, status_code, None
            
    # except aiohttp.TooManyRedirects:
    #     return None, None, "Too many redirects"
    # except asyncio.TimeoutError:
    #     return None, None, "Request timeout"
    # except aiohttp.ClientConnectionError:
    #     return None, None, "Connection error"
    # except aiohttp.ClientError as e:
    #     return None, None, f"Client error: {str(e)}"
    except Exception as e:
        return None, None, f"Unexpected error: {str(e)}"

def compare_urls(resolved_url, expected_url):
    """check if resolved url is the expected url"""
    if resolved_url is None or expected_url is None:
        return "FAIL"
    
    def normalize_url(url):
        if not url:
            return ""
        normalized = url.lower().rstrip('/')
        return normalized
    
    if normalize_url(resolved_url) == normalize_url(expected_url):
        return "PASS"

    return "FAIL"


async def process_url(session, url):
    expected_url = get_expected_url(url)
    resolved_url, status_code, error = await resolve_url(session, url)
    if status_code != 200:
        result = "FAIL" # includes 404 when vocab doesn't exist
    else:
        result = compare_urls(resolved_url, expected_url)
    
    return {
        'original_url': url,
        'expected_url': expected_url,
        'resolved_url': resolved_url,
        'status_code': status_code,
        'error': error,
        'result': result
    }


async def process_all_urls():
    connector = aiohttp.TCPConnector()
    async with aiohttp.ClientSession(connector=connector) as session:
        tasks = [process_url(session, url) for url in URLS]
        results = await asyncio.gather(*tasks, return_exceptions=True)
        processed_results = []
        for _, result in enumerate(results):
            # if isinstance(result, Exception):
            #     processed_results.append({
            #         'original_url': URLS[i],
            #         'expected_url': get_expected_url(URLS[i]),
            #         'resolved_url': None,
            #         'status_code': None,
            #         'error': f"error: {str(result)}",
            #         'result': 'FAIL'
            #     })
            # else:
            processed_results.append(result)
        return processed_results


def print_results(results):
    print("URL Validation Report")
    print("=" * 120)
    print(f"{'Original URL':<50} {'Status':<5} {'Resolved URL':<50} {'Result':<5}")
    print("-" * 120)
    
    for result in results:
        url = result['original_url']
        resolved_url = result['resolved_url']
        status_code = result['status_code']
        error = result['error']
        test_result = result['result']
        expected_url = result['expected_url']
        
        status_display = str(status_code) if status_code else "ERROR"
        
        print(f"{url:<50} {status_display:<5} {resolved_url or 'N/A':<50} {test_result:<5}")
        
        if error:
            print(f"{'Error:':<40} {error}")
        
        if test_result == "FAIL" and resolved_url:
            print(f"{'Expected:':<50} {expected_url}")
            print(f"{'Actual:':<50} {resolved_url}")
        
        if error or (test_result == "FAIL" and resolved_url):
            print()
    
    print("-" * 120)
    
    total = len(results)
    passed = sum(1 for r in results if r['result'] == 'PASS')
    failed = total - passed
    print(f"Summary: {passed}/{total} passed, {failed}/{total} failed")


async def main():
    init_URLS()
    print(f"Validating {len(URLS)} URLs...")
    results = await process_all_urls()
    print_results(results)


if __name__ == "__main__":
    try:
        import aiohttp
    except ImportError:
        print("Error: aiohttp package is required for async functionality.")
        print("Install it using: pip install aiohttp")
        sys.exit(1)

    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('-L', '--live', default=False, action='store_true', help="check purl urls for latest version")
    parser.add_argument('-D', '--dev', default=False, action='store_true', help="check dev urls on dpvcg.org")
    parser.add_argument('-P', '--purl', default=False, action='store_true', help="check purl urls for w3id version")
    args = parser.parse_args()

    if args.live:
        MODE = "live"
        _DPV_VERSION_override = '2.2/'
        URL_BASE = {
            'live': 'https://w3c.github.io/dpv/',
            'purl': 'https://w3id.org/dpv/',
        }
    elif args.dev:
        MODE = "dev"
        _DPV_VERSION_override = ''
        URL_BASE = {
            'live': f'https://dev.dpvcg.org/{DPV_VERSION}/',
            'purl': f'https://dev.dpvcg.org/{DPV_VERSION}/',
        }
    elif args.purl:
        MODE = "purl"
        # _DPV_VERSION_override = f'{_DPV_VERSION_w3id}/'
        _DPV_VERSION_override = ''
        URL_BASE = {
            'live': f'https://w3c.github.io/dpv/{_DPV_VERSION_w3id}/',
            'purl': 'https://w3id.org/dpv/',
        }
    else:
        raise ValueError('You must choose one of the modes')
        import sys
        sys.exit(-1)
    
    asyncio.run(main())
