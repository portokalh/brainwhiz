from __future__ import print_function

import webbrowser

import numpy as np

import neuroglancer

viewer = neuroglancer.Viewer()

a = np.zeros((3, 100, 100, 100), dtype=np.uint8)
ix, iy, iz = np.meshgrid(*[np.linspace(0, 1, n) for n in a.shape[1:]], indexing='ij')
a[0, :, :, :] = np.abs(np.sin(4 * (ix + iy))) * 255
a[1, :, :, :] = np.abs(np.sin(4 * (iy + iz))) * 255
a[2, :, :, :] = np.abs(np.sin(4 * (ix + iz))) * 255

with viewer.txn() as s:
    s.layers['image'] = neuroglancer.ImageLayer(
        source='a.  nifti://http://127.0.0.1:9000/Users/alex/AlexBadeaMyAtlases/atlases/chass_symmetric3/chass_symmetric3_FA.nii.gz',
    )
    # s.layers['ground_truth'] = neuroglancer.SegmentationLayer(
    #    source='precomputed://gs://neuroglancer-public-data/flyem_fib-25/ground_truth',
    # )
    s.layers['overlay'] = neuroglancer.ImageLayer(
        # source=neuroglancer.LocalVolume(a, voxel_size=[8, 8, 8], voxel_offset=[3000, 3000, 3000]),
        shader="""

void main() {
  emitRGB(vec3(toNormalized(getDataValue(0)),
               toNormalized(getDataValue(1)),
               toNormalized(getDataValue(2))));
}
""",
    )
    s.voxel_coordinates = [3000, 3000, 3000]

num_actions = 0


def my_action(s):
    global num_actions
    num_actions += 1
    with viewer.config_state.txn() as st:
        st.status_messages['hello'] = ('Got action %d: mouse position = %r' %
                                       (num_actions, s.mouse_voxel_coordinates))
    print('Got my-action')
    print('  Mouse position: %s' % (s.mouse_voxel_coordinates,))
    print('  Layer selected values: %s' % (s.selected_values,))


viewer.actions.add('my-action', my_action)
with viewer.config_state.txn() as s:
    s.input_event_bindings.viewer['keyt'] = 'my-action'
    s.status_messages['hello'] = 'Welcome to this example'

# with viewer.txn() as s:
#    s.layout = '3d'
#    s.projection_scale = 3000

"""
from ipywidgets import Image
screenshot = viewer.screenshot(size=[1000, 1000])
screenshot_image = Image(value=screenshot.screenshot.image)
screenshot_image
"""

with viewer.txn() as s:
    s.layout = neuroglancer.row_layout(
        [neuroglancer.LayerGroupViewer(layers=['image', 'overlay'])])
#         neuroglancer.LayerGroupViewer(layers=['segmentation'])])

# with viewer.txn() as s:
#    s.layout = neuroglancer.row_layout(
#        [neuroglancer.LayerGroupViewer(layers=['image']),
#         neuroglancer.LayerGroupViewer(layers=['segmentation'])])

print(neuroglancer.to_url(viewer.state))
print(viewer.state)
print(viewer)
webbrowser.open_new(viewer.get_viewer_url())
