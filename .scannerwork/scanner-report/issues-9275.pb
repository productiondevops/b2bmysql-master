�
pythonS1192�Define a constant instead of duplicating this literal """
    query SetsNullable($value: String) {
        fieldWithNullableStringInput(input: $value)
    }
    """ 3 times. )       @2
��
 :
�H
��
 Duplication:
�H
��
 Duplication�
pythonS1192�Define a constant instead of duplicating this literal """
    query SetsNonNullable($value: String!) {
        fieldWithNonNullableStringInput(input: $value)
    }
    """ 3 times. )       @2
��
 :
�H
��
 Duplication:
�H
��
 Duplication�
pythonS1192�Define a constant instead of duplicating this literal """
    query q($input: [String!]!) {
        nnListNN(input: $input)
    }
    """ 3 times. )       @2
��
 :
�H
��
 Duplication:
�H
��
 Duplication�
pythonS1192�Define a constant instead of duplicating this literal """
    query q($input: [String]) {
        list(input: $input)
    }
    """ 3 times. )       @2
��
 :
�H
��
 Duplication:
�H
��
 Duplication�
pythonS1192�Define a constant instead of duplicating this literal """
    query q($input: [String!]) {
        listNN(input: $input)
    }
    """ 3 times. )       @2
��
 :
�H
��
 Duplication:
�H
��
 Duplication�
pythonS1192�Define a constant instead of duplicating this literal """
    query q($input: [String]!) {
        nnList(input: $input)
    }
    """ 3 times. )       @2
��
 :
�H
��
 Duplication:
�H
��
 Duplication�
pythonS1192NDefine a constant instead of duplicating this literal '"Hello World"' 3 times. )       @2
��7 F:
�H
��7 FDuplication:
�H
��7 FDuplication9
pythonS125Remove this commented out code. 2 H
pythonS5806+Rename this variable; it shadows a builtin. 2FF 	