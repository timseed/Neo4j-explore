from neo4j import GraphDatabase

uri = "bolt://localhost:7687"
driver = GraphDatabase.driver(uri, auth=("neo4j", "ducati"))


def del_all(tx):
    """
    delete the links and the nodes
    """
    tx.run("match(n) "
           "detach delete n ")


def add_people(tx, name, gender, years=21):
    """
    Create a people object with 3 attributes 
    """
    tx.run("CREATE (n:people {name: $value, gender: $gender, age:$years})",
           value=name,
           gender=gender,
           years=years)


def link_people(tx):
    """
    Link two nodes with a relationship.
    """
    tx.run("MATCH (p:people {gender:'M'}), (m:male {gender:'M'}) "
           "create (p)-[r:ARE_MEN]->(m) ")
    tx.run("MATCH (p:people {gender:'F'}), (f:female {gender:'F'}) "
           "create (p)-[r:ARE_WOMEN]->(f) ")


def create_gender(tx):
    tx.run("Create (n:male   {gender:'M'})")
    tx.run("Create (n:female {gender:'F'})")


with driver.session() as session:
    session.read_transaction(del_all)

    session.read_transaction(create_gender)
    session.read_transaction(add_people, "Snow White", "F", 22)
    session.read_transaction(add_people, "Happy", "M", 62)
    session.read_transaction(add_people, "Bashful", "M", 63)
    session.read_transaction(add_people, "Doc", "M", 60)
    session.read_transaction(add_people, "Grumpy", "M")
    session.read_transaction(link_people)


#
#
#


print("""In the Web browser please enter this Cypher statement

match(n)
return n

""")
