import gradio as gr
import json
from typing import List, Dict, Optional, Tuple
from collections import deque

# Load the family tree data
def load_family_tree():
    with open("game_of_thrones_family_tree.json", "r", encoding="utf-8") as f:
        return json.load(f)

# Initialize the tree
family_tree = load_family_tree()

# Get all character names for dropdown
def get_all_names():
    return sorted(family_tree.keys())

# Query functions
def get_parents(name: str) -> List[str]:
    """Get the parents of a character"""
    if name not in family_tree:
        return []
    return family_tree[name].get("parents", [])

def get_children(name: str) -> List[str]:
    """Get the children of a character"""
    if name not in family_tree:
        return []
    return family_tree[name].get("children", [])

def get_siblings(name: str) -> List[str]:
    """Get siblings (same parents) of a character"""
    parents = get_parents(name)
    if not parents:
        return []
    
    siblings = set()
    for parent in parents:
        children = get_children(parent)
        siblings.update(children)
    
    # Remove the person themselves
    siblings.discard(name)
    return sorted(list(siblings))

def get_ancestors(name: str, max_generations: Optional[int] = None) -> Dict[str, int]:
    """Get all ancestors with their generation distance"""
    if name not in family_tree:
        return {}
    
    results = {}
    queue = deque([(name, 0)])
    visited = {name}
    
    while queue:
        current, dist = queue.popleft()
        
        if max_generations is not None and dist >= max_generations:
            continue
        
        for parent in get_parents(current):
            if parent not in visited:
                visited.add(parent)
                gen = dist + 1
                results[parent] = gen
                queue.append((parent, gen))
    
    return results

def get_descendants(name: str, max_generations: Optional[int] = None) -> Dict[str, int]:
    """Get all descendants with their generation distance"""
    if name not in family_tree:
        return {}
    
    results = {}
    queue = deque([(name, 0)])
    visited = {name}
    
    while queue:
        current, dist = queue.popleft()
        
        if max_generations is not None and dist >= max_generations:
            continue
        
        for child in get_children(current):
            if child not in visited:
                visited.add(child)
                gen = dist + 1
                results[child] = gen
                queue.append((child, gen))
    
    return results

def find_common_ancestor(name1: str, name2: str) -> Optional[Tuple[str, int, int]]:
    """Find the closest common ancestor of two people"""
    ancestors1 = get_ancestors(name1)
    ancestors2 = get_ancestors(name2)
    
    common = set(ancestors1.keys()) & set(ancestors2.keys())
    if not common:
        return None
    
    # Find the closest common ancestor (minimum total distance)
    best = None
    min_dist = float('inf')
    
    for ancestor in common:
        total_dist = ancestors1[ancestor] + ancestors2[ancestor]
        if total_dist < min_dist:
            min_dist = total_dist
            best = (ancestor, ancestors1[ancestor], ancestors2[ancestor])
    
    return best

def get_relationship(name1: str, name2: str) -> str:
    """Determine the relationship between two people"""
    if name1 not in family_tree or name2 not in family_tree:
        return "❌ One or both characters not found"
    
    if name1 == name2:
        return "👤 Same person"
    
    # Check parent-child
    if name2 in get_parents(name1):
        return f"👨‍👦 {name2} is a parent of {name1}"
    if name2 in get_children(name1):
        return f"👶 {name2} is a child of {name1}"
    
    # Check siblings
    siblings1 = get_siblings(name1)
    if name2 in siblings1:
        return f"👫 {name1} and {name2} are siblings"
    
    # Check ancestors/descendants
    ancestors1 = get_ancestors(name1)
    descendants1 = get_descendants(name1)
    
    if name2 in ancestors1:
        gen = ancestors1[name2]
        if gen == 2:
            return f"👴 {name2} is a grandparent of {name1}"
        else:
            return f"🏛️ {name2} is an ancestor of {name1} ({gen} generations back)"
    
    if name2 in descendants1:
        gen = descendants1[name2]
        if gen == 2:
            return f"👶 {name2} is a grandchild of {name1}"
        else:
            return f"👨‍👩‍👧‍👦 {name2} is a descendant of {name1} ({gen} generations forward)"
    
    # Check for common ancestor
    common = find_common_ancestor(name1, name2)
    if common:
        ancestor, dist1, dist2 = common
        return f"🔗 {name1} and {name2} share a common ancestor: {ancestor} ({dist1} gens from {name1}, {dist2} gens from {name2})"
    
    return f"❓ No direct family relationship found between {name1} and {name2}"

# Gradio interface functions
def query_parents(name: str) -> str:
    """Query handler for parents"""
    parents = get_parents(name)
    if not parents:
        return f"❌ {name} has no recorded parents in the database"
    
    result = f"👨‍👩 **Parents of {name}:**\n\n"
    for i, parent in enumerate(parents, 1):
        result += f"{i}. {parent}\n"
    return result

def query_children(name: str) -> str:
    """Query handler for children"""
    children = get_children(name)
    if not children:
        return f"❌ {name} has no recorded children in the database"
    
    result = f"👶 **Children of {name}:**\n\n"
    for i, child in enumerate(sorted(children), 1):
        result += f"{i}. {child}\n"
    return result

def query_siblings(name: str) -> str:
    """Query handler for siblings"""
    siblings = get_siblings(name)
    if not siblings:
        return f"❌ {name} has no recorded siblings in the database"
    
    result = f"👫 **Siblings of {name}:**\n\n"
    for i, sibling in enumerate(siblings, 1):
        result += f"{i}. {sibling}\n"
    return result

def query_ancestors(name: str, max_gen: int = 10) -> str:
    """Query handler for ancestors"""
    ancestors = get_ancestors(name, max_generations=max_gen if max_gen > 0 else None)
    if not ancestors:
        return f"❌ {name} has no recorded ancestors in the database"
    
    result = f"🏛️ **Ancestors of {name}** (up to {max_gen} generations):\n\n"
    
    # Group by generation
    by_gen = {}
    for ancestor, gen in ancestors.items():
        if gen not in by_gen:
            by_gen[gen] = []
        by_gen[gen].append(ancestor)
    
    for gen in sorted(by_gen.keys()):
        result += f"**Generation {gen}:**\n"
        for ancestor in sorted(by_gen[gen]):
            result += f"  • {ancestor}\n"
        result += "\n"
    
    return result

def query_descendants(name: str, max_gen: int = 10) -> str:
    """Query handler for descendants"""
    descendants = get_descendants(name, max_generations=max_gen if max_gen > 0 else None)
    if not descendants:
        return f"❌ {name} has no recorded descendants in the database"
    
    result = f"👨‍👩‍👧‍👦 **Descendants of {name}** (up to {max_gen} generations):\n\n"
    
    # Group by generation
    by_gen = {}
    for descendant, gen in descendants.items():
        if gen not in by_gen:
            by_gen[gen] = []
        by_gen[gen].append(descendant)
    
    for gen in sorted(by_gen.keys()):
        result += f"**Generation {gen}:**\n"
        for descendant in sorted(by_gen[gen]):
            result += f"  • {descendant}\n"
        result += "\n"
    
    return result

def query_relationship(name1: str, name2: str) -> str:
    """Query handler for relationship between two people"""
    return f"**Relationship Analysis:**\n\n{get_relationship(name1, name2)}"

def query_common_ancestor(name1: str, name2: str) -> str:
    """Query handler for common ancestor"""
    common = find_common_ancestor(name1, name2)
    if not common:
        return f"❌ No common ancestor found between {name1} and {name2}"
    
    ancestor, dist1, dist2 = common
    result = f"🔗 **Common Ancestor Analysis:**\n\n"
    result += f"**Closest Common Ancestor:** {ancestor}\n\n"
    result += f"• Distance from {name1}: {dist1} generation(s)\n"
    result += f"• Distance from {name2}: {dist2} generation(s)\n"
    result += f"• Total distance: {dist1 + dist2} generation(s)\n"
    
    return result

# Create Gradio interface
with gr.Blocks(theme=gr.themes.Soft(), title="Game of Thrones Family Tree") as demo:
    gr.Markdown("""
    # ⚔️ Game of Thrones Family Tree Explorer
    
    Explore the complex family relationships of the Seven Kingdoms!
    Select a query type and character(s) to discover their lineage.
    """)
    
    all_names = get_all_names()
    
    with gr.Tabs():
        # Tab 1: Single Character Queries
        with gr.Tab("👤 Character Info"):
            with gr.Row():
                with gr.Column(scale=1):
                    char_select = gr.Dropdown(
                        choices=all_names,
                        label="Select Character",
                        value=all_names[0] if all_names else None,
                        filterable=True
                    )
                    
                    query_type = gr.Radio(
                        choices=["Parents", "Children", "Siblings", "Ancestors", "Descendants"],
                        label="Query Type",
                        value="Parents"
                    )
                    
                    max_gen = gr.Slider(
                        minimum=1,
                        maximum=20,
                        value=10,
                        step=1,
                        label="Max Generations (for Ancestors/Descendants)",
                        visible=False
                    )
                    
                    query_btn = gr.Button("🔍 Query", variant="primary", size="lg")
                
                with gr.Column(scale=2):
                    result_output = gr.Markdown(label="Results")
            
            def update_slider_visibility(query_type):
                return gr.update(visible=query_type in ["Ancestors", "Descendants"])
            
            query_type.change(
                fn=update_slider_visibility,
                inputs=[query_type],
                outputs=[max_gen]
            )
            
            def execute_query(name, qtype, max_g):
                if qtype == "Parents":
                    return query_parents(name)
                elif qtype == "Children":
                    return query_children(name)
                elif qtype == "Siblings":
                    return query_siblings(name)
                elif qtype == "Ancestors":
                    return query_ancestors(name, max_g)
                elif qtype == "Descendants":
                    return query_descendants(name, max_g)
            
            query_btn.click(
                fn=execute_query,
                inputs=[char_select, query_type, max_gen],
                outputs=[result_output]
            )
        
        # Tab 2: Relationship Analysis
        with gr.Tab("🔗 Relationship Finder"):
            with gr.Row():
                with gr.Column(scale=1):
                    char1_select = gr.Dropdown(
                        choices=all_names,
                        label="First Character",
                        value="Jon Snow" if "Jon Snow" in all_names else all_names[0],
                        filterable=True
                    )
                    
                    char2_select = gr.Dropdown(
                        choices=all_names,
                        label="Second Character",
                        value="Daenerys Targaryen" if "Daenerys Targaryen" in all_names else all_names[1] if len(all_names) > 1 else all_names[0],
                        filterable=True
                    )
                    
                    rel_type = gr.Radio(
                        choices=["General Relationship", "Common Ancestor"],
                        label="Analysis Type",
                        value="General Relationship"
                    )
                    
                    rel_btn = gr.Button("🔍 Analyze Relationship", variant="primary", size="lg")
                
                with gr.Column(scale=2):
                    rel_output = gr.Markdown(label="Analysis")
            
            def execute_relationship(name1, name2, rel_type):
                if rel_type == "General Relationship":
                    return query_relationship(name1, name2)
                else:
                    return query_common_ancestor(name1, name2)
            
            rel_btn.click(
                fn=execute_relationship,
                inputs=[char1_select, char2_select, rel_type],
                outputs=[rel_output]
            )
        
        # Tab 3: Database Stats
        with gr.Tab("📊 Database Info"):
            gr.Markdown(f"""
            ### 📈 Database Statistics
            
            - **Total Characters:** {len(family_tree)}
            - **Houses Represented:** Stark, Targaryen, Lannister, Baratheon, Tully, Martell, Tyrell, Greyjoy, Arryn, Frey
            
            ### 🏰 Major Houses
            
            **House Stark** - Winterfell, Kings of the North  
            **House Targaryen** - Dragonstone, Kings of Westeros  
            **House Lannister** - Casterly Rock, Wardens of the West  
            **House Baratheon** - Storm's End, Kings of Westeros  
            
            ### 📝 Available Queries
            
            1. **Parents** - Find the parents of any character
            2. **Children** - List all children of a character
            3. **Siblings** - Find siblings (shared parents)
            4. **Ancestors** - Trace lineage back multiple generations
            5. **Descendants** - Find all descendants forward
            6. **Relationship** - Analyze connection between two characters
            7. **Common Ancestor** - Find shared ancestry
            
            ### 🎯 Example Queries
            
            Try these interesting queries:
            - Parents of **Jon Snow**
            - Ancestors of **Daenerys Targaryen**
            - Relationship between **Jon Snow** and **Daenerys Targaryen**
            - Common ancestor of **Robb Stark** and **Jon Snow**
            """)

if __name__ == "__main__":
    demo.launch(share=False, server_name="127.0.0.1", server_port=7861)
