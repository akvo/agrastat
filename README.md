# AGRASAT

Test Site: https://agrastat.akvotest.org

## Prerequisite
To run AGRASAT, ensure that the following dependencies are installed on your system:

- Docker > v19
- Docker Compose > v2.1

These tools will allow you to run the application within isolated containers, ensuring a consistent development and production environment.

## Documentations

- User Guide: https://agrastat.readthedocs.io/en/latest/user-guide.html
- SysAdmin Guide: https://agrastat.readthedocs.io/en/latest/sysadmin-guide.html
- API Guide: https://agrastat.readthedocs.io/en/latest/api/index.html

## Development
<details>
<summary>Environment Setup</summary>

To configure your development environment, copy the example environment file and make any necessary modifications to match your setup:

```bash
cp .env.dev.example .env
```

This file contains critical configurations, including database connections, plugins, and other essential environment variables.
</details>
<details>
<summary>Run the Dev Mode</summary>

For the first-time setup, you may need to build the Docker images before running the development environment:

```bash
docker compose -f docker-compose.dev.yml up -d --build
```

This command builds and starts the necessary containers for AGRASTAT, including CKAN-dev, PostgreSQL, Redis, Solr, and other dependencies required for AGRASAT to function in development mode.

</details>
<details>
<summary>List of Running Containers</summary>

Once the application is running, you can check the status of running containers using:

```bash
docker compose -f docker-compose.dev.yml ps
```

```bash
NAME                    IMAGE                              COMMAND                  SERVICE             CREATED             STATUS                 PORTS
agrastat-ckan-dev-1     agrastat-ckan-dev                  "/srv/app/start_ckan…"   ckan-dev            3 hours ago         Up 3 hours (healthy)   0.0.0.0:5000->5000/tcp
agrastat-datapusher-1   ckan/ckan-base-datapusher:0.0.20   "sh -c 'uwsgi --plug…"   datapusher          3 hours ago         Up 3 hours (healthy)   8800/tcp
agrastat-db-1           agrastat-db                        "docker-entrypoint.s…"   db                  3 hours ago         Up 3 hours (healthy)   5432/tcp
agrastat-pgadmin-1      dpage/pgadmin4:5.7                 "/entrypoint.sh"         pgadmin             3 hours ago         Up 3 hours             80/tcp, 443/tcp, 0.0.0.0:5050->5050/tcp, :::5050->5050/tcp
agrastat-redis-1        redis:6                            "docker-entrypoint.s…"   redis               3 hours ago         Up 3 hours (healthy)   6379/tcp
agrastat-solr-1         ckan/ckan-solr:2.9-solr8           "docker-entrypoint.s…"   solr                3 hours ago         Up 3 hours (healthy)   0.0.0.0:8983->8983/tcp, :::8983->8983/tcp
```

</details>
<details>
<summary>Logs</summary>

To view real-time logs of a specific container, use the following command:

```bash
docker compose -f docker-compose.dev.yml logs --follow <container_name>
```

This is useful for debugging and monitoring the application during development. Example:

```bash
docker compose -f docker-compose.dev.yml logs --follow ckan-dev
```

</details>
<details>
<summary>Command Line Interface</summary>

To interact with the AGRASTAT application via the command line, you can execute CKAN commands inside the running container:

```bash
docker compose -f docker-compose.dev.yml exec ckan-dev ckan
```

This will provide access to various commands, such as:

```bash
Usage: ckan [OPTIONS] COMMAND [ARGS]...

Options:
  -c, --config CONFIG  Config file to use (default: ckan.ini)
  -h, --help           Show this message and exit.

Commands:
  asset            WebAssets commands.
  clean            Provide commands to clean entities from the database
  config-tool      Tool for editing options in a CKAN config file.
  dataset          Manage datasets
  db               Database management commands.
  front-end-build  Creates and minifies css and JavaScript files.
  generate         Scaffolding for regular development tasks.
  jobs             Manage background jobs.
  less             Compile all root less documents into their CSS counterparts
  minify
  notify           Send out modification notifications.
  plugin-info      Provide info on installed plugins.
  profile          Code speed profiler.
  run              Start development server
  search-index     Search index commands
  seed             Create test data in the database.
  sysadmin         Gives sysadmin rights to a named user.
  tracking         Update tracking statistics
  translation      Translation management
  user             Manage user commands
  views            Manage resource views.

Plugins:
  agra
  kobo

Entry points:
  datapusher  Perform commands in the datapusher.
  datastore  Perform commands to set up the datastore.
```
</details>

## Production

<details>
<summary>Start the App</summary>
For production deployment, first, copy the example environment file and adjust it according to your needs:

```bash
cp .env.example .env
```

Then, build and start the application:

```bash
docker compose up -d --build
```

This will start the application in detached mode, ensuring it runs in the background without blocking the terminal.
</details>
<details>
<summary>Restart the App</summary>

If you need to restart the application after making changes or updates, use the following command:

```bash
docker compose restart
```
This command will gracefully restart all running services while maintaining their configurations.
</details>

Copying and License
-------------------

AGRASAT is open-source software, licensed under the GNU Affero General Public License (AGPL) v3.0. The full license text can be found at:

[AGPL v3.0 License](http://www.fsf.org/licensing/licenses/agpl-3.0.html)

By using this software, you agree to the terms outlined in the AGPL, which ensures that modifications and improvements to the code remain open and accessible to the community.
