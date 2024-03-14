nested_list = ["div", 0, 0, "a-section a-spacing-none a-spacing-top-small s-title-instructions-style",
    [["h2", 1, 1, "a-size-mini a-spacing-none a-color-base s-line-clamp-4", [["a",
    2, 1, "a-link-normal s-underline-text s-underline-link-text s-link-style a-text-normal",
    [["span", 3, 1, "a-size-base-plus a-color-base a-text-normal", []]]]]]]]

def visualize_nested_list(nested_list, indent=0):
    for item in nested_list:
        if isinstance(item, list):
            visualize_nested_list(item, indent + 1)
        else:
            print("  " * indent + str(item))

visualize_nested_list(nested_list)

def visualize_nested_list(nested_list, indent=0, same_line=False):
    for item in nested_list:
        if isinstance(item, list):
            visualize_nested_list(item, indent + 1, same_line)
        else:
            if same_line:
                print(" " * indent + str(item), end=" ")
            else:
                print(" " * indent + str(item))
            same_line = False
visualize_nested_list(nested_list)
