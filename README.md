# Neo4j Testing

Trying to explore how to efficiently load and manipulate a GraphDb.

# Where is the Db ?

The DB is running on a Docker which I pulled from the Docker repo with

    docker pull neo4j

I start the docker image like this

```bash
docker run -p 7474:7474 -p 7473:7473 -p 7687:7687 -v "$(pwd)"/data:/data neo4j
```

Then open the base url:


    open http://localhost:7474

Login (password is Neo4j/Neo4j) -> now set the password to being something more secure.
