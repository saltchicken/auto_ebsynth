import argparse, subprocess, os
import image_gridder
import shutil

# def count_files_in_folder(folder_path):
#     file_count = 0
#     for item in os.listdir(folder_path):
#         item_path = os.path.join(folder_path, item)
#         if os.path.isfile(item_path):
#             file_count += 1
#     return file_count

if __name__ == "__main__":
    folder_path = '/path/to/your/folder'
    num_files = count_files_in_folder(folder_path)
    print(f"Number of files in '{folder_path}': {num_files}")


def split_video_to_png(input, output, rate):
    if os.path.exists(output) and os.path.isdir(output):
        # TODO Check if files are in the output folder
        pass
    else:
        os.mkdir(output)
        os.mkdir(output + '/frames')
        os.mkdir(output + '/keyframes')
    
    ffmpeg_command = [
        'ffmpeg',
        '-i', input,
        '-r', rate,
        output + '/frames' + '/%05d.png'
    ]

    # Run the ffmpeg command
    try:
        subprocess.run(ffmpeg_command, check=True)
        print(f'Conversion complete.')
    except subprocess.CalledProcessError as e:
        print(f'Error during conversion: {e}')

def main():
    parser = argparse.ArgumentParser(description="Automatically setup EBSynth.")
    
    parser.add_argument('-i', '--input', required=True, help='Input video')
    parser.add_argument('-o', '--output', default='output', type=str, help='Output folder')
    parser.add_argument('-r', '--rate', default='1/1', type=str, help='Frames per second')
    # parser.add_argument('--flag', action='store_true', help='Optional flag')
    
    args = parser.parse_args()
    
    # if args.flag:
    #     print('Flag is set')
    
    
    split_video_to_png(args.input, args.output, args.rate)
    # num_files = count_files_in_folder(args.output)
    image_files = [f for f in os.listdir(args.output + '/frames') if f.endswith('.png')]
    shutil.copy(args.output + '/frames/' + image_files[0], args.output + '/keyframes')

    
    
    
    
if __name__ == "__main__":
    main()
