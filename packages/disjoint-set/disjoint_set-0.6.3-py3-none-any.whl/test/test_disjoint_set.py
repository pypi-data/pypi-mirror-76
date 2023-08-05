from unittest import TestCase

import disjoint_set


class TestDisjointSet(TestCase):
    def setUp(self) -> None:
        self.dset = disjoint_set.DisjointSet()

    def test_initializes_value_for_absent_key(self):
        self.assertTrue(1 not in self.dset._data)
        self.assertEqual(
            self.dset.find(1),
            1,
        )
        self.assertTrue(1 in self.dset._data)

    def test_holds_and_compares_different_data_types(self):
        values = [
            "a", 1, (1, 2, 3)
        ]

        for a, b in zip(values, values[1:]):
            self.assertEqual(
                self.dset.connected(a, b),
                False,
            )

    def test_sets_the_same_class_for_united_elements(self):
        self.assertNotEqual(
            self.dset._data[1],
            self.dset._data[2],
        )

        self.dset.union(1, 2)

        self.assertEqual(
            self.dset._data[1],
            self.dset._data[2],
        )

    def test_unites_symmetrically(self):
        self.dset.union(1, 2)
        self.dset.union(3, 4)
        self.dset.union(1, 6)
        self.dset.union(8, 2)

        self.assertEqual(
            self.dset.connected(6, 8),
            True,
        )

        self.assertEqual(
            self.dset.connected(8, 6),
            True,
        )

    def test_updates_class_assignment(self):
        self.dset.union(1, 2)
        self.dset.union(2, 3)

        self.assertEqual(
            self.dset.find(3),
            3
        )

        self.assertEqual(
            self.dset.find(1),
            3
        )

    def test_contains_elements_returns_existing_keys(self):
        self.assertEqual(
            1 in self.dset,
            False,
        )

        self.dset.find(1)
        self.assertEqual(
            1 in self.dset,
            True,
        )

    def test_repr(self):
        self.dset.union(1, 2)
        self.assertEqual(
            str(self.dset),
            "DisjointSet(2 <- [1, 2])"
        )

    def test_iter(self):
        self.dset.union(1, 2)

        self.assertEqual(
            list(self.dset),
            [(1, 2), (2, 2)]
        )

    def test_bool(self):
        self.assertEqual(
            bool(self.dset),
            False,
        )

        self.dset.union(1, 2)

        self.assertEqual(
            bool(self.dset),
            True,
        )

    def test_itersets_iterates_over_all_component_classes(self):
        self.dset.union(1, 2)
        self.dset.union(2, 3)
        self.assertEqual(
            list(self.dset.itersets()),
            [{1, 2, 3}],
        )
        self.dset.union(4, 5)
        self.assertEqual(
            list(self.dset.itersets()),
            [{1, 2, 3}, {4, 5}],
        )
