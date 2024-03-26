from langchain_community.graphs import Neo4jGraph
from langchain_community.vectorstores.neo4j_vector import Neo4jVector
from typing import Optional, Any, List

class Graph:
    def __init__(self, uri, username, password) -> None:
        self.uri = uri
        self.username = username
        self.password = password

    def initGraph(self) -> None:
        self.graph = Neo4jGraph(
                url=self.uri,
                username=self.username,
                password=self.password,
            )

    def getGraph(self) -> Optional[Any]:
        return self.graph
    
    def getNeo4jVector(self, embeddings: str, indexName: str, nodeLabel: str, nodeProperties: List, columnName: str) -> Optional[Any]:
        self.neo4jvector = Neo4jVector.from_existing_graph(
                                        embeddings,                              
                                        url=self.uri,
                                        username=self.username,   
                                        password=self.password,   
                                        index_name=indexName,                 
                                        node_label=nodeLabel,                      
                                        text_node_properties=nodeProperties,               
                                        embedding_node_property=columnName, 
                                    )
        return self.neo4jvector