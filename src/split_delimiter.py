from textnode import TextNode, TextType


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_list = []

    for node in old_nodes:
        if node.text_type == TextType.PLAIN_TEXT:
            # Raise exception if matching delimiter not found
            delimiter_count = node.text.count(delimiter)
            if not delimiter_count % 2 == 0:
                raise Exception("Missing closing delimiter")

            # Split str by delimiter
            split_str_list = node.text.split(delimiter)

            for i in range(0, len(split_str_list)):
                if split_str_list[i]:
                    if not i % 2 == 0:
                        txt_node = TextNode(split_str_list[i], text_type)
                        new_list.append(txt_node)
                    else:
                        txt_node = TextNode(split_str_list[i], TextType.PLAIN_TEXT)
                        new_list.append(txt_node)
        else:
            # Add to the list if it's not plain text
            new_list.append(node)
    return new_list
