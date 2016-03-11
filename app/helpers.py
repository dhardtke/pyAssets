def get_mime_type(extension):
    mime_map = {
        "woff": "application/font-woff",
        "woff2": "application/font-woff2",
        "ttf": "application/octet-stream",
        "eot": "application/vnd.ms-fontobject",
        "otf": "application/font-otf",
        "svg": "image/svg+xml",
        "png": "image/png",
        "jpg": "image/jpeg",
        "gif": "image/gif"
    }

    if not extension in mime_map:
        raise Exception("Can't find mime type for " + extension)

    return mime_map[extension]