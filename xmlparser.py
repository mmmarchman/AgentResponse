#!/usr/bin/env python

"""xmlparser.py: parses an xml file without using any libraries and pushes info to treebuilder.py
                 to create a behavior tree"""

import re
import random
from treebuilder import TreeBuilder

__author__ = 'McClain Marchman'

list_behavior = []


class XmlParser:

    # Parses an xml file into a behavior tree
    def parse_xml(self, file_name, tree):
        index = 0

        with open(file_name)as f:
            for line in f:

                # Returns either a behavior, response, or None
                beh_res = self.get_behavior_response(line)

                # Check if the first element in the first line is <,
                # if not we do not have a correct xml file
                if index == 0:
                    if line[0].lstrip() != '<':
                        print 'File Provided is not in XML format'
                        SystemExit(0)
                    tree.behavior = self.remove_brackets(line)

                # Checks if /> is in the line
                elif '/>' in line:
                    tree = self.create_leafs(tree, beh_res)

                # Checks to see if line is '</node>' (new node)
                elif self.is_new_node(line):
                    tree = tree.get_previous()

                # If it was not root, />, or </node> then it
                # must be a branch
                elif beh_res is not None:
                    tree = self.create_branch(tree, beh_res)

                index += 1

            print tree
            f.close()
            return tree

    # Returns either a behavior, response, or None
    def get_behavior_response(self, line):

        # Returns each occurrence of "*" as a list
        behavior_response = re.findall(r'"(.*?)"', line)

        # Check and return a behavior or response
        # if not either then None
        if behavior_response:
            if behavior_response[0] is not '':
                return str("Behavior = " + str(behavior_response[0]))
            elif behavior_response[1]:
                return str("Response = " + str(behavior_response[1]))
        else:
            return None

    # Returns a tree at root
    def return_root(self, tree):
        while tree.previous is not None:
            tree = tree.get_previous()
        return tree

    # Creates a leaf with response = beh_res
    def create_leafs(self, tree, beh_res,):
        tree = tree.add_node()
        tree.response = beh_res
        tree = tree.get_previous()
        return tree

    # Creates a branch with behavior = beh_res
    def create_branch(self, tree, beh_res):
        global list_behavior
        tree = tree.add_node()
        tree.behavior = beh_res

        # Add tree to the queue so that we can perform breadth first search
        list_behavior.append(tree)
        return tree

    # Boolean check to see if the line argument contains the string </node>
    def is_new_node(self, line):
        return '</node>' in str(line.lstrip())

    def remove_brackets(self, string):
        return string.replace('<', '').replace('>', '').rstrip('\n')

    # Performs a breadth first search using a list as a queue
    def breadth_first_search(self, node_name):

        behavior_queue = list(list_behavior)

        for behavior in behavior_queue:
            if str(behavior.get_name()) == str(node_name):
                return behavior
            print "Breadth Checked: " + behavior.get_name()

    # Removes 'Behavior = ' and 'Response = ' from list_behavior
    # and list_response
    def remove_non_names(self):
        global list_behavior
        for i, name in enumerate(list_behavior):
            list_behavior[i] = name[11:]

    def get_random_choice(self, tree):
        possible_choices = []
        children = str(tree.children).splitlines()
        children = iter(children)
        for child in children:
            if "Response" in str(child):
                possible_choices.append(str(child)[12:].rstrip("\n").rstrip("'"))

        choice = random.choice(possible_choices)
        return choice

    def __init__(self):
        global list_behavior

        tree = TreeBuilder()

        print ""
        print ""
        print "Parsing .xml file into a behavior tree... \n"

        tree1 = self.parse_xml('test2.xml', tree)
        print "------------------------------------------------------------"

        check = True

        while check is True:

            event_input = raw_input("Type an event/behavior to which \n "
                                    "the agent may respond ('quit' to exit): ")
            if event_input == 'quit':
                break
            else:

                x = str("Behavior = " + event_input)
                try:

                    # tree1.get_node(x) is a depth first search for behaviors
                    #
                    # tree1 = self.return_root(tree1) && self.breadth_first_search(x)
                    # is for breadth
                    #
                    # tree1 = tree1.get_node(x) # uncomment this line for breadth first

                    tree1 = self.return_root(tree1)  # un comment out these two line for breadth first
                    tree1 = self.breadth_first_search(x)  # <---

                    if tree1 is not None:
                        choice = self.get_random_choice(tree1)
                        print "Response " + str(choice)
                        tree1 = self.return_root(tree1)
                    else:
                        print "Behavior not found!"
                        print "EXITING"
                        check = False
                    print "------------------------------------------------------------"
                except:
                    pass
        print "------------------------------------"


parser = XmlParser()



