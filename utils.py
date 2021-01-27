# Numpy and pandas by default assume a narrow screen - this fixes that
from fastai.vision.all import *
from nbdev.showdoc import *
from ipywidgets import widgets
from pandas.api.types import CategoricalDtype
from itertools import chain

import matplotlib as mpl
# mpl.rcParams['figure.dpi']= 200
mpl.rcParams['savefig.dpi']= 200
mpl.rcParams['font.size']=12

set_seed(42)
torch.backends.cudnn.deterministic = True
torch.backends.cudnn.benchmark = False
pd.set_option('display.max_columns',999)
np.set_printoptions(linewidth=200)
torch.set_printoptions(linewidth=200)

import graphviz
def gv(s): return graphviz.Source('digraph G{ rankdir="LR"' + s + '; }')

def get_image_files_sorted(path, recurse=True, folders=None): return get_image_files(path, recurse, folders).sorted()


# +
# pip install azure-cognitiveservices-search-imagesearch

from azure.cognitiveservices.search.imagesearch import ImageSearchClient as api
from msrest.authentication import CognitiveServicesCredentials as auth

def search_images_bing(key, term, min_sz=128, max_images=150):    
     params = {'q':term, 'count':max_images, 'min_height':min_sz, 'min_width':min_sz}
     headers = {"Ocp-Apim-Subscription-Key":key}
     search_url = "https://api.bing.microsoft.com/v7.0/images/search"
     response = requests.get(search_url, headers=headers, params=params)
     response.raise_for_status()
     search_results = response.json()    
     return L(search_results['value'])

def search_images_bing_many(key, term, total_count=150, min_sz=224):
    """Search for images using the Bing API
    
    :param key: Your Bing API key
    :type key: str
    :param term: The search term to search for
    :type term: str
    :param total_count: The total number of images you want to return (default is 150)
    :type total_count: int
    :param min_sz: the minimum height and width of the images to search for (default is 128)
    :type min_sz: int
    :returns: An L-collection of ImageObject
    :rtype: L
    """
    headers = {"Ocp-Apim-Subscription-Key":key}
    search_url = "https://api.bing.microsoft.com/v7.0/images/search"

    max_count = 150

    imgs = []
    for offset in range(0, total_count, max_count):
        if ((total_count - offset) > max_count):
            count = max_count
        else:
            count = total_count - offset

        params = {'q':term, 'count':count, 'min_height':min_sz, 'min_width':min_sz, 'offset': offset}
        response = requests.get(search_url, headers=headers, params=params)
        search_results = response.json()
        imgs.append(L(search_results['value']))

    return L(chain(*imgs)).attrgot('contentUrl').unique()

PLANT_NAMES = ['nike','adidas','reebok']
plants = map(lambda plant: plant.lower(), PLANT_NAMES)
plants = set(plants)

i = 0
for o in plants:
    i= i+1
    print(f"Downloading images for {o} ({i}/{len(plants)})")
    data_path = Path('shoes')
    if not data_path.exists():
      data_path.mkdir()
    dest = (data_path/o)
    dest.mkdir(exist_ok=True)
    imgs_urls = search_images_bing_many('cde11e5586cb4e9e9f52586c2403588e', f'{o} shoes', total_count=449)
    download_images(dest, urls=imgs_urls)
