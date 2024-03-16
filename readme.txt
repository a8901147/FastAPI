# development mode:

# build image
docker build -t taskapi .

# use bind mount for development enviroment
docker run -d --name taskapi_dev_container -p 8000:8000 -v $(pwd)/app:/app taskapi
docker run -d --name taskapi_dev_container -p 8000:8000 -v /Users/pegatron/Desktop/Jeremmy/Interview/gogolook:/app taskapi uvicorn main:app --host 0.0.0.0 --reload

# run uni test  
docker exec -it taskapi_dev_container pytest 


docker container stop taskapi_dev_container 
docker container rm taskapi_dev_container
==================================================================================================================================
# production mode 
   - in production mode we shouldn't use bind mount. we should use name volume(persist_data) if we want to keep any data in it.(we don't have any at the moment)
docker run -d --name taskapi_prod_container -p 8000:8000 -v presist_data:/app taskapi

# normal production mode
docker run -d --name taskapi_prod_container -p 8000:8000 taskapi


