import argparse, subprocess, os
import image_gridder

def split_video_to_png(input, output, rate):
    if os.path.exists(output) and os.path.isdir(output):
        # TODO Check if files are in the output folder
        pass
    else:
        os.mkdir(output)
    
    ffmpeg_command = [
        'ffmpeg',
        '-i', input,
        '-r', rate,
        output + '/%05d.png'
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
    
if __name__ == "__main__":
    main()
