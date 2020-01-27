import logging
import os
import runpy
import tempfile
import uvicorn

from fastapi import FastAPI
from git import Repo

logger = logging.getLogger(__name__)

app = FastAPI()


@app.post('/pipelines/clone-and-run')
def clone_and_run(git_repo_url: str, pipeline_script_name: str):
    try:
        with tempfile.TemporaryDirectory() as tmp_dir_path:
            logger.info(f'Cloning repository {git_repo_url} to {tmp_dir_path}')
            Repo.clone_from(url=git_repo_url, to_path=tmp_dir_path)

            pipeline_script_path = os.path.join(tmp_dir_path, pipeline_script_name)
            logger.info(f'Using runpy to load Pipeline from pipeline script {pipeline_script_path}')
            context = runpy.run_path(pipeline_script_path)

            pipeline = context['pipeline']

            for step in pipeline.steps:
                step()
    except PermissionError as e:
        error_str = str(e)
        if 'WinError' in error_str and '.git' in error_str:
            logger.warning('Unable to delete temporary git directory in Windows')

    return {}


if __name__ == '__main__':
    # TODO: this is just here for testing, organize it better once the project is more complete
    uvicorn.run('start_server:app', host='127.0.0.1', port=5000, log_level='debug', reload=True)
