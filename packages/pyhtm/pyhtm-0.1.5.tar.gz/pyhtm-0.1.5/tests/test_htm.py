#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `htm` package."""

import math
import os
import pickle

import pytest

import htm
import htm.intersection
from htm.geometry import Vector, Halfspace
from htm.intersection import Intersection
from htm.node import Node


def test_partially_intersecting_parent_trixel_with_no_child_intersections_raises():
    """This test uses the same halfspace as test_AN_455_region_bug."""
    ra = 271.19949781459
    dec = -35.85359105538
    radius = 0.00028
    with pytest.raises(htm.PrecisionError):
        # A trixel at depth 10 has a partial intersection but its children
        # don't intersect.
        htm.get_htm_circle_region(ra, dec, radius, 11)


def test_AN_455_region_bug():
    # There is a precision issue with the edge solver that causes some trixels, if
    # their edge is very close to a halfspace boundary, to test positive for
    # intersection at some depth N but for all their children trixels to test
    # negative at depth N+1. We can see the issue with the following cone:
    #
    ra = 271.19949781459
    dec = -35.85359105538
    radius = 0.00028
    #
    # At level 10, the intersection routines work as expected:
    #
    ranges = htm.get_htm_circle_region(ra, dec, radius, 10)
    assert ranges[0] == (11608422, 11608422)
    assert ranges[1] == (11611801, 11611801)
    #
    # But at level 11, all of the latter trixel's (11611801) children test
    # negative for intersection. These are the ranges that we would expect
    # to see:
    #
    with pytest.raises(htm.PrecisionError):
        ranges = htm.get_htm_circle_region(ra, dec, radius, 11)
        assert ranges[0] == (46433688, 46433688)
        assert ranges[1] == (46447204, 46447204)

    # As a minimum working example of the problem, this next test case shows the
    # results of the intersection routine on the particular parent trixel and its
    # children trixels:
    #
    # This is the suspect halfspace (same as above, just serialized) and the
    # particular depth 10 trixel:
    #
    data_dir = os.path.join(
        os.path.abspath(os.path.dirname(__file__)), "data", "AN-455"
    )
    with open(os.path.join(data_dir, "halfspace.p"), "rb") as f:
        halfspace = pickle.load(f)
    with open(os.path.join(data_dir, "node.p"), "rb") as f:
        node = pickle.load(f)
    #
    # As we can see, the trixel tests as a partial intersection:
    #
    assert htm.intersection.test_node(node, halfspace) == Intersection.PARTIAL
    #
    # Now, testing each of its children, we see that none intersect:
    #
    intersections = [
        htm.intersection.test_node(child, halfspace) for child in node.yield_children()
    ]
    with pytest.raises(AssertionError):
        # This assertion fails
        assert any([i != Intersection.NONE for i in intersections])


@pytest.mark.parametrize(
    "v,c,expected",
    [
        (Vector(0, 0, 1), Halfspace(Vector(0, 0, 1), 0.8), True),
        (Vector(0, 0, 1), Halfspace(Vector(0, 0, -1), 0.0), False),
        (
            Vector(1 / math.sqrt(2), 0, 1 / math.sqrt(2)),
            Halfspace(
                Vector(1 / math.sqrt(2), 1 / math.sqrt(2), 0), math.cos(math.pi / 2)
            ),
            True,
        ),
        # Edge Case: Vector on halfspace boundary
        (Vector(0, 0, 1), Halfspace(Vector(0, 1, 0), 0.0), False),
        # Edge Case: Vector just inside halfspace
        (Vector(0, 0, 1), Halfspace(Vector(0, 1, 0), -0.000000001), True),
        # Edge Case: Vector inside halfspace w/ d < 0
        (
            Vector(0, 1 / math.sqrt(2), 1 / math.sqrt(2)),
            Halfspace(Vector(0, 0, -1), -0.8),
            True,
        ),
    ],
)
def test_vertex_in_halfspace(v, c, expected):
    assert htm.geometry.point_in_halfspace(v, c) == expected


@pytest.mark.parametrize(
    "c1,c2,expected",
    [
        (
            Halfspace(Vector(0, 0, 1), 0.0),
            Halfspace(Vector(0, 1, 0), math.cos(math.pi / 8)),
            True,
        ),
        (
            Halfspace(Vector(1 / math.sqrt(3), 1 / math.sqrt(3), 1 / math.sqrt(3)), -1),
            Halfspace(Vector(-1, 0, 0), 0.99),
            True,
        ),
        (
            Halfspace(Vector(1, 0, 0), math.cos(math.pi / 8)),
            Halfspace(Vector(-1, 0, 0), math.cos(math.pi / 8)),
            False,
        ),
        # Edge Case: Halfspaces touch
        (Halfspace(Vector(0, 0, 1), 0.0), Halfspace(Vector(0, 0, -1), 0.0), False),
        # Edge Case: Both halfspaces w/ d < 0
        (Halfspace(Vector(0, 0, 1), -0.1), Halfspace(Vector(0, 0, -1), -0.1), True),
    ],
)
def test_halfspace_intersects_halfspace(c1, c2, expected):
    assert htm.geometry.halfspace_intersects_halfspace(c1, c2) == expected


@pytest.mark.parametrize(
    "edge_v0,edge_v1,halfspace,expected",
    [
        (
            Vector(1, 0, 0),
            Vector(0, 0, 1),
            Halfspace(
                Vector(1 / math.sqrt(2), 0, 1 / math.sqrt(2)), math.cos(math.pi / 8)
            ),
            True,
        ),
        (
            Vector(1, 0, 0),
            Vector(0, 1, 0),
            Halfspace(
                Vector(1 / math.sqrt(3), 1 / math.sqrt(3), 1 / math.sqrt(3)),
                math.cos(0.6154),
            ),
            False,
        ),
        # Edge (heh) Case: Edge inside halfspace
        (
            Vector(1, 0, 0),
            Vector(0, 0, 1),
            Halfspace(Vector(1 / math.sqrt(2), 0, 1 / math.sqrt(2)), 0),
            False,
        ),
        # Edge Case: Edge tangent to halfspace
        (
            Vector(1, 0, 0),
            Vector(0, 0, 1),
            Halfspace(
                Vector(1 / math.sqrt(2), 1 / math.sqrt(2), 0), math.cos(math.pi / 4)
            ),
            False,
        ),
        # Edge Case: Edge starts and ends on halfspace
        (
            Vector(1, 0, 0),
            Vector(0, 1, 0),
            Halfspace(
                Vector(1 / math.sqrt(2), 1 / math.sqrt(2), 0), math.cos(math.pi / 4)
            ),
            True,
        ),
    ],
)
def test_edge_intersects_halfspace(edge_v0, edge_v1, halfspace, expected):
    assert (
        htm.geometry.edge_intersects_halfspace(edge_v0, edge_v1, halfspace) == expected
    )


@pytest.mark.parametrize(
    "c,v0,v1,v2,expected",
    [
        (
            Halfspace(Vector(*([1 / math.sqrt(3)] * 3)), math.cos(math.pi / 8)),
            Vector(0, 1, 0),
            Vector(0, 0, 1),
            Vector(1, 0, 0),
            True,
        ),
        (
            Halfspace(Vector(*([-1 / math.sqrt(3)] * 3)), math.cos(math.pi / 8)),
            Vector(0, 1, 0),
            Vector(0, 0, 1),
            Vector(1, 0, 0),
            False,
        ),
        # Edge Case: Halfspace inscribed in trixel
        (
            Halfspace(Vector(*([1 / math.sqrt(3)] * 3)), math.cos(math.pi / 4)),
            Vector(0, 1, 0),
            Vector(0, 0, 1),
            Vector(1, 0, 0),
            True,
        ),
    ],
)
def test_halfspace_in_trixel(c, v0, v1, v2, expected):
    assert htm.geometry.halfspace_in_triangle(c, v0, v1, v2) == expected


@pytest.mark.parametrize(
    "t,c,expected",
    [
        # Node fully inside halfspace
        (
            Node(
                Vector(0, 1 / math.sqrt(2), 1 / math.sqrt(2)),
                Vector(1 / math.sqrt(2), 0, 1 / math.sqrt(2)),
                Vector(0, 0, 1),
                0b0011,
            ),
            Halfspace(Vector(0, 0, 1), 0.0),
            Intersection.FULL,
        ),
        # Node 2 corners inside halfspace
        (
            Node(
                Vector(0, 1 / math.sqrt(2), 1 / math.sqrt(2)),
                Vector(1 / math.sqrt(2), 0, 1 / math.sqrt(2)),
                Vector(0, 0, -1),
                0b0011,
            ),
            Halfspace(Vector(0, 0, 1), 0.0),
            Intersection.PARTIAL,
        ),
        # Node 1 corner inside halfspace
        (
            Node(
                Vector(0, 1 / math.sqrt(2), 1 / math.sqrt(2)),
                Vector(1 / math.sqrt(2), 0, -1 / math.sqrt(2)),
                Vector(0, 0, -1),
                0b0011,
            ),
            Halfspace(Vector(0, 0, 1), 0.0),
            Intersection.PARTIAL,
        ),
        # Node outside halfspace
        (
            Node(
                Vector(0, 1 / math.sqrt(2), -1 / math.sqrt(2)),
                Vector(1 / math.sqrt(2), 0, -1 / math.sqrt(2)),
                Vector(0, 0, -1),
                0b0011,
            ),
            Halfspace(Vector(0, 0, 1), 0.0),
            Intersection.NONE,
        ),
        # Node edge intersects halfspace
        (
            Node(Vector(0, 1, 0), Vector(0, 0, 1), Vector(1, 0, 0), 0b0011),
            Halfspace(
                Vector(1 / math.sqrt(2), 0, 1 / math.sqrt(2)), math.cos(math.pi / 8)
            ),
            Intersection.PARTIAL,
        ),
        # Halfspace inside trixel
        (
            Node(Vector(0, 1, 0), Vector(0, 0, 1), Vector(1, 0, 0), 0b0011),
            Halfspace(Vector(*([1 / math.sqrt(3)] * 3)), math.cos(math.pi / 8)),
            Intersection.PARTIAL,
        ),
        # Error Case
        (
            Node(Vector(0, 1, 0), Vector(0, 0, -1), Vector(-1, 0, 0), 0b0011),
            Halfspace(Vector(1, 0, 0), 0.01),
            Intersection.NONE,
        ),
    ],
)
def test_trixel(t, c, expected):
    assert htm.intersection.test_node(t, c) == expected


def test_get_htm_id():
    path = os.path.join(os.path.abspath(os.path.dirname(__file__)), "data", "htm_ids.p")
    with open(path, "rb") as f:
        htm_ids = pickle.load(f)
    for (ra, dec, expected) in htm_ids:
        actual = htm.get_htm_id(ra, dec, 20)
        assert actual == expected


def test_get_htm_circle_region():
    path = os.path.join(
        os.path.abspath(os.path.dirname(__file__)), "data", "htm_ranges.p"
    )
    with open(path, "rb") as f:
        htm_regions = pickle.load(f)
    for i, (ra, dec, radius, level, expected) in enumerate(htm_regions):
        # if level == 20: continue
        # if ra != 224.9472226: continue
        actual = htm.get_htm_circle_region(ra, dec, radius, level)
        assert actual == expected


def test_alerts_database_errors():
    """
    These are RA/DEC coordinates from the ANTARES DB that caused the
    htm library routine `get_htm_id` to error.
    """
    path = os.path.join(
        os.path.abspath(os.path.dirname(__file__)), "data", "database_alerts_errors.csv"
    )
    with open(path, "r") as f:
        for line in f:
            _, alert_id, ra, dec, htm_id, _ = line.split(",")
            alert_id = int(alert_id)
            ra = float(ra)
            dec = float(dec)
            htm_id = int(htm_id)
            assert htm.get_htm_id(ra, dec, 20) == htm_id


def test_alerts_database_wrong():
    """
    These are RA/DEC coordinates from the ANTARES DB that caused the
    htm library routine `get_htm_id` to error.
    """
    path = os.path.join(
        os.path.abspath(os.path.dirname(__file__)), "data", "database_alerts_wrong.csv"
    )
    with open(path, "r") as f:
        for line in f:
            _, alert_id, ra, dec, htm_id, _ = line.split(",")
            alert_id = int(alert_id)
            ra = float(ra)
            dec = float(dec)
            htm_id = int(htm_id)
            assert htm.get_htm_id(ra, dec, 20) == htm_id


@pytest.mark.xfail
def test_fix_issue_1():
    # This parent node has a child node that registers a PARTIAL
    # intersection but the routine doesn't find any further intersection
    # with the children of that child node. This should not be possible.
    #
    # Load the halfspace
    path = os.path.join(
        os.path.abspath(os.path.dirname(__file__)), "data", "issue-1-halfspace.p"
    )
    with open(path, "rb") as f:
        halfspace = pickle.load(f)
    # Load the parent node
    path = os.path.join(
        os.path.abspath(os.path.dirname(__file__)), "data", "issue-1-parent.p"
    )
    with open(path, "rb") as f:
        parent = pickle.load(f)

    #
    # The parent has a PARTIAL intersect type
    #
    parent_intersection = htm.intersection.test_node(parent, halfspace)
    assert parent_intersection == htm.intersection.Intersection.PARTIAL

    #
    # But all of the children are NONE
    #
    child_intersections = [
        htm.intersection.test_node(child, halfspace)
        for child in htm.intersection.yield_nodes(parent=parent)
    ]
    assert any(
        [
            intersection != htm.intersection.Intersection.NONE
            for intersection in child_intersections
        ]
    )
