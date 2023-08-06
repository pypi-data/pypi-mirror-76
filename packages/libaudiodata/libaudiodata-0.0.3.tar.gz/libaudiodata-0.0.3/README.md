# libdct: A library for audio processing by Discrete Cosine Transform (DCT)

### The library is to facilitate audio processing with  Discrete Cosine Transform. 

DCT are the kind of transforms that avoid doing signal process in complex Fourier space. 
Since most deep networks are difficult to capture relations in complext space, DCT are good choices for extacting audio features or generating audio signal using deep learning

The wav graph of LJ001-0025.wav:




![alt text](./samples/wav.png "wav")

The dct_spectrogram: 

![alt text](./samples/dct.png "dct")


### install


git clone https://github.com/ranchlai/libdct.git
cd libdct && python setup.py install

or 

pip install libdct --upgrade





### Reference: 
[1] Method and device for conducting noise suppression on image, WO2015135208A1
