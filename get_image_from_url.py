def get_image_from_url(uniq_id,name,category,url):
    try:
    # Image
        import requests
        import pandas as pd
        import numpy as np
        from PIL import Image
        import requests
        from io import BytesIO
        from concurrent.futures import ProcessPoolExecutor
        import json
        import uuid
        from tqdm import tqdm_notebook as tqdm
        response = requests.get(url)
        print(response)
        img = Image.open(BytesIO(response.content))
        img = img.resize((250, 250), Image.ANTIALIAS)
        
        img.save('/Users/jyotibhandari/Documents/Machine Learning /Project/Flipkart_images2/{}.jpg'.format(uniq_id))
        
        # Metadata
        img_metadata = pd.DataFrame({'id': [uniq_id],
                                     'name': [name],
                                     'category': [category]})
        return img_metadata
    except:
        print('fail: {}'.format(url))
        pass