import os
from urllib.parse import unquote, urlparse

import numpy as np
import supervisely as sly
from cv2 import connectedComponents
from dataset_tools.convert import unpack_if_archive
from dotenv import load_dotenv
from supervisely.imaging.color import hex2rgb
from supervisely.io.fs import (
    file_exists,
    get_file_ext,
    get_file_name,
    get_file_name_with_ext,
    get_file_size,
)
from supervisely.io.json import load_json_file
from tqdm import tqdm

import src.settings as s

# https://www.kaggle.com/datasets/humansintheloop/teeth-segmentation-on-dental-x-ray-images


def download_dataset(teamfiles_dir: str) -> str:
    """Use it for large datasets to convert them on the instance"""
    api = sly.Api.from_env()
    team_id = sly.env.team_id()
    storage_dir = sly.app.get_data_dir()

    if isinstance(s.DOWNLOAD_ORIGINAL_URL, str):
        parsed_url = urlparse(s.DOWNLOAD_ORIGINAL_URL)
        file_name_with_ext = os.path.basename(parsed_url.path)
        file_name_with_ext = unquote(file_name_with_ext)

        sly.logger.info(f"Start unpacking archive '{file_name_with_ext}'...")
        local_path = os.path.join(storage_dir, file_name_with_ext)
        teamfiles_path = os.path.join(teamfiles_dir, file_name_with_ext)
        fsize = get_file_size(local_path)
        with tqdm(desc=f"Downloading '{file_name_with_ext}' to buffer..", total=fsize) as pbar:
            api.file.download(team_id, teamfiles_path, local_path, progress_cb=pbar)
        dataset_path = unpack_if_archive(local_path)

    if isinstance(s.DOWNLOAD_ORIGINAL_URL, dict):
        for file_name_with_ext, url in s.DOWNLOAD_ORIGINAL_URL.items():
            local_path = os.path.join(storage_dir, file_name_with_ext)
            teamfiles_path = os.path.join(teamfiles_dir, file_name_with_ext)

            if not os.path.exists(get_file_name(local_path)):
                fsize = get_file_size(local_path)
                with tqdm(
                    desc=f"Downloading '{file_name_with_ext}' to buffer {local_path}...",
                    total=fsize,
                    unit="B",
                    unit_scale=True,
                ) as pbar:
                    api.file.download(team_id, teamfiles_path, local_path, progress_cb=pbar)

                sly.logger.info(f"Start unpacking archive '{file_name_with_ext}'...")
                unpack_if_archive(local_path)
            else:
                sly.logger.info(
                    f"Archive '{file_name_with_ext}' was already unpacked to '{os.path.join(storage_dir, get_file_name(file_name_with_ext))}'. Skipping..."
                )

        dataset_path = storage_dir
    return dataset_path


def convert_and_upload_supervisely_project(
    api: sly.Api, workspace_id: int, project_name: str
) -> sly.ProjectInfo:
    # project_name = "Teeth Segmentation"
    dataset_path = "APP_DATA/archive/Teeth Segmentation JSON/d2"
    obj_class_to_machine_color = (
        "APP_DATA/archive/Teeth Segmentation JSON/obj_class_to_machine_color.json"
    )
    obj_class_to_color = "APP_DATA/archive/Teeth Segmentation JSON/meta.json"
    ds_name = "ds"
    batch_size = 30

    """
        13(plygon) DELETE IN FUTURE DROM RAW DATA
    """

    images_folder_name = "img"
    masks_folder_name = "masks_machine"
    masks_ext = ".png"

    def create_ann(image_path):
        labels = []

        image_name = get_file_name(image_path)
        mask_path = os.path.join(masks_path, image_name + masks_ext)

        if file_exists(mask_path):
            mask_np = sly.imaging.image.read(mask_path)[:, :, 0]
            img_height = mask_np.shape[0]
            img_wight = mask_np.shape[1]
            unique_pixels = np.unique(mask_np)
            for pixel in unique_pixels[1:]:
                obj_class = pixel_to_class[pixel]
                mask = mask_np == pixel
                curr_bitmap = sly.Bitmap(mask)
                curr_label = sly.Label(curr_bitmap, obj_class)
                labels.append(curr_label)

        return sly.Annotation(img_size=(img_height, img_wight), labels=labels)

    class_to_color = {}
    class_to_color_data = load_json_file(obj_class_to_color)["classes"]
    for curr_class_to_color in class_to_color_data:
        class_to_color[curr_class_to_color["title"]] = hex2rgb(curr_class_to_color["color"])

    pixel_to_class = {}
    obj_class_to_color = load_json_file(obj_class_to_machine_color)
    for curr_data in obj_class_to_color:
        pixel = obj_class_to_color[curr_data][0]
        color = class_to_color[curr_data]
        curr_class = sly.ObjClass(curr_data, sly.Bitmap, color=color)
        pixel_to_class[pixel] = curr_class

    project = api.project.create(workspace_id, project_name, change_name_if_conflict=True)
    meta = sly.ProjectMeta(obj_classes=list(pixel_to_class.values()))
    api.project.update_meta(project.id, meta.to_json())

    dataset = api.dataset.create(project.id, ds_name, change_name_if_conflict=True)

    images_path = os.path.join(dataset_path, images_folder_name)
    masks_path = os.path.join(dataset_path, masks_folder_name)

    images_names = os.listdir(images_path)

    progress = sly.Progress("Create dataset {}".format(ds_name), len(images_names))

    for img_names_batch in sly.batched(images_names, batch_size=batch_size):
        images_pathes_batch = [
            os.path.join(images_path, image_name) for image_name in img_names_batch
        ]
        anns_batch = [create_ann(image_path) for image_path in images_pathes_batch]

        img_infos = api.image.upload_paths(dataset.id, img_names_batch, images_pathes_batch)
        img_ids = [im_info.id for im_info in img_infos]

        api.annotation.upload_anns(img_ids, anns_batch)

        progress.iters_done_report(len(img_names_batch))
    return project
