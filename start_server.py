import uvicorn

from cinco.app import app

if __name__ == '__main__':
    # TODO: this is just here for testing, organize it better once the project is more complete
    uvicorn.run('start_server:app', host='127.0.0.1', port=5000, log_level='debug', reload=True)
