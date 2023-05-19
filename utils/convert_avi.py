from moviepy.editor import VideoFileClip

def convert_avi_to_mp4(input_path, output_path):
    # Load the AVI video
    video = VideoFileClip(input_path)

    # Set the output file path with the .mp4 extension
    output_path_with_extension = output_path if output_path.endswith(".mp4") else output_path + ".mp4"

    # Write the video to MP4 format
    video.write_videofile(output_path_with_extension, codec="libx264")

    # Close the video file
    video.close()
