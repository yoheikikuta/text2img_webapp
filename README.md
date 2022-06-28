# text2img_webapp
A web application of a text2img model.

## For local (with cpu) environment
Need to set the environment variable `$GCP_KEY_PATH` on your local machine.  
Note that it takes dozens of minutes to generate images using cpu.

```sh
docker compose up --build
```

Then access `http://localhost:8501`.
