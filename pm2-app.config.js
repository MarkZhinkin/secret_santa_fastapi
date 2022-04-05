const path = require('path');
const fs = require('fs');
const dotenv = require('dotenv');


const projectDirectory = process.cwd();

const pathToEnvFile = path.join(projectDirectory, '.env')
dotenv.config({ path: pathToEnvFile });

const domain = process.env.DOMAIN;
if (!domain) {
  console.error('ERROR: domain not found');
  process.exit(1);
}

const projectName = "app_secret_santa_api";

const projectHost = domain.split('//')[1].split(':')[0]
const projectPort = domain.split('//')[1].split(':')[1]

let pythonInterpreter = null;
let uvicornScript = null;
if (process.platform === 'win32') {
    pythonInterpreter = path.join(projectDirectory, '.venv', 'Scripts', 'python.exe');
    uvicornScript = path.join(projectDirectory, '.venv', 'Scripts', 'uvicorn.exe');
} else {
    pythonInterpreter = path.join(projectDirectory, '.venv', 'bin', 'python');
    uvicornScript = path.join(projectDirectory, '.venv', 'bin', 'uvicorn');
}
if (!fs.existsSync(pythonInterpreter)) {
  console.error('ERROR: python(virtualenv) not found');
  process.exit(1);
}
if (!fs.existsSync(uvicornScript)) {
  console.error('ERROR: uvicorn not found');
  process.exit(1);
}

module.exports = {
  apps: [{
      name: projectName,
      script: uvicornScript,
      args: `main:app --host ${projectHost} --port ${projectPort}`,
      interpreter: pythonInterpreter,
      instances: 1,
      autorestart: true,
      max_memory_restart: "1024M",
      max_restarts: 1,
      restart_delay: 5000,
      combine_logs: true,
      merge_logs: true,
      error_file: `${projectName}.log`,
      out_file: `${projectName}.log`
  }]
};
