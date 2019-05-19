import requests

def download_image(url):
        images_dir = "/images/"
        img_name = url.split("/")[-1]
        img_file = images_dir + img_name

        #print img_file
        print("downloading {} file...".format(img_file))
        with open(img_file, 'wb') as ifile:
                response = requests.get(url, stream=True)
                if not response.ok:
                        print response
                for block in response.iter_content(1024):
                        if not block:
                                break
                        ifile.write(block)
        print("'{}' file downloaded!!".format(img_file))


urls = [
'http://somewebsrv.com/img/992147.jpg',
'https://homepages.cae.wisc.edu/~ece533/images/airplane.png',
'https://homepages.cae.wisc.edu/~ece533/images/arctichare.png',
'https://homepages.cae.wisc.edu/~ece533/images/baboon.png',
'https://homepages.cae.wisc.edu/~ece533/images/barbara.bmp',
'https://homepages.cae.wisc.edu/~ece533/images/barbara.png',
'https://homepages.cae.wisc.edu/~ece533/images/boat.png'
]

url2 = [
'https://homepages.cae.wisc.edu/~ece533/images/boy.bmp',
'https://homepages.cae.wisc.edu/~ece533/images/boy.ppm',
'https://homepages.cae.wisc.edu/~ece533/images/cameraman.tif',
'https://homepages.cae.wisc.edu/~ece533/images/cat.png',
'https://homepages.cae.wisc.edu/~ece533/images/fprint3.pgm'
]

for url in urls:
        download_image(url)

