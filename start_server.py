import logging
import os
import tempfile
import uvicorn

from fastapi import FastAPI
from git import Repo

logger = logging.getLogger(__name__)

app = FastAPI()


@app.post('/clone-and-run-git-repo')
def clone_and_run_git_repo(git_repo_url: str, python_script_name: str):
    try:
        with tempfile.TemporaryDirectory() as tmp_dir_path:
            logger.info(f'Cloning repository {git_repo_url} to {tmp_dir_path}')
            Repo.clone_from(url=git_repo_url, to_path=tmp_dir_path)
            script_path = os.path.join(tmp_dir_path, python_script_name)

            logger.info(f'Reading and executing {script_path}')
            with open(script_path, 'r') as script_file:
                exec(script_file.read())
    except PermissionError as e:
        error_str = str(e)
        if 'WinError' in error_str and '.git' in error_str:
            logger.warning('Unable to delete temporary git directory in Windows')

    return {}


if __name__ == '__main__':
    # TODO: this is just here for testing, organize it better once the project is more complete
    uvicorn.run('start_server:app', host='127.0.0.1', port=5000, log_level='debug', reload=True)
