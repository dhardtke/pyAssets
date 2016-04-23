# pyAssets
[![Build Status](https://travis-ci.org/dhardtke/pyAssets.svg?branch=master)](https://travis-ci.org/dhardtke/pyAssets)

Another asset managing tool, designed to be flexible yet easy

Running pyEncode
=========
You can run pyAssets using its run.py script:
```
C:\pyAssets>.\run.py --help
usage: run.py [-h] [--working-dir WORKING_DIR] [--debug] [--verbose]
              [--filter FILTER] [--filters-enabled FILTERS_ENABLED]
              def_file output_dir
run.py: error: the following arguments are required: def_file, output_dir
```

Sample Asset Definition
=========
Here is an example for an Assets Definition:
```yaml
internals:
  fontawesome:
    files:
      - stylesheets/vendor/font-awesome-custom.min.css

  select2:
    files:
      - bower_components/select2/dist/css/select2.min.css
      - bower_components/select2-bootstrap-theme/dist/select2-bootstrap.min.css

base:
  files:
    - bower_components/jquery/dist/jquery.min.js
    - bower_components/bootstrap-sass/assets/javascripts/bootstrap.min.js
    - bower_components/topbar/topbar.min.js
    - javascripts/base.js
    - stylesheets/base.scss

  dependencies:
    - fontawesome

ucp/overview:
  files:
    - stylesheets/ucp/overview.css

  dependencies:
    - base
```

Each group (except for groups listed under "internal") will be compiled to `GROUPNAME`.`EXT`, where `GROUPNAME` stands for the name of the
group and `EXT` for `js` or `css`.

Sample Call
=========
```
python "C:\pyAssets\run.py" --filters-enabled CleanCssFilter,CleanSourceMapFilter,SassFilter,UglifyJsFilter "C:\assets\assets.yml" "C:\builds"

Process finished with exit code 0
```