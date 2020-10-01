conda env list
python3 -m venv py38/
. py38/bin/activate

#Make sure that /usr/local/bin is in your $PATH.
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.36.0/install.sh | bash
export NVM_DIR="$HOME/.nvm"
echo $NVM_DIR
cd $NVM_DIR
npm i

# install neuroglancer dev
pip install neuroglancer-scripts
#serifos soup
cd /Users/alex/anaconda/envs/py38/lib/python3.8/site-packages/neuroglancer/neuroglancer-scripts/src/neuroglancer_scripts/scripts
python /Users/alex/anaconda/envs/py38/lib/python3.8/site-packages/neuroglancer/neuroglancer-scripts/src/neuroglancer_scripts/scripts/volume_to_precomputed.py '/Users/alex/AlexBadeaMyCodes/skullstrip-master/images/B52825_T1_masked.nii.gz' '/Users/alex/skullstrip-master/precomputed/'  --generate-info

 python generate_scales_info.py /Users/alex/skullstrip-master/precomputed/info_fullres.json /Users/alex/skullstrip-master/precomputed
 python /Users/alex/anaconda/envs/py38/lib/python3.8/site-packages/neuroglancer/neuroglancer-scripts/src/neuroglancer_scripts/scripts/volume_to_precomputed.py '/Users/alex/AlexBadeaMyCodes/skullstrip-master/images/B52825_T1_masked.nii.gz' '/Users/alex/skullstrip-master/precomputed/'
