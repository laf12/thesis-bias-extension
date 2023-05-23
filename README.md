# Forming Behavior Assessment of Commercially Available Carbon Fiber Reinforced Thermoplastic Tapes

This repository includes the code for calculating the Average Shear Angle for zones A, B and C in the Bias Extension Test.
For more information about this code, please read the thesis found [here](soon)

## Results

500 mm/min | 500 mm/min | 50 mm/min
:--: | :--: | :--:
<img src="github_viz/500_245C_1.gif" alt="GIF 1" width="300%"> | <img src="github_viz/500_245C_2.gif" alt="GIF 1" width="150%"> | <img src="github_viz/50_245C.gif" alt="GIF 1" width="150%">


## Getting Started

To run this code, follow the instructions below:


### Prerequisites

- Make sure you have Python installed on your system. You can download it from the official Python website: [python.org](https://www.python.org/).

### Installation
1. Clone this repository to your local machine using the following command:
```
git clone https://github.com/laf12/thesis-bias-extension/
```
2. On your local machine, change to the project directory:
```
cd thesis-bias-extension/
```
3. Install the requirements, preferably in an anaconda environment:
```
pip install -r requirements.txt
```

### Usage

To run this code, paste the following command in your terminal or command prompt:
```
python main.py
```

### Additional Notes

In the provided `config.yaml` file, there are several flags that control the behavior of the code. Here's an explanation of each flag:

- `trackbar`: This flag determines whether a trackbar (a graphical user interface element) is enabled or disabled. If set to `true`, it implies that a trackbar will be displayed, allowing the user to interactively choose the displayed video frame. 

- `save`: This flag controls whether the processed video will be saved or not.

- `log_values`: This flag determines whether values or metrics related to the video processing will be logged. If set to `true`, the program will log relevant values or metrics.

- `get_gif`: This flag controls whether a GIF (Graphics Interchange Format) will be generated as output. If set to `true`, the program will generate a GIF from the processed video.

- `input_dir`: This specifies the directory where the input videos are located. The program will look for input videos in this directory.

- `input_file`: This specifies the filename of the input video that will be processed.

- `output_dir`: This specifies the directory where the processed videos will be saved. The program will save the output videos in this directory.

- `output_name`: This specifies the desired filename for the processed video.

- `log_dir`: This specifies the directory where log files will be stored. If logging is enabled, the program will save log files in this directory.

- `plot`: This flag controls whether plots or graphs will be generated based on the video processing results. If set to `true`, the program will generate plots. If set to `false`, no plots will be generated.

- `excel`: This flag determines whether an Excel file will be created to store the video processing data or results. If set to `true`, the program will generate an Excel file. If set to `false`, a txt file will be created instead.

## Citation

If you found this repository useful in your work, please consider citing the associated thesis:

```
@thesis{laf-thesis,
  author = {Lara Fadel},
  title = {Forming Behavior Assessment of Commercially Available Carbon Fiber Reinforced Thermoplastic Tapes},
  year = {2023},
  school = {Katholieke Universiteit Leuven },
  address = {Leuven, Belgium}
}
```


