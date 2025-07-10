# -*- coding: utf-8 -*-
"""
NetworkXDB is a small python library exposes a RDBMS persisted knowledge graph using NetworkX
    Copyright (C) 2025  William N. Roney, ScD (drbill688@gmail.com)

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU Affero General Public License as published
    by the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU Affero General Public License for more details.

    You should have received a copy of the GNU Affero General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""

import networkx as nx
import sqlalchemy as sqla
from dataclasses import dataclass
from enum import Enum

MAX_LABEL = 64
MAX_DESCRIPTION = 64
MAX_CORPUS = 4096
NUMBER_OF_EXAMPLES=3

@dataclass
class NetworkXDBNode:
    node_type: str
    node_value: str

    
@dataclass
class NetworkXDBCriteria:
    class Operator(Enum):
        EQUALS = '='
        NOT_EQUALS = '!='
    node_type: str
    operator: Operator
    node_value: str

class NetworkXDB:
    def __init__(self, engine = sqla.create_engine('sqlite+pysqlite:///:memory:')):
        self.engine = engine
        dbconn = self.engine.connect()
        iengine = sqla.inspect(self.engine)
        if len(set(iengine.get_table_names()) & set(['nxdb_model', 'nxdb_metadata', 'nxdb_corpus'])) != 3:
            dbconn.execute(sqla.text(f'CREATE TABLE nxdb_model (parent_type varchar({MAX_LABEL}), child_type varchar({MAX_LABEL}))'))
            dbconn.execute(sqla.text(f'CREATE TABLE nxdb_metadata (node_type varchar({MAX_LABEL}), node_description varchar({MAX_DESCRIPTION}))'))
            dbconn.execute(sqla.text(f'CREATE TABLE nxdb_corpus (parent_type varchar({MAX_LABEL}), parent_value varchar({MAX_CORPUS}), child_type varchar({MAX_LABEL}), child_value varchar({MAX_CORPUS}))'))
    def verbalize_model(self) -> str:
        # load NUMBER_OF_EXAMPLES maxrows into the dict.
        dbconn = self.engine.connect()
        model = nx.DiGraph()
        for record in dbconn.execute(sqla.text('select * from nxdb_model')):
            model.add_edge(record[0], record[1])
        metadata = {}
        node_types = list(model.nodes)
        for child_type in node_types:
            metadata[child_type] = {'description': '', 'examples':[]}
            i = 0
            for record in dbconn.execute(sqla.text('select child_type, child_value from nxdb_corpus where child_type = :child_type'), {'child_type': child_type}):
                if i < NUMBER_OF_EXAMPLES:
                    metadata[record[0]]['examples'].append(record[1])
                    i+=1
                else:
                    break
        for record in dbconn.execute(sqla.text('select * from nxdb_metadata')):
            metadata[record[0]]['description'] = record[1]
        res = ""
        def verbalize_subtree(model:nx.DiGraph, metadata:dict, thisnode:str, indent_level:int = 0) -> str:
            result = '{}{}{}'.format("--".join(['' for n in range(0, indent_level+1)]),' ' if indent_level > 0 else '', thisnode)
            metastring = ""
            thisnode_metadata = metadata.get(thisnode)
            metastring += ' ('
            if thisnode_metadata is not None:
                metastring += f"{thisnode_metadata['description']}"
                examples = thisnode_metadata.get('examples')
                if examples is not None and len(examples) > 0:
                    metastring += " Ex. {}".format(', '.join([f'"{m}"' for m in examples]))
            metastring += ')'
            result += '{}\n'.format(metastring if metastring != ' ()' else '')
            for child in model.successors(thisnode):
                result += verbalize_subtree(model, metadata, child, indent_level+1)
            return result
        for rootnode in {n for n, d in model.in_degree() if d == 0}:
            res += verbalize_subtree(model, metadata, rootnode)
        return res
    def add_metadata(self, node_type: str, description: str) -> None:
        dbconn = self.engine.connect()
        if len(list(dbconn.execute(sqla.text('select * from nxdb_metadata where node_type = :node_type'), {'node_type': node_type}))) == 0:
            dbconn.execute(sqla.text('insert into nxdb_metadata(node_type, node_description) values(:node_type, :node_description)'), {'node_type': node_type, 'node_description': description})
        else:
            dbconn.execute(sqla.text('update nxdb_metadata set node_description = :node_description where node_type = :node_type'), {'node_type': node_type, 'node_description': description})
    def add_edge(self, u: NetworkXDBNode, v: NetworkXDBNode) -> None:
        dbconn = self.engine.connect()
        if len(list(dbconn.execute(sqla.text('select * from nxdb_model where parent_type = :parent_type and child_type = :child_type'), {'parent_type': u.node_type, 'child_type': v.node_type}))) == 0:
            dbconn.execute(sqla.text('insert into nxdb_model(parent_type, child_type) values(:parent_type, :child_type)'), {'parent_type': u.node_type, 'child_type': v.node_type})
        if len(list(dbconn.execute(sqla.text('select * from nxdb_corpus where parent_type = :parent_type and parent_value = :parent_value and child_type = :child_type'), {'parent_type': u.node_type, 'parent_value': u.node_value, 'child_type': v.node_type}))) == 0:
            dbconn.execute(sqla.text('insert into nxdb_corpus(parent_type, parent_value, child_type, child_value) values(:parent_type, :parent_value, :child_type, :child_value)'), {'parent_type': u.node_type, 'parent_value': u.node_value, 'child_type': v.node_type, 'child_value': v.node_value})
        else:
            dbconn.execute(sqla.text('update nxdb_corpus set child_value = :child_value where parent_type = :parent_type and parent_value = :parent_value and child_type = :child_type'), {'parent_type': u.node_type, 'parent_value': u.node_value, 'child_type': v.node_type, 'child_value': v.node_value})
    def shortest_path(self, src_type: str, dest_type: str) -> list:
        dbconn = self.engine.connect()
        G = nx.DiGraph()
        for edge in dbconn.execute(sqla.text('select * from nxdb_model')) :
            G.add_edge(edge[0], edge[1])
        uG = nx.Graph(G)            
        path = list(nx.shortest_path(uG, src_type, dest_type))
        result = []
        for step in [(u, v) for u, v in zip(path, path[1:])]:
            if G.has_edge(step[0], step[1]):
                result.append((step[0], step[1], 'F'))
            else:
                result.append((step[0], step[1], 'R'))
        return result
    def model_has_edge(self, src_type: str, dest_type: str) -> bool:
        dbconn = self.engine.connect()
        return len(list(dbconn.execute(sqla.text('select * from nxdb_model where parent_type = :parent_type and child_type = :child_type'), {'parent_type': src_type, 'child_type': dest_type}))) > 0
    def result_graph(self, root_type: str, criteria: NetworkXDBCriteria) -> dict:
        steps = self.shortest_path(root_type, criteria.node_type)
        if len(steps) == 0:
            if criteria.node_type == root_type:
                query = "select * from nxdb_corpus where parent_type = '{}' and parent_value = '{}'".format(criteria.node_type, criteria.node_value)
            else:
                query = "select * from nxdb_corpus where parent_type = '{}' and child_type = '{}' and child_value = '{}'".format(root_type, criteria.node_type, criteria.node_value)
        else:
            query = 'select {}\n'.format('{}'.format(','.join([f'{chr(ord("a")+m)}.*' for m in range(0, len(steps))])))
            query += ' from {}\n'.format(','.join([f'nxdb_corpus {chr(ord("a")+m)}' for m in range(0, len(steps))]))
            query += ' where {}\n'.format(f"a.parent_type = '{root_type}'")
            tbl = 'a'
            for i in range(1, len(steps)):
                nextstep = steps[i] if i < (len(steps)) else None
                if nextstep[2] == 'F':
                    if i > 1 and steps[i-2][2] == 'F':
                        add = f' and {tbl}.parent_type = {chr(ord(tbl)+1)}.parent_type and {tbl}.parent_value = {chr(ord(tbl)+1)}.parent_value '
                    else:
                        add = f' and {tbl}.child_type = {chr(ord(tbl)+1)}.parent_type and {tbl}.child_value = {chr(ord(tbl)+1)}.parent_value '
                    query += add
                else:
                    add = f' and {tbl}.child_type = {chr(ord(tbl)+1)}.child_type and {tbl}.child_value = {chr(ord(tbl)+1)}.child_value '
                    query += add
                tbl = chr(ord(tbl)+1)
            if steps[-1][2] == 'F':
                query += f" and {tbl}.child_type = '{criteria.node_type}' and {tbl}.child_value = '{criteria.node_value}'"
            else:
                query += f" and {tbl}.parent_type = '{criteria.node_type}' and {tbl}.parent_value = '{criteria.node_value}'"
        dbconn = self.engine.connect()
        RG = nx.DiGraph()
        print(f'QUERY: {query}')
        for record in dbconn.execute(sqla.text(query)):
            print(f'REC: {record}')
            step_number = 0
            for pt, pv, ct, cv in zip(record[0::4], record[1::4], record[2::4], record[3::4]):
                direction = 'F'
                if len(steps) > 0:
                    direction = steps[step_number][2]
                if (pt == root_type):
                    RG.add_edge((None,None),(pt,pv))
                if direction == 'F':
                    RG.add_edge((pt,pv), (ct,cv))
                else:
                    RG.add_edge((ct,cv), (pt,pv))
                step_number+=1
        def dump_dict(G: nx.DiGraph, root: NetworkXDBNode):
            res = {}
            if G.has_node((None, None)):
                for node in [m for m in G.successors(root) if m != root]:
                    if node[0] not in res:
                        d = dump_dict(G, node)
                        if isinstance(d, str):
                            res[node[0]] = node[1]
                        else:
                            res.update({node[0]:{node[1]:d}})
            return res if bool(res) else ''
        import json
        return json.dumps(dump_dict(RG, (None,None)), indent=4)
        
        
if __name__ == '__main__':
    G = NetworkXDB()
    p1 = NetworkXDBNode('Parent1', 'p1')
    p2 = NetworkXDBNode('Parent2', 'p2')
    p3 = NetworkXDBNode('Parent3', 'p3')
    p4 = NetworkXDBNode('Parent4', 'p4')
    
    c11 = NetworkXDBNode('Child1.1', 'c11')
    c12 = NetworkXDBNode('Child1.2', 'c12')
    c13 = NetworkXDBNode('Child1.3', 'c13')
    c14 = NetworkXDBNode('Child1.1', 'c14')
    
    c21 = NetworkXDBNode('Child2.1', 'c21')
    c22 = NetworkXDBNode('Child2.2', 'c22')
    c23 = NetworkXDBNode('Child2.3', 'c23')
    
    c31 = NetworkXDBNode('Child3.1', 'c31')
    c32 = NetworkXDBNode('Child3.2', 'c32')
    c33 = NetworkXDBNode('Child3.3', 'c33')
    
    c41 = NetworkXDBNode('Child4.1', 'c41')
    c42 = NetworkXDBNode('Child4.2', 'c42')
    c43 = NetworkXDBNode('Child4.3', 'c43')

    c431 = NetworkXDBNode('Child4.3.1', 'c431')
    
    G.add_edge(p1, c11)
    G.add_edge(p1, c12)
    G.add_edge(p1, c13)
    G.add_edge(p1, c14) #update
    
    G.add_edge(p2, c21)
    G.add_edge(p2, c22)
    G.add_edge(p2, c23)
    
    G.add_edge(p3, c31)
    G.add_edge(p3, c32)
    G.add_edge(p3, c33)
    
    G.add_edge(p4, c41)
    G.add_edge(p4, c42)
    G.add_edge(p4, c43)
    G.add_edge(c43, c431)
    
    G.add_edge(p2, c13)
    G.add_edge(p3, c23)
    G.add_edge(p4, c33)
    
    print("====> Direct: Parent4 == p4")                
    print(G.result_graph('Parent4', NetworkXDBCriteria('Parent4', NetworkXDBCriteria.Operator.EQUALS, 'p4')))    
    print("====> Down1: Parent4 when Child4.3 == c43")                
    print(G.result_graph('Parent4', NetworkXDBCriteria('Child4.3', NetworkXDBCriteria.Operator.EQUALS, 'c43')))    
    print("====> Down2: Parent 4 when Child4.3.1 == c431")                
    print(G.result_graph('Parent4', NetworkXDBCriteria('Child4.3.1', NetworkXDBCriteria.Operator.EQUALS, 'c431')))    
    print("====> Down2 UP1: Parent 4 when Parent3 == p3")                
    print(G.result_graph('Parent4', NetworkXDBCriteria('Parent3', NetworkXDBCriteria.Operator.EQUALS, 'p3')))    
    print("====> Ugly: Parent 4 when Parent2 == p2")                
    print(G.result_graph('Parent4', NetworkXDBCriteria('Parent2', NetworkXDBCriteria.Operator.EQUALS, 'p2')))    
    print("====> Ugly: Parent 4 when Parent1 == p1")                
    print(G.result_graph('Parent4', NetworkXDBCriteria('Parent1', NetworkXDBCriteria.Operator.EQUALS, 'p1')))    
    print("====> Direct: Parent1 == p1")                
    print(G.result_graph('Parent1', NetworkXDBCriteria('Parent1', NetworkXDBCriteria.Operator.EQUALS, 'p1')))    
    print("====> Ugly: Parent 4 when Child1.1 == c14")                
    print(G.result_graph('Parent4', NetworkXDBCriteria('Child1.1', NetworkXDBCriteria.Operator.EQUALS, 'c14')))    
    G.add_metadata('Parent1', 'This is a description of what Parent1 nodes represent.')
    G.add_metadata('Parent4', 'This is a description of what Parent4 nodes represent.')
    G.add_metadata('Child4.3.1', 'This is a description of what Child4.3.1 nodes represent.')
    print(G.verbalize_model())
    
   
