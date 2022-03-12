# pubdbserve: standalone lifeboat PubDB document server

pubdbserve is a python ASGI-based web service that serves files from Kitware's old MIDAS-based publication database for the Surgical Planning Lab at Brigham and Women's Hospital.

This server is a legacy hack to get existing document assets back on line and accessible. It should not be used for any new functionality.

The service is designed to be run either directly:

 `python pubdbserve <port>`

 or from an ASGI framework:

 `uvicorn pubdbserve:app --reload`

 Config file: `./etc/config.env`
 
 Or use environment variables:

 * `ASSETSTORE_DIR`: path to the root of the assetstore where the documents are held (default: `./assetstore`)
 * `PUBDB_DB`: path to the sqlite database that contains information about the assetstore documents (default: `./etc/pubdb-tables.sqlite`)
 * `URL_BASE`: base path of the document urls. The `bitstream_id` of the document will be concatenated onto this path.

Note that if the server is being used behing a proxy server, the proxy will have a root path configuration variable for this service. THe proxy will strip out the root path (for example, `"/publications/bitstream/download"`) before handing the URL off to this service. In this case, the `URL_BASE` is likely to be `/`.

pubdbserve is written in python and depends on the `sqlite_utils` and `starlette` packages. It should run on python 3.6 or so and up. See requirements.txt.
