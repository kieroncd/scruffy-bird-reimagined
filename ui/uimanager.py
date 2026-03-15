class UIManager:

    def __init__(self):
        self.elements = {}

    def add(self, tag, element):
        self.elements[tag] = element

    def remove(self, tag):
        if tag in self.elements:
            del self.elements[tag]

    def get(self, tag):
        return self.elements.get(tag)

    def process_input(self, events):
        for element in self.elements.values():
            if hasattr(element, "process_input"):
                element.process_input(events)

    def update(self, delta):
        for element in self.elements.values():
            if hasattr(element, "update"):
                element.update(delta)

    def render(self, screen):
        for element in self.elements.values():
            if hasattr(element, "update"):
               element.render(screen)