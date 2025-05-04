# YouTube Video Tools

**YouTube Video Tools** is a modular, Python-based collection of video post-processing applications.  
Designed for creators and developers, the toolkit automates common editing tasks—from subtitles and scene detection to AI-assisted editing.

Each tool lives in its own folder with a consistent structure:  
`input/`, `output/`, `config/`, `logs/`, `scripts/` — making the project easy to scale, customize, or contribute to.

This project is under active development. Expect frequent updates and new tools.

## Project Status

- ✅ Core tools like subtitle generation, translation, and burning are implemented and tested.
- ❌ Many advanced and AI-powered tools are planned and will be added incrementally.
- All tools are modular and live in separate folders.

## Functions

### ✅ Implemented

- ✅ [subtitle_burner](./subtitle_burner): Burns `.srt` subtitles into a video file using `ffmpeg`.
- ✅ [subtitle_generator](./subtitle_generator): Generates `.srt` subtitle files from video files using OpenAI Whisper.
- ✅ [subtitle_translator](./subtitle_translator): Translates subtitle files into different languages using offline models.

### ❌ Planned

#### Audio Tools
- ❌ [audio_cleanup](./audio_cleanup): Remove or reduce background noise from video audio.
- ❌ [audio_extractor](./audio_extractor): Extract audio tracks (e.g., `.mp3`) from video files.
- ❌ [volume_normalizer](./volume_normalizer): Normalize audio levels across multiple videos automatically.

#### AI Audio & Speech
- ❌ [ai_auto_tagger](./ai_auto_tagger): Generate tags and keywords from transcripts and visual content.
- ❌ [ai_title_generator](./ai_title_generator): Generate engaging clip titles from transcripts using LLMs.
- ❌ [ai_voice_overdub](./ai_voice_overdub): Clone and overdub speech using the original speaker’s voice.

#### AI Editing & Automation
- ❌ [ai_editor_agent](./ai_editor_agent): Perform editing tasks based on text prompts via AI assistant.
- ❌ [ai_highlight_extractor](./ai_highlight_extractor): Automatically identify and extract the most engaging parts of a video.
- ❌ [ai_jump_cutter](./ai_jump_cutter): Automatically remove silences and pauses to tighten pacing.
- ❌ [ai_retimer](./ai_retimer): Smartly adjust timing of video segments to enhance pacing and storytelling.
- ❌ [ai_shorts_generator](./ai_shorts_generator): Create short-form content from longer videos using highlight detection.

#### AI Visual Tools
- ❌ [ai_color_corrector](./ai_color_corrector): Automatically adjust color grading using style-matching models.
- ❌ [ai_face_blur](./ai_face_blur): Detect and blur faces in videos for privacy protection.
- ❌ [ai_smart_thumbnail_picker](./ai_smart_thumbnail_picker): AI-assisted thumbnail selection based on visual appeal and content.
- ❌ [ai_smart_video_cropper](./ai_smart_video_cropper): Automatically crop to focus on subjects (e.g., for portrait formats).
- ❌ [ai_style_transfer](./ai_style_transfer): Apply neural art styles to video frames for creative transformation.

#### Frame & Thumbnail Tools
- ❌ [frame_extractor](./frame_extractor): Extract frames at specific intervals and save them as images.
- ❌ [storyboard_generator](./storyboard_generator): Create visual storyboards with snapshots and scene summaries.
- ❌ [thumbnail_generator](./thumbnail_generator): Basic thumbnail generation at regular intervals or keyframes.

#### Metadata & Text
- ❌ [bad_word_muter](./bad_word_muter): Detect and mute curse words or unwanted speech from videos.
- ❌ [video_scene_indexer](./video_scene_indexer): Generate a clickable index from scene detection to navigate videos.

#### Video Composition & Enhancement
- ❌ [intro_outro_merger](./intro_outro_merger): Automatically batch-add intro and outro segments to multiple videos.
- ❌ [video_compressor](./video_compressor): Compress videos to reduce file size while maintaining quality.
- ❌ [video_resizer](./video_resizer): Manually resize or crop videos for different dimensions and platforms.

#### Video Splitting & Timing
- ❌ [scene_splitter](./scene_splitter): Automatically split videos into clips based on scene changes.
- ❌ [speed_changer](./speed_changer): Speed up or slow down videos in batch processing.
- ❌ [video_splitter](./video_splitter): Split video into parts based on user-defined time ranges.

## Contributing

Contributions are welcome!  
To contribute:

1. Fork this repository
2. Create your tool based on the folder structure (`input/`, `output/`, `config/`, `logs/`, `scripts/`)
3. Submit a pull request

You can also open issues to report bugs or suggest features.

## License

This project is licensed under the MIT License.  
See the [LICENSE](LICENSE) file for details.

---

*This README will be updated regularly as development progresses.*
