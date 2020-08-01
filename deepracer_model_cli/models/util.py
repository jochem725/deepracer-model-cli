import glob
import os

from typing import Optional, List

def find_coach_chkpt(folder_path: str) -> Optional[str]:
    # First try to find the coach checkpoint file.
    coach_checkpoint_path = glob.glob(os.path.join(folder_path, "**", ".coach_checkpoint"), recursive=True)
    
    # If found return as checkpoint,
    if len(coach_checkpoint_path) > 0:
        with open(coach_checkpoint_path[-1]) as f:
            # Grab last line.
            for line in f:
                pass

            return line

    # If not found load the last available checkpoint.
    coach_checkpoints = find_available_checkpoints(folder_path)
    coach_checkpoint_fn = list(map(lambda x: os.path.basename(x), coach_checkpoints))
    coach_checkpoint_fn_sorted = list(sorted(coach_checkpoint_fn, key = lambda x: int(x.split("_")[0])))

    if len(coach_checkpoint_fn_sorted) > 0:
        return coach_checkpoint_fn_sorted[-1]
    else:
        return None

def find_deepracer_checkpoints_json(folder_path: str) -> Optional[str]:
    coach_checkpoints = glob.glob(os.path.join(folder_path, "**", "deepracer_checkpoints.json"), recursive=True)

    if len(coach_checkpoints) > 0:
        return coach_checkpoints[-1]
    else:
        return None

def find_model_pb(folder_path:str, model_idx: Optional[int] = None) -> Optional[str]:
    # Get all pb files,
    if model_idx is not None:
        model_protobufs = glob.glob(os.path.join(folder_path, "**", "model_{}.pb".format(model_idx)), recursive=True)
    else:
        model_protobufs = glob.glob(os.path.join(folder_path, "**", "*.pb"), recursive=True)

    if len(model_protobufs) > 0:
        return model_protobufs[-1]
    else:
        return None

def find_available_checkpoints(folder_path: str) -> List[str]:
    coach_checkpoints = glob.glob(os.path.join(folder_path, "**", "*.ckpt.index"), recursive=True)

    return list(map(lambda x: x.rstrip(".index"), coach_checkpoints))

def find_model_metadata(folder_path: str) -> Optional[str]:
    coach_checkpoints = glob.glob(os.path.join(folder_path, "**", "model_metadata.json"), recursive=True)

    if len(coach_checkpoints) > 0:
        return coach_checkpoints[-1]
    else:
        return None