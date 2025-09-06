class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag  # HTML tag (p, a, div ect.)
        self.value = value  # Content inside the tag
        self.children = children  # Child nodes in non-leaf nodes
        self.props = (
            props  # HTML properties/attributes ({"href": "https://example.com"})
        )

    def to_html(self):
        raise NotImplemented

    def props_to_html(self):
        # Convert props dict into a string
        if not self.props:
            return ""
        result = " " + " ".join(f'{key}="{value}"' for key, value in self.props.items())
        return result

    def __repr__(self):
        return f"HTMLNode(tag: {self.tag}, value: {self.value}, children: {self.children}, props: {self.props})"

    def __eq__(self, other):
        if not isinstance(other, HTMLNode):
            return False
        return (
            self.tag == other.tag
            and self.value == other.value
            and self.children == other.children
            and self.props == other.props
        )


class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        # Leaf node must always have a value
        if value is None:
            raise ValueError("LeafNode must have a value")
        super().__init__(tag=tag, value=value, children=None, props=props)

    def to_html(self):
        # Leaf node must always have a value
        if self.value is None:
            raise ValueError("LeafNode must have a value")

        # If tag is None, return raw text without wrapping
        if not self.tag:
            return self.value

        # Return full HTML
        props_str = self.props_to_html()
        return f"<{self.tag}{props_str}>{self.value}</{self.tag}>"


class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        # ParentNode must always have tag and children
        if tag is None:
            raise ValueError("ParentNode must have a tag")
        if not children:
            raise ValueError("ParentNode must have children")
        super().__init__(tag=tag, value=None, children=children, props=props)

    def to_html(self):
        # ParentNode must always have tag and children
        if self.tag is None:
            raise ValueError("ParentNode must have a tag")
        if not self.children:
            raise ValueError("ParentNode must have children")

        # Return full HTML
        props_str = self.props_to_html()
        result = f"<{self.tag}{props_str}>"
        for child in self.children:
            result += child.to_html()
        result += f"</{self.tag}>"
        return result
