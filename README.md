# profile_collection
Repository for the RSoXS SST collection environment


To install a new custom package for repid development, clone the package into:
`/nsls2/data/sst/rsoxs/shared/config/bluesky/collection_packages`

Directories will be automatically exposed to the bsui namespace.  

If your package has requirements that are not met by the base environment, it is recommended that they be 
installed in a shared overlay. 
```${BS_PYTHONPATH}```

A specific dependency can similarly be installed from github with, for example:
```bash
pip install git+https://github.com/tacaswell/mpl-qtthread --prefix ${BS_PYTHONPATH%/lib*} --upgrade -I --no-dependencies
```