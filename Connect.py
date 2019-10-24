from neo4j import GraphDatabase

uri = "bolt://localhost:7687"
driver = GraphDatabase.driver(uri, auth=("neo4j", "ducati"))


def del_all(tx):
    tx.run("match(n) "
           "delete n ")

def add_people(tx, name, gender, years=21):
    """
    Create a people object with 3 attributes 
    """
    tx.run("CREATE (people {name: $value, gender: $gender, age:$years})",
      value=name,
      gender=gender,
      years=years) 


with driver.session() as session:
    session.read_transaction(del_all)
    session.read_transaction(add_people, "Snow White","F",22)
    session.read_transaction(add_people, "Happy","M",62)
    session.read_transaction(add_people, "Bashful","M",63)
    session.read_transaction(add_people, "Doc","M",60)
    session.read_transaction(add_people, "Grumpy","M")

print("""In the Web browser please enter this Cypher statement

match(n)
return n

""")
