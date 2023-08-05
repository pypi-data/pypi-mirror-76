from nose.tools import *
import pygraphviz as pgv


def stringify(agraph):
    result = agraph.string().split()
    if '""' in result:
        result.remove('""')
    return " ".join(result)


def test_edge_attributes():
    A = pgv.AGraph()
    A.add_edge(1, 2, label="test", spam="eggs")
    ans = """strict graph { 1 -- 2 [label=test, spam=eggs]; }"""
    assert_equal(stringify(A), " ".join(ans.split()))


def test_edge_attributes2():
    A = pgv.AGraph()
    A.add_edge(1, 2)
    one = A.get_edge(1, 2)
    one.attr["label"] = "test"
    one.attr["spam"] = "eggs"
    assert_true("label" in one.attr)
    assert_equal(one.attr["label"], "test")
    assert_equal(sorted(one.attr.keys()), ["label", "spam"])

    ans = """strict graph { 1 -- 2 [label=test, spam=eggs]; }"""
    assert_equal(stringify(A), " ".join(ans.split()))

    one.attr["label"] = ""
    one.attr["spam"] = ""
    ans = """strict graph { 1 -- 2; }"""
    assert_equal(stringify(A), " ".join(ans.split()))

    one.attr["label"] = "test"
    del one.attr["label"]
    ans = """strict graph { 1 -- 2; }"""
    assert_equal(stringify(A), " ".join(ans.split()))


def test_anonymous_edges():
    text_graph = (
        b"""graph test {\n a -- b [label="edge1"];\n a -- b [label="edge2"];\n }"""
    )

    import os
    import tempfile

    fd, fname = tempfile.mkstemp()
    os.write(fd, text_graph)
    os.close(fd)
    A = pgv.AGraph(fname)

    ans = """graph test { a -- b [label=edge1]; a -- b [label=edge2]; }"""
    assert_equal(stringify(A), " ".join(ans.split()))
    os.unlink(fname)


def test_edge_attribute_update():
    A = pgv.AGraph(strict=True)
    A.add_edge(1, 2, label="test", spam="eggs")
    A.add_edge(1, 2, label="update", spam="")
    ans = """strict graph { 1 -- 2 [label=update]; }"""
    assert_equal(stringify(A), " ".join(ans.split()))


def test_edge_attribute_update_nonstrict():
    A = pgv.AGraph(strict=False)
    A.add_edge(1, 2, label="test", spam="eggs", key="one")
    A.add_edge(1, 2, label="update", spam="", key="one")
    ans = """graph { 1 -- 2 [key=one, label=update]; }"""
    assert_equal(stringify(A), " ".join(ans.split()))
