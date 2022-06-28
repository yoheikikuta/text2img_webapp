# text2img_webapp
A web application of a text2img model.

## For local (with cpu) environment
Need to set the environment variable `$GCP_KEY_PATH` on your local machine.  
Note that it takes dozens of minutes to generate images using cpu.

```sh
docker compose up --build
```

Then access `http://localhost:8501`.

## For GCP (with gpu) environment
Need to set the google cloud credential json file that has enough authority.  
Note that it takes a few minutes for backend server to be ready.

```sh
terraform plan
terraform apply
terraform destory
```

Then access the URL shown as `cloud_run_url` on CLI.
