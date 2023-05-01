"""Summary."""
import glob
import json
import os
import sys
from typing import Dict, Generator, List, Tuple, Union

import graphviz


def format_component(config: Dict[str, Union[None, str, List[str]]]) -> Tuple[str, str]:
    return (f'component_{config.get("name")}', f'<<table border="0" cellborder="0"><tr><td bgcolor="#0071BD">{config.get("name")}</td></tr></table>>')


def format_topic(typestr: str, config: Dict[str, Union[None, str, List[str]]]) -> Generator[Tuple[str, str], None, None]:
    tlist = config.get(typestr) or []
    if isinstance(tlist, str):
        tlist = [tlist]

    for routingkey_element in tlist:
        routingkey_str = '.'.join(sorted('&#x3a;'.join(routingkey_element.split(':')).split('.')))
        yield (f'routingkey_{routingkey_str}', routingkey_str)


def load_configs(folders: List[str]) -> List[Dict[str, Union[None, str, List[str]]]]:
    configs = []

    for folder in folders:
        config_files = glob.glob(os.path.join(folder, '**/*.json'), recursive=True)
        for config_file in config_files:
            with open(config_file, 'r', encoding='utf8') as stream:
                config = json.load(stream)
                if config and 'name' in config:
                    configs.append(config)
    return configs


def topics(dot: graphviz.Digraph, configs: List[Dict[str, Union[None, str, List[str]]]]) -> None:
    dot.attr('node', shape='none', penwidth='0')

    for config in configs:
        for routing_key_element in format_topic('output_keys', config):
            dot.edge(format_component(config)[0], routing_key_element[0])
            dot.node(*routing_key_element, shape='box')
        for routing_key_element in format_topic('error_output_keys', config):
            dot.edge(format_component(config)[0], routing_key_element[0])
            dot.node(*routing_key_element, shape='octagon')
        for routing_key_element in format_topic('input_keys', config):
            dot.node(*routing_key_element, shape='box')
            dot.edge(routing_key_element[0], format_component(config)[0])


def derived_edges_inner(output_key: Tuple[str, str], in_keys: List[Tuple[str, str]]) -> List[Tuple[str, str]]:
    edges: List[Tuple[str, str]] = []
    for input_key in in_keys:
        if input_key[0] == output_key[0]:
            continue
        if all(key in output_key[1].split('.') for key in input_key[1].split('.')):
            edges.append((output_key[0], input_key[0]))
    return edges


def derived_edges(in_keys: List[Tuple[str, str]], out_keys: List[Tuple[str, str]]) -> List[Tuple[str, str]]:
    edges: List[Tuple[str, str]] = []
    for output_key in out_keys:
        edges.extend(derived_edges_inner(output_key, in_keys))
    return edges


def derived_topics(dot: graphviz.Digraph, configs: List[Dict[str, Union[None, str, List[str]]]]) -> None:
    in_keys: List[Tuple[str, str]] = []
    out_keys: List[Tuple[str, str]] = []
    for config in configs:
        in_keys.extend(format_topic('input_keys', config))
        out_keys.extend(format_topic('output_keys', config))
    for edge in derived_edges(in_keys, out_keys):
        dot.edge(*edge)


def components(dot: graphviz.Digraph, configs: List[Dict[str, Union[None, str, List[str]]]]) -> None:
    dot.attr('node', shape='circle', width='2', color='#ffffff80', penwidth='1', fixedsize='true')

    for config in configs:
        dot.node(*format_component(config))


def graph(folders: List[str]) -> None:
    configs: List[Dict[str, Union[None, str, List[str]]]] = load_configs(folders)

    dot = graphviz.Digraph(comment='Component Diagram')
    dot.attr('graph', bgcolor='#0071BD', nodesep='2', pad='1')
    dot.attr('edge', color='#ffffff80')
    dot.attr('node', fontcolor='#ffffff', fontname='courier')

    components(dot, configs)
    topics(dot, configs)
    derived_topics(dot, configs)

    dot.render('.ergo.gv', view=True)


if __name__ == '__main__':
    graph(sys.argv[1:])
