import argparse, subprocess, os
from image_gridder import grid_joiner, grid_splitter
import shutil

def split_video_to_png(input, output, rate):
    if os.path.exists(output) and os.path.isdir(output):
        # TODO Check if files are in the output folder
        print("Output already exists")
        # TODO better error checking if output already exists
        return False
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
    output_path = args.output + '_' + args.input.split('.')[0]
    
    split_video_to_png(args.input, output_path, args.rate)
    image_files = [f for f in os.listdir(output_path + '/frames') if f.endswith('.png')]
    shutil.copy(output_path + '/frames/' + image_files[0], output_path + '/keyframes')
    shutil.copy(output_path + '/frames/' + image_files[int(len(image_files) / 3)], output_path + '/keyframes')
    shutil.copy(output_path + '/frames/' + image_files[int(len(image_files) / 3) * 2], output_path + '/keyframes')
    shutil.copy(output_path + '/frames/' + image_files[len(image_files) - 1], output_path + '/keyframes')
    
    grid_joiner(output_path + '/keyframes/')
    # TODO Better way to fet filenames of keyframes
    grid_splitter('combined_grid2.png', ['00001', '00006', '00011', '00015'])
    
    
if __name__ == "__main__":
    main()
