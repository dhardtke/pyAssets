import datetime

from tqdm import tqdm

from app.definitions import Definitions


def get_header():
    now = datetime.datetime.now()
    return "/* Compiled %s */" % (now.strftime("%a %b %d %Y %H:%M:%S"))


def get_dependencies_files(definitions, dependencies):
    files = []

    for name in dependencies:
        dependency = definitions[name]

        if "files" in dependency:
            files.extend(dependency["files"])

        if "dependencies" in dependency:
            files.extend(get_dependencies_files(definitions, dependency["dependencies"]))

    return files


def run(def_file, output_dir, working_dir, debug=False):
    definitions = Definitions()
    definitions.load_from_file(def_file, working_dir)

    # cache files after filtering
    cache = {}

    for name in tqdm(definitions, mininterval=0, miniters=0):
        bundle = definitions[name]

        files = bundle["files"] + get_dependencies_files(definitions, bundle["dependencies"])

        # apply filters
        for f in []:  # TODO filters list
            # only apply filter if not in debug mode or this filter should be enforced (like with scss for instance)
            if not debug or f.enforce:
                # TODO
                # TODO get list of file extensions responsible for
                f.apply()

                # bundles flagged as internal will not be written to a file
                # if not bundle["is_internal"]:
                # output_file = output_dir + os.path.sep + name + "." + group[0]
                # header = get_header()
                # with open(output_file, "w") as f:
                #    f.write(header + "\n" + result)
