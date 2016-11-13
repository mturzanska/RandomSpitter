from random_shrubs.shrubs import Shrub


class TestShrub:

    def test_grow(self, data):
        shrub = Shrub(df=data.df, attr_cols=data.attr_cols,
                      class_col=data.class_col)
        shrub.grow()
        assert shrub.nodes
        assert shrub.leaves
        assert not shrub.stubs

    def test_nodes(self, data):
        shrub = Shrub(df=data.df, attr_cols=data.attr_cols,
                      class_col=data.class_col)
        shrub.grow()
        depth = len(shrub.attr_cols)
        nodes_vs_depth = {d: pow(2, d) for d in range(depth + 1)}
        assert len(shrub.stubs) == 0
        assert len(shrub.leaves) == nodes_vs_depth[depth]
        assert len(shrub.nodes) == (pow(2, depth + 1) - 1) - len(shrub.leaves)
