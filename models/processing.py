from moviepy.video.io.VideoFileClip import VideoFileClip
import numpy as np
import librosa
import torch
import math
import av
import os


def process_video(video_file, segment_length, output_dir):
    os.makedirs(output_dir, exist_ok=True)
    container = None

    try:
        container = av.open(video_file)
        audio_stream = next(stream for stream in container.streams if stream.type == "audio")

        video_paths = []
        video_part = 0
        clip_start = 0.0

        start_time_offset = audio_stream.start_time * float(audio_stream.time_base)
        duration = audio_stream.duration * float(audio_stream.time_base)

        while clip_start < duration:
            clip_end = min(clip_start + segment_length, duration)

            adjusted_clip_start = clip_start + start_time_offset
            adjusted_clip_end = clip_end + start_time_offset

            output_path = os.path.join(output_dir, f"subclip_{video_part}.wav")
            output_container = av.open(output_path, mode="w")
            output_stream = output_container.add_stream("pcm_s16le", rate=audio_stream.rate)
            # output_stream.channels = audio_stream.channels

            container.seek(int(adjusted_clip_start / float(audio_stream.time_base)), stream=audio_stream)

            for frame in container.decode(audio_stream):
                frame_time = frame.pts * float(frame.time_base)

                if frame_time >= adjusted_clip_end:
                    break

                if frame_time >= adjusted_clip_start:
                    output_container.mux(output_stream.encode(frame))

            output_container.close()
            video_paths.append(output_path)

            clip_start = clip_end
            video_part += 1

        container.close()
        return video_paths

    finally:
        if container:
            container.close()


def make_prediction(model, scaler, video_path, threshold=0.5, device="cpu"):
    audio, sr = librosa.load(video_path, sr=None, mono=True)
    mfcc = librosa.feature.mfcc(y=audio, sr=sr, n_mfcc=40, n_fft=4096, hop_length=2048)

    mfcc = torch.Tensor(scaler.transform(mfcc.T).transpose(-1, 0)).unsqueeze(0)
    mfcc = mfcc.to(device)

    with torch.no_grad():
        if device != "cpu":
            mfcc = mfcc.half()
        predictions = torch.sigmoid(model(mfcc)).squeeze().detach().cpu().numpy()

    predictions = (predictions >= threshold).astype(int)
    return predictions, sr


def find_clips(predictions, sr, minimum_length, maximum_length, number_of_clips):
    clips = []
    start_idx = np.argmax(predictions)

    minimum_length = math.floor(minimum_length * (sr / 2048))
    maximum_length = math.floor(maximum_length * (sr / 2048))

    while len(clips) < number_of_clips:
        if start_idx >= len(predictions) - minimum_length:
            break

        segment = predictions[start_idx:start_idx + minimum_length]
        if 0 in segment:
            start_idx = start_idx + (len(segment) - 1 - segment[::-1].index(0)) + 1
        else:
            end_idx = start_idx + minimum_length
            while end_idx < len(predictions) and predictions[end_idx] != 0 and (end_idx - start_idx) < maximum_length:
                end_idx += 1

            start_sample = start_idx * 2048
            end_sample = (end_idx - 1) * 2048

            start_time = start_sample / sr
            end_time = end_sample / sr

            clips.append((start_time, end_time))
            start_idx = end_idx + 1

    return clips


def create_clips(video_file, clip_timestamps, output_dir, pad_clip_start, pad_clip_end):
    os.makedirs(output_dir, exist_ok=True)
    clip_paths = []

    video = VideoFileClip(video_file)
    clip_number = int(len(os.listdir(output_dir)))

    try:
        for start_time, end_time in clip_timestamps:
            start_time = max(0, (start_time - pad_clip_start))
            end_time = min(video.duration, (end_time + pad_clip_end))

            subclip = video.subclipped(start_time, end_time)
            output_path = os.path.join(output_dir, f"{clip_number}.mp4")
            subclip.write_videofile(output_path, codec="libx264", audio_codec="aac", fps=None, audio_fps=None, logger=None, temp_audiofile=None)

            clip_paths.append(output_path)
            clip_number += 1
        
        return clip_paths
    finally:
        video.close()
