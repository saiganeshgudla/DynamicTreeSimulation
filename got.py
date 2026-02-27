# Retry: fixed the module_code construction bug and re-run the population + export + demo.

import json
from collections import deque, defaultdict
from dataclasses import dataclass, field
from typing import Dict, List, Set, Tuple, Optional

@dataclass
class Person:
    name: str
    parents: Set[str] = field(default_factory=set)
    children: Set[str] = field(default_factory=set)
    meta: Dict = field(default_factory=dict)

class FamilyTree:
    def __init__(self):
        self.nodes: Dict[str, Person] = {}

    def _ensure(self, name: str) -> Person:
        if name not in self.nodes:
            self.nodes[name] = Person(name=name)
        return self.nodes[name]

    def add_person(self, name: str, parents: Optional[List[str]] = None, meta: Optional[Dict] = None):
        p = self._ensure(name)
        if meta:
            p.meta.update(meta)
        if parents:
            for par in parents:
                par_node = self._ensure(par)
                par_node.children.add(name)
                p.parents.add(par)

    def add_parent_child(self, parent: str, child: str):
        self._ensure(parent).children.add(child)
        self._ensure(child).parents.add(parent)

    def get_parents(self, name: str) -> List[str]:
        if name not in self.nodes:
            return []
        return list(self.nodes[name].parents)

    def get_children(self, name: str) -> List[str]:
        if name not in self.nodes:
            return []
        return list(self.nodes[name].children)

    def _bfs_ancestors(self, name: str, max_generations: Optional[int] = None) -> Dict[str, Tuple[int, List[str]]]:
        if name not in self.nodes:
            return {}
        results: Dict[str, Tuple[int, List[str]]] = {}
        q = deque()
        q.append((name, 0, [name]))
        visited = set([name])
        while q:
            cur, dist, path = q.popleft()
            if max_generations is not None and dist >= max_generations:
                continue
            for par in self.get_parents(cur):
                if par in visited:
                    # still record if path shorter isn't necessary here
                    pass
                visited.add(par)
                new_path = path + [par]
                gen = dist + 1
                if par not in results or gen < results[par][0]:
                    results[par] = (gen, new_path)
                q.append((par, gen, new_path))
        return results

    def get_ancestors(self, name: str, max_generations: Optional[int] = None) -> Dict[str, int]:
        raw = self._bfs_ancestors(name, max_generations=max_generations)
        return {k: v[0] for k, v in raw.items()}

    def get_ancestors_with_paths(self, name: str, max_generations: Optional[int] = None) -> Dict[str, Tuple[int, List[str]]]:
        return self._bfs_ancestors(name, max_generations=max_generations)

    def get_ancestor_path(self, name: str, ancestor: str) -> Optional[List[str]]:
        raw = self._bfs_ancestors(name)
        if ancestor in raw:
            return raw[ancestor][1]
        return None

    def get_descendants(self, name: str, max_generations: Optional[int] = None) -> Dict[str, int]:
        if name not in self.nodes:
            return {}
        results: Dict[str, int] = {}
        q = deque([(name, 0)])
        visited = set([name])
        while q:
            cur, dist = q.popleft()
            if max_generations is not None and dist >= max_generations:
                continue
            for ch in self.get_children(cur):
                if ch in visited:
                    continue
                visited.add(ch)
                gen = dist + 1
                results[ch] = gen
                q.append((ch, gen))
        return results

    def export_json(self) -> Dict:
        data = {}
        for name, person in self.nodes.items():
            data[name] = {
                "parents": list(person.parents),
                "children": list(person.children),
                "meta": person.meta,
            }
        return data

    def save_json(self, filepath: str):
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(self.export_json(), f, indent=2, ensure_ascii=False)

    def load_json(self, filepath: str):
        with open(filepath, "r", encoding="utf-8") as f:
            data = json.load(f)
        self.nodes.clear()
        for name, rec in data.items():
            self.add_person(name, parents=rec.get("parents", []), meta=rec.get("meta", {}))

# Populate the tree (same nodes as prior but with corrected module save)
ft = FamilyTree()

# Stark
ft.add_person("Brandon the Builder")
ft.add_person("Edwyle Stark", parents=["Brandon the Builder"])
ft.add_person("Rickard Stark", parents=["Edwyle Stark"])
ft.add_person("Lyarra Stark")
ft.add_person("Brandon Stark", parents=["Rickard Stark", "Lyarra Stark"])
ft.add_person("Eddard Stark", parents=["Rickard Stark", "Lyarra Stark"])
ft.add_person("Lyanna Stark", parents=["Rickard Stark", "Lyarra Stark"])
ft.add_person("Benjen Stark", parents=["Rickard Stark", "Lyarra Stark"])
ft.add_person("Catelyn Tully")
ft.add_person("Robb Stark", parents=["Eddard Stark", "Catelyn Tully"])
ft.add_person("Sansa Stark", parents=["Eddard Stark", "Catelyn Tully"])
ft.add_person("Arya Stark", parents=["Eddard Stark", "Catelyn Tully"])
ft.add_person("Bran Stark", parents=["Eddard Stark", "Catelyn Tully"])
ft.add_person("Rickon Stark", parents=["Eddard Stark", "Catelyn Tully"])
ft.add_person("Jon Snow", parents=["Rhaegar Targaryen", "Lyanna Stark"])

# Targaryen
ft.add_person("Aegon I Targaryen")
ft.add_person("Jaehaerys I Targaryen", parents=["Aegon I Targaryen"])
ft.add_person("Aegon V Targaryen", parents=["Jaehaerys I Targaryen"])
ft.add_person("Jaehaerys II Targaryen", parents=["Aegon V Targaryen"])
ft.add_person("Aerys II Targaryen", parents=["Jaehaerys II Targaryen"])
ft.add_person("Rhaella Targaryen", parents=["Jaehaerys II Targaryen"])
ft.add_person("Rhaegar Targaryen", parents=["Aerys II Targaryen", "Rhaella Targaryen"])
ft.add_person("Elia Martell")
ft.add_person("Rhaenys Targaryen", parents=["Rhaegar Targaryen", "Elia Martell"])
ft.add_person("Aegon (young) Targaryen", parents=["Rhaegar Targaryen", "Elia Martell"])
ft.add_person("Viserys Targaryen", parents=["Aerys II Targaryen", "Rhaella Targaryen"])
ft.add_person("Daenerys Targaryen", parents=["Aerys II Targaryen", "Rhaella Targaryen"])

# Lannister
ft.add_person("Tytos Lannister")
ft.add_person("Joanna Lannister")
ft.add_person("Tywin Lannister", parents=["Tytos Lannister"])
ft.add_person("Jaime Lannister", parents=["Tywin Lannister", "Joanna Lannister"])
ft.add_person("Cersei Lannister", parents=["Tywin Lannister", "Joanna Lannister"])
ft.add_person("Tyrion Lannister", parents=["Tywin Lannister", "Joanna Lannister"])

# Baratheon
ft.add_person("Orys Baratheon")
ft.add_person("Steffon Baratheon")
ft.add_person("Robert Baratheon", parents=["Steffon Baratheon"])
ft.add_person("Stannis Baratheon", parents=["Steffon Baratheon"])
ft.add_person("Renly Baratheon", parents=["Steffon Baratheon"])

# Tully
ft.add_person("Hoster Tully")
ft.add_person("Minisa Whent")
ft.add_person("Catelyn Tully", parents=["Hoster Tully", "Minisa Whent"])
ft.add_person("Lysa Tully", parents=["Hoster Tully", "Minisa Whent"])
ft.add_person("Edmure Tully", parents=["Hoster Tully", "Minisa Whent"])
ft.add_person("Robin Arryn", parents=["Lysa Tully"])

# Martell
ft.add_person("Doran Martell")
ft.add_person("Oberyn Martell", parents=["Doran Martell"])
ft.add_person("Elia Martell", parents=["Doran Martell"])

# Tyrell
ft.add_person("Mace Tyrell")
ft.add_person("Olenna Tyrell")
ft.add_person("Margaery Tyrell", parents=["Mace Tyrell", "Olenna Tyrell"])
ft.add_person("Loras Tyrell", parents=["Mace Tyrell", "Olenna Tyrell"])

# Greyjoy
ft.add_person("Balon Greyjoy")
ft.add_person("Theon Greyjoy", parents=["Balon Greyjoy"])
ft.add_person("Asha Greyjoy", parents=["Balon Greyjoy"])

# Arryn
ft.add_person("Jon Arryn")
ft.add_person("Robert Arryn", parents=["Jon Arryn", "Lysa Tully"])

# Frey
ft.add_person("Walder Frey")
ft.add_person("Stevron Frey", parents=["Walder Frey"])
ft.add_person("Roslin Frey", parents=["Walder Frey"])

# Save JSON export and a module file
json_path = "game_of_thrones_family_tree.json"
ft.save_json(json_path)

data_blob = json.dumps(ft.export_json(), indent=2, ensure_ascii=False)
module_code = (
    "# Auto-generated minimal Game of Thrones Family Tree data module\n\n"
    "DATA_JSON = " + repr(data_blob) + "\n\n"
    "def load_data():\n"
    "    import json\n"
    "    return json.loads(DATA_JSON)\n\n"
    "if __name__ == '__main__':\n"
    "    print('This module contains GAME OF THRONES family data (partial).\\n')\n"
    "    d = load_data()\n"
    "    print('Loaded', len(d), 'nodes')\n"
)

module_path = "game_of_thrones_family_tree.py"
with open(module_path, "w", encoding="utf-8") as f:
    f.write(module_code)

# Demonstration queries
print("=== Demo queries ===")
print("Parents of Jon Snow ->", ft.get_parents("Jon Snow"))
print("Children of Rhaegar Targaryen ->", ft.get_children("Rhaegar Targaryen"))
print("Ancestors of Jon Snow (name -> generations) ->", ft.get_ancestors("Jon Snow"))

anc_with_paths = ft.get_ancestors_with_paths("Jon Snow")
print("\nAncestors of Jon Snow with paths (showing up to 10):")
count = 0
for anc, (gen, path) in sorted(anc_with_paths.items(), key=lambda x: (x[1][0], x[0])):
    print(f" - {anc} : {gen} gen(s) via {' -> '.join(path)}")
    count += 1
    if count >= 10:
        break

print("\nPath from Jon Snow to Aegon V Targaryen:", ft.get_ancestor_path("Jon Snow", "Aegon V Targaryen"))
print("Descendants of Aerys II Targaryen (up to 3 gen):", ft.get_descendants("Aerys II Targaryen", max_generations=3))

print(f"\n✅ Files saved: {json_path} and {module_path}")
