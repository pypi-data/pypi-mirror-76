from typing import Optional, Tuple, Union, List
import torch
import numpy as np
from ....data.subject import Subject
from ....utils import to_tuple
from ....torchio import DATA, TypeTuple, TypeData, TypeTripletInt
from .. import RandomTransform


class RandomSwap(RandomTransform):
    r"""Randomly swap patches within an image.

    This is typically used in `context restoration for self-supervised learning
    <https://www.sciencedirect.com/science/article/pii/S1361841518304699>`_.

    Args:
        patch_size: Tuple of integers :math:`(d, h, w)` to swap patches
            of size :math:`d \times h \times w`.
            If a single number :math:`n` is provided, :math:`d = h = w = n`.
        num_iterations: Number of times that two patches will be swapped.
        p: Probability that this transform will be applied.
        seed: See :py:class:`~torchio.transforms.augmentation.RandomTransform`.
        keys: See :py:class:`~torchio.transforms.Transform`.
    """
    def __init__(
            self,
            patch_size: TypeTuple = 15,
            num_iterations: int = 100,
            p: float = 1,
            seed: Optional[int] = None,
            keys: Optional[List[str]] = None,
            ):
        super().__init__(p=p, seed=seed, keys=keys)
        self.patch_size = to_tuple(patch_size)
        self.num_iterations = self.parse_num_iterations(num_iterations)

    @staticmethod
    def parse_num_iterations(num_iterations):
        if not isinstance(num_iterations, int):
            raise TypeError('num_iterations must be an int,'
                            f'not {num_iterations}')
        if num_iterations < 0:
            raise ValueError('num_iterations must be positive,'
                             f'not {num_iterations}')
        return num_iterations

    @staticmethod
    def get_params():
        # TODO: return locations?
        return

    def apply_transform(self, sample: Subject) -> dict:
        for image in sample.get_images():
            tensors = []
            for tensor in image[DATA]:
                tensor = swap(tensor, self.patch_size, self.num_iterations)
                tensors.append(tensor)
            image[DATA] = torch.stack(tensors)
        return sample


def swap(
        tensor: torch.Tensor,
        patch_size: TypeTuple,
        num_iterations: int,
        ) -> None:
    tensor = tensor.clone()
    patch_size = to_tuple(patch_size)
    for _ in range(num_iterations):
        first_ini, first_fin = get_random_indices_from_shape(
            tensor.shape,
            patch_size,
        )
        while True:
            second_ini, second_fin = get_random_indices_from_shape(
                tensor.shape,
                patch_size,
            )
            larger_than_initial = np.all(second_ini >= first_ini)
            less_than_final = np.all(second_fin <= first_fin)
            if larger_than_initial and less_than_final:
                continue  # patches overlap
            else:
                break  # patches don't overlap
        first_patch = crop(tensor, first_ini, first_fin)
        second_patch = crop(tensor, second_ini, second_fin).clone()
        insert(tensor, first_patch, second_ini)
        insert(tensor, second_patch, first_ini)
    return tensor


def insert(tensor: TypeData, patch: TypeData, index_ini: np.ndarray) -> None:
    index_fin = index_ini + np.array(patch.shape)
    i_ini, j_ini, k_ini = index_ini
    i_fin, j_fin, k_fin = index_fin
    tensor[i_ini:i_fin, j_ini:j_fin, k_ini:k_fin] = patch


def crop(
        image: Union[np.ndarray, torch.Tensor],
        index_ini: np.ndarray,
        index_fin: np.ndarray,
        ) -> Union[np.ndarray, torch.Tensor]:
    i_ini, j_ini, k_ini = index_ini
    i_fin, j_fin, k_fin = index_fin
    return image[..., i_ini:i_fin, j_ini:j_fin, k_ini:k_fin]


def get_random_indices_from_shape(
        shape: TypeTripletInt,
        patch_size: TypeTripletInt,
        ) -> Tuple[np.ndarray, np.ndarray]:
    shape_array = np.array(shape)
    patch_size_array = np.array(patch_size)
    max_index_ini = shape_array - patch_size_array
    if (max_index_ini < 0).any():
        message = (
            f'Patch size {patch_size} must not be'
            f' larger than image size {shape}'
        )
        raise ValueError(message)
    max_index_ini = max_index_ini.astype(np.uint16)
    coordinates = []
    for max_coordinate in max_index_ini.tolist():
        if max_coordinate == 0:
            coordinate = 0
        else:
            coordinate = torch.randint(max_coordinate, size=(1,)).item()
        coordinates.append(coordinate)
    index_ini = np.array(coordinates, np.uint16)
    index_fin = index_ini + patch_size_array
    return index_ini, index_fin
