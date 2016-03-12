import codecs
import os

from tqdm import tqdm

from app.definitions import Definitions
from app.filters.Base64Filter import Base64Filter
from app.filters.BaseFilter import BaseFilter
from app.filters.CleanCssFilter import CleanCssFilter
from app.filters.CleanSourceMapFilter import CleanSourceMapFilter
from app.filters.SassFilter import SassFilter
from app.filters.UglifyJsFilter import UglifyJsFilter
from app.helpers import get_header, get_extension_from_filename

# print additional information on screen if enabled
VERBOSE = False


def get_filters_for_file(filename):
    # TODO read from config file or cmd arguments which filters are enabled
    # the order of the filters is very important here
    available_filters = [SassFilter(), Base64Filter(), CleanCssFilter(), UglifyJsFilter(), CleanSourceMapFilter()]
    filters = []
    ext = get_extension_from_filename(filename)

    for f in available_filters:
        if ext in f.input_extensions:
            filters.append(f)

    return filters


def run(def_file, output_dir, working_dir, debug=False, filter_file=None):
    """
    run the process
    :param def_file: filename of the definition file
    :param output_dir: this is where the processed files will be put
    :param working_dir: this path is used when looking for asset files
    :param debug: when debug is enabled, minification is disabled
    :param filter_file: if given only process bundles that include this file
    """
    definitions = Definitions()
    definitions.load_from_file(def_file, working_dir)

    # cache files after filtering
    cache = {}

    for name in tqdm(definitions, mininterval=0, miniters=0):
        bundle = definitions[name]
        filtered = {}

        files = definitions.get_dependencies_files(bundle["dependencies"]) + bundle["files"]
        
        # if filter_file is not included, skip this bundle
        if filter_file is not None and filter_file not in files:
            continue

        # apply filters
        for filename in files:
            filters = get_filters_for_file(filename)
            output_extension = BaseFilter.get_output_extension(filename)

            if output_extension not in filtered:
                filtered[output_extension] = ""

            if filename not in cache:
                if VERBOSE:
                    print("Applying filters %s for %s, detected output extension: %s" % (
                        filters, filename, output_extension))

                with open(filename, "rb") as file_handle:
                    tmp = file_handle.read()

                for f in filters:
                    # only apply filter if not in debug mode and not is minified already
                    # or this filter should be enforced (like with scss for instance)
                    if (not debug and not filename.endswith("min." + output_extension)) or f.enforce:
                        tmp = f.apply(tmp, filename).encode("utf8")

                cache[filename] = tmp.decode("utf8")
                filtered[output_extension] += tmp.decode("utf8")
            else:
                filtered[output_extension] += cache[filename]

        # bundles flagged as internal will not be written to a file
        if not bundle["is_internal"]:
            for ext in filtered:
                output_file = os.path.normpath(output_dir + "/" + name + "." + ext)

                # create directories if necessary
                dirname = os.path.dirname(os.path.abspath(output_file))
                if not os.path.exists(dirname):
                    os.makedirs(dirname)

                header = get_header()
                with codecs.open(output_file, "w", "utf-8") as file_handle:
                    file_handle.write(header + "\n" + filtered[ext])
