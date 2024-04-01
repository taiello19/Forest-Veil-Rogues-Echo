import pygame

SCREEN_WIDTH = 1300
SCREEN_HEIGHT = 800
GREEN = (0, 255, 0)


class MapNode:
    def __init__(self, position):
        self.position = position
        self.connected_nodes = []
        self.visited = False

    def add_connection(self, node):
        self.connected_nodes.append(node)

    def is_clicked(self, mouse_pos):
        return pygame.Rect(self.position[0] - 20, self.position[1] - 20, 40, 40).collidepoint(mouse_pos)

    def render(self, screen, mouse_pos):
        # Render connections between nodes
        for connected_node in self.connected_nodes:
            pygame.draw.line(screen, (0, 0, 0), self.position, connected_node.position, 2)

        # Render the node on the screen
        if self.visited:
            pygame.draw.line(screen, (255, 0, 0), (self.position[0] - 20, self.position[1] - 20),
                             (self.position[0] + 20, self.position[1] + 20), 2)
            pygame.draw.line(screen, (255, 0, 0), (self.position[0] - 20, self.position[1] + 20),
                             (self.position[0] + 20, self.position[1] - 20), 2)
        else:
            pygame.draw.circle(screen, (255, 255, 255), self.position, 20)
            pygame.draw.circle(screen, (0, 0, 0), self.position, 20, 2)
            # Check if mouse is hovering over the node
            if pygame.Rect(self.position[0] - 20, self.position[1] - 20, 40, 40).collidepoint(mouse_pos):
                pygame.draw.circle(screen, (173, 216, 230), self.position, 22, 2)  # Light blue ring

    def handle_click(self, mouse_pos):
        if self.is_clicked(mouse_pos):
            self.visited = True


class Map:
    def __init__(self):
        self.nodes = []
        self.groups = {}  # Dictionary to store nodes grouped by connected components
        self.display_map = True

    def add_node(self, node):
        self.nodes.append(node)

    def connect_nodes(self, node1, node2):
        node1.add_connection(node2)
        node2.add_connection(node1)

    def generate_map(self):
        # Create starting nodes on the left side
        start_node1 = MapNode((150, 200))
        start_node2 = MapNode((150, 400))
        start_node3 = MapNode((150, 600))

        battle_node1 = MapNode((250, 200))
        battle_node2 = MapNode((250, 300))
        battle_node3 = MapNode((250, 500))
        battle_node4 = MapNode((250, 600))

        battle_node5 = MapNode((350, 225))
        battle_node6 = MapNode((350, 350))
        battle_node7 = MapNode((350, 515))

        battle_node8 = MapNode((450, 100))
        battle_node9 = MapNode((450, 200))
        battle_node10 = MapNode((450, 400))
        battle_node11 = MapNode((450, 500))
        battle_node12 = MapNode((450, 700))

        battle_node13 = MapNode((550, 150))
        battle_node14 = MapNode((550, 300))
        battle_node15 = MapNode((550, 450))
        battle_node16 = MapNode((550, 700))

        battle_node17 = MapNode((650, 150))
        battle_node18 = MapNode((650, 250))
        battle_node19 = MapNode((650, 350))
        battle_node20 = MapNode((650, 450))
        battle_node21 = MapNode((650, 550))
        battle_node22 = MapNode((650, 700))

        battle_node23 = MapNode((750, 100))
        battle_node24 = MapNode((750, 250))
        battle_node25 = MapNode((750, 400))
        battle_node26 = MapNode((750, 550))
        battle_node27 = MapNode((750, 700))

        battle_node28 = MapNode((850, 175))
        battle_node29 = MapNode((850, 350))
        battle_node30 = MapNode((850, 500))
        battle_node31 = MapNode((850, 675))

        battle_node32 = MapNode((950, 250))
        battle_node33 = MapNode((950, 400))
        battle_node34 = MapNode((950, 600))

        self.add_node(start_node1)
        self.add_node(start_node2)
        self.add_node(start_node3)
        self.add_node(battle_node1)
        self.add_node(battle_node2)
        self.add_node(battle_node3)
        self.add_node(battle_node4)
        self.add_node(battle_node5)
        self.add_node(battle_node6)
        self.add_node(battle_node7)
        self.add_node(battle_node8)
        self.add_node(battle_node9)
        self.add_node(battle_node10)
        self.add_node(battle_node11)
        self.add_node(battle_node12)
        self.add_node(battle_node13)
        self.add_node(battle_node14)
        self.add_node(battle_node15)
        self.add_node(battle_node16)
        self.add_node(battle_node17)
        self.add_node(battle_node18)
        self.add_node(battle_node19)
        self.add_node(battle_node20)
        self.add_node(battle_node21)
        self.add_node(battle_node22)
        self.add_node(battle_node23)
        self.add_node(battle_node24)
        self.add_node(battle_node25)
        self.add_node(battle_node26)
        self.add_node(battle_node27)
        self.add_node(battle_node28)
        self.add_node(battle_node29)
        self.add_node(battle_node30)
        self.add_node(battle_node31)
        self.add_node(battle_node32)
        self.add_node(battle_node33)
        self.add_node(battle_node34)

        # Create end node on the right side
        end_node_position = (SCREEN_WIDTH - 150, SCREEN_HEIGHT // 2)
        end_node = MapNode(end_node_position)
        self.add_node(end_node)

        # Connect each starting node to the end node
        self.connect_nodes(start_node1, battle_node1)
        self.connect_nodes(start_node2, battle_node2)
        self.connect_nodes(start_node2, battle_node3)
        self.connect_nodes(start_node3, battle_node4)

        self.connect_nodes(battle_node1, battle_node5)
        self.connect_nodes(battle_node2, battle_node6)
        self.connect_nodes(battle_node3, battle_node7)
        self.connect_nodes(battle_node4, battle_node7)

        self.connect_nodes(battle_node5, battle_node8)
        self.connect_nodes(battle_node5, battle_node9)
        self.connect_nodes(battle_node6, battle_node10)
        self.connect_nodes(battle_node7, battle_node11)
        self.connect_nodes(battle_node7, battle_node12)

        self.connect_nodes(battle_node8, battle_node13)
        self.connect_nodes(battle_node9, battle_node14)
        self.connect_nodes(battle_node10, battle_node14)
        self.connect_nodes(battle_node11, battle_node15)
        self.connect_nodes(battle_node12, battle_node16)

        self.connect_nodes(battle_node13, battle_node17)
        self.connect_nodes(battle_node13, battle_node18)
        self.connect_nodes(battle_node14, battle_node18)
        self.connect_nodes(battle_node14, battle_node19)
        self.connect_nodes(battle_node15, battle_node19)
        self.connect_nodes(battle_node15, battle_node20)
        self.connect_nodes(battle_node15, battle_node21)
        self.connect_nodes(battle_node16, battle_node21)
        self.connect_nodes(battle_node16, battle_node22)

        self.connect_nodes(battle_node17, battle_node23)
        self.connect_nodes(battle_node17, battle_node24)
        self.connect_nodes(battle_node18, battle_node24)
        self.connect_nodes(battle_node19, battle_node25)
        self.connect_nodes(battle_node20, battle_node25)
        self.connect_nodes(battle_node20, battle_node26)
        self.connect_nodes(battle_node21, battle_node26)
        self.connect_nodes(battle_node22, battle_node27)

        self.connect_nodes(battle_node23, battle_node28)
        self.connect_nodes(battle_node24, battle_node28)
        self.connect_nodes(battle_node24, battle_node29)
        self.connect_nodes(battle_node25, battle_node29)
        self.connect_nodes(battle_node26, battle_node30)
        self.connect_nodes(battle_node27, battle_node31)

        self.connect_nodes(battle_node28, battle_node32)
        self.connect_nodes(battle_node29, battle_node32)
        self.connect_nodes(battle_node29, battle_node33)
        self.connect_nodes(battle_node30, battle_node33)
        self.connect_nodes(battle_node30, battle_node34)
        self.connect_nodes(battle_node31, battle_node34)

        self.connect_nodes(battle_node32, end_node)
        self.connect_nodes(battle_node33, end_node)
        self.connect_nodes(battle_node34, end_node)

        self.find_connected_components()

    def find_connected_components(self):
        """
        Find connected components in the map and store them in the groups dictionary.
        """
        visited = set()
        for node in self.nodes:
            if node not in visited:
                group = set()
                self.dfs(node, visited, group)
                if group:
                    self.groups[node] = group

    def dfs(self, node, visited, group):
        """
        Depth-first search to find connected components.
        """
        visited.add(node)
        group.add(node)
        for neighbor in node.connected_nodes:
            if neighbor not in visited:
                self.dfs(neighbor, visited, group)

    def handle_click(self, mouse_pos):
        clicked_node = None
        for node in self.nodes:
            if node.is_clicked(mouse_pos):
                clicked_node = node
                break

        if clicked_node:
            print("Selected node:", clicked_node.position)  # Display the selected node's position in the terminal

            # Check if the clicked node is in a group
            for group_leader, group in self.groups.items():
                if clicked_node in group:
                    # Disable selection for all nodes in the same group
                    for node_in_group in group:
                        node_in_group.visited = True

                    # Enable selection for nodes connected to the clicked node and on the right
                    for neighbor in clicked_node.connected_nodes:
                        if neighbor.position[0] > clicked_node.position[0]:
                            neighbor.visited = False
                    break

            # Toggle the display_map variable to hide the map
            self.display_map = True

    def render(self, screen, mouse_pos):
        if self.display_map:  # Render the map only if display_map is True
            for node in self.nodes:
                node.render(screen, mouse_pos)

# Example usage:
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()

# Create map object
map = Map()
map.generate_map()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            # Handle mouse clicks
            if event.button == 1:
                map.handle_click(pygame.mouse.get_pos())
        elif event.type == pygame.KEYDOWN:
            # Toggle map visibility with space key
            if event.key == pygame.K_SPACE:
                map.display_map = not map.display_map

    screen.fill(GREEN)  # Fill screen with green color

    # Render the map
    map.render(screen, pygame.mouse.get_pos())

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
