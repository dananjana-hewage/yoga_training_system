import os
import shutil

# Define source paths for datasets
dataset1 = r"C:\Projects\yoga_pose_dataset\DATASET"
dataset2 = r"C:\Projects\archive (8)\yoga_poses"

# Define destination path for merged dataset
merged_dataset = r"C:\Projects\Merged_Dataset"

# Define folder mappings (if needed)
folder_map = {
    "train": "Train",
    "test": "Test",
    "downdog": "Downdog",
    "chair": "Chair",
}

def merge_datasets(source, dest, folder_map):
    for split in ["TRAIN", "TEST"]:  # Adjust as per dataset structure
        for label in os.listdir(os.path.join(source, split.lower())):
            source_folder = os.path.join(source, split.lower(), label)
            if os.path.isdir(source_folder):
                dest_folder = os.path.join(dest, folder_map.get(split.lower(), split), folder_map.get(label.lower(), label))
                os.makedirs(dest_folder, exist_ok=True)
                for file in os.listdir(source_folder):
                    src_file = os.path.join(source_folder, file)
                    dst_file = os.path.join(dest_folder, file)
                    shutil.copy(src_file, dst_file)
                    print(f"Copied {src_file} to {dst_file}")

# Merge datasets
merge_datasets(dataset1, merged_dataset, folder_map)
merge_datasets(dataset2, merged_dataset, folder_map)
