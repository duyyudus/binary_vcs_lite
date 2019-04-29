from _setup_test import *


class TestCoreState(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super(TestCoreState, self).__init__(*args, **kwargs)

    def setUp(self):
        create_workspace_dir()

    def tearDown(self):
        cleanup_output_data()

    def test_state_node(self):
        log_info()
        last = state.Node('last')
        med_res = state.Node('medRes', None, last, verbose=1)
        med_asset = state.Node('asset.ma', 'med_asset_hash', med_res, verbose=1)
        med_asset_rig = state.Node('asset.rig.ma', 'med_asset_rig_hash', med_res, verbose=1)
        med_tex = state.Node('textures', None, med_res, verbose=1)
        tex_1 = state.Node('tex_1.tif', 'tex_1_hash', med_tex, verbose=1)
        tex_2 = state.Node('tex_2_new.tif', 'tex_2_hash', med_tex, verbose=1)
        med_old = state.Node('old', None, med_res, verbose=1)

        proxy_res = state.Node('proxyRes', None, last, verbose=1)
        proxy_asset = state.Node('asset.ma', 'proxy_asset_hash', proxy_res, verbose=1)
        proxy_asset_rig = state.Node('asset.rig.ma', 'proxy_asset_rig_hash', proxy_res, verbose=1)

        self.assertEqual(last.child_count, 2)
        self.assertEqual(med_asset.node_path, Path('last/medRes/asset.ma'))
        self.assertEqual(med_asset_rig.node_path, Path('last/medRes/asset.rig.ma'))
        self.assertEqual(tex_1.node_path, Path('last/medRes/textures/tex_1.tif'))
        self.assertEqual(tex_2.node_path, Path('last/medRes/textures/tex_2_new.tif'))
        self.assertEqual(tex_1.parent, med_tex)

        self.assertEqual(proxy_asset.node_path, Path('last/proxyRes/asset.ma'))
        self.assertEqual(proxy_asset_rig.node_path, Path('last/proxyRes/asset.rig.ma'))
        self.assertFalse(med_tex.is_file)
        self.assertEqual(med_tex.child_count, 2)

        med_old.add_child(med_asset)
        self.assertEqual(med_asset.node_path, Path('last/medRes/old/asset.ma'))
        self.assertEqual(med_res.child_count, 3)
        self.assertEqual(med_asset.parent, med_old)

        med_old.set_parent(last)
        self.assertEqual(med_asset.node_path, Path('last/old/asset.ma'))
        self.assertEqual(med_res.child_count, 2)


@log_test(__file__)
def run():
    testcase_classes = [
        TestCoreState,
    ]
    for tc in testcase_classes:
        testcase = unittest.TestLoader().loadTestsFromTestCase(tc)
        unittest.TextTestRunner(verbosity=2).run(testcase)


if __name__ == '__main__':
    run()
