import requests
from tqdm import tqdm
from git import Repo
import os
import subprocess
files = {
    'ComfyUI/models/checkpoints/realisticVisionV60B1_v60B1VAE.safetensors':'https://civitai.com/api/download/models/245598?type=Model&format=SafeTensor&size=full&fp=fp16',
    'ComfyUI/models/loras/add_detail.safetensors':'https://civitai.com/api/download/models/62833',
    'ComfyUI/models/unet/iclight_sd15_fc_unet_ldm.safetensors':'https://huggingface.co/huchenlei/IC-Light-ldm/resolve/main/iclight_sd15_fc_unet_ldm.safetensors?download=true'
}

repos = {
    'ComfyUI-Manager': 'https://github.com/ltdrdata/ComfyUI-Manager',
    'ComfyMath': 'https://github.com/evanspearman/ComfyMath.git',
    'ComfyUI-Easy-Use': 'https://github.com/yolain/ComfyUI-Easy-Use',
    'ComfyUI-KJNodes' : 'https://github.com/kijai/ComfyUI-KJNodes',
    'ComfyUI_UltimateSDUpscale': 'https://github.com/ssitu/ComfyUI_UltimateSDUpscale',
    'comfyui-art-venture': 'https://github.com/sipherxyz/comfyui-art-venture',
    'ComfyUI_essentials': 'https://github.com/cubiq/ComfyUI_essentials',
    'ComfyUI-layerdiffuse': 'https://github.com/huchenlei/ComfyUI-layerdiffuse',
    'sdxl_prompt_styler': 'https://github.com/twri/sdxl_prompt_styler',
    'ComfyUI_Comfyroll_CustomNodes': 'https://github.com/Suzie1/ComfyUI_Comfyroll_CustomNodes',
    'ComfyUI-IC-Light': 'https://github.com/kijai/ComfyUI-IC-Light',
    'image-resize-comfyui': 'https://github.com/palant/image-resize-comfyui',
    'was-node-suite-comfyui' : 'https://github.com/WASasquatch/was-node-suite-comfyui',
    'ComfyUI-IC-Light-Native': 'https://github.com/huchenlei/ComfyUI-IC-Light-Native',
    'ComfyUI-QualityOfLifeSuit_Omar92': 'https://github.com/omar92/ComfyUI-QualityOfLifeSuit_Omar92',
    'masquerade-nodes-comfyui': 'https://github.com/BadCafeCode/masquerade-nodes-comfyui'
}

def download_file(url, local_filename):
    try:
        # Send a GET request to the URL with stream=True
        response = requests.get(url, stream=True)

        # Check if the request was successful
        if response.status_code == 200:
            # Get the total file size from the headers
            total_size = int(response.headers.get('content-length', 0))

            # Open a local file with write-binary mode
            with open(local_filename, 'wb') as file:
                # Use tqdm to create a progress bar
                with tqdm(total=total_size, unit='B', unit_scale=True, desc=local_filename, initial=0, ascii=True) as pbar:
                    # Write the response content to the local file in chunks
                    for chunk in response.iter_content(chunk_size=8192):
                        if chunk:
                            file.write(chunk)
                            pbar.update(len(chunk))
            print(f"File downloaded successfully and saved as {local_filename}")
            return True
        else:
            print(f"Failed to download file. Status code: {response.status_code}")
            return False
    except Exception as e:
        print(f"An error occurred: {e}")
        return False

def clone_repo_and_install_requirements(repo_url, destination):
    try:
        repo_name = os.path.basename(repo_url).replace('.git', '')
        full_path = os.path.join(destination, repo_name)
        
        Repo.clone_from(repo_url, full_path)
        print(f"Repository cloned successfully to {full_path}.")
        
        requirements_path = os.path.join(full_path, 'requirements.txt')
        if os.path.exists(requirements_path):
            subprocess.run(["pip", "install", "-r", requirements_path], check=True)
            print("Dependencies installed successfully.")
        else:
            print("No requirements.txt found.")
    except Exception as e:
        print(f"Failed to clone repository or install dependencies: {e}")

def download_all_files(model_files = files,repos_links = repos):
    for model_file in model_files.items():
        name,link = model_file
        download_file(link,name)
    destination = 'ComfyUI/custom_nodes'
    for repo in repos_links.items():
        name,link = repo
        clone_repo_and_install_requirements(link,destination)
