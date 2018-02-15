"""
This file implements all classes needed to parse boolean expression.
Here is the definition of our parser:
    + Our alphabet is composed with:
        - [a-zA-Z] letters
        - &, |, , !, ( and ) symbols
        - white space

    + Our language is composed by 3 types of words:
        - '!', '&&' and '||' operator
        - '(' and ')' parenthesis
        - [a-zA-Z]+ words

    + Our grammar is defined here:
        S::= Expression
        Expression::= SubExpression
                      | SubExpression '||' Expression  Operator: OR
                      | SubExpression '&&' Expression  Operator: AND
        SubExpression::= '('Expression')'
                         | '!'SubExpression            Operator: NOT
                         | RoleName
        RoleName::= [a-zA-Z]+
"""


class ParsingError(Exception):
    """This is a custom exception raised when a parsing error is detected."""


class Node(object):
    """This class defines a node contains in our tree built from parsing."""

    def eval(self, index):
        """
        This function to implement defines how we should eval the current node.
        + params:
            - index: ReverseIndex object where we look for results.
        + returns:
            a set containing all posting_ids corresponding to the boolean expression given:
            {posting_ids ...}
        """
        raise NotImplementedError


class UnaryNode(Node):
    """This class defines a node which has one child."""

    def __init__(self, expression):
        """self.expression contains the child node."""
        self.expression = expression


class BinaryNode(Node):
    """This class defines a node which has two children."""

    def __init__(self, left_expression, right_expression):
        """self.left_expression and self.right_expression contains the two children node."""
        self.left_expression = left_expression
        self.right_expression = right_expression


class AndNode(BinaryNode):
    """This class defines the AND operator logic in our tree."""

    def eval(self, index):
        """
        Implements the and eval function.
        This is the intersection between the result of eval function of the two children nodes.
        """
        return self.left_expression.eval(index).intersection(self.right_expression.eval(index))

    def __str__(self):
        return '({} && {})'.format(self.left_expression, self.right_expression)


class OrNode(BinaryNode):
    """This class defines the OR operator logic in our tree."""

    def eval(self, index):
        """
        Implements the or eval function.
        This is the union between the result of eval function of the two children nodes.
        """
        return self.left_expression.eval(index).union(self.right_expression.eval(index))

    def __str__(self):
        return '({} || {})'.format(self.left_expression, self.right_expression)


class NotNode(UnaryNode):
    """This class defines the NOT operator logic in our tree."""

    def eval(self, index):
        """
        Implements the not eval function.
        This is the difference between:
            - all posting_ids in index
            - the result of eval function of the child node.
        """
        all_posting_ids = {
            posting_id
            for term_id in index.keys()
            for posting_id, _ in index[term_id][1]
        }
        return all_posting_ids.difference(self.expression.eval(index))

    def __str__(self):
        return '!({})'.format(self.expression)


class RoleNode(Node):
    """This class defines the logic for leaves in our tree."""

    def __init__(self, role_name):
        """self.role_name is the value of the leaf (a word)"""
        self.role_name = role_name

    def eval(self, index):
        """
        Implements the eval function for RoleNode.
        Return all posting_ids associated to self.role_name.
        """
        return {posting_id for posting_id, _, in index[self.role_name][1]}

    def __str__(self):
        return str(self.role_name)


class Tokenizer(object):
    """This class defines all the logic to tokenize a boolean expression."""

    @staticmethod
    def tokenize(text):
        """
        This methods tokenizes the given text input.
        + params:
            - text: string to tokenize
        + returns:
            a list of tokens
        """
        tokenized_text = []
        current_token = ''

        for char in text:
            if char == ' ':
                continue

            if char in '!()':
                if len(current_token) > 0:
                    tokenized_text.append(current_token)
                    current_token = ''
                tokenized_text.append(char)
                continue

            if char in '|&':
                if len(current_token) > 0:
                    if char == current_token[-1]:
                        tokenized_text.append(current_token[:-1]) if current_token[:-1] else None
                        current_token = ''
                        tokenized_text.append(char * 2)
                        continue

            current_token += char
        tokenized_text.append(current_token) if current_token else None

        return tokenized_text


class BooleanParser(object):
    """This class contains the logic to build a tree given a tokenized expression."""
    index = 0

    @staticmethod
    def parse(tokens):
        """
        Method to call to build tree from tokenized expression.
        Reset BooleanParser.index to 0 and build the tree for the given token list.
        + params:
            - tokens: tokenized expression [token ...]
        + returns:
            root Node of our tokenized expression
        """
        BooleanParser.index = 0
        return BooleanParser.parse_exp(tokens)

    @staticmethod
    def parse_exp(tokens):
        """This methods implements Expression rule."""
        left_expression = BooleanParser.parse_subexp(tokens)

        if BooleanParser.index >= len(tokens):
            return left_expression

        elif tokens[BooleanParser.index] == ')':
            return left_expression

        current_token = tokens[BooleanParser.index]

        if current_token == '&&':
            BooleanParser.index += 1
            right_expression = BooleanParser.parse_exp(tokens)
            return AndNode(left_expression, right_expression)

        elif current_token == '||':
            BooleanParser.index += 1
            right_expression = BooleanParser.parse_exp(tokens)
            return OrNode(left_expression, right_expression)

        raise ParsingError('Expected \'&&\' or \'||\' or EOF')

    @staticmethod
    def parse_subexp(tokens):
        """This method implements SubExpression rule."""
        current_token = tokens[BooleanParser.index]

        if current_token == '(':
            BooleanParser.index += 1
            expression = BooleanParser.parse_exp(tokens)

            if tokens[BooleanParser.index] != ')':
                raise ParsingError('Expected \')\'')

            BooleanParser.index += 1
            return expression

        elif current_token == '!':
            BooleanParser.index += 1
            expression = BooleanParser.parse_subexp(tokens)
            return NotNode(expression)

        BooleanParser.index += 1
        return RoleNode(current_token)
