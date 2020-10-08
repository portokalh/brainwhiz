
import neuroglancer
import numpy as np
import argparse
from pathlib import Path

viewer = neuroglancer.Viewer()

print(viewer)

parser = argparse.ArgumentParser()
parser.add_argument("nifti_path", type=Path)
p = parser.parse_args()

with viewer.txn() as s:
    s.layers['image'] = neuroglancer.ImageLayer(
        #source='nifti://http://127.0.0.1:9000/B51315_T1_masked.nii.gz',
        source='nifti://http://127.0.0.1:9000/B51325_invivoAPOE1_labels.nii.gz'
    )

webbrowser.open_new(viewer.get_viewer_url())
print(neuroglancer.to_url(viewer.state))
print(viewer.state)
print(viewer)

neuroglancer.stop()