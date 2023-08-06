import detect_binod
import argparse

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--image','-i', type=str, required=True, help='Image file for detecting Binod')
    args = parser.parse_args()
    detect_binod.detect(args.image)
