
from replay import *

########################################
# network
########################################
def chunk_report(bytes_so_far, chunk_size, total_size):
    percent = float(bytes_so_far) / total_size
    percent = round(percent * 100, 2)
    sys.stdout.write(
        "Downloaded %d of %d bytes (%0.2f%%)\r" %
        (bytes_so_far, total_size, percent))

    if bytes_so_far >= total_size:
        sys.stdout.write('\n')


def chunk_read(response, chunk_size=8192, report_hook=None):
    total_size = response.info().getheader('Content-Length').strip()
    total_size = int(total_size)
    bytes_so_far = 0

    total = ''
    while 1:
        chunk = response.read(chunk_size)
        bytes_so_far += len(chunk)

        if not chunk:
            break
        total += chunk
        if report_hook:
            report_hook(bytes_so_far, chunk_size, total_size)
    return total


"""
python 3.x中urllib库和urilib2库合并成了urllib库。。
其中urllib2.urlopen()变成了urllib.request.urlopen()
       urllib2.Request()变成了urllib.request.Request()
"""
# python2
# data = urllib.urlencode(v) if v else None
# data = urllib.parse.urlencode(v) if v else None
# buf = StringIO.StringIO(result)
logger = logging.getLogger('listenone.' + __name__)
def h(
        url, v=None, progress=False, extra_headers={},
        post_handler=None, return_post=False):
    '''
    base http request
    progress: show progress information
    need_auth: need douban account login
    '''
    logger.debug('fetching url:' + url)
    user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_1) ' + \
                 'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.86' + \
                 ' Safari/537.36'
    headers = {'User-Agent': user_agent}
    headers.update(extra_headers)

    data = urllib.parse.urlencode(v).encode("utf-8") if v else None
    req = urllib.request.Request(url, data, headers)
    # POST data should be bytes or an iterable of bytes. It cannot be of type str
    # req = req.encode('utf-8')
    response = urllib.request.urlopen(req)
    if progress:
        result = chunk_read(response, report_hook=chunk_report)
    else:
        result = response.read()
    # python 3
    # The content is compressed with gzip. You need to decompress it:
    # result = gzip.decompress(result).decode('utf-8')
    # print(result)
    if response.info().get('Content-Encoding') == 'gzip':
        # note
        # buf = io.StringIO(result)
        # f = gzip.GzipFile(fileobj=buf)
        # result = f.read()
        result = gzip.decompress(result).decode('utf-8')
        return result
    if post_handler:
        post_result = post_handler(response, result)
        if return_post:
            return post_result
    return result.decode('utf-8')