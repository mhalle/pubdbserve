from tracemalloc import start
import sqlite_utils
import os.path

from starlette.responses import FileResponse
from starlette.applications import Starlette
from starlette.exceptions import HTTPException
from starlette.routing import Route
from starlette.config import Config

config = Config('./etc/config.env')

settings = {
    'assetstore_dir': config('ASSETSTORE_DIR', default='./assetstore'),
    'pubdb_db': config('PUBDB_DB', default='./etc/pubdb-tables.sqlite'),
    'url_base': config('URL_BASE', default='/')
}

bitstream_mapping = {}

def format_assetstore_file(dir, internal_id):
    return os.path.join(dir, 
        internal_id[0:2], 
        internal_id[2:4],
        internal_id[4:6],
        internal_id)



urlpat = f'{settings["url_base"]}' + '{bitstream_id}'

async def get_bitstream_file(request):
    bitstream_id = request.path_params['bitstream_id']
    try:
        info = bitstream_mapping[bitstream_id]
    except KeyError:
        raise HTTPException(status_code=404, 
            detail=f"HTTP Error 404: Item {bitstream_id} not found")

    return FileResponse(format_assetstore_file(settings['assetstore_dir'], info['hash']), 
                        media_type=info['mimetype'],
                        headers = { 
                            'Content-Disposition': f'inline; filename={info["filename"]}'
                        })

def startup():
    global bitstream_mapping
    db = sqlite_utils.Database(f'file:{settings["pubdb_db"]}?mode=ro')
    bitstream_mapping = {x['id']: x for x in (db.query('''select 
            bitstream.bitstream_id as id, 
            bitstream.internal_id as hash,
            bitstream.name as filename,
            bitstream_format.mimetype as mimetype
        from bitstream join bitstream_format
        on bitstream.bitstream_format_id = bitstream_format.bitstream_format_id
        '''
        ))}

routes = [
    Route(urlpat, get_bitstream_file)
]
app = Starlette(routes=routes, on_startup=[startup])
