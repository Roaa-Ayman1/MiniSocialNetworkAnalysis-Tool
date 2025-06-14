import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from tkinter import filedialog
import networkx as nx
import preprocessing
import Algorithms
import tkinter as tk
from tkinter import ttk, colorchooser
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


G = nx.DiGraph()


def homePage():
    root = tk.Tk()
    root.geometry("600x400")
    root.title("Social Network Analysis")

    # Create a main frame with padding
    main_frame = tk.Frame(root, padx=20, pady=20)
    main_frame.pack(fill=tk.BOTH, expand=True)

    # Title with better styling
    title_label = tk.Label(main_frame, text="Social Network Analysis", font=("Arial", 16, "bold"))
    title_label.pack(pady=10)
    tk.Button(main_frame, text="Visualize Graph", command=visualize_graph_window, bg="#2196F3", fg="white").pack(pady=10)
    
    # Graph type selection frame
    graph_type_frame = tk.LabelFrame(main_frame, text="Graph Type", padx=10, pady=10)
    graph_type_frame.pack(fill=tk.X, pady=10)

    # Radio button variable
    graph_type = tk.StringVar(value="directed")  # Default to directed

    def radio_click1():
        global G
        G = nx.Graph()
        graph_type.set("undirected")

    def radio_click2():
        global G
        G = nx.DiGraph()
        graph_type.set("directed")

    # Create the radio buttons
    option1 = tk.Radiobutton(graph_type_frame, text="Undirected", value="undirected", variable=graph_type,
                             command=radio_click1)
    option2 = tk.Radiobutton(graph_type_frame, text="Directed", value="directed", variable=graph_type,
                             command=radio_click2)

    # Pack the radio buttons side by side
    option1.pack(side=tk.LEFT, padx=20)
    option2.pack(side=tk.LEFT, padx=20)

    # Data import frame
    data_frame = tk.LabelFrame(main_frame, text="Data Import", padx=10, pady=10)
    data_frame.pack(fill=tk.X, pady=10)

    # Status labels
    nodes_status = tk.StringVar(value="No nodes file selected")
    edges_status = tk.StringVar(value="No edges file selected")

    nodes_label = tk.Label(data_frame, textvariable=nodes_status)
    nodes_label.grid(row=0, column=1, sticky=tk.W, padx=5)

    edges_label = tk.Label(data_frame, textvariable=edges_status)
    edges_label.grid(row=1, column=1, sticky=tk.W, padx=5)

    def button1_click():
        # Show a file dialog window and get the selected file path
        node_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
        if node_path:
            preprocessing.readNodes(G, node_path)
            nodes_status.set(f"Nodes file: {node_path.split('/')[-1]}")

    def button2_click():
        # Show a file dialog window and get the selected file path
        edges_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
        if edges_path:
            preprocessing.readEdges(G, edges_path)
            edges_status.set(f"Edges file: {edges_path.split('/')[-1]}")

    button1 = tk.Button(data_frame, text="Browse Nodes", command=button1_click, width=15)
    button1.grid(row=0, column=0, padx=5, pady=5)

    button2 = tk.Button(data_frame, text="Browse Edges", command=button2_click, width=15)
    button2.grid(row=1, column=0, padx=5, pady=5)

    def Next():
        # Navigate to algorithms page
        print("Navigating to algorithm selection")
        select_algorithm(root)

    # Navigation button with better styling
    button_frame = tk.Frame(main_frame)
    button_frame.pack(pady=20)

    next_button = tk.Button(button_frame, text="Next", command=Next, width=15,
                            bg="#4CAF50", fg="white", font=("Arial", 10, "bold"))
    next_button.pack()

    # Add a status bar
    status_bar = tk.Label(root, text="Ready", bd=1, relief=tk.SUNKEN, anchor=tk.W)
    status_bar.pack(side=tk.BOTTOM, fill=tk.X)

    root.mainloop()


def select_algorithm(root):
    ty = "Directed" if G.is_directed() else "Undirected"
    print("Type of the graph is " + ty)

    # Create a new top-level window
    new_window = tk.Toplevel(root)
    new_window.geometry("800x600")
    new_window.title("Algorithm Selection")

    # Main container with padding
    main_frame = tk.Frame(new_window, padx=20, pady=20)
    main_frame.pack(fill=tk.BOTH, expand=True)

    # Title
    title_label = tk.Label(main_frame, text="Select Analysis Technique", font=("Arial", 14, "bold"))
    title_label.pack(pady=10)

    # Graph info
    info_label = tk.Label(main_frame, text=f"Graph Type: {ty}", font=("Arial", 10))
    info_label.pack()

    # Create categories for algorithms
    categories = {
        "Community Detection": [
            "Louvain algorithm",
            "Modularity",
            "Conductance",
            "NMI",
            "Girvan_Newman_one_level",
            "Girvan_Newman_all_level",
            "Community Detection Comparison"
        ],
        "Centrality Measures": [
            "Page rank",
            "Degree centrality",
            "Closeness centrality",
            "Betweenness centrality"
        ],
        "Graph Visualization": [
            "Fruchterman Reingold",
            "Radial Layout",
            "Tree Layout",
            "Fruchterman Reingold animated"
        ],
        "Graph Analysis": [
            "Graph Metrics and Statistics",
            "Degree filter"
        ],
        "Graph Partitioning": [
            "Gender",
            "class",
            "partitioning by degree centrality",
            "partitioning by closeness centrality"
        ]
    }

    # Create a frame for the algorithm categories
    categories_frame = tk.Frame(main_frame)
    categories_frame.pack(pady=20, fill=tk.BOTH, expand=True)

    # Dictionary to store the comboboxes
    comboboxes = {}
    selected_options = {}

    # Create a combobox for each category
    row = 0
    for category, algorithms in categories.items():
        # Create a label frame for each category
        category_frame = tk.LabelFrame(categories_frame, text=category, padx=10, pady=10)
        category_frame.grid(row=row, column=0, sticky="ew", padx=5, pady=5)

        # Create a StringVar to store the selected option
        selected_option = tk.StringVar()
        selected_options[category] = selected_option

        # Create the combobox
        combobox = ttk.Combobox(category_frame, values=algorithms, textvariable=selected_option, width=30)
        combobox.pack(side=tk.LEFT, padx=10, pady=5)
        comboboxes[category] = combobox

        # Set default value
        if algorithms:
            selected_option.set(algorithms[0])

        # Create an execute button for each category
        execute_button = tk.Button(
            category_frame,
            text="Execute",
            command=lambda cat=category: execute_algorithm(cat, selected_options[cat].get()),
            bg="#007BFF",
            fg="white"
        )
        execute_button.pack(side=tk.LEFT, padx=10, pady=5)

        row += 1

    # Function to execute the selected algorithm
    def execute_algorithm(category, algorithm):
        print(f"Executing {algorithm} from {category}")

        if algorithm == "Louvain algorithm":
            Algorithms.Louvain_algorithm(G)
        elif algorithm == "Page rank":
            Algorithms.PageRank(G)
        elif algorithm == "Degree centrality":
            Algorithms.Degree_Centrality(G)
        elif algorithm == "Closeness centrality":
            Algorithms.Closeness_Centrality(G)
        elif algorithm == "Betweenness centrality":
            Algorithms.Betweenness_Centrality(G)
        elif algorithm == "Modularity":
            Algorithms.Modularity(G)
        elif algorithm == "Conductance":
            Algorithms.Conductance(G)
        elif algorithm == "NMI":
            Algorithms.NMI(G)
        elif algorithm == "Fruchterman Reingold":
            Algorithms.Fruchterman_Reingold(G)
        elif algorithm == "Tree Layout":
            Algorithms.Tree_Layout(G)
        elif algorithm == "Radial Layout":
            Algorithms.Radial_Layout(G)
        elif algorithm == "Girvan_Newman_one_level":
            Algorithms.Girvan_Newman_algorithm_single_level(G)
        elif algorithm == "Girvan_Newman_all_level":
            g = nx.karate_club_graph()
            communities, num_communities, modularity = Algorithms.Girvan_Newman_algorithm(g)
            print(num_communities, modularity)
            # Plotting the final communities
            plt.figure(figsize=(10, 6))
            pos = nx.spring_layout(g)
            for i, community in enumerate(communities[-1]):
                nx.draw_networkx_nodes(g, pos, nodelist=community, node_color=f'C{i}', label=f'Community {i + 1}')
            nx.draw_networkx_edges(g, pos, alpha=0.5)
            plt.title('Final Communities Detected by Girvan-Newman Algorithm')
            plt.legend()
            plt.show()
        elif algorithm == "Community Detection Comparison":
            Algorithms.Comparing_Community_Detection(G)
        elif algorithm == "Graph Metrics and Statistics":
            Algorithms.Statistics_Of_Graph_Metrics(G)
        elif algorithm == "Gender":
            Algorithms.partition_graph(G, "gender")
        elif algorithm == "class":
            Algorithms.partition_graph(G, "class")
        elif algorithm == "Fruchterman Reingold animated":
            Algorithms.Fruchterman_Reingold_animated(G, gravity=0.1, speed=0.1)
        elif algorithm == "Degree filter":
            open_degree_filter_window()
        elif algorithm == "partitioning by degree centrality":
            clusters = Algorithms.partitioning_by_degree(G)
            Algorithms.draw_partitioned_graph(G, clusters)
        elif algorithm == "partitioning by closeness centrality":
            clusters = Algorithms.partitioning_by_closeness(G)
            Algorithms.draw_partitioned_graph_centrality(G, clusters)
        elif algorithm == "Adjust graph":
            open_adjust_graph_window()

    # def open_adjust_graph_window():
    #     param_window = tk.Toplevel(new_window)
    #     param_window.geometry("400x500")
    #     param_window.title("Adjust Graph Parameters")

    #     # Create a frame with padding
    #     param_frame = tk.Frame(param_window, padx=20, pady=20)
    #     param_frame.pack(fill=tk.BOTH, expand=True)

    #     # Create labels and input fields for each parameter with better styling
    #     tk.Label(param_frame, text="Node Color:", anchor="w").grid(row=0, column=0, sticky="w", pady=5)
    #     node_color_entry = tk.Entry(param_frame, width=20)
    #     node_color_entry.grid(row=0, column=1, pady=5, padx=10)
    #     node_color_entry.insert(0, "skyblue")  # Default value

    #     tk.Label(param_frame, text="Edge Color:", anchor="w").grid(row=1, column=0, sticky="w", pady=5)
    #     edge_color_entry = tk.Entry(param_frame, width=20)
    #     edge_color_entry.grid(row=1, column=1, pady=5, padx=10)
    #     edge_color_entry.insert(0, "gray")  # Default value

    #     tk.Label(param_frame, text="Node Shape:", anchor="w").grid(row=2, column=0, sticky="w", pady=5)
    #     node_shape_entry = tk.Entry(param_frame, width=20)
    #     node_shape_entry.grid(row=2, column=1, pady=5, padx=10)
    #     node_shape_entry.insert(0, "o")  # Default value

    #     tk.Label(param_frame, text="Label Attribute:", anchor="w").grid(row=3, column=0, sticky="w", pady=5)
    #     label_attribute_entry = tk.Entry(param_frame, width=20)
    #     label_attribute_entry.grid(row=3, column=1, pady=5, padx=10)
    #     label_attribute_entry.insert(0, "")  # Default value

    #     tk.Label(param_frame, text="Node Size Factor:", anchor="w").grid(row=4, column=0, sticky="w", pady=5)
    #     node_size_factor_entry = tk.Entry(param_frame, width=20)
    #     node_size_factor_entry.grid(row=4, column=1, pady=5, padx=10)
    #     node_size_factor_entry.insert(0, "500")  # Default value

    #     tk.Label(param_frame, text="Edge Size Factor:", anchor="w").grid(row=5, column=0, sticky="w", pady=5)
    #     edge_size_factor_entry = tk.Entry(param_frame, width=20)
    #     edge_size_factor_entry.grid(row=5, column=1, pady=5, padx=10)
    #     edge_size_factor_entry.insert(0, "1")  # Default value

    #     tk.Label(param_frame, text="Gender Filter:", anchor="w").grid(row=6, column=0, sticky="w", pady=5)
    #     gender_factor_entry = tk.Entry(param_frame, width=20)
    #     gender_factor_entry.grid(row=6, column=1, pady=5, padx=10)
    #     gender_factor_entry.insert(0, "")  # Default value

    #     # Help text
    #     help_text = """
    #     Node Shape Options:
    #     - 'o' for circle
    #     - 's' for square
    #     - '^' for triangle up
    #     - 'v' for triangle down
    #     - 'd' for diamond

    #     Gender Filter:
    #     - Leave empty for all
    #     - 'M' for male
    #     - 'F' for female

    #     Label Attribute:
    #     - 'gender' or 'class' or leave empty
    #     """

    #     help_label = tk.Label(param_frame, text=help_text, justify=tk.LEFT,
    #                           font=("Arial", 9), bg="#f0f0f0", padx=10, pady=10)
    #     help_label.grid(row=7, column=0, columnspan=2, sticky="ew", pady=10)

    #     def execute_adjust_graph():
    #         # Get the parameter values from the input fields
    #         node_color = node_color_entry.get()
    #         edge_color = edge_color_entry.get()
    #         node_shape = node_shape_entry.get()
    #         gender = gender_factor_entry.get()
    #         label_attribute = label_attribute_entry.get()

    #         try:
    #             node_size_factor = int(node_size_factor_entry.get())
    #             edge_size_factor = int(edge_size_factor_entry.get())
    #         except ValueError:
    #             tk.messagebox.showerror("Error", "Size factors must be integers")
    #             return

    #         # Call the adjust_graph function with the provided parameters
    #         Algorithms.adjust_graph(G, node_color, edge_color, node_shape,
    #                                 label_attribute, node_size_factor,
    #                                 edge_size_factor, gender)

    #         # Close the parameter window after executing the function
    #         param_window.destroy()

    #     # Create a button to execute the adjust_graph function
    #     execute_button = tk.Button(param_frame, text="Execute", command=execute_adjust_graph,
    #                                bg="#4CAF50", fg="white", font=("Arial", 10, "bold"),
    #                                width=15, height=1)
    #     execute_button.grid(row=8, column=0, columnspan=2, pady=15)


    def open_degree_filter_window():
        param_window = tk.Toplevel(new_window)
        param_window.geometry("300x200")
        param_window.title("Degree Filter")

        # Create a frame with padding
        param_frame = tk.Frame(param_window, padx=20, pady=20)
        param_frame.pack(fill=tk.BOTH, expand=True)

        # Create labels and input fields
        tk.Label(param_frame, text="Min Degree:").grid(row=0, column=0, sticky="w", pady=5)
        min_entry = tk.Entry(param_frame)
        min_entry.grid(row=0, column=1, pady=5, padx=10)
        min_entry.insert(0, "1")  # Default value

        tk.Label(param_frame, text="Max Degree:").grid(row=1, column=0, sticky="w", pady=5)
        max_entry = tk.Entry(param_frame)
        max_entry.grid(row=1, column=1, pady=5, padx=10)
        max_entry.insert(0, "10")  # Default value

        def execute_filter():
            try:
                min_val = int(min_entry.get())
                max_val = int(max_entry.get())
                # Call the filter function with the provided parameters
                Algorithms.filter_and_visualize_graph(G, degree_range=(min_val, max_val))
                # Close the parameter window after executing the function
                param_window.destroy()
            except ValueError:
                tk.messagebox.showerror("Error", "Please enter valid integer values")

        # Create a button to execute the filter function
        execute_button = tk.Button(param_frame, text="Apply Filter", command=execute_filter,
                                   bg="#4CAF50", fg="white", width=15)
        execute_button.grid(row=2, column=0, columnspan=2, pady=15)

    # Add a back button to return to the home page
    back_button = tk.Button(
        main_frame,
        text="Back to Home",
        command=lambda: new_window.destroy(),
        bg="#f44336",
        fg="white"
    )
    back_button.pack(pady=10)

def visualize_graph_window():
        vis_window = tk.Toplevel()
        vis_window.geometry("900x700")
        vis_window.title("Graph Visualization")

        # Default attributes
        node_color = "#1f78b4"
        edge_color = "#333333"
        node_size = tk.IntVar(value=500)
        edge_width = tk.DoubleVar(value=1.0)
        show_labels = tk.BooleanVar(value=True)
        node_shape = tk.StringVar(value="o")  # default shape is circle

        def pick_node_color():
            color = colorchooser.askcolor()[1]
            if color:
                nonlocal node_color
                node_color = color

        def pick_edge_color():
            color = colorchooser.askcolor()[1]
            if color:
                nonlocal edge_color
                edge_color = color

        # Settings UI
        settings_frame = tk.Frame(vis_window)
        settings_frame.pack(side=tk.TOP, fill=tk.X, padx=10, pady=10)

        tk.Label(settings_frame, text="Node Size:").grid(row=0, column=0, sticky='w')
        tk.Entry(settings_frame, textvariable=node_size).grid(row=0, column=1)

        tk.Label(settings_frame, text="Edge Width:").grid(row=1, column=0, sticky='w')
        tk.Entry(settings_frame, textvariable=edge_width).grid(row=1, column=1)

        tk.Checkbutton(settings_frame, text="Show Labels", variable=show_labels).grid(row=2, column=0, columnspan=2, sticky='w')

        tk.Button(settings_frame, text="Pick Node Color", command=pick_node_color).grid(row=0, column=2, padx=10)
        tk.Button(settings_frame, text="Pick Edge Color", command=pick_edge_color).grid(row=1, column=2, padx=10)

        tk.Label(settings_frame, text="Node Shape:").grid(row=2, column=2, sticky='w')
        shape_menu = ttk.Combobox(settings_frame, textvariable=node_shape, state="readonly", width=15)
        shape_menu['values'] = ['o (circle)', 's (square)', '^ (triangle)', 'D (diamond)', 'v (down triangle)']
        shape_menu.grid(row=2, column=3)
        shape_menu.current(0)

        # Visualization area
        fig, ax = plt.subplots(figsize=(7, 6))
        canvas = FigureCanvasTkAgg(fig, master=vis_window)
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

        def draw_graph():
            ax.clear()
            pos = nx.spring_layout(G)

            selected_shape = node_shape.get()[0]  # Get symbol only, e.g., 'o'

            nx.draw_networkx_edges(G, pos, ax=ax, edge_color=edge_color, width=edge_width.get())
            nx.draw_networkx_nodes(G, pos, ax=ax, node_color=node_color, node_size=node_size.get(), node_shape=selected_shape)

            if show_labels.get():
                nx.draw_networkx_labels(G, pos, ax=ax)

            ax.set_axis_off()
            canvas.draw()

        tk.Button(settings_frame, text="Draw Graph", command=draw_graph, bg="#4CAF50", fg="white").grid(row=3, column=0, columnspan=4, pady=10)
