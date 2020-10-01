
import neuroglancer
import numpy as np
import argparse
from pathlib import Path

viewer = neuroglancer.Viewer()

print(viewer)

#parser = argparse.ArgumentParser()
#parser.add_argument("nifti_path", type=Path)
#p = parser.parse_args()

with viewer.txn() as s:
  s.layers['image'] = neuroglancer.ImageLayer(source="nifti://http://127.0.0.1:9000/average_template_25.nii")
  #s.layers['segmentation'] = neuroglancer.SegmentationLayer(source='precomputed://gs://neuroglancer-public-data/flyem_fib-25/ground_truth', selected_alpha=0.3)

with viewer.txn() as s:
    #s.voxel_coordinates = [3000, 3000, 3000]
    s.voxel_coordinates = [1000, 1000, 1000]

with viewer.txn() as s:
    s.layers['segmentation'].visible = False

import cloudvolume
image_vol = cloudvolume.CloudVolume('https://storage.googleapis.com/neuroglancer-public-data/flyem_fib-25/image',
                                    mip=0, bounded=True, progress=False, provenance={})
a = np.zeros((200,200,200), np.uint8)
def make_thresholded(threshold):
  a[...] = image_vol[3000:3200,3000:3200,3000:3200][...,0] > threshold
make_thresholded(110)
# This volume handle can be used to notify the viewer that the data has changed.
volume = neuroglancer.LocalVolume(
    a,
    dimensions=neuroglancer.CoordinateSpace(
        names=['x', 'y', 'z'],
        units='nm',
        scales=[8, 8, 8],
    ),
    voxel_offset=[3000, 3000, 3000])
with viewer.txn() as s:
  s.layers['overlay'] = neuroglancer.ImageLayer(
        source=volume,
      # Define a custom shader to display this mask array as red+alpha.
        shader="""
void main() {
  float v = toNormalized(getDataValue(0)) * 255.0;
  emitRGBA(vec4(v, 0.0, 0.0, v));
}
""",
    )

make_thresholded(100)
volume.invalidate()
"""
with viewer.txn() as s:
  s.layers['segmentation'].segments.update([1752, 88847])
  s.layers['segmentation'].visible = True

viewer.state

viewer.state.layers['segmentation'].segments
"""
import copy
new_state = copy.deepcopy(viewer.state)
#new_state.layers['segmentation'].segments.add(10625)
viewer.set_state(new_state)

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


with viewer.txn() as s:
    s.layout = '3d'
    s.projection_scale = 3000


from ipywidgets import Image
screenshot = viewer.screenshot(size=[1000, 1000])
screenshot_image = Image(value=screenshot.screenshot.image)
screenshot_image


with viewer.txn() as s:
    s.layout = neuroglancer.row_layout(
        [neuroglancer.LayerGroupViewer(layers=['image', 'overlay']),
         neuroglancer.LayerGroupViewer(layers=['segmentation'])])



with viewer.txn() as s:
    s.layout = neuroglancer.row_layout(
        [neuroglancer.LayerGroupViewer(layers=['image']),
         neuroglancer.LayerGroupViewer(layers=['segmentation'])])


print(neuroglancer.to_url(viewer.state))
print(viewer)
webbrowser.open_new(viewer.get_viewer_url())

neuroglancer.stop()