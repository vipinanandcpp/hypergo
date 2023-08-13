from typing import List, Dict, Any
import glob
import os
import json
from hypergo.utility import Utility
from collections import OrderedDict
import re
import graphviz

nodes = []

class Node:
    def __init__(self, name):
        self._name = ".".join(sorted(set(name.split("."))))
        self._nodes = []
        nodes.append(self)

    def add_node(self, node):
        self._nodes.append(node)

    def __str__(self):
        return self._name

class Component(Node):
    def __init__(self, config):
        super().__init__(Utility.deep_get(config, "name"))
        self._config = config

    def attr(self):
        config = lambda key: Utility.deep_get(self._config, key, None)
        defined = config("package") and config("lib_func")
        return {
            "fontcolor": "#ffffff" if defined else "#000000",
            "color": "#ffffff80" if defined else "#00000080",
            "style": "solid" if defined else "dashed",
            "penwidth": "4" if defined else "4",
            "fixedsize": "true",
            "shape": "circle",
            "width": "3",
            "label": f'<<table border="0" cellborder="0"><tr><td bgcolor="#0071BD">{str(self)}</td></tr></table>>'
        }


class Edge(Node):
    def attr(self):
        return {
            "fontcolor": "#88A8D8",
            "fixedsize": "false",
            "shape": "none",
            "label": str(self)
        }

def load_configs(folders: List[str]) -> List[Dict[str, Any]]:
    configs = []

    for folder in folders:
        config_files = glob.glob(os.path.join(folder, '**/*.json'), recursive=True)
        for config_file in config_files:
            with open(config_file, 'r', encoding='utf8') as stream:
                config_json = json.load(stream)
                if not isinstance(config_json, list):
                    config_json = [config_json]
                for config in config_json:
                    if config and 'name' in config:
                        configs.append(config)
    return configs




def do_graph(keys: List[str], folders: List[str]) -> None:
    configs: List[Dict[str: Any]] = load_configs(folders)
    for config in configs:
        for ok in keys:
            build_graph(Edge(ok), config, configs)


def build_graph(out_edge, cfg, configs):
    out_key = str(out_edge)
    
    get_key = lambda key: Utility.deep_get(cfg, key)
        
    for input_key in get_key("input_keys"):
        if set(input_key.split(".")).issubset(set(out_key.split("."))):
            in_edge = Edge(input_key)
            out_edge.add_node(in_edge)
            
            component = Component(cfg)
            in_edge.add_node(component)
            
            for output_key in get_key("output_keys"):
                calculated_out_key = re.sub(r"\?", ".".join(set(out_key.split(".")) - set(input_key.split("."))), output_key)
                outbound = Edge(calculated_out_key)

                for config in configs:
                    build_graph(outbound, config, configs)             

                if calculated_out_key != output_key:
                    interim = Edge(output_key)
                    interim.add_node(outbound)
                    outbound = interim
                
                component.add_node(outbound)


def graph(rks: List[str], folders: List[str]) -> None:
    do_graph(rks, folders)

    dot = graphviz.Digraph(comment='Component Diagram')
    dot.attr('graph', bgcolor='#0071BD', nodesep='2', pad='1', rankdir='TB')
    dot.attr('edge', color='#ffffff80')
    dot.attr('node', fontcolor='#ffffff', fontname='courier', fontsize="30")
   
    for node in nodes:
        dot.node(str(node), **node.attr())
    edges = set()
    for node in nodes:
        for child in node._nodes:
            if (str(node) == str(child)):
                continue
            edges.add((str(node), str(child)))
    for edge in edges:
        dot.edge(*edge, color="#ffffff88", arrowsize="1.0", minlen="3")

    dot.render('.graph.gv', view=True)

