from tld import get_tld


def get_shortlink_from_url(link):
    short_link = ""
    if link:
        ext = get_tld(url, as_object=True)
        short_link = ".".join([ext.domain, ext.suffix])
    return short_link


def build_url_variants(url, sections):
    urls = []
    # sections = ['careers', 'about-us', 'about-us/careers', 'about', 'about/careers',
    #             'about/jobs']
    res = get_tld(url, as_object=True)
    parsed_url = res.parsed_url
    for section in sections:
        page_link = "{url.scheme}://{url.netloc}/{section}/".format(url=parsed_url, section=section)
        urls.append(page_link)
    return urls
