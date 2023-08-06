# hishiryo 
*Consciousness beyond thought ^_^*

Hishiryo is a tool to generate a circular dataviz of any csv dataset.

This little experiment aims at trying to quickly represent the content of a dataset and make it funny to discover it's patterns!

Each datapoint (like a cell in an excel sheet) is converted into a pixel , and this pixel is diplayed on a circular graph.

This version supports the following column data formats : float, integers and text as nominal categories.

## How to install

With PyPI

    pip install hishiryo

## Dependencies

- Pandas
- CV2 (OpenCV)
- Pillow
- svgwrite

## How to use

1 - find an appropriate csv. (more than 100 rows will start to overload the result a little)

2 - in python 3 in your code or from a Jupyter notebook :

    from hishiryo import Hishiryo

    HishiryoConverter = Hishiryo.Hishiryo()
    
    input_path = "/home/user/iris.csv"
    separator = ','
    output_path = "/home/user/iris.png"
    radius = 500
    
    HishiryoConverter.convertCSVToRadialBitmap(input_path,separator,output_path,radius,None,"Dot")

Arguments :

- `input path` is the path to your csv file (e.g. /home/user/iris.csv)
- `output path` is the path to your target image file (e.g. /home/user/iris.png) The fileformat you want is autodetected thanks to CV2 functionalities.
- `separator` is the character separator in your csv (e.g. ",")
- `radius` (in pixel) is the size of the radius of the disk where the pixels will be drawn. The higher it is the bigger and sharper your output image will be. (e.g:  1500)'
- `sort_by` is the name of the column or the list of column you want to sort you data. (e.g. "Sepal.Length", or ["Sepal.Length","Sepal.Width"])
- `glyph_type` is the type of representation you want for the pixels. it can be one among the following : "Dot","Square" or "Polygon"

        input_path = "path/to/your/csv/file.csv"
        output_path = "path/to/your/rendered/image.png"
        separator = ","
        radius = 3000
        sort_by = None
        glyph_type = "Polygon"

Colors are assigned based on the variable type.

- Blue circles represent integer values
- Red circles, float values
- Random colors are assigned to categorical variables.
- Black is the default value for value 0 or when there is no data

## Output example

See below an example of a visualisation generated from the train titanic dataset
![output example](thumbnail_example.png)

The 12 columns of the dataset are represented as 12 circular rows. The first column is rendered as the inner circle, and the last as the outer one.


Here is an overview of the MNIST train dataset, sort by label
![output example](thumbnail_mnist.png)

## Licence

GNU General Public License v3.0