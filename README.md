# text2img_webapp
A web application of a text2img model.

## For local (with cpu) environment
Need to set the environment variable `GCP_KEY_PATH` that has enough authority on your local machine.  
Note that it takes dozens of minutes to generate images using cpu (model parameters should be changed to reduce the computation time).

```sh
docker compose up --build
```

Then access `http://localhost:8501`.

## For GCP (with gpu) environment
Need to set the google cloud credential json file as `google_cloud_credential_file` that has enough authority.  
Note that it takes several minutes for backend server to be ready (because of model download and load).

```sh
terraform plan
terraform apply
terraform destory
```

Then access the URL shown as `cloud_run_url` on CLI.

## Screenshot
<p align="center">
  <img src="https://imgur.com/TbUlZMQ.png">
</p>

## Copyright of pretrained models
Pretrained models are originally from glide-text2im repository.  
Copyright (c) 2021 OpenAI  
Released under the MIT license: https://github.com/openai/glide-text2im/blob/69b530740eb6cef69442d6180579ef5ba9ef063e/LICENSE
