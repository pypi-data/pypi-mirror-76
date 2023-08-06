#!/usr/bin/env python
# -*- coding: utf-8 -*-
import traceback
from abc import ABCMeta, abstractmethod
from copy import deepcopy

import gensim
import networkx
from networkx import MultiDiGraph

from sekg.graph.accessor import GraphAccessor
from sekg.graph.creator import NodeBuilder
from sekg.graph.index_accessor import IndexGraphAccessor
from sekg.graph.metadata_accessor import MetadataGraphAccessor
from sekg.util.annotation import catch_exception

DEFAULT_LABEL = "entity"
DEFAULT_PRIMARY_KEY = "_node_id"

"""
this package is used to export a neo4j instance to Memory to build a copy of graph.
You can used it to train graph vector or to query graph 
"""


class NodeInfo(object):
    """
    A basic abstract class for NodeInfo.
    This class could be extended to a project-specific purpose.
    e.g., APINodeInfo, WikidataInfo. They could implement their get_main_name,get_all_names method.

    """
    __metaclass__ = ABCMeta
    PRIVATE_PROPERTY = {
        "lastrevid",
        "_create_time",
        "_update_time",
        "_modify_version",
        "modified",
        "logo image"
    }

    def __init__(self, node_id, labels, properties):
        self.labels = labels  # labels must be a list
        self.properties = properties  # properties must be a dict
        self.node_id = node_id

    @abstractmethod
    def get_main_name(self):
        pass

    @abstractmethod
    def get_all_names(self):
        return []

    def get_all_names_str(self):
        return " , ".join(self.get_all_names())

    @abstractmethod
    def get_all_valid_attributes(self):
        valid_attribute_pairs = []

        for property_name in self.properties.keys():
            if self.is_valid_property(property_name):
                value = self.properties[property_name]
                if not value:
                    continue
                valid_attribute_pairs.append((property_name, value))
        return valid_attribute_pairs

    def get_all_valid_attributes_str(self):
        result = []
        valid_attribute_pairs = self.get_all_valid_attributes()
        for (property_name, value) in valid_attribute_pairs:
            result.append(property_name + " : " + value)

        return " , ".join(result)

    @abstractmethod
    def is_valid_property(self, property_name):
        if property_name in NodeInfo.PRIVATE_PROPERTY:
            return False
        return True

    def __repr__(self):
        return "<NodeInfo id=%d labels=%r properties=%r>" % (self.node_id, self.labels, self.properties)


class NodeInfoFactory(object):
    """
    a basic abstract class for NodeInfo
    """
    __metaclass__ = ABCMeta
    """
    a factory to create NodeInfo, can be extend to create Multi type NodeInfo instance by condition
    """

    def __init__(self):
        pass

    @abstractmethod
    def create_node_info(self, node_info_dict):
        """need to implement.
        example implement,CodeElementNodeInfo,DomainEntityNodeInfo,OperationEntityNodeInfo are three different NodeInfo
        subclass:

        labels = node_info_dict["labels"]
        node_id = node_info_dict["id"]
        properties = node_info_dict["properties"]

        if CodeConstant.LABEL_CODE_ELEMENT in labels:
            return CodeElementNodeInfo(node_id=node_id,
                                       labels=labels,
                                       properties=properties)
        if DomainConstant.LABEL_DOMAIN_TERM in labels:
            return DomainEntityNodeInfo(node_id=node_id,
                                        labels=labels,
                                        properties=properties)

        if OperationConstance.LABEL_OPERATION in labels:
            return OperationEntityNodeInfo(node_id=node_id,
                                           labels=labels,
                                           properties=properties)


        """
        return None


class RelationInfo:

    def __init__(self, start_node_info, relation_name, end_node_info):
        self.relation_name = relation_name
        self.end_node_info = end_node_info
        self.start_node_info = start_node_info

    def get_in_relation_str(self):
        return "{start} {r}".format(
            start=self.start_node_info.get_main_name(),
            r=self.relation_name
        )

    def get_out_relation_str(self):
        return "{r} {end}".format(
            r=self.relation_name,
            end=self.end_node_info.get_main_name()
        )

    def get_full_relation_str(self):
        return "{start} {r} {end}".format(start=self.start_node_info.get_main_name(),
                                          r=self.relation_name,
                                          end=self.end_node_info.get_main_name())


class GraphDataReader:
    """
    this class is a graph Data reader, can get the graph exporter not in the raw json,
    but in more clean format, wrap the result to a specific Object NodeInfo or RelationInfo.
    """

    def __init__(self, graph_data, node_info_factory):
        if isinstance(graph_data, GraphData):
            self.graph_data = graph_data
        else:
            self.graph_data = None

        if isinstance(node_info_factory, NodeInfoFactory):
            self.node_info_factory = node_info_factory
        else:
            self.node_info_factory = None

    def get_all_out_relation_infos(self, node_id):
        relation_list = self.graph_data.get_all_out_relations(node_id=node_id)

        return self.create_relation_info_list(relation_list)

    def get_all_in_relation_infos(self, node_id):
        relation_list = self.graph_data.get_all_in_relations(node_id=node_id)

        return self.create_relation_info_list(relation_list)

    @staticmethod
    def create_relation_info(start_node_info, relation_type, end_node_info):
        return RelationInfo(start_node_info=start_node_info,
                            relation_name=relation_type,
                            end_node_info=end_node_info)

    def create_from_relation_info_dict(self, relation_info):
        graph_data = self.graph_data
        start_id, relation_type, end_id = relation_info
        start_node_info_dict = graph_data.get_node_info_dict(start_id)
        start_node_info = self.node_info_factory.create_node_info(start_node_info_dict)

        end_node_info_dict = graph_data.get_node_info_dict(end_id)
        end_node_info = self.node_info_factory.create_node_info(end_node_info_dict)

        return self.create_relation_info(start_node_info=start_node_info, relation_type=relation_type,
                                         end_node_info=end_node_info,
                                         )

    def create_relation_info_list(self, relation_info_dict_list):
        info_list = []
        for r in relation_info_dict_list:
            info_list.append(self.create_from_relation_info_dict(r))
        return info_list

    def get_node_info(self, node_id):
        node_info_dict = self.graph_data.get_node_info_dict(node_id=node_id)
        return self.node_info_factory.create_node_info(node_info_dict)

    def get_all_node_infos(self):
        result = []
        for node_id in self.graph_data.get_node_ids():
            result.append(self.get_node_info(node_id))
        return result


class NodePropertyIndexer:
    """
    a helper class to help the graph data object create the index on some properties.
    And it could find node id with specific property value on the some properties.
    """

    def __init__(self, index_property_name):
        self.index_property_name = index_property_name
        self.property_value_to_ids_map = {}
        self.id_2_property_values_map = {}

    def index_node(self, node_id, node_properties):
        if self.index_property_name not in node_properties:
            return False
        property_value = node_properties[self.index_property_name]

        exist_property_values = self.get_indexed_property_values(node_id)

        if type(property_value) == list or type(property_value) == set:
            new_property_values = set(property_value)
        else:
            new_property_values = {property_value}

        if exist_property_values == new_property_values:
            return False

        delete_property_values = exist_property_values - new_property_values
        add_property_values = new_property_values - exist_property_values

        for t_value in delete_property_values:
            self.remove_index_on_value(node_id=node_id, property_value=t_value)

        for t_value in add_property_values:
            self.add_index_on_value(node_id=node_id, property_value=t_value)

        return True

    def get_indexed_property_values(self, node_id):
        if node_id not in self.id_2_property_values_map:
            self.id_2_property_values_map[node_id] = set([])
        exist_property_values = self.id_2_property_values_map[node_id]
        return exist_property_values

    def find_node_ids_by_value(self, value):
        if value in self.property_value_to_ids_map:
            return self.property_value_to_ids_map[value]
        return set([])

    def remove_index_on_value(self, node_id, property_value):
        if property_value not in self.property_value_to_ids_map:
            return

        id_set = self.property_value_to_ids_map[property_value]
        if node_id in id_set:
            id_set.remove(node_id)

        if node_id not in self.id_2_property_values_map:
            return

        property_values = self.id_2_property_values_map[node_id]
        if property_value in property_values:
            property_values.remove(property_value)

    def add_index_on_value(self, node_id, property_value):
        if property_value not in self.property_value_to_ids_map:
            self.property_value_to_ids_map[property_value] = set([])

        id_set = self.property_value_to_ids_map[property_value]

        id_set.add(node_id)

        if node_id not in self.id_2_property_values_map:
            self.id_2_property_values_map[node_id] = set([])

        property_values = self.id_2_property_values_map[node_id]
        property_values.add(property_value)

    def remove_index_on_node(self, node_id):
        if node_id in self.id_2_property_values_map:
            index_values = self.id_2_property_values_map[node_id]

            all_index_values = list(index_values)
            for value in all_index_values:
                self.remove_index_on_value(node_id=node_id, property_value=value)
            self.id_2_property_values_map.pop(node_id)


class GraphIndexCollection:
    def __init__(self):
        self.property_to_indexer_map = {}

    def create_index_on_property(self, *property_name_list):
        for name in property_name_list:
            if name not in self.property_to_indexer_map:
                self.property_to_indexer_map[name] = NodePropertyIndexer(index_property_name=name)

    def add_node(self, node_id, node_properties):
        for property_name, indexer in self.property_to_indexer_map.items():
            indexer.index_node(node_id, node_properties)

    def remove_node(self, node_id):
        for property_name, indexer in self.property_to_indexer_map.items():
            indexer.remove_index_on_node(node_id)

    def find_ids(self, property_name, property_value):
        if self.is_property_indexed(property_name) == False:
            return set([])
        return self.property_to_indexer_map[property_name].find_node_ids_by_value(property_value)

    def is_property_indexed(self, property_name):
        """
        check if one property indexed
        :param property_name:
        :return:
        """
        if property_name in self.get_index_property():
            return True
        return False

    def get_index_property(self):
        """
        get all indexed property name
        :return:
        """
        return self.property_to_indexer_map.keys()


class GraphData(gensim.utils.SaveLoad):
    # todo: make the information return by graph data are copy by value, not reference
    # todo: in case the change
    """
    the store of a graph data.

    each node is represent as a dict of node info named 'node_json',
    Example Format for 'node_json':

     {
        "id": 1,
        "properties": {"name":"bob","age":1},
        "labels": ["entity","man"]
    }

    """

    DEFAULT_KEY_NODE_ID = "id"  # the key name for the node id, every node must have it.
    DEFAULT_KEY_NODE_PROPERTIES = "properties"  # the key name for the node properties, every node must have it.
    DEFAULT_KEY_NODE_LABELS = "labels"  # the key name for the node labels, every node must have it.

    DEFAULT_KEYS = [DEFAULT_KEY_NODE_ID, DEFAULT_KEY_NODE_PROPERTIES, DEFAULT_KEY_NODE_LABELS]
    UNASSIGNED_NODE_ID = -1  # a node without a id specify, a newly created node, its id is -1

    DEFAULT_KEY_RELATION_START_ID = "startId"
    DEFAULT_KEY_RELATION_TYPE = "relationType"
    DEFAULT_KEY_RELATION_END_ID = "endId"

    DEFAULT_KEY_PROPERTY_QUALIFIED_NAME = "qualified_name"
    DEFAULT_KEY_PROPERTY_ALIAS = "alias"

    def __init__(self):
        # two map for
        self.__init_graph()

    def clear(self):
        self.__init_graph()

    def __init_graph(self):
        self.graph = MultiDiGraph()
        self.max_node_id = 0
        self.label_to_ids_map = {}
        self.index_collection = GraphIndexCollection()
        self.relation_type_to_num_map = {}

    def create_index_on_property(self, *property_name_list):
        self.index_collection.create_index_on_property(*property_name_list)

    def find_all_shortest_paths(self, startId, endId):
        """
        找到所有的最短路
        :param startId:
        :param endId:
        :return:
        """
        shortest_paths = networkx.all_shortest_paths(self.graph, startId, endId)
        return shortest_paths

    def find_shortest_path(self, startId, endId):
        """
        找到一个最短路
        :param startId:
        :param endId:
        :return:
        """
        shortest_paths = networkx.shortest_path(self.graph, startId, endId)
        return shortest_paths

    def set_nodes(self, nodes):
        for n in nodes:
            self.add_node(node_id=n[self.DEFAULT_KEY_NODE_ID],
                          node_properties=n[self.DEFAULT_KEY_NODE_PROPERTIES],
                          node_labels=n[self.DEFAULT_KEY_NODE_LABELS])

    def add_labels(self, *labels):
        """
        add a list of label to the graph
        :param labels:
        :return:
        """

        for label in labels:
            if not label:
                return
            if label not in self.label_to_ids_map.keys():
                self.label_to_ids_map[label] = set([])

    def add_label_by_node_id(self, node_id, label):
        """
        add a label to a node
        :param node_id: the node id which the label need to add
        :param label: the label that need to added
        :return: True, add successful.False, add fail.
        """
        if not label:
            return False
        node_json = self.get_node_info_dict(node_id)
        if not node_json:
            return False
        node_json[GraphData.DEFAULT_KEY_NODE_LABELS].add(label)
        if label not in self.label_to_ids_map.keys():
            self.label_to_ids_map[label] = set()
        self.label_to_ids_map[label].add(node_id)
        return True

    def get_node_ids_by_label(self, label):
        if label not in self.label_to_ids_map.keys():
            return set([])
        return self.label_to_ids_map[label]

    def add_label_by_label(self, label, new_label):
        """
        add a label to node in graph, the node must has the specific label
        :param new_label: the new_label add to node
        :param label: the node must has the label
        :return:
        """

        for node_id in self.get_node_ids_by_label(label):
            self.add_label_by_node_id(node_id, new_label)

    def add_label_to_all(self, label):
        """
        add a label to node in graph
        :param label:
        :return:
        """
        if not label:
            return
        self.add_labels(label)
        for node_id in self.get_node_ids():
            self.add_label_by_node_id(node_id, label)

    def add_node(self, node_labels, node_properties, node_id=UNASSIGNED_NODE_ID, primary_property_name=""):
        """
        add a node json to the graph
        :param node_id: the node_id to identify the node, if not given, it will be add as new node and give a node id
        :param node_properties: a dict of node properties, key-value pair
        :param node_labels: a set of node labels
        :param primary_property_name:make sure the node_json["properties"][primary_property_name] is unique in GraphData.
         if no passing, the node json will be add to graph without check. otherwise, only the node json
        with unique property value ( property value is got by primary_property_name ) will be added to the GraphData.
                :return:-1, means that adding node json fail. otherwise, return the id of the newly added node
        """

        if primary_property_name:
            if primary_property_name not in node_properties:
                print("node json must have a primary_property_name ( %r ) in properties " % primary_property_name)
                return self.UNASSIGNED_NODE_ID

            node_json = self.find_one_node_by_property(property_name=primary_property_name,
                                                       property_value=node_properties[
                                                           primary_property_name])
            if node_json:
                return node_json[self.DEFAULT_KEY_NODE_ID]

        if node_id == self.UNASSIGNED_NODE_ID:
            node_id = self.max_node_id + 1
            self.max_node_id = self.max_node_id + 1

        new_node_json = {
            self.DEFAULT_KEY_NODE_ID: node_id,
            self.DEFAULT_KEY_NODE_PROPERTIES: node_properties,
            self.DEFAULT_KEY_NODE_LABELS: set(node_labels)
        }

        self.graph.add_node(node_id, **new_node_json)

        if self.max_node_id < node_id:
            self.max_node_id = node_id

        self.add_labels(*new_node_json[self.DEFAULT_KEY_NODE_LABELS])
        for label in new_node_json[self.DEFAULT_KEY_NODE_LABELS]:
            self.label_to_ids_map[label].add(node_id)
        self.index_collection.add_node(node_id=node_id,
                                       node_properties=new_node_json[GraphData.DEFAULT_KEY_NODE_PROPERTIES])
        return node_id

    def remove_node(self, node_id):
        if node_id not in self.graph.nodes:
            return None
        # print(type(self.graph.nodes))
        node_json = self.graph.nodes[node_id]
        in_relations = set(self.graph.in_edges(node_id, keys=True))
        out_relations = set(self.graph.out_edges(node_id, keys=True))
        self.graph.remove_node(node_id)

        for label in node_json[self.DEFAULT_KEY_NODE_LABELS]:
            self.label_to_ids_map[label].remove(node_id)

        self.index_collection.remove_node(node_id)

        return node_json, out_relations, in_relations

    def merge_two_nodes_by_id(self, main_node_id, merged_node_id,
                              main_alias_property=DEFAULT_KEY_PROPERTY_QUALIFIED_NAME,
                              merged_alias_property=DEFAULT_KEY_PROPERTY_QUALIFIED_NAME, merge_properties=True):
        if main_node_id not in self.graph.nodes or merged_node_id not in self.graph.nodes:
            return None

        main_node_json, main_out_relations, main_in_relations = self.remove_node(main_node_id)
        merged_node_json, merged_out_relations, merged_in_relations = self.remove_node(merged_node_id)
        new_node_labels = main_node_json[self.DEFAULT_KEY_NODE_LABELS] | merged_node_json[self.DEFAULT_KEY_NODE_LABELS]
        new_node_properties = main_node_json[self.DEFAULT_KEY_NODE_PROPERTIES]
        alias_set = set()

        alias = new_node_properties.get(main_alias_property, set())
        if len(alias):
            alias_set.update(alias)
            # alias_set.add(alias)

        alias = merged_node_json[self.DEFAULT_KEY_NODE_PROPERTIES].get(merged_alias_property, set())
        if len(alias):
            alias_set.update(alias)
            # alias_set.add(alias)

        if len(alias_set) > 0:
            if self.DEFAULT_KEY_PROPERTY_ALIAS not in new_node_properties:
                new_node_properties[self.DEFAULT_KEY_PROPERTY_ALIAS] = set()
            new_node_properties[self.DEFAULT_KEY_PROPERTY_ALIAS].update(alias_set)

        if merge_properties:
            for k, v in merged_node_json[self.DEFAULT_KEY_NODE_PROPERTIES].items():
                if k not in new_node_properties:
                    new_node_properties[k] = v
        new_node_id = self.add_node(new_node_labels, new_node_properties)

        new_relations = set()
        for startId, endId, relationType in (
                main_out_relations | main_in_relations | merged_out_relations | merged_in_relations):
            if startId == main_node_id or startId == merged_node_id:
                startId = new_node_id
            if endId == main_node_id or endId == merged_node_id:
                endId = new_node_id
            new_relations.add((startId, relationType, endId))
        new_relations = filter(lambda r: r[0] != r[2], new_relations)
        for startID, relationType, endId in new_relations:
            self.add_relation(startID, relationType, endId)

        return new_node_id

    def merge_node(self, node_labels, node_properties, primary_property_name):
        """
        merge a node json to the graph, that is if we can't not find the node with primary_property_value match the given node.
        we will add a new node, if we found, we will add copy all properties given to the exist node, copy all labels to the exist node.
        properties will be updated by this merge. That is, if the node to be merged has the same attributes as the existing node, the attributes of the new node are used.

        :param node_properties: a dict of node properties, key-value pair
        :param node_labels: a set of node labels
        :param primary_property_name: The name of the property to check, the merged node and the new node are the same on this property.
        :return:-1, means that adding node json fail. otherwise, return the id of the newly added(merged) node.If it already exists, the id of this merged node will not change.
        """

        if not primary_property_name:
            print("primary_property_name must given on merge")
            return GraphData.UNASSIGNED_NODE_ID

        if primary_property_name not in node_properties:
            print("node json must have a primary_property_name ( %r ) in properties " % primary_property_name)
            return self.UNASSIGNED_NODE_ID

        node_json = self.find_one_node_by_property(property_name=primary_property_name,
                                                   property_value=node_properties[
                                                       primary_property_name])

        if not node_json:
            return self.add_node(node_labels=node_labels, node_properties=node_properties,
                                 node_id=GraphData.UNASSIGNED_NODE_ID)

        merge_node_id = node_json[self.DEFAULT_KEY_NODE_ID]
        merge_properties = node_json[self.DEFAULT_KEY_NODE_PROPERTIES]
        for k, v in node_properties.items():
            merge_properties[k] = v

        merge_labels = set(node_json[self.DEFAULT_KEY_NODE_LABELS])
        for label in node_labels:
            merge_labels.add(label)

        return self.add_node(node_labels=merge_labels, node_properties=merge_properties, node_id=merge_node_id)

    def add_node_with_multi_primary_property(self, node_labels, node_properties, node_id=UNASSIGNED_NODE_ID,
                                             primary_property_names=None):
        """
        add a node json to the graph
        :param node_id: the node_id to identify the node, if not given, it will be add as new node and give a node id
        :param node_properties: a dict of node properties, key-value pair
        :param node_labels: a set of node labels
        :param primary_property_names:a list of primary properties. make sure the node_json["properties"][primary_property_name] is unique in GraphData.
         if no passing, the node json will be add to graph without check. otherwise, only the node json
        with unique property value ( property value is got by primary_property_name ) will be added to the GraphData.
                :return:-1, means that adding node json fail. otherwise, return the id of the newly added node
        """

        if primary_property_names is None:
            primary_property_names = []

        match_properties = {}

        for primary_property_name in primary_property_names:
            if primary_property_name not in node_properties:
                print("node json must have a primary_property_name ( %r ) in properties " % primary_property_name)
                return self.UNASSIGNED_NODE_ID
            match_properties[primary_property_name] = node_properties[primary_property_name]

        node_json = self.find_one_node_by_properties(**match_properties)
        if node_json:
            return node_json[self.DEFAULT_KEY_NODE_ID]

        if node_id == self.UNASSIGNED_NODE_ID:
            node_id = self.max_node_id + 1

        new_node_json = {
            self.DEFAULT_KEY_NODE_ID: node_id,
            self.DEFAULT_KEY_NODE_PROPERTIES: node_properties,
            self.DEFAULT_KEY_NODE_LABELS: set(node_labels)
        }

        self.graph.add_node(node_id, **new_node_json)
        if self.max_node_id < node_id:
            self.max_node_id = node_id

        self.add_labels(*new_node_json[self.DEFAULT_KEY_NODE_LABELS])
        for label in new_node_json[self.DEFAULT_KEY_NODE_LABELS]:
            self.label_to_ids_map[label].add(node_id)
        self.index_collection.add_node(node_id=node_id,
                                       node_properties=new_node_json[GraphData.DEFAULT_KEY_NODE_PROPERTIES])

        return node_id

    def merge_node_with_multi_primary_property(self, node_labels, node_properties, primary_property_names=None):
        """
        merge a node json to the graph, that is if we can't not find the node with primary_property_value match the given node.
        we will add a new node, if we found, we will add copy all properties given to the exist node, copy all labels to the exist node.
        properties will be updated by this merge. That is, if the node to be merged has the same attributes as the existing node, the attributes of the new node are used.

        :param node_properties: a dict of node properties, key-value pair
        :param node_labels: a set of node labels
        :param primary_property_name: The list of name of the property to check, the merged node and the new node are the same on this property.
        :return:-1, means that adding node json fail. otherwise, return the id of the newly added(merged) node.If it already exists, the id of this merged node will not change.
        """

        if not primary_property_names:
            print("primary_property_names must given on merge")
            return GraphData.UNASSIGNED_NODE_ID
        match_properties = {}

        for primary_property_name in primary_property_names:
            if primary_property_name not in node_properties:
                print("node json must have a primary_property_name ( %r ) in properties " % primary_property_name)
                return self.UNASSIGNED_NODE_ID
            match_properties[primary_property_name] = node_properties[primary_property_name]

        node_json = self.find_one_node_by_properties(**match_properties)
        if not node_json:
            return self.add_node(node_labels=node_labels, node_properties=node_properties,
                                 node_id=GraphData.UNASSIGNED_NODE_ID)

        merge_node_id = node_json[self.DEFAULT_KEY_NODE_ID]
        merge_properties = node_json[self.DEFAULT_KEY_NODE_PROPERTIES]
        for k, v in node_properties.items():
            merge_properties[k] = v

        merge_labels = set(node_json[self.DEFAULT_KEY_NODE_LABELS])
        for label in node_labels:
            merge_labels.add(label)

        return self.add_node(node_labels=merge_labels, node_properties=merge_properties, node_id=merge_node_id)

    def refresh_indexer(self):
        """
        refresh the index on all properties.
        :return:
        """
        index_properties = self.index_collection.get_index_property()
        index_properties = list(index_properties)
        del self.index_collection
        self.index_collection = GraphIndexCollection()

        self.create_index_on_property(*index_properties)
        for node_id, node_json in self.graph.nodes(data=True):
            if node_json is None:
                continue
            node_properties_json = node_json[self.DEFAULT_KEY_NODE_PROPERTIES]
            self.index_collection.add_node(node_id, node_properties_json)

    def find_one_node_by_property(self, property_name, property_value):
        if self.index_collection.is_property_indexed(property_name):
            candidate_node_ids = list(self.index_collection.find_ids(property_name, property_value=property_value))
            if len(candidate_node_ids) == 0:
                return None
            return self.get_node_info_dict(candidate_node_ids[0])

        for node_id, node_json in self.graph.nodes(data=True):
            node_properties_json = node_json[self.DEFAULT_KEY_NODE_PROPERTIES]
            if property_name in node_properties_json.keys() and node_properties_json[property_name] == property_value:
                return node_json
        return None

    def find_nodes_by_ids(self, *ids):
        result = []
        for node_id in ids:
            node_json = self.get_node_info_dict(node_id)
            if node_json:
                result.append(node_json)
        return result

    def find_nodes_by_property(self, property_name, property_value):
        if self.index_collection.is_property_indexed(property_name):
            candidate_node_ids = list(self.index_collection.find_ids(property_name, property_value=property_value))

            return self.find_nodes_by_ids(*candidate_node_ids)

        nodes = []
        for node_id, node_json in self.graph.nodes(data=True):
            node_properties_json = node_json[self.DEFAULT_KEY_NODE_PROPERTIES]
            if property_name in node_properties_json.keys() and node_properties_json[property_name] == property_value:
                nodes.append(node_json)
        return nodes

    def find_one_node_by_property_value_starts_with(self, property_name, property_value_starter):
        """
        find a node which its property value is string and the string is startswith a given string
        :param property_name:
        :param property_value_starter:
        :return:
        """
        for node_id, node_json in self.graph.nodes(data=True):
            node_properties_json = node_json[self.DEFAULT_KEY_NODE_PROPERTIES]
            if property_name not in node_properties_json.keys():
                continue

            property_value = node_properties_json[property_name]
            if type(property_value) != str:
                continue
            if property_value.startswith(property_value_starter):
                return node_json
        return None

    def find_nodes_by_property_value_starts_with(self, property_name, property_value_starter):
        """
        find all nodes which its property value is string and the string is startswith a given string
        :param property_name:
        :param property_value_starter:
        :return:
        """
        nodes = []
        for node_id, node_json in self.graph.nodes(data=True):
            node_properties_json = node_json[self.DEFAULT_KEY_NODE_PROPERTIES]
            if property_name not in node_properties_json.keys():
                continue

            property_value = node_properties_json[property_name]
            if type(property_value) != str:
                continue
            if property_value.startswith(property_value_starter):
                nodes.append(node_json)
        return nodes

    def __find_node_ids_by_index_properties(self, **index_properties):
        result_ids = self.get_node_ids()

        for property_name, property_value in index_properties.items():
            result_ids = result_ids.intersection(
                self.index_collection.find_ids(property_name=property_name,
                                               property_value=property_value))

        return result_ids

    def find_one_node_by_properties(self, **properties):
        indexed_properties = {}
        unindexed_properties = {}
        for property_name, property_value in properties.items():
            if self.index_collection.is_property_indexed(property_name=property_name):
                indexed_properties[property_name] = property_value
            else:
                unindexed_properties[property_name] = property_value

        candidate_node_ids = self.__find_node_ids_by_index_properties(**indexed_properties)

        if len(candidate_node_ids) == 0:
            return None

        if len(unindexed_properties) == 0:
            return self.get_node_info_dict(list(candidate_node_ids)[0])

        for node_id in candidate_node_ids:
            node_json = self.get_node_info_dict(node_id=node_id)
            node_properties_json = node_json[self.DEFAULT_KEY_NODE_PROPERTIES]

            is_match = True
            for property_name, property_value in unindexed_properties.items():
                if property_name not in node_properties_json.keys() or node_properties_json[
                    property_name
                ] != property_value:
                    is_match = False
                    break
            if is_match:
                return node_json

        return None

    def set_relations(self, relations):
        for t in relations:
            self.add_relation(startId=t[self.DEFAULT_KEY_RELATION_START_ID],
                              relationType=t[self.DEFAULT_KEY_RELATION_TYPE],
                              endId=t[self.DEFAULT_KEY_RELATION_END_ID])

    def add_relation(self, startId, relationType, endId):
        """
        add a new relation to graphData, if exist, not add.
        :param startId:
        :param relationType:
        :param endId:
        :return:False, the relation is already exist adding fail, True, add the relation successsful
        """
        # if startId == GraphData.UNASSIGNED_NODE_ID:
        #     return False
        # if endId == GraphData.UNASSIGNED_NODE_ID:
        #     return False

        if startId not in self.graph.nodes or endId not in self.graph.nodes:
            return False

        if self.exist_relation(startId=startId, relationType=relationType, endId=endId):
            return False

        self.__add_one_relation_count(relationType)

        self.graph.add_edge(startId, endId, relationType)
        return True

    def __add_one_relation_count(self, relation_type):
        relation_type_to_num_map = self.get_relation_type_to_num_map()
        relation_type_to_num_map[relation_type] = relation_type_to_num_map.get(relation_type, 0) + 1

    def __remove_one_relation_count(self, relation_type):
        relation_type_to_num_map = self.get_relation_type_to_num_map()
        relation_type_to_num_map[relation_type] = max(0, relation_type_to_num_map.get(relation_type, 0) - 1)

    def add_relation_with_property(self, startId, relationType, endId, **kwargs):
        if startId not in self.graph.nodes or endId not in self.graph.nodes:
            return False

        if self.exist_relation(startId=startId, relationType=relationType, endId=endId):
            return False

        self.__add_one_relation_count(relationType)
        self.graph.add_edge(startId, endId, relationType, **kwargs)
        return True

    def remove_relation(self, startId, relationType, endId):
        if not self.exist_relation(startId=startId, relationType=relationType, endId=endId):
            return False
        self.__remove_one_relation_count(relationType)

        self.graph.remove_edge(startId, endId, relationType)
        return True

    def exist_relation(self, startId, relationType, endId):
        return self.graph.has_edge(startId, endId, relationType)

    def get_relations(self, start_id=None, relation_type=None, end_id=None):
        candidates = None
        if start_id is not None:
            candidates = self.get_all_out_relations(start_id)
        if end_id is not None:
            tmp = self.get_all_in_relations(end_id)
            if candidates is not None:
                candidates &= tmp
            else:
                candidates = tmp
        candidates = self.get_relation_pairs_with_type() if candidates is None else candidates

        if relation_type is not None:
            candidates = set(filter(lambda r: r[1] == relation_type, candidates))
        return candidates

    def get_edge_extra_info(self, start_id, end_id, relation_name, extra_key):
        relation_dict = self.graph.get_edge_data(start_id, end_id)
        if relation_name in relation_dict:
            if extra_key in relation_dict[relation_name]:
                return relation_dict[relation_name][extra_key]
        return ""

    def save_as_json(self, path):
        pass
        # temp = {
        #     "out_relation_map": self.out_relation_map,
        #     "in_relation_map": self.in_relation_map,
        #     "id_to_nodes_map": self.id_to_node_map
        # }
        # json.dump(temp, path)

    def get_node_num(self):
        return len(self.graph.nodes)

    def get_relation_num(self):
        return len(self.graph.edges)

    def get_node_ids(self):
        return set(self.graph.nodes)

    def get_relation_pairs(self):
        # todo:cache the result?
        """
        get the relation list in [(startId,endId)] format
        :return:
        """
        pairs = set(self.graph.edges(keys=False))

        return pairs

    def get_relation_pairs_with_type(self):
        """
        get the relation list in [(startId,endId)] format
        :return:
        """
        pairs = {(r[0], r[2], r[1]) for r in self.graph.edges(keys=True)}
        return pairs

    def get_all_out_relations(self, node_id):
        if node_id not in self.graph.nodes:
            return set()
        return {(r[0], r[2], r[1]) for r in self.graph.out_edges(node_id, keys=True)}

    def get_all_in_relations(self, node_id):
        if node_id not in self.graph.nodes:
            return set()
        return {(r[0], r[2], r[1]) for r in self.graph.in_edges(node_id, keys=True)}

    def update_node_index(self, node_id):

        node_info = self.get_node_info_dict(node_id=node_id)
        node_properties = node_info[self.DEFAULT_KEY_NODE_PROPERTIES]
        self.index_collection.add_node(node_id=node_id
                                       , node_properties=node_properties)

    def get_node_info_dict(self, node_id):
        """
        get the node info dict,
        :param node_id: the node id
        :return:
        """
        return self.graph.nodes.get(node_id, None)

    def get_properties_for_node(self, node_id, key_node_properties=DEFAULT_KEY_NODE_PROPERTIES):
        """
        get the node properties part from node info dict
        :param key_node_properties: specify the key of key_node_properties, default is "properties"
        :param node_id: the node id
        :return: {} if the node not exist
        """
        node_info_dict = self.get_node_info_dict(node_id)
        if node_info_dict is None:
            return {}

        return node_info_dict[key_node_properties]

    def get_labels_for_node(self, node_id, key_node_labels=DEFAULT_KEY_NODE_LABELS):
        """
        get the node properties part from node info dict
        :param key_node_labels: specify the key of node_labels, default is "labels"
        :param node_id: the node id
        :return: [] if the node not exist
        """
        node_info_dict = self.get_node_info_dict(node_id)
        if node_info_dict is None:
            return []

        return node_info_dict[key_node_labels]

    def get_all_labels(self):
        """
        get all labels as set for current node.
        :return: a set of labels.
        """
        return self.label_to_ids_map.keys()

    def get_all_relation_types(self):
        """
        get all relation types in graph data
        :return: a set of relation type strings
        """
        if len(self.get_relation_type_to_num_map()) == 0:
            return set()
        res = set()
        for k in self.get_relation_type_to_num_map():
            res.add(k)
        return res

    def get_relation_count_by_type(self, relation_type):
        relation_type_to_num_map = self.get_relation_type_to_num_map()
        return relation_type_to_num_map.get(relation_type, 0)

    def get_relation_type_to_num_map(self):
        if not hasattr(self, "relation_type_to_num_map"):
            relation_type_to_num_map = self.__count_relation_type_to_num_map()
            self.relation_type_to_num_map = relation_type_to_num_map
        return self.relation_type_to_num_map

    def __count_relation_type_to_num_map(self):
        relation_type_to_num_map = {}
        relation_type_to_relation = {}
        for r in self.get_relation_pairs_with_type():
            if r[1] not in relation_type_to_relation:
                relation_type_to_relation[r[1]] = set()
            relation_type_to_relation[r[1]].add(r)
        for k, v in relation_type_to_relation.items():
            relation_type_to_num_map[k] = len(v)
        return relation_type_to_num_map

    def print_label_count(self):
        print("Label Num=%d" % len(self.label_to_ids_map.keys()))
        for k, v in self.label_to_ids_map.items():
            print("<Label:%r Num:%d>" % (k, len(v)))

    def print_graph_info(self):
        print("----- Graph Info ------")
        print(self)
        self.print_label_count()
        self.print_relation_info()
        print("-----------------------")

    def print_relation_info(self):
        relation_type_to_num_map = self.get_relation_type_to_num_map()
        print("Relation Num=%d" % len(relation_type_to_num_map.keys()))
        for k, v in relation_type_to_num_map.items():
            print("<Relation:%r Num:%d>" % (k, v))

    def __repr__(self):
        return "<GraphData nodeNum=%d relNum=%d maxNodeId=%d>" % (
            self.get_node_num(), self.get_relation_num(), self.max_node_id)

    def subgraph(self, node_ids):
        """
        get a sub graph of graph data which keep only given nodes and relations between nodes
        :param node_ids: the kept node ids in graph
        :return: a graph that keep all things.
        """
        graph_data = deepcopy(self)

        remove_nodes = set(self.get_node_ids()) - node_ids
        for node_id in remove_nodes:
            graph_data.remove_node(node_id)

        return graph_data


class DataExporterAccessor(GraphAccessor):
    def get_all_nodes_not_batch(self, node_label):
        try:
            query = 'Match (n:`{node_label}`) return n'.format(node_label=node_label)

            cursor = self.graph.run(query)
            nodes = []
            for record in cursor:
                nodes.append(record["n"])
            return nodes
        except Exception:
            return []

    def get_all_nodes(self, node_label, step=100000):
        metadata_accessor = MetadataGraphAccessor(self)
        max_node_id = metadata_accessor.get_max_id_for_node()

        nodes = []

        for start_id in range(0, max_node_id, step):
            end_id = min(max_node_id, start_id + step)
            nodes.extend(self.get_all_nodes_in_scope(node_label, start_id=start_id, end_id=end_id))
            print("get nodes step %d-%d" % (start_id, end_id))

        return nodes

    def get_all_nodes_in_scope(self, node_label, start_id, end_id):
        try:
            query = 'Match (n:`{node_label}`) where ID(n)>{start_id} and ID(n)<={end_id} return n'.format(
                node_label=node_label, start_id=start_id, end_id=end_id)

            cursor = self.graph.run(query)
            nodes = []
            for record in cursor:
                nodes.append(record["n"])

            return nodes
        except Exception:
            return []

    def get_all_relation(self, node_label, step=200000):
        metadata_accessor = MetadataGraphAccessor(self)
        max_relation_id = metadata_accessor.get_max_id_for_relation()

        relations = []

        for start_id in range(0, max_relation_id, step):
            end_id = min(max_relation_id, start_id + step)
            relations.extend(self.get_all_relation_in_scope(node_label, start_id=start_id, end_id=end_id))
            print("get relation step %d-%d" % (start_id, end_id))
        return relations

    def get_all_relation_in_scope(self, node_label, start_id, end_id):
        try:
            query = 'Match (n:`{node_label}`)-[r]->(m:`{node_label}`) where ID(r)>{start_id} and ID(r)<={end_id} return ID(n) as startId,ID(m) as endId, type(r) as relationType'.format(
                node_label=node_label, start_id=start_id, end_id=end_id)

            cursor = self.graph.run(query)
            data = cursor.data()
            return data
        except Exception:
            return []

    def get_all_relation_not_batch(self, node_label):
        try:
            query = 'Match (n:`{node_label}`)-[r]->(m:`{node_label}`) return ID(n) as startId,ID(m) as endId, type(r) as relationType'.format(
                node_label=node_label)

            cursor = self.graph.run(query)
            data = cursor.data()
            return data
        except Exception:
            return []


class Neo4jImporter:
    """
    The class is used to import one GraphData obj to a Neo4j database.
    """

    def __init__(self, graph_client: GraphAccessor):
        self.graph_accessor = graph_client

    def import_all_graph_data(self, graph_data: GraphData, clear=True):
        """
        import all data in one GraphData into neo4j and create index on node
        :param graph_data:
        :param clear: clear the graph content, default is not clear the graph contain
        :return:
        """
        index_accessor = IndexGraphAccessor(self.graph_accessor)
        index_accessor.create_index(label=DEFAULT_LABEL, property_name=DEFAULT_PRIMARY_KEY)

        if clear:
            self.graph_accessor.delete_all_relations()
            self.graph_accessor.delete_all_nodes()

        # todo: this is slow, need to speed up, maybe not commit on every step
        all_node_ids = graph_data.get_node_ids()
        for node_id in all_node_ids:
            ## todo: fix this by not using 'properties','labels'
            node_info_dict = graph_data.get_node_info_dict(node_id)
            properties = node_info_dict['properties']
            labels = node_info_dict['labels']
            self.import_one_entity(node_id, properties, labels)

        print("all entity imported")
        relations = graph_data.get_relations()
        for r in relations:
            start_node_id, r_name, end_node_id = r
            start_node = self.graph_accessor.find_node(primary_label=DEFAULT_LABEL,
                                                       primary_property=DEFAULT_PRIMARY_KEY,
                                                       primary_property_value=start_node_id)
            end_node = self.graph_accessor.find_node(primary_label=DEFAULT_LABEL, primary_property=DEFAULT_PRIMARY_KEY,
                                                     primary_property_value=end_node_id)

            if start_node is not None and end_node is not None:
                try:
                    self.graph_accessor.create_relation_without_duplicate(start_node, r_name, end_node)
                except Exception as e:
                    traceback.print_exc()
            else:
                print("fail create relation because start node or end node is none.")
        print("all relation imported")

        print("all graph data import finish")

    @catch_exception
    def import_one_entity(self, node_id, property_dict, labels):
        builder = NodeBuilder()
        builder.add_label(DEFAULT_LABEL).add_property(**property_dict). \
            add_one_property(property_name=DEFAULT_PRIMARY_KEY, property_value=node_id).add_labels(*labels)
        node = builder.build()

        node = self.graph_accessor.create_or_update_node(node, primary_label=DEFAULT_LABEL,
                                                         primary_property=DEFAULT_PRIMARY_KEY)


class GraphDataExporter:
    """
    export specific data
    """

    ## todo: this class should be a opponent class Neo4jImporter, it export Neo4j data as a GraphData obj
    ## todo: take care of the "node_id" problem,
    def __init__(self):
        pass

    def export_all_graph_data(self, graph, node_label):
        accessor = DataExporterAccessor(graph=graph)
        nodes = accessor.get_all_nodes(node_label=node_label)
        graph_data = GraphData()

        for node in nodes:
            labels = [label for label in node.labels]
            graph_data.add_node(node_id=node.identity, node_labels=labels, node_properties=dict(node))

        print("load entity complete, num=%d" % len(nodes))
        relations = accessor.get_all_relation(node_label=node_label)
        print("load relation complete,num=%d" % len(relations))
        graph_data.set_relations(relations=relations)

        return graph_data
