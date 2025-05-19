class HTMLNode():
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def __to_html__(self):
        raise Exception(NotImplementedError)
    
    def __props_to_html__(self):
        html_props = ""
        for key, value in self.props:
            html_props = ' '.join(f'{key}="{value}"')
        return html_props
    
    def __repr__(self):
        print(f"HTMLNode{self.tag}, {self.value}, {self.children}, {self.props}")