import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from models.processing import process_video, make_prediction, find_clips, create_clips
from flask import Flask, render_template, request, jsonify
from models.model import VideoAutoClipper2, load_model
from werkzeug.utils import secure_filename
from datetime import datetime
import joblib
import json


class Config:
    def __init__(self, config_file_path):
        config_default = {
            "use_gpu": False,
            "auto_load_model": False,
            "segment_length": 600,
            "minimum_clip_length": 5,
            "maximum_clip_length": 30,
            "pad_clip_start": 1.0,
            "pad_clip_end": 1.0,
            "number_of_clips": 2,
            "threshold": 0.7,
            "leniency": 2
        }

        if not os.path.exists(config_file_path):
            with open(config_file_path, "w") as f:
                json.dump(config_default, f, indent="\t")

        with open(config_file_path, "r") as f:
            config = json.load(f)

        self.use_gpu = config.get("use_gpu", False)
        self.auto_load_model = config.get("auto_load_model", False)
        self.segment_length = config.get("segment_length", 600)

        self.minimum_clip_length = config.get("minimum_clip_length", 5)
        self.maximum_clip_length = config.get("maximum_clip_length", 30)
        self.pad_clip_start = config.get("pad_clip_start", 1.0)
        self.pad_clip_end = config.get("pad_clip_end", 1.0)
        self.number_of_clips = config.get("number_of_clips", 2)

        self.threshold = config.get("threshold", 0.7)
        self.leniency = config.get("leniency", 2)

    def get_device(self):
        return "cuda" if self.use_gpu else "cpu"


def get_folder_name():
    return datetime.now().strftime("%Y-%m-%d")


def get_files(clip_folder):
    folder_list = os.listdir(clip_folder)
    all_files = {}

    for folder in folder_list:
        folder_path = os.path.join(clip_folder, folder)
        files = os.listdir(folder_path)
        all_files[folder] = files

    return all_files


app = Flask(__name__)
video_folder = os.path.abspath("./static/uploads")
clip_folder = os.path.abspath("./static/clips")
static_folder = os.path.abspath("./static")
output_folder = os.path.abspath(os.path.join(clip_folder, get_folder_name()))

os.makedirs(video_folder, exist_ok=True)
os.makedirs(clip_folder, exist_ok=True)

model_path = os.path.abspath("./models/VideoAutoClipper.pt")
scaler_path = os.path.abspath("./models/mfcc_scaler.joblib")

config_file_path = os.path.abspath("./config.json")
config = Config(config_file_path)

model = load_model(VideoAutoClipper2(), model_path, device=config.get_device()) if config.auto_load_model else False

@app.route("/", methods=["GET", "POST"])
def main():
    global model

    if request.method == "POST":
        if "video" in request.files:
            try:
                video = request.files["video"]
                if video:
                    print("Processing video...")

                    filename = secure_filename(video.filename)
                    video_path = os.path.join(video_folder, filename)
                    video.save(video_path)

                    if not model:
                        model = load_model(VideoAutoClipper2(), model_path, device=config.get_device())

                    video_paths = process_video(video_path, config.segment_length, video_folder)
                    predictions = []

                    print("Making predictions...")

                    for path in video_paths:
                        prediction, sr = make_prediction(model, joblib.load(scaler_path), path, threshold=config.threshold, device=config.get_device())
                        predictions.extend(prediction)

                    print("Creating clips...")

                    clip_timestamps = find_clips(predictions, sr, config.minimum_clip_length, config.maximum_clip_length, config.number_of_clips, config.leniency)
                    clip_paths = create_clips(video_path, clip_timestamps, output_folder, config.pad_clip_start, config.pad_clip_end)
                    clip_urls = [os.path.relpath(clip_path, static_folder).replace("\\", "/") for clip_path in clip_paths]

                    print("Done!")

                    return render_template("index.html", config=config, clips=clip_urls, folders=get_files(clip_folder))

            except Exception as e:
               print(e)

            finally:
                if len(os.listdir(video_folder)) != 0:
                    for path in os.listdir(video_folder):
                        os.remove(os.path.join(video_folder, path))

    return render_template("index.html", config=config, folders=get_files(clip_folder))


@app.route("/get-config", methods=["POST"])
def get_config():
    try:
        global model
        previous_device = config.use_gpu

        config.use_gpu = request.form.get("use-gpu") == "on"
        config.auto_load_model = request.form.get("auto-load-model") == "on"
        config.segment_length = int(request.form.get("segment-length"))

        config.minimum_clip_length = int(request.form.get("minimum-clip-length"))
        config.maximum_clip_length = int(request.form.get("maximum-clip-length"))
        config.pad_clip_start = float(request.form.get("pad-clip-start"))
        config.pad_clip_end = float(request.form.get("pad-clip-end"))
        config.number_of_clips = int(request.form.get("number-of-clips"))

        config.threshold = float(request.form.get("threshold"))
        config.leniency = int(request.form.get("leniency"))
        if previous_device != config.use_gpu and model:
            model = load_model(VideoAutoClipper2(), model_path, device=config.get_device())

    except ValueError as e:
        print(e)

    finally:
        return jsonify({"status": "success", "message": "Settings succesfully updated"})


@app.route("/save-config", methods=["POST"])
def save_config():
    with open(config_file_path, "w") as f:
        json.dump(config.__dict__, f)
    
    return jsonify({"status": "success", "message": "Settings succesfully updated"})


if __name__ == "__main__":
    app.run(port=5000)
