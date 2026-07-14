class HTMLNode():
    def __init__(self,tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props
    
    def __repr__(self):
        return f" {self.tag} \n {self.value} \n {self.children} \n {self.props}"

    def to_html(self):
        raise NotImplemented
    
    def props_to_html(self):
        html = ""
        if self.props != None:
            for key, value in self.props.items():
                html += f' {key}="{value}"'
        return html
    
class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag = tag, value = value, props = props)

    def to_html(self):
        html = ""
        if self.value == None:
            raise ValueError
        if self.tag == None:
            return f"{self.value}"
        
        if self.tag == "img":
            return f'<{self.tag}{self.props_to_html()}>'
        elif self.tag =="a":
            return f'<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>'
        else:
            return f'<{self.tag}>{self.value}{self.props_to_html()}</{self.tag}>'

    def __repr__(self):
        return f" {self.tag} \n {self.value} \n {self.props}"
    
class ParentNode(HTMLNode):
    def __init__(self, tag, children,props=None):
        super().__init__(tag = tag, children = children, props = props)
    
    def to_html(self):
        if self.tag == None or self.tag == "":
            raise ValueError("No Tag Data")
        if self.children == None or self.children == []:
            raise ValueError("No Children")
        else:
            children_html = ""
            for child in self.children:
                children_html += child.to_html()
            return f"<{self.tag}{self.props_to_html()}>{children_html}</{self.tag}>"

