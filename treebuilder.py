#!/usr/bin/env python

"""treebuilder.py: defines a treebuilder object with appropriate get,
                   and add methods"""

__author__ = 'McClain Marchman'


class TreeBuilder(object):
    def __init__(self):

        self.children = []
        self.behavior = None
        self.response = None
        self.previous = None

    # Return the node who's name is node_name
    # This is a depth first search
    def get_node(self, nod_name):

        if str(self.get_name()) == str(nod_name):
            return self
        else:
            for child in self.children:
                found_name = child.get_node(nod_name)
                # print "Depth Checked: " + str(child)
                if found_name:
                    return found_name

    def get_previous(self):
        return self.previous or self

    # Create a new node
    def add_node(self):
        new_node = TreeBuilder()
        self.children.append(new_node)
        new_node.previous = self
        return new_node

    # If behavior is not None then return it
    # If response is not None then return it
    # Basically returns whatever the 'name' is for the current tree
    def get_name(self):
        if self.behavior is not None:
            return self.behavior
        if self.response is not None:
            return self.response

    # Recursively format the printing of a treebuilder()
    # into a decent looking tree
    def __repr__(self, level=0):
        output = "\t" * level + repr(self.get_name()) + "\n"
        for child in self.children:
            output += child.__repr__(level+1)
        return output





