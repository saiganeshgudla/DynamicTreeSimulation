# ⚔️ Game of Thrones Family Tree Explorer

An interactive web application for exploring family relationships in the Game of Thrones universe.

## 🎯 Features

### 📊 Query Types

1. **Parents** - Find the parents of any character
2. **Children** - List all children of a character  
3. **Siblings** - Find siblings (characters with shared parents)
4. **Ancestors** - Trace lineage back multiple generations
5. **Descendants** - Find all descendants going forward
6. **Relationship Analysis** - Determine how two characters are related
7. **Common Ancestor** - Find shared ancestry between two people

### 🎨 User Interface

**Three Main Tabs:**

1. **👤 Character Info**
   - Dropdown to select any character
   - Radio buttons for query type
   - Adjustable generation depth for ancestor/descendant queries
   - Formatted results with emojis and clear hierarchy

2. **🔗 Relationship Finder**
   - Compare two characters
   - Find their relationship (parent, child, sibling, ancestor, etc.)
   - Discover common ancestors with generation distances

3. **📊 Database Info**
   - Statistics about the database
   - List of major houses
   - Example queries to try
   - Quick reference guide

## 🚀 How to Run

```bash
python got_app.py
```

The app will launch at: **http://127.0.0.1:7861**

## 📝 Example Queries

### Character Info Examples

- **Parents of Jon Snow**
  - Result: Rhaegar Targaryen, Lyanna Stark

- **Ancestors of Daenerys Targaryen**
  - Shows entire Targaryen lineage going back generations

- **Children of Eddard Stark**
  - Lists: Robb, Sansa, Arya, Bran, Rickon

### Relationship Examples

- **Jon Snow ↔ Daenerys Targaryen**
  - Share common ancestors in the Targaryen line
  
- **Robb Stark ↔ Jon Snow**
  - Half-siblings (shared father Eddard, different mothers)

- **Tyrion Lannister ↔ Jaime Lannister**
  - Siblings (shared parents Tywin and Joanna)

## 🏰 Database Coverage

### Major Houses Included

- **House Stark** - Winterfell, Kings of the North
- **House Targaryen** - Dragonstone, Former Kings of Westeros
- **House Lannister** - Casterly Rock, Wardens of the West
- **House Baratheon** - Storm's End
- **House Tully** - Riverrun
- **House Martell** - Sunspear
- **House Tyrell** - Highgarden
- **House Greyjoy** - Pyke
- **House Arryn** - The Eyrie
- **House Frey** - The Twins

### Notable Characters

- **Stark Line**: Brandon the Builder → Rickard → Eddard → Robb, Sansa, Arya, Bran, Rickon
- **Targaryen Line**: Aegon I → Jaehaerys I → Aegon V → Aerys II → Rhaegar, Daenerys, Viserys
- **Jon Snow**: Child of Rhaegar Targaryen and Lyanna Stark

## 🛠️ Technical Details

### Dependencies
- `gradio` - Web UI framework
- Built-in Python modules: `json`, `typing`, `collections`

### Data Structure
- JSON file with parent-child relationships
- Each character has:
  - `parents`: List of parent names
  - `children`: List of child names
  - `meta`: Additional metadata (extensible)

### Algorithms
- **BFS (Breadth-First Search)** for ancestor/descendant traversal
- **Set operations** for sibling detection
- **Shortest path** for common ancestor finding

## 📚 Query Results Format

Results are formatted with:
- **Emojis** for visual clarity (👨‍👩 parents, 👶 children, etc.)
- **Generation numbers** for ancestors/descendants
- **Hierarchical grouping** by generation level
- **Markdown formatting** for readability

## 🎮 Interactive Features

- **Filterable dropdowns** - Search for characters by typing
- **Dynamic controls** - Max generation slider appears only when needed
- **Real-time updates** - Instant query results
- **Clean layout** - Responsive design with clear visual hierarchy

---

**Total Characters**: 57  
**Total Relationships**: Hundreds of parent-child connections  
**Generation Depth**: Up to 20 generations trackable
