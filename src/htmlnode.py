class HTMLNode():
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props or {}

    def to_html(self):
        raise NotImplementedError()
    
    def props_to_html(self):
        if not self.props:
            return ""
        html_props = [f' {key}="{value}"' for key, value in self.props.items()]
        return "".join(html_props) #joins the list elements into single string
    
    def __repr__(self):
        return f"HTMLNode(tag={self.tag}, value={self.value}, children={self.children}, props={self.props})"

class LeafNode(HTMLNode):
    def __init__(self, tag, value, props):
        if value is None:
            raise ValueError
        super().__init__(tag=tag, value=value, props=props)
     
    def to_html(self):
        if self.value is None or self.value == "":
            raise ValueError
        if self.tag is None or self.tag == "":
            return self.value
        attr = ""
        if self.props:
            attr = ' ' + ' '.join(f'{key}="{value}"' for key, value in self.props.items())
        return f"<{self.tag}{attr}>{self.value}</{self.tag}>"
    
    