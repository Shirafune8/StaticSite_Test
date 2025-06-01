class HTMLNode():
    # represent a node in the structure of HTML document, building blocks for all different parts of a webpage
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
    # handle HTML tags that contain a value and no child elements nested inside them
    def __init__(self, tag, value, props=None):
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
    
class ParentNode(HTMLNode):
    # node that has child nodes nested within it
    # potential nesting tags could be italics and bold within a normal text block or a paragraph with bold text.
    def __init__(self, tag, children, props=None): # no value argument required
        super().__init__(tag=tag, children=children, props=props)

    def to_html(self):
        if self.tag is None:
            raise ValueError("no tag exists")
        if self.children is None or self.children == []:
            raise ValueError("no children exists")
        
        # check if have child nodes otherwise return string representing HTML tag of node and its children. 
        # Nested child node.
        if self.props:
            attr_str = " " + " ".join(f'{key}="{value}"' for key, value in self.props.items())
        else:
            attr_str = ""

        children_html = "".join(child.to_html() for child in self.children)
        return f"<{self.tag}{attr_str}>{children_html}</{self.tag}>"
