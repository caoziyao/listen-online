
def get_doubanfmUrl():
    """
    豆瓣FM URL
    """
    ls = [306878, 7925757,  287050, 450370, 9714644, 260086, 1298891, 287050, 6595891, 485660, 5521949]
    urls = []
    for l in ls:
        url = 'https://douban.fm/j/v2/songlist/{}/?kbps=192'.format(l)
        urls.append(url)

    return urls

if __name__ == '__main__':
    urls = get_doubanfmUrl()
    print(urls)