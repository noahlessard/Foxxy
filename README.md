# Foxxy

A easy to use web GUI that allows you to play with the codegen models, even if you don't have a huge amount of memory. Needs Cuda and accelerate. 

Currently, the 350 million, 2 billion and 6 billion models are supported. They are loaded by utilizing the automatic device mapping provided by huggingface's transformers. 

It is not an end all solution. Large models will take longer to run and could strain your computer's hard drive/SSD, but will be more accurate. Small models will be faster but might not be as accurate. 

## Installation
First install CUDA 11.6 or greater first, and get the correct pytorch from your system.
Then install the requirements in requirements.txt with pip
Finally, just run the python file and go the the url outputted.
