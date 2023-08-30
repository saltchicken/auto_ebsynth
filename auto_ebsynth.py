import argparse, subprocess, os, shutil, time
from image_gridder import grid_joiner, grid_splitter
from run_a1111 import process_image
from pyesrgan import run_esrgan

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
        os.mkdir(output + '/tempkeyframes')
    
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
    shutil.copy(output_path + '/frames/' + image_files[0], output_path + '/tempkeyframes')
    shutil.copy(output_path + '/frames/' + image_files[int(len(image_files) / 3)], output_path + '/tempkeyframes')
    shutil.copy(output_path + '/frames/' + image_files[int(len(image_files) / 3) * 2], output_path + '/tempkeyframes')
    shutil.copy(output_path + '/frames/' + image_files[len(image_files) - 1], output_path + '/tempkeyframes')
    
    grid_joiner(output_path + '/tempkeyframes/', output_path + '/')
    process_image(output_path + '/combined_grid.png', output_path)
    run_esrgan(output_path + '/filtered.png', output_path + '/resized.png', 2)
    directory_path = output_path + "/tempkeyframes"
    all_items = os.listdir(directory_path)
    file_names = [item for item in all_items if os.path.isfile(os.path.join(directory_path, item))]
    grid_splitter(output_path + '/resized.png', output_path + '/keyframes', file_names)
    
    
if __name__ == "__main__":
    main()
