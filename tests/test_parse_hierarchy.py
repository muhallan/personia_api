import unittest
from hierarchy.parse_hierarchy import construct_hierarchy_tree, do_mptt_traversal, organize_hierarchy


class TestOrganizeHierarchy(unittest.TestCase):

    def test_organize_hierarchy_single_root(self):
        entry = {
            "Pete": "Nick",
            "Barbara": "Nick",
            "Nick": "Sophie",
            "Sophie": "Jonas",
        }

        output = {
            "Jonas": {
                "Sophie": {
                    "Nick": {
                        "Pete": {},
                        "Barbara": {}
                    }
                }
            }
        }
        self.assertDictEqual(organize_hierarchy(entry), output)

    def test_organize_hierarchy_multiple_roots(self):
        entry = {
            "Pete": "Nick",
            "Barbara": "Nick",
            "Nick": "Sophie",
            "Sophie": "Jonas",
            "Jane": "Reenah",
        }

        two_roots = {
            'Jonas': {
                'Sophie': {
                    'Nick': {
                        'Pete': {},
                        'Barbara': {}
                    }
                }
            },
            'Reenah': {
                'Jane': {}
            }
        }
        self.assertDictEqual(organize_hierarchy(entry), two_roots)

    def test_organize_hierarchy_empty_dict(self):
        self.assertDictEqual(organize_hierarchy({}), {})


class TestConstructHierarchyTree(unittest.TestCase):

    def test_construct_hierarchy_tree_with_multiple_children(self):
        hierarchy = {
            "Jonas": {
                "Sophie": {
                    "Nick": {
                        "Pete": {},
                        "Barbara": {}
                    }
                }
            }
        }
        root_employee = construct_hierarchy_tree(hierarchy)
        self.assertEqual(root_employee.name, "Jonas")
        self.assertIsNone(root_employee.supervisor)
        self.assertEqual(len(root_employee.subordinates), 1)
        self.assertEqual(root_employee.subordinates[0].name, "Sophie")
        self.assertEqual(root_employee.subordinates[0].subordinates[0].name, "Nick")

    def test_construct_hierarchy_tree_with_one_child(self):
        hierarchy = {"Peter": {"Ham": {}}}
        root_employee = construct_hierarchy_tree(hierarchy)
        self.assertEqual(root_employee.name, "Peter")
        self.assertIsNone(root_employee.supervisor)
        self.assertEqual(len(root_employee.subordinates), 1)
        self.assertEqual(root_employee.subordinates[0].name, "Ham")
        self.assertEqual(len(root_employee.subordinates[0].subordinates), 0)

    def test_construct_hierarchy_tree_with_no_child(self):
        hierarchy = {"Tender": {}}
        root_employee = construct_hierarchy_tree(hierarchy)
        self.assertEqual(root_employee.name, "Tender")
        self.assertIsNone(root_employee.supervisor)
        self.assertEqual(len(root_employee.subordinates), 0)

    def test_construct_hierarchy_tree_with_no_employee(self):
        hierarchy = {}
        root_employee = construct_hierarchy_tree(hierarchy)
        self.assertIsNone(root_employee)


class TestDoMPTTtraversal(unittest.TestCase):

    def test_do_mptt_traversal_with_multiple_children(self):
        hierarchy = {
            "Jonas": {
                "Sophie": {
                    "Nick": {
                        "Pete": {},
                        "Barbara": {}
                    }
                }
            }
        }
        mppt_dict = do_mptt_traversal(hierarchy)
        self.assertListEqual(list(mppt_dict.keys()), ["Jonas", "Sophie", "Nick", "Pete", "Barbara"])
        self.assertIsNone(mppt_dict["Jonas"]["supervisor_id"])
        self.assertEqual(mppt_dict["Jonas"]["lft"], 1)
        self.assertEqual(mppt_dict["Jonas"]["rgt"], 10)
        self.assertEqual(mppt_dict['Sophie']['lft'], 2)
        self.assertEqual(mppt_dict['Sophie']['rgt'], 9)
        self.assertEqual(mppt_dict['Barbara']['lft'], 6)
        self.assertEqual(mppt_dict['Barbara']['rgt'], 7)

    def test_do_mptt_traversal_with_one_child(self):
        hierarchy = {"Peter": {"Ham": {}}}
        mppt_dict = do_mptt_traversal(hierarchy)
        self.assertListEqual(list(mppt_dict.keys()), ["Peter", "Ham"])
        self.assertIsNone(mppt_dict["Peter"]["supervisor_id"])
        self.assertEqual(mppt_dict["Peter"]["lft"], 1)
        self.assertEqual(mppt_dict["Peter"]["rgt"], 4)
        self.assertEqual(mppt_dict['Ham']['lft'], 2)
        self.assertEqual(mppt_dict['Ham']['rgt'], 3)

    def test_do_mptt_traversal_with_no_child(self):
        hierarchy = {"Tender": {}}
        mppt_dict = do_mptt_traversal(hierarchy)
        print(mppt_dict)
        self.assertListEqual(list(mppt_dict.keys()), ["Tender"])
        self.assertIsNone(mppt_dict["Tender"]["supervisor_id"])
        self.assertEqual(mppt_dict["Tender"]["lft"], 1)
        self.assertEqual(mppt_dict["Tender"]["rgt"], 2)

    def test_construct_hierarchy_tree_with_no_employee(self):
        hierarchy = {}
        mppt_dict = do_mptt_traversal(hierarchy)
        self.assertDictEqual(mppt_dict, {})
