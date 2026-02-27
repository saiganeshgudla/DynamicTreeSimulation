import gradio as gr
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
import io
from PIL import Image

class NumberClassifier:
    def __init__(self):
        self.reset()
    
    def reset(self):
        """Reset the classification state"""
        self.current_step = 0
        self.path = []
        self.questions = []
        self.answers = []
        self.result = None
        
    def get_current_question(self):
        """Get the current question based on the path taken"""
        if self.current_step == 0:
            return "Is your number 5?"
        
        # Step 1: Check if 5
        if self.current_step == 1:
            if self.answers[0]:  # Yes to "Is it 5?"
                self.result = 5
                return None
            else:
                return "Is your number even?"
        
        # Step 2: Check if even
        if self.current_step == 2:
            return "Is your number a prime number?"
        
        # Step 3: Prime check
        if self.current_step == 3:
            is_even = self.answers[1]
            is_prime = self.answers[2]
            
            if is_even and is_prime:
                self.result = 2
                return None
            elif is_even and not is_prime:
                return "Is your number divisible by 3?"
            elif not is_even and is_prime:
                return "Is your number divisible by 3?"
            else:  # odd and not prime (1, 9)
                return "Is your number greater than 5?"
        
        # Step 4: Additional checks
        if self.current_step == 4:
            is_even = self.answers[1]
            is_prime = self.answers[2]
            last_answer = self.answers[3]
            
            if is_even and not is_prime:
                # Asked about divisible by 3
                if last_answer:
                    self.result = 6
                else:
                    return "Is your number a perfect square?"
            elif not is_even and is_prime:
                # Asked about divisible by 3
                if last_answer:
                    self.result = 3
                else:
                    self.result = 7
            else:  # odd and not prime
                # Asked "Is your number greater than 5?"
                if last_answer:  # Greater than 5 (could be 7 or 9)
                    return "Is your number a perfect square?"
                else:  # Less than 5 (could be 1 or 3)
                    return "Is your number divisible by 3?"
            return None
        
        # Step 5: Final determination
        if self.current_step == 5:
            is_even = self.answers[1]
            is_prime = self.answers[2]
            greater_than_5 = self.answers[3]
            perfect_sq_or_div = self.answers[4]
            
            if is_even and not is_prime:
                # Perfect square check for even numbers
                if perfect_sq_or_div:
                    self.result = 4
                else:
                    self.result = 8
            else:  # odd and not prime
                if greater_than_5:
                    # Asked about perfect square
                    if perfect_sq_or_div:
                        self.result = 9
                    else:
                        self.result = 7
                else:
                    # Asked about divisible by 3
                    if perfect_sq_or_div:
                        self.result = 3
                    else:
                        self.result = 1
            return None
        
        return None
    
    def answer_question(self, answer):
        """Process an answer and move to next question"""
        self.answers.append(answer)
        self.current_step += 1
        return self.get_current_question()


def create_decision_tree_graph(classifier):
    """Create a visual decision tree showing the current path"""
    fig = Figure(figsize=(16, 11))
    ax = fig.add_subplot(111)
    
    # Create directed graph
    G = nx.DiGraph()
    
    # Define the complete decision tree structure
    nodes = {
        "start": "Start\n(1-9)",
        "q1": "Is it 5?",
        "5": "✓ 5",
        "q2": "Is it even?",
        "q3_even": "Prime?",
        "q3_odd": "Prime?",
        "2": "✓ 2",
        "q4_even": "Div by 3?",
        "6": "✓ 6",
        "q5_even": "Perfect\nSquare?",
        "4": "✓ 4",
        "8": "✓ 8",
        "q4_odd_prime": "Div by 3?",
        "3": "✓ 3",
        "7": "✓ 7",
        "q4_odd_not": "> 5?",
        "q5_odd_gt5": "Perfect\nSquare?",
        "q5_odd_lt5": "Div by 3?",
        "9": "✓ 9",
        "7_2": "✓ 7",
        "3_2": "✓ 3",
        "1": "✓ 1"
    }
    
    # Add all nodes
    for node_id, label in nodes.items():
        G.add_node(node_id, label=label)
    
    # Define edges
    edges = [
        ("start", "q1", ""),
        ("q1", "5", "Yes"),
        ("q1", "q2", "No"),
        ("q2", "q3_even", "Yes"),
        ("q2", "q3_odd", "No"),
        ("q3_even", "2", "Yes"),
        ("q3_even", "q4_even", "No"),
        ("q4_even", "6", "Yes"),
        ("q4_even", "q5_even", "No"),
        ("q5_even", "4", "Yes"),
        ("q5_even", "8", "No"),
        ("q3_odd", "q4_odd_prime", "Yes"),
        ("q3_odd", "q4_odd_not", "No"),
        ("q4_odd_prime", "3", "Yes"),
        ("q4_odd_prime", "7", "No"),
        ("q4_odd_not", "q5_odd_gt5", "Yes"),
        ("q4_odd_not", "q5_odd_lt5", "No"),
        ("q5_odd_gt5", "9", "Yes"),
        ("q5_odd_gt5", "7_2", "No"),
        ("q5_odd_lt5", "3_2", "Yes"),
        ("q5_odd_lt5", "1", "No"),
    ]
    
    for src, dst, label in edges:
        G.add_edge(src, dst, label=label)
    
    # Create hierarchical layout
    pos = {
        "start": (8, 11),
        "q1": (8, 10),
        "5": (3, 9),
        "q2": (11, 9),
        "q3_even": (9, 8),
        "q3_odd": (13, 8),
        "2": (7, 7),
        "q4_even": (10, 7),
        "6": (9, 6),
        "q5_even": (11, 6),
        "4": (10, 5),
        "8": (12, 5),
        "q4_odd_prime": (12, 7),
        "3": (11.5, 6.5),
        "7": (12.5, 6.5),
        "q4_odd_not": (14, 7),
        "q5_odd_gt5": (13, 6),
        "q5_odd_lt5": (15, 6),
        "9": (12.5, 5),
        "7_2": (13.5, 5),
        "3_2": (14.5, 5),
        "1": "15.5, 5",
    }
    
    # Determine current path
    current_path_edges = []
    current_node = "start"
    
    if classifier.current_step > 0:
        current_path_edges.append(("start", "q1"))
        
        if classifier.current_step >= 1 and len(classifier.answers) >= 1:
            if classifier.answers[0]:
                current_path_edges.append(("q1", "5"))
                current_node = "5"
            else:
                current_path_edges.append(("q1", "q2"))
                current_node = "q2"
                
                if classifier.current_step >= 2 and len(classifier.answers) >= 2:
                    is_even = classifier.answers[1]
                    if is_even:
                        current_path_edges.append(("q2", "q3_even"))
                        current_node = "q3_even"
                    else:
                        current_path_edges.append(("q2", "q3_odd"))
                        current_node = "q3_odd"
                    
                    if classifier.current_step >= 3 and len(classifier.answers) >= 3:
                        is_prime = classifier.answers[2]
                        
                        if is_even and is_prime:
                            current_path_edges.append(("q3_even", "2"))
                            current_node = "2"
                        elif is_even and not is_prime:
                            current_path_edges.append(("q3_even", "q4_even"))
                            current_node = "q4_even"
                            
                            if classifier.current_step >= 4 and len(classifier.answers) >= 4:
                                div_by_3 = classifier.answers[3]
                                if div_by_3:
                                    current_path_edges.append(("q4_even", "6"))
                                    current_node = "6"
                                else:
                                    current_path_edges.append(("q4_even", "q5_even"))
                                    current_node = "q5_even"
                                    
                                    if classifier.current_step >= 5 and len(classifier.answers) >= 5:
                                        perfect_sq = classifier.answers[4]
                                        if perfect_sq:
                                            current_path_edges.append(("q5_even", "4"))
                                            current_node = "4"
                                        else:
                                            current_path_edges.append(("q5_even", "8"))
                                            current_node = "8"
                        
                        elif not is_even and is_prime:
                            current_path_edges.append(("q3_odd", "q4_odd_prime"))
                            current_node = "q4_odd_prime"
                            
                            if classifier.current_step >= 4 and len(classifier.answers) >= 4:
                                div_by_3 = classifier.answers[3]
                                if div_by_3:
                                    current_path_edges.append(("q4_odd_prime", "3"))
                                    current_node = "3"
                                else:
                                    current_path_edges.append(("q4_odd_prime", "7"))
                                    current_node = "7"
                        
                        else:  # not even and not prime
                            current_path_edges.append(("q3_odd", "q4_odd_not"))
                            current_node = "q4_odd_not"
                            
                            if classifier.current_step >= 4 and len(classifier.answers) >= 4:
                                greater_than_5 = classifier.answers[3]
                                if greater_than_5:
                                    current_path_edges.append(("q4_odd_not", "q5_odd_gt5"))
                                    current_node = "q5_odd_gt5"
                                    
                                    if classifier.current_step >= 5 and len(classifier.answers) >= 5:
                                        perfect_sq = classifier.answers[4]
                                        if perfect_sq:
                                            current_path_edges.append(("q5_odd_gt5", "9"))
                                            current_node = "9"
                                        else:
                                            current_path_edges.append(("q5_odd_gt5", "7_2"))
                                            current_node = "7_2"
                                else:
                                    current_path_edges.append(("q4_odd_not", "q5_odd_lt5"))
                                    current_node = "q5_odd_lt5"
                                    
                                    if classifier.current_step >= 5 and len(classifier.answers) >= 5:
                                        div_by_3 = classifier.answers[4]
                                        if div_by_3:
                                            current_path_edges.append(("q5_odd_lt5", "3_2"))
                                            current_node = "3_2"
                                        else:
                                            current_path_edges.append(("q5_odd_lt5", "1"))
                                            current_node = "1"
    
    # Draw edges
    for src, dst, label in edges:
        if (src, dst) in current_path_edges:
            nx.draw_networkx_edges(G, pos, [(src, dst)], 
                                 edge_color='#00ff00', width=4, 
                                 arrowsize=20, ax=ax, arrows=True,
                                 connectionstyle="arc3,rad=0.1")
        else:
            nx.draw_networkx_edges(G, pos, [(src, dst)], 
                                 edge_color='#666666', width=1.5, 
                                 arrowsize=15, ax=ax, arrows=True,
                                 connectionstyle="arc3,rad=0.1", alpha=0.3)
    
    # Draw nodes
    result_nodes = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "3_2", "7_2"]
    
    for node in G.nodes():
        if node == current_node:
            color = '#ffff00'  # Yellow for current
            size = 3000
        elif node in result_nodes:
            color = '#90EE90'  # Light green for results
            size = 2500
        elif node == "start":
            color = '#87CEEB'  # Sky blue for start
            size = 2500
        else:
            color = '#FFB6C1'  # Light pink for questions
            size = 2500
        
        nx.draw_networkx_nodes(G, pos, [node], node_color=color, 
                             node_size=size, ax=ax, alpha=0.9)
    
    # Draw labels
    labels = {node: nodes[node] for node in G.nodes()}
    nx.draw_networkx_labels(G, pos, labels, font_size=9, 
                           font_weight='bold', ax=ax)
    
    # Draw edge labels
    edge_labels = {(src, dst): label for src, dst, label in edges if label}
    nx.draw_networkx_edge_labels(G, pos, edge_labels, font_size=8, ax=ax)
    
    ax.set_title("Decision Tree - Number Classification (1-9)", 
                fontsize=16, fontweight='bold', pad=20)
    ax.axis('off')
    ax.set_xlim(0, 18)
    ax.set_ylim(3, 12)
    
    # Convert to image
    buf = io.BytesIO()
    fig.savefig(buf, format='png', dpi=100, bbox_inches='tight', 
                facecolor='white', edgecolor='none')
    buf.seek(0)
    img = Image.open(buf)
    plt.close(fig)
    
    return img


# Global classifier instance
classifier = NumberClassifier()


def start_game():
    """Start a new game"""
    classifier.reset()
    question = classifier.get_current_question()
    tree_img = create_decision_tree_graph(classifier)
    
    return (
        tree_img,
        question,
        gr.update(visible=True, interactive=True),
        gr.update(visible=True, interactive=True),
        gr.update(visible=False),
        "Game started! Answer the questions to find your number.",
        ""
    )


def answer_yes():
    """Handle Yes answer"""
    return process_answer(True)


def answer_no():
    """Handle No answer"""
    return process_answer(False)


def process_answer(answer):
    """Process the user's answer"""
    current_question = classifier.questions[-1] if classifier.questions else classifier.get_current_question()
    
    next_question = classifier.answer_question(answer)
    tree_img = create_decision_tree_graph(classifier)
    
    answer_text = "Yes" if answer else "No"
    
    # Build history
    if current_question:
        classifier.questions.append(current_question)
    
    history_lines = []
    for i in range(len(classifier.answers)):
        if i < len(classifier.questions):
            history_lines.append(f"Q: {classifier.questions[i]}")
            history_lines.append(f"A: {'Yes' if classifier.answers[i] else 'No'}\n")
    
    history = "\n".join(history_lines)
    
    if classifier.result is not None:
        # Game over
        return (
            tree_img,
            f"🎉 Your number is: {classifier.result}",
            gr.update(visible=False),
            gr.update(visible=False),
            gr.update(visible=True),
            f"Classification complete! Your number is {classifier.result}.",
            history
        )
    else:
        # Continue game
        return (
            tree_img,
            next_question,
            gr.update(visible=True, interactive=True),
            gr.update(visible=True, interactive=True),
            gr.update(visible=False),
            "Keep answering...",
            history
        )


# Create Gradio interface
with gr.Blocks(theme=gr.themes.Soft(), title="Number Classifier") as demo:
    gr.Markdown("""
    # 🎯 Interactive Number Classification (1-9)
    Think of a number between 1 and 9, and I'll guess it by asking questions!
    Watch the decision tree highlight your path in real-time.
    """)
    
    with gr.Row():
        with gr.Column(scale=2):
            tree_output = gr.Image(label="Decision Tree Visualization", 
                                  type="pil", height=650)
        
        with gr.Column(scale=1):
            gr.Markdown("### 🎮 Game Controls")
            
            question_display = gr.Textbox(
                label="Current Question",
                value="Click 'Start Game' to begin!",
                interactive=False,
                lines=2
            )
            
            with gr.Row():
                yes_btn = gr.Button("✅ Yes", variant="primary", 
                                   visible=False, size="lg")
                no_btn = gr.Button("❌ No", variant="secondary", 
                                  visible=False, size="lg")
            
            start_btn = gr.Button("🎮 Start New Game", 
                                 variant="primary", size="lg")
            
            status_display = gr.Textbox(
                label="Status",
                value="Ready to play!",
                interactive=False
            )
            
            gr.Markdown("### 📝 Answer History")
            history_display = gr.Textbox(
                label="Your Answers",
                value="",
                interactive=False,
                lines=10
            )
    
    # Event handlers
    start_btn.click(
        fn=start_game,
        outputs=[tree_output, question_display, yes_btn, no_btn, 
                start_btn, status_display, history_display]
    )
    
    yes_btn.click(
        fn=answer_yes,
        outputs=[tree_output, question_display, yes_btn, no_btn, 
                start_btn, status_display, history_display]
    )
    
    no_btn.click(
        fn=answer_no,
        outputs=[tree_output, question_display, yes_btn, no_btn, 
                start_btn, status_display, history_display]
    )


if __name__ == "__main__":
    demo.launch(share=False, server_name="127.0.0.1", server_port=7860)
