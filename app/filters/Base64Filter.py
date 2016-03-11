import base64
import logging
import os

import cssutils

from app import app
from app.filters.BaseFilter import BaseFilter
from app.helpers import get_mime_type, get_extension_from_filename


class Base64Filter(BaseFilter):
    # determines, how large a file can be to still get encoded in base64
    BASE64_MAX_SIZE = 48 * 1000  # in bytes

    def __init__(self):
        super().__init__()

        self.input_extensions = ["css", "sass", "scss"]
        self.enforce = True

        self.base64_filepath = ""  # this is needed as temporary variable for process_url(), see below

        # disable cssutils warnings
        cssutils.log.setLevel(logging.CRITICAL)

    def apply(self, file_contents, filename):
        # print("[Base64] Filtering %s\n" % filename)

        sheet = cssutils.parseString(file_contents, "utf-8")  # or ascii
        self.base64_filepath = os.path.dirname(os.path.abspath(filename))  # TODO?
        cssutils.replaceUrls(sheet, self.process_url)
        return sheet.cssText.decode("utf-8")

    def process_url(self, url):
        # only use dirname as base64_filepath
        # we don't want to apply base64 twice
        if url.startswith("data:"):
            return url

        # remove eventual query strings from url
        loc_url = url

        if "?" in url:
            loc_url = loc_url[:loc_url.find("?")]

        # this could be a valid CDN url
        if loc_url[:2] == "//":
            return loc_url

        # try to locate file in the current url tag
        location = os.path.normpath("%s%s%s" % (self.base64_filepath, os.path.sep, loc_url))

        if not os.path.exists(location):
            # raise FileNotFoundError("Can't find %s" % location)
            if app.VERBOSE:
                print("[Warning] Can't find %s for Base64Filter" % location)
            return url

        # check file size
        location_size = os.stat(location).st_size
        if location_size > self.BASE64_MAX_SIZE:
            if app.VERBOSE:
                print("[Info] Skipping %s because it is larger than BASE64_MAX_SIZE (%d vs %d" % (
                    location, location_size, self.BASE64_MAX_SIZE))
            return url

        # do the encoding and return as encoded string
        handle = open(location, "rb")
        data = handle.read()
        handle.close()

        base64_encoded = base64.b64encode(data)
        mime_type = get_mime_type(get_extension_from_filename(location))
        # print("Habe aus " + url + " " + base64_encoded.decode("utf-8") + " gemacht!")
        return "data:%s;base64,%s" % (mime_type, base64_encoded.decode("utf-8"))
