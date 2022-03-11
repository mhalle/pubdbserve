import sqlite_utils
import os.path

from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseSettings

bitstream_mapping = {}

def format_assetstore_file(dir, internal_id):
    return os.path.join(dir, 
        internal_id[0:2], 
        internal_id[2:4],
        internal_id[4:6],
        internal_id)

class Settings(BaseSettings):
    assetstore_dir: str = 'assetstore'
    pubdb_db: str = ''

    class Config:
        env_file = './etc/config.env'

settings = Settings()

app = FastAPI()

@app.get('/publications/bitstream/download/{bitstream_id}')
async def get_bitstream_file(bitstream_id: str):
    try:
        info = bitstream_mapping[bitstream_id]
    except KeyError:
        raise HTTPException(status_code=404, detail=f"HTTP Error 404: Item {bitstream_id} not found")

    return FileResponse(format_assetstore_file(settings.assetstore_dir, info['hash']), 
                        media_type=info['mimetype'],
                        headers = { 
                            'Content-Disposition': f'inline; filename={info["filename"]}'
                        })

@app.on_event('startup')
def startup_event():
    global bitstream_mapping
    db = sqlite_utils.Database(f'file:{settings.pubdb_db}?mode=ro')
    bitstream_mapping = {x['id']: x for x in (db.query('''select 
            bitstream.bitstream_id as id, 
            bitstream.internal_id as hash,
            bitstream.name as filename,
            bitstreamformatregistry.mimetype as mimetype
        from bitstream join bitstreamformatregistry
        on bitstream.bitstream_format_id = bitstreamformatregistry.bitstream_format_id
        '''
        ))}
