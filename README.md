# 🎯 Interactive Number Classification App

A beautiful Gradio web application that guesses numbers 1-9 through an interactive question-and-answer game with **real-time decision tree visualization**.

## ✨ Features

### 🌳 Dynamic Decision Tree Visualization
- **Real-time updates**: The decision tree graph updates dynamically as you answer each question
- **Color-coded nodes**:
  - 🟡 **Yellow**: Current position in the tree
  - 🟢 **Green**: Final result nodes (1-9)
  - 🩷 **Pink**: Question nodes
  - 🔵 **Blue**: Start node
- **Highlighted path**: Your journey through the tree is shown with bright green arrows
- **Complete tree structure**: See all possible paths and outcomes at once

### 🎮 Interactive Gameplay
- Simple Yes/No questions to narrow down your number
- Questions include:
  - Is your number 5?
  - Is your number even?
  - Is your number a prime number?
  - Is your number divisible by 3?
  - Is your number a perfect square?

### 📊 Visual Feedback
- Answer history tracking
- Status updates at each step
- Clear result display when your number is found

## 🚀 How to Run

1. **Install dependencies**:
   ```bash
   pip install gradio networkx matplotlib pillow
   ```

2. **Run the application**:
   ```bash
   python gradio_app.py
   ```

3. **Open in browser**:
   - The app will automatically open at `http://127.0.0.1:7860`
   - Or manually navigate to the URL shown in the terminal

## 🎯 How to Play

1. **Think of a number** between 1 and 9
2. **Click "Start New Game"**
3. **Answer the questions** by clicking Yes or No
4. **Watch the tree** highlight your path in real-time
5. **Get your result** - the app will guess your number!

## 🛠️ Technical Details

### Technologies Used
- **Gradio**: Modern web UI framework
- **NetworkX**: Graph creation and layout
- **Matplotlib**: Tree visualization rendering
- **Pillow**: Image processing

### Architecture
- `NumberClassifier` class manages game state and logic
- Decision tree is rendered using NetworkX's directed graph
- Hierarchical layout positions nodes for optimal visualization
- Real-time updates through Gradio's reactive interface

## 📝 Classification Logic

The app uses a decision tree to classify numbers 1-9:

- **Prime numbers** (2, 3, 5, 7): Identified first
- **Even numbers** (4, 6, 8): Checked for divisibility by 3 and perfect squares
- **Odd numbers** (1, 9): Checked for perfect squares

Each path through the tree leads to exactly one number from 1-9.

## 🎨 Interface Preview

The application features:
- **Left panel**: Large decision tree visualization (600px height)
- **Right panel**: Game controls and status
  - Current question display
  - Yes/No buttons
  - Start game button
  - Status messages
  - Answer history

## 🔧 Customization

You can modify:
- Tree layout in the `pos` dictionary
- Node colors and sizes
- Question logic in `NumberClassifier`
- UI theme by changing `gr.themes.Soft()` to other Gradio themes

---

**Enjoy playing with the Interactive Number Classifier!** 🎉
