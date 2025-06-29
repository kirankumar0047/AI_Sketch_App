import torch

def load_midas_model():
    midas = torch.hub.load("intel-isl/MiDaS", "MiDaS_small")
    midas.eval()
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    midas.to(device)

    transforms = torch.hub.load("intel-isl/MiDaS", "transforms")
    transform = transforms.small_transform

    return midas, transform, device