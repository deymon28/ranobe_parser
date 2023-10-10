import os
import subprocess

# Specify the folder path containing the audio files
folder_path = r"C:\Users\dimag\Desktop\Уроки по минету — копия"

# Get a list of all the .mp3 files in the folder
audio_files = [file for file in os.listdir(folder_path) if file.endswith('.mp3')]

# Sort the audio files in alphabetical order
audio_files.sort()

# Iterate over the audio files in pairs and merge them
for i in range(0, len(audio_files), 2):
    # Get the names of the two files to be merged
    file1 = audio_files[i]
    file2 = audio_files[i + 1] if i + 1 < len(audio_files) else None

    # Skip if file2 is None (odd number of files)
    if file2 is None:
        continue

    # Define the output file name based on file1 and file2
    output_file = f"{file1.split('.')[0]}-{int(file2.split('.')[0][-1:]) + 1}.mp3"

    # Execute FFmpeg command to merge the two files
    ffmpeg_cmd = [
        'ffmpeg', '-i', os.path.join(folder_path, file1), '-i', os.path.join(folder_path, file2),
        '-filter_complex', '[0:a][1:a]concat=n=2:v=0:a=1[outa]', '-map', '[outa]',
        os.path.join(folder_path, output_file)
    ]
    subprocess.run(ffmpeg_cmd)

    # Delete the merged files
    os.remove(os.path.join(folder_path, file1))
    os.remove(os.path.join(folder_path, file2))
