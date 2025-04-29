# YouTube Video Tools

**YouTube Video Tools** is a Python-based collection of ready-to-use applications designed for automating tasks related to video post-processing.  
Each tool is set up as an independent app with its own `input`, `output`, `config`, `logs`, and `scripts` folders for clean modular usage.

This project is under active development, and currently includes tools for subtitle generation and burning, with more functionality planned.

---

## Current Status

The project is currently in development, and functionalities are being implemented gradually.  
Each function is organized into its own folder within the repository to allow easy, modular usage of each tool.

---

## Functions and status

- ✅ [subtitle-generator](./subtitle_generator): Generates `.srt` subtitle files from video files using OpenAI Whisper.
- ✅ [subtitle-burner](./subtitle_burner): Burns `.srt` subtitles into a video file using `ffmpeg`.
- ❌ [auto-clipper](./auto_clipper): Automatically extract highlight clips from long videos based on volume or face activity detection.
- ❌ [intro-outro-merger](./intro_outro_merger): Batch-add intro and outro segments to multiple videos automatically.
- ❌ [audio-extractor](./audio_extractor): Extract audio tracks (e.g., `.mp3`) from video files.
- ❌ [thumbnail-generator](./thumbnail_generator): Generate thumbnail images by selecting keyframes from videos.
- ❌ [video-resizer-cropper](./video_resizer_cropper): Resize or crop videos to different dimensions for different platforms.
- ❌ [video-compressor](./video_compressor): Compress videos to reduce file size while maintaining quality.
- ❌ [volume-normalizer](./volume_normalizer): Normalize audio levels across multiple videos automatically.
- ❌ [bad-word-muter](./bad_word_muter): Detect and mute curse words or unwanted speech from videos.
- ❌ [frame-extractor](./frame_extractor): Extract frames at specific intervals and save them as images.
- ❌ [caption-to-video](./caption_to_video): Create a text-only video from a `.srt` subtitle file.
- ❌ [batch-metadata-editor](./batch_metadata_editor): Edit metadata (title, tags, etc.) in batches across multiple video files.
- ❌ [audio-cleanup](./audio_cleanup): Remove or reduce background noise from video audio.
- ❌ [speed-changer](./speed_changer): Speed up or slow down videos in batch processing.
- ❌ [scene-splitter](./scene_splitter): Automatically split videos into clips based on scene changes.

---

## Contributing

Contributors are welcome!  
If you'd like to contribute, please fork the repository, make your changes, and submit a pull request.  
Feel free to open issues for feature requests, bug reports, or general improvements.

---

## License

This project is licensed under the MIT License.  
See the [LICENSE](LICENSE) file for details.

---

*This README will be updated as new functionalities are added.*