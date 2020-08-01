import tarfile
import typer
import os
import glob
import json

from typing import Optional
from .util import find_coach_chkpt, find_available_checkpoints, find_model_metadata, find_deepracer_checkpoints_json, find_model_pb

class DeepRacerModel():
    def __init__(self, base_path, reward_function_path=None):
        self.base_path = base_path
        self.reward_function_path = reward_function_path

    def validate_car():
        pass
        # TODO: Validate if can be loaded to car using internal car validation code.

    def archive(self, output_file, mode="best"):
        if not mode in ["best", "last"]:
            raise ValueError("Invalid archive mode specified, choose options [\"best\", \"latest\"]")   

        # Attempt to find deepracer_checkpoints.json
        deepracer_checkpoints_json = find_deepracer_checkpoints_json(self.base_path)
        coach_ckpt = find_coach_chkpt(self.base_path)

        checkpoints = {"last": None, "best": None}
        if not deepracer_checkpoints_json:
            if mode == "best":
                typer.echo(u"💾 -> deepracer_checkpoints.json unavailable, attempting to export last checkpoint...")
                mode = "last"
            
            checkpoints = {"last": coach_ckpt, "best": coach_ckpt}
        else:
            typer.echo(u"💾 -> deepracer_checkpoints.json found, loading checkpoints!")
            with open(deepracer_checkpoints_json, "r") as f:
                chkpt_json = json.load(f)
                checkpoints = {"last": chkpt_json["last_checkpoint"]["name"], "best": chkpt_json["best_checkpoint"]["name"]}


        # Get the checkpoint and try to find the model.pb that belongs to it.
        checkpoint = checkpoints[mode]
        typer.echo(u"💾 -> Found {} checkpoint {}".format(mode, checkpoint))
        checkpoint_idx = checkpoint.split("_")[0]

        typer.echo("")
        # Select correct pb file.
        model_pb = find_model_pb(self.base_path, checkpoint_idx)

        if model_pb:
            typer.echo(u"🏎️  -> Found {}".format(model_pb))
        else:
            typer.echo(u"❌ -> Could not find model.pb, aborting...")
            return

        # Find model metadata.
        model_metadata = find_model_metadata(self.base_path)
        
        if model_metadata:
            typer.echo(u"✨ -> Found {}".format(model_metadata))
        else:
            typer.echo(u"❌ -> Could not find model_metadata.json, aborting...")
            return

        # Now create tarball.
        typer.echo(u"\n🗄️  -> Archiving...")

        def reset(tarinfo):
            tarinfo.uid = tarinfo.gid = 0
            tarinfo.uname = tarinfo.gname = ""
            return tarinfo

        with tarfile.open(output_file, "w:gz") as f:
            # Add agent directory.
            t = tarfile.TarInfo('agent')
            t.type = tarfile.DIRTYPE
            t.mode = 0o755

            f.addfile(t)

            f.add(model_metadata, arcname="model_metadata.json", filter=reset)
            f.add(model_pb, arcname=os.path.join("agent", "model.pb"), filter=reset)  

        typer.echo(u"✅ -> Successfully archived model!")