import torch
# CLIP (Contrastive Language-Image Pre-Training) from the openAI 
import open_clip
# util module is used for working with embeddings
from sentence_transformers import util
from PIL import Image
import requests
from PIL import Image
from io import BytesIO




# Define the device
device = "cuda" if torch.cuda.is_available() else "cpu"

# Create the model and preprocess function
model, _, preprocess = open_clip.create_model_and_transforms('ViT-L-14', pretrained="laion2b_s32b_b82k")
model.to(device)



def imageEncoder(url):
    """
        This function takes image in numpy array, convert to 'rgb' format.
        The preprocess function is obtained from the open_clip.create_model_and_transforms 
        function and includes steps such as resizing, normalization, .unsqueeze(0) adds an extra 
        dimension to the tensor, making it a batch of size 1. The encode_image method outputs a feature vector.
    """
    print("url: ", url)
    response = requests.get(url)
    img = Image.open(BytesIO(response.content)).convert("RGB")
    img = preprocess(img).unsqueeze(0).to(device)
    img = model.encode_image(img)
    return img


def generateScore(image1, image2):
    """
    pytorch_cos_sim computes the cosine similarity between the two tensors img1 and img2.
    float(cos_scores[0][0])*100 converts the extracted score to a percentage.

    """
    img1 = imageEncoder(image1)
    img2 = imageEncoder(image2)

    cos_scores = util.pytorch_cos_sim(img1, img2)
    score = round(float(cos_scores[0][0])*100, 2)
    
    return score


url1 = 'https://photos.zillowstatic.com/fp/1ef03badd2812c19df1a33c7f38cc76e-cc_ft_384.webp'
url2 = 'https://photos.zillowstatic.com/fp/1223ee83a76d9913677197e31ab36c7b-cc_ft_384.webp'

print(generateScore(url1, url2))