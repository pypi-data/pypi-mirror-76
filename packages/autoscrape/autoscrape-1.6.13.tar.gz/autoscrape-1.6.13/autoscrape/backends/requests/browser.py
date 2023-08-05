# -*- coding: UTF-8 -*-
import logging
import re
import time

import requests
from autoscrape.backends.base.browser import BrowserBase
from autoscrape.backends.requests.tags import Tagger
from autoscrape.search.graph import Graph


logger = logging.getLogger('AUTOSCRAPE')


class RequestsBrowser(BrowserBase, Tagger):
    """
    A simple HTTP-requests based scraper, currently capable of only
    doing crawls and very basic HTTP Post requests, but is between
    2x and 5x faster.

        bxroberts.org full crawl - requests backend
        real    0m34.066s
        user    0m23.062s
        sys     0m0.640s

        bxroberts.org full crawl - selenium backend
        real    2m5.373s
        user    1m0.872s
        sys     0m10.976s
    """

    def __init__(self, leave_host=False, **kwargs):
        # requests Session
        self.s = requests.Session()
        self.s.headers.update({
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:35.0)"
                "Gecko/20100101 Firefox/35.0"
            )
        })

        # set of clicked elements
        self.visited = set()

        # queue of the path that led us to the current page
        # this is in the form of (command, *args, **kwargs)
        self.path = []

        # tree building
        self.graph = Graph()

        # setting to False, ensures crawl will stay on same host
        self.leave_host = leave_host

        self.current_url = None
        self.current_html = None

    def _no_endslash_url(self, url):
        # remove trailing slash
        url_noslash = re.sub(r"/$", "", url)
        # and trailing slash before query params
        return re.sub(r"/&", "&", url_noslash)

    def _check_and_set_visited(self, url):
        """
        Take a URL and see if we've visited it (or a slash-ending
        variation) if we haven't this sets the URL to the
        visited set. Returns True if we've visited False if not.
        """
        url_no_endslash = self._no_endslash_url(url)
        if url_no_endslash in self.visited or url in self.visited:
            return True
        self.visited.add(url)
        self.visited.add(url_no_endslash)
        return False

    def click(self, tag, **kwargs):
        element = self.element_by_tag(tag)
        text = self.element_text(element)
        url = None
        tag_name = self.element_tag_name(element)
        logger.debug(" - tag name: %s Text: %s" % (tag_name, text))
        if tag_name == "a":
            raw_href = self.element_attr(element, "href")
            if not raw_href:
                logger.debug("[!] No HREF, skipping link...")
                return False

            url = self._normalize_url(raw_href)
            if self._check_and_set_visited(url):
                logger.debug("[!] Already visited URL %s" % (url))
                return False

            logger.info("[+] Clicking link: %s" % url)
            if not self.fetch(url):
                logger.debug("[!] Fetch failed on %s" % (url))
                return False
        elif tag_name == "input":
            element_type = element.type
            if element_type == "submit":
                parent_form = element.xpath(".//ancestor::form")[0]
                parent_form_tag = self.tag_from_element(parent_form)
                self.submit(parent_form_tag, add_node=False)
                url = self.current_url
                if self._check_and_set_visited(url):
                    return False

        elif tag_name == "iframe":
            raw_href = self.element_attr(element, "src")
            if not raw_href:
                return False

            url = self._normalize_url(raw_href)
            if self._check_and_set_visited(url):
                return False

            logger.info("[+] Fetching iframe: %s" % url)
            if not self.fetch(url):
                return False
        else:
            raise NotImplementedError(
                "click not implemented for element: %s" % (tag_name)
            )

        self.path.append((
            "click", [tag], {"url": url}
        ))
        node = "Click\n text: %s\n URL: %s" % (text, url)
        node_meta = {
            "click": tag,
            "click_text": text,
            "click_iterating_form": None,
        }
        self.graph.add_node(
            node,
            **node_meta
        )
        self.graph.move_to_node(node)
        return True

    def fetch(self, url, initial=False):
        """
        Fetch a page from a given URL (entry point, typically). Most of
        the time we just want to click a link or submit a form using
        webdriver.
        """
        logger.info("%s Fetching url=%s initial=%s" % (
            ("[+]" if initial else " -"), url, initial,
        ))
        retries = 3
        success = True
        while True:
            try:
                response = self.s.get(url)
                break
            except requests.exceptions.ConnectionError as e:
                logger.error(" ! Connection error retrying...")
                logger.error(e)
                if not retries:
                    logger.error(" ! Connection error, skipping URL...")
                    return False
                time.sleep(30)
            retries -= 1

        if not response.text:
            logger.error(" ! Blank response. Skipping URL...")
            return False

        # Requests' encoding detection is faulty. The following
        # block will fix most issues
        if response.encoding and "utf" not in response.encoding.lower():
            response.encoding = response.apparent_encoding
        self.current_html = response.text
        # this check fixes improper decoding of UTF byte order mark
        if self.current_html[:3] == "ï»¿":
            self.current_html = self.current_html.encode(
                response.encoding
            ).decode("utf-8-sig")

        self.current_url = response.url
        self.dom = self._get_dom()

        if initial:
            self.path.append(("fetch", [url], {"initial": initial}))
            node = "Fetch\n url: %s" % url
            self.graph.add_root_node(node, url=url, action="fetch")

        return True

    def back(self):
        logger.info("[+] Going back...")
        logger.debug(" - current path-length=%s path=%s" % (
            len(self.path), self._no_tags(self.path),
        ))
        # We're now where we started from
        self.path.pop()
        if not self.path:
            self.path = []
            return

        prev = self.path[-1]
        if prev[0] == "fetch":
            self.graph.move_to_parent()
            self.fetch(prev[1][0])

        elif prev[0] == "click":
            self.graph.move_to_parent()
            self.fetch(prev[2]["url"])

    @property
    def page_html(self):
        return self.current_html

    @property
    def page_url(self):
        return self.current_url

    def get_clickable(self, **kwargs):
        logger.debug(" - Getting clickable...")
        self.dom = self._get_dom()
        tagger = Tagger(
            current_html=self.current_html,
            current_url=self.current_url,
            leave_host=self.leave_host,
        )
        clickable = tagger.get_clickable()
        return clickable

    # def download_file(self, url):
    #     response = self.s.get(url)
    #     action = {
    #         "action": "download_page",
    #         "url": url,
    #     }
    #     self.graph.add_action_to_current(action)
    #     return response.text

    def input(self, tag, input):
        """
        Enter some input into an element by a given tag.
        """
        logger.info("[+] Injecting text \"%s\" to input" % (input))
        elem = self.element_by_tag(tag)

        input_name = self.element_name(elem)
        value = self.element_value(elem)
        logger.debug("Input name=%s value=%s" % (input_name, value))

        elem.attrib["value"] = input

        self.path.append(("input", ("", input,), {}))
        action = {
            "action": "input",
            "text": input,
            "tag": tag,
        }
        self.graph.add_action_to_current(action)

    def submit(self, tag, add_node=True):
        """
        Submit a form, by extracting the method and url, then
        constructing the params and sending the request, along
        with the form data.
        """
        form = self.element_by_tag(tag)
        inputs = self.elements_by_path("//input", from_element=form)

        data = {}
        for input in inputs:
            # TODO: handle non-text type inputs
            name = self.element_name(input)
            if not name:
                continue
            value = self.element_value(input)
            data[name] = value

        action = self.element_attr(form, "action", default=self.current_url)
        method = self.element_attr(form, "method", default="get")
        url = self._normalize_url(action)

        request_kwargs = {}
        if method.lower() == "post":
            request_kwargs["data"] = data
        elif method.lower() == "get":
            params = []
            for key in data.keys():
                params.append([key, data.get(key, "")])
            request_kwargs["params"] = params

        request = requests.Request(
            method,
            url,
            **request_kwargs
        )
        prepped = request.prepare()
        response = self.s.send(prepped)
        self.current_url = response.url
        self.current_html = response.text
        self.dom = self._get_dom()

        # TODO: all higher level stuff
        if add_node:
            self.path.append(("submit", (tag,), {}))
            node = "Submit\n tag: %s" % (tag)
            node_meta = {
                "submit": tag,
            }
            self.graph.add_node(node, **node_meta)
            self.graph.move_to_node(node)

    def get_screenshot(self):
        return None
