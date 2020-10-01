from __future__ import print_function

import webbrowser

import numpy as np

import neuroglancer

viewer = neuroglancer.Viewer()
print(viewer)

with viewer.txn() as s:
    s.layers['image'] = neuroglancer.ImageLayer(
        #source='nifti://http://127.0.0.1:9000/B51315_T1_masked.nii.gz',
        source='nifti://http://127.0.0.1:9000/B51325_invivoAPOE1_labels.nii.gz'
    )

webbrowser.open_new(viewer.get_viewer_url())
print(neuroglancer.to_url(viewer.state))
print(viewer.state)
print(viewer)
"""