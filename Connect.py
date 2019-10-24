"""
Neo4j Testing for ease of use.
"""
#pylint: disable=invalid-name
import dataclasses
from neo4j import GraphDatabase


@dataclasses.dataclass
class house:
    """
    data class for house
    """
    name: str
    address: str

    @property
    def cypher(self) -> str:
        """
        Manipulate the __repr__ method to return Cypher create statement
        """
        obj_str = str(self)
        return (
            "CREATE (n:"
            + str(obj_str).replace("=", ":").replace("(", "{").replace(")", "}")
            + ")"
        )


uri = "bolt://localhost:7687"
driver = GraphDatabase.driver(uri, auth=("neo4j", "ducati"))


def del_all(tx):
    """
    delete the links and the nodes
    """
    tx.run("match(n) " "detach delete n ")


def add_dataclass_obj(tx, args):
    """
    generic class for adding dataclass based objects
    """
    for n in args:
        print("adding")
        tx.run(n.cypher)


def add_people(tx, name, gender, years=21):
    """
    Create a people object with 3 attributes
    """
    tx.run(
        "CREATE (n:people {name: $value, gender: $gender, age:$years})",
        value=name,
        gender=gender,
        years=years,
    )


def link_people(tx):
    """
    Link two nodes with a relationship.
    """
    tx.run(
        "MATCH (p:people {gender:'M'}), (m:male {gender:'M'}) "
        "create (p)-[r:ARE_MEN]->(m) "
    )
    tx.run(
        "MATCH (p:people {gender:'F'}), (f:female {gender:'F'}) "
        "create (p)-[r:ARE_WOMEN]->(f) "
    )


def link_housing(tx):
    """
    Link some people to some houses
    """
    tx.run(
        "MATCH (p:people {name:'Snow White'}), (h:house {name:'Castle'}) "
        "create (p)-[r:LIVES_IN]->(h) "
    )
    tx.run(
        "MATCH (p:people {gender:'M'}), (h:house {name:'Dwarf House'}) "
        "create (p)-[r:LIVES_IN]->(h) "
    )
    tx.run(
        "MATCH (p:people {gender:'F'}), (h:house {name:'Dwarf House'}) "
        "create (p)-[r:WORKS_IN]->(h) "
    )
    tx.run(
        "MATCH (p:people {gender:'M'}), (h:house {name:'Mine'}) "
        "create (p)-[r:WORKS_IN]->(h) "
    )


def create_gender(tx):
    """
    Create a rather meaningless Gender class
    """
    tx.run("Create (n:male   {gender:'M'})")
    tx.run("Create (n:female {gender:'F'})")


housing = []
housing.append(house(name="Dwarf House", address="City"))
housing.append(house(name="Gold Mine", address="City"))
housing.append(house(name="Castle", address="Countryside"))


with driver.session() as session:
    session.read_transaction(del_all)

    session.read_transaction(create_gender)
    session.read_transaction(add_people, "Snow White", "F", 22)
    session.read_transaction(add_people, "Happy", "M", 62)
    session.read_transaction(add_people, "Bashful", "M", 63)
    session.read_transaction(add_people, "Doc", "M", 60)
    session.read_transaction(add_people, "Grumpy", "M")
    session.read_transaction(link_people)
    session.read_transaction(add_dataclass_obj, housing)
    session.read_transaction(link_housing)


print(
    """In the Web browser please enter this Cypher statement

match(n)
return n

"""
)
