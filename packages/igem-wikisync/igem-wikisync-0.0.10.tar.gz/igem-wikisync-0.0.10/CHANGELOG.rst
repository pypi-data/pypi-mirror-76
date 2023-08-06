
Changelog
=========

0.0.10 (2020-08-14)
-------------------
* Check if URL is empty in is_relative()
* File size limit was 1mb instead of 100mb

0.0.9 (2020-08-04)
------------------
* Fix return values

0.0.8 (2020-08-03)
------------------
* Fix assets path error in Windows

0.0.7 (2020-08-03)
------------------
* Fix Python version in setup.py

0.0.6 (2020-08-02)
------------------
* Allow silencing warnings
* Add WikiSync to upload description

0.0.5 (2020-07-30)
------------------

* Check file size before uploading
* Don't change URL if file not found
* Add year configuration option
* Enforce asset paths to start with 'assets/'
* Improve logging and change log and cookie filenames
* Classify logging messages
* Refactor upload_map
* Don't rename files if they already follow iGEM spec
* Check for filename too large
* Print summary after execution

0.0.4 (2020-07-25)
------------------

* Drop jsmin.
* Add version specifiers to dependencies.

0.0.3 (2020-07-25)
------------------

* Ensures that directories exist before writing files.

0.0.2 (2020-07-25)
------------------

* Assets are also written to disk in build_dir.

0.0.1 (2020-07-25)
------------------

* Build directory doesn't get cleared on every run.

0.0.0 (2020-07-25)
------------------

* First release on PyPI.
