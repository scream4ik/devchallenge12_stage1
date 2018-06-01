# General information
Simple online web service for upload/download large files

Project use next technologies:
* Python 3.6
* Django - web framework
* Twisted - event-driven networking engine
* Celery - asynchronous task queue/job queue
* RabbitMQ - message broker
* PostgreSQL - object-relational database management system
* Docker - container platform

### Directory structure
```
|-- etc
|   |-- docker (docker configs)
|   |-- fixtures (initial data for models)
|   |-- supervisor (supervisor configs)
|   |-- node_requirements.txt (node requirements)
|   |-- requirements.txt (proxy requirements)
|-- node (node server)
|-- proxy (proxy server)
```

### Service architecture
Sending GB's of data in one single HTTP POST is not very reliable. Unless you have a very good internet connection the chances are that such POSTs will time out. Therefore implement the chunked uploads help with this issue. For chunked uploads each chunk is written to a separate file and the application has to then reassemble it.

User send request to upload/download file to `proxy server` and server decides on which `nodes` file will be sync. `Proxy server` have monitoring tool for "ping" `nodes` and get information about there availability and free space. For upload request `proxy server` sync file using `rsync` (maybe for next project version can be used `git-annex`). For download request `proxy server` calculate nearest available server and redirect user.

If we need add new one `node` we can add new container or remote `node` and add information about new `node` at admin panel. `Proxy server` automatically starts using new server.

### Setup
At root of the project run:
```
docker-compose up --build
```
Docker will download needed images and build `proxy` and `node` servers images. Then will be created database scheme, apply migrations and load initial data for models.

Now you can found panel administration located at `http://127.0.0.1:8000/admin/`. 

For login use credentials: user - `admin`, password - `adminadmin`

At `http://127.0.0.1:8000/admin/storage/server/` you can see already added `node` server information (with status and free space which updated all times) and in `docker-compose.yml` appropriate container named `node1`

_Note: user and node data was loaded from fixtures_

Also available API documentation at `http://127.0.0.1:8000/docs/redoc/` (be sure you login at admin panel before open, because you need full permissions)

### Testing
Get JWT token for user
```bash
curl -X POST -d "username=admin&password=adminadmin" http://127.0.0.1:8000/api-token-auth/
```

Response
```json
{"token":"<YOUR_TOKEN>"}
```

PUT request with the chunks of the file
```bash
curl -H "Authorization: JWT <YOUR_TOKEN>" -H "Content-Range: bytes 1-32634/32634" -F file=@some-image.png -F filename=some-image.png -X PUT http://127.0.0.1:8000/storage/tmp-upload/
```

Response
```json
{"id":"<UUID>","url":"http://127.0.0.1:8000/storage/tmp-upload/<UUID>/","file":"http://127.0.0.1:8000/media/chunked_uploads/2018/05/13/<UUID>.part","filename":"some-image.png","offset":32634,"created_at":"2018-05-13T11:54:32.190080Z","status":1,"completed_at":null,"user":1,"parent":null}
```

_If needed repeatedly PUT subsequent chunks to the `url` returned from the server_

_Server will continue responding with the `url`, current `offset` and expiration (`expires`)_

_If you want create file versions you need send parent id too_

Finally, when upload is completed, POST a request to the returned `url`. This request must include the `md5` checksum (hex) of the entire file
```bash
curl -H "Authorization: JWT <YOUR_TOKEN>" -X POST http://127.0.0.1:8000/storage/tmp-upload/<UUID>/
```

_If you want to upload a file as a single chunk, this is also possible! Simply make the first request a POST and include the md5 for the file. You don't need to include the `Content-Range` header if uploading a whole file_

After POST request `proxy server` get available `nodes` by status and free space and sync file using `rsync`

Get list of available files for current user
```bash
curl -H "Authorization: JWT <YOUR_TOKEN>" http://127.0.0.1:8000/storage/files/
```

Response
```json
{"count":1,"next":null,"previous":null,"results":[{"id":"<UUID>","filename":"some-image.png","created_at":"2018-05-13T11:54:32.190080Z","download_url":"http://127.0.0.1:8000/storage/download/<UUID>/","versions":[]}]}
```

For download file use GET request to the returned `download_url`
```bash
curl -L -H "Authorization: JWT <YOUR_TOKEN>" --range 0-29999 -o img.part1 http://127.0.0.1:8000/storage/download/<UUID>/
curl -L -H "Authorization: JWT <YOUR_TOKEN>" --range 30000-32634 -o img.part2 http://127.0.0.1:8000/storage/download/<UUID>/
cat img.part? > img.png
```

When user GET request download file `proxy server` calculate nearest and available server and redirect user for download
