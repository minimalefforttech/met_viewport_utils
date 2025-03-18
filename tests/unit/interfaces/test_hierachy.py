import pytest
from met_viewport_utils.interfaces.hierachy import IHierarchyItem

class TestIHierarchyItem:
    def test_parent_setter(self):
        item1 = IHierarchyItem()
        item2 = IHierarchyItem()
        item1.parent = item2
        assert item1.parent == item2
        assert item2.children == [item1]
        item1.parent = None
        assert item1.parent == None
        assert item2.children == []

    def test_append(self):
        parent = IHierarchyItem()
        child1 = IHierarchyItem()
        child2 = IHierarchyItem()
        parent.append(child1)
        assert parent.children == [child1]
        assert child1.parent == parent
        parent.append([child2])
        assert parent.children == [child1, child2]
        assert child2.parent == parent

    def test_insert(self):
        parent = IHierarchyItem()
        child1 = IHierarchyItem()
        child2 = IHierarchyItem()
        parent.append(child1)
        parent.insert(0, child2)
        assert parent.children == [child2, child1]
        assert child1.parent == parent
        assert child2.parent == parent

    def test_clear(self):
        parent = IHierarchyItem()
        child1 = IHierarchyItem()
        child2 = IHierarchyItem()
        parent.append([child1, child2])
        parent.clear()
        assert parent.children == []

    def test_get_root(self):
        item1 = IHierarchyItem()
        item2 = IHierarchyItem()
        item3 = IHierarchyItem()
        item1.append(item2)
        item2.append(item3)
        assert item3.get_root() == item1
        assert item1.get_root() == item1

    def test_iter_descendants(self):
        item1 = IHierarchyItem()
        item2 = IHierarchyItem()
        item3 = IHierarchyItem()
        item1.append([item2, item3])
        descendants = list(item1.iter_descendants())
        assert descendants == [item2, item3]

        item4 = IHierarchyItem()
        item2.append(item4)
        descendants = list(item1.iter_descendants())
        assert descendants == [item2, item4, item3]

    def test_iter_parents(self):
        item1 = IHierarchyItem()
        item2 = IHierarchyItem()
        item3 = IHierarchyItem()
        item1.name = "item1"
        item2.name = "item2"
        item3.name = "item3"
        item1.append(item2)
        item2.append(item3)
        parents = list(item3.iter_parents())
        assert len(parents) == 2
        assert parents[0].name == "item2"
        assert parents[1].name == "item1"

    def test_path(self):
        item1 = IHierarchyItem()
        item2 = IHierarchyItem()
        item3 = IHierarchyItem()
        item1.name = "item1"
        item2.name = "item2"
        item3.name = "item3"

        item1.append(item2)
        item2.append(item3)

        assert item1.path == "/item1"
        assert item2.path == "/item1/item2"
        assert item3.path == "/item1/item2/item3"
