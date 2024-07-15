def fetch_parameter_values(input_index, parameter_name):
    import loputils
    node = hou.pwd().inputs()[input_index]
    return loputils.fetchParameterValues(node, parameter_name)
