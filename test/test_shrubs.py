from random_shrubs.shrubs import Shrub


class TestShrubInit:

    def test_grow(self, data):
        shrub = Shrub(df=data.df, attr_cols=data.attr_cols,
                      class_col=data.class_col)
        assert shrub.nodes
        assert shrub.leaves
        assert not shrub.stubs

    def test_nodes(self, data):
        shrub = Shrub(df=data.df, attr_cols=data.attr_cols,
                      class_col=data.class_col)
        non_root_nodes = [node for node in shrub.nodes if not node.is_root]
        for node in non_root_nodes:
            assert node.attr in data.attr_cols
            assert node.parent in shrub.nodes
            assert set(node.kids) < set(shrub.nodes)
