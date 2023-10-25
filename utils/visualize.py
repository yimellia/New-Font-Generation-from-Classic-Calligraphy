from pathlib import Path
import paddle
import torch
from torchvision import utils as tv_utils
import numpy as np
from PIL import Image, ImageDraw, ImageFont


def make_comparable_grid(*batches, nrow):
    """
    make_comparable_grid
    """
    assert all(len(batches[0]) == len(batch) for batch in batches[1:])
    N = len(batches[0])

    grids = []
    for i in range(0, N, nrow): #nrow=30, N=300
        rows = [batch[i:i+nrow] for batch in batches]
        row = torch.cat(rows)
        grid = to_grid(row, 'torch', nrow=nrow)
        grids.append(grid)

        C, _H, W = grid.shape
        sep_bar = torch.zeros(C, 10, W)
        grids.append(sep_bar)
    return torch.cat(grids[:-1], dim=1)

def normalize(tensor, eps=1e-5):
    """ Normalize tensor to [0, 1] """
    # eps=1e-5 is same as make_grid in torchvision.
    minv, maxv = tensor.min(), tensor.max()
    tensor = (tensor - minv) / (maxv - minv + eps)

    return tensor

def to_grid(tensor, to, **kwargs):
    """ Integrated functions of make_grid and save_image
    Convert-able to torch tensor [0, 1] / ndarr [0, 255] / PIL image / meta_file save
    """
    to = to.lower()
    grid = tv_utils.make_grid(tensor, **kwargs, normalize=True)
    if to == 'torch':
        return grid

def save_tensor_to_image(tensor, filepath, scale=None):
    """ Save torch tensor to filepath
    Same as torchvision.save_image; only scale factor is difference.
    """
    tensor = normalize(tensor)
    ndarr = tensor.mul(255).clamp(0, 255).byte().permute(1, 2, 0).cpu().numpy()
    if ndarr.shape[-1] == 1:
        ndarr = ndarr.squeeze(-1)
    im = Image.fromarray(ndarr)
    if scale:
        size = tuple(map(lambda v: int(v*scale), im.size))
        im = im.resize(size, resample=Image.BILINEAR)
    im.save(filepath)