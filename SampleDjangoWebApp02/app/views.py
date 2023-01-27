"""
Definition of views.
"""

from datetime import datetime
from django.shortcuts import render
from django.http import HttpRequest
import time
import requests
import json
from pprint import pprint
import mimetypes
from django.conf import settings
from .forms import UploadForm
from .models import FileUpload
import tweepy
import facebook
import schedule
from time import sleep
from django.views.generic.edit import CreateView
from .forms import ImageUploadForm

class ImageUploadView(CreateView):
    template_name = "app/PostImage/image-upload.html"
    form_class = ImageUploadForm
    success_url = "/"

def home(request):
    """Renders the home page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/index.html',
        {
            'title':'Home Page',
            'year':datetime.now().year,
        }
    )

def PostImage(request):
    """Renders the home page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/PostImage/Index.html',
        {
            'title':'SNS Post',
            'message':'SNS投稿機能',
            'commit': '',
            'year':datetime.now().year,
        },
    )

def Commit(request):

    filepath = request.FILES

    if request.method == 'POST':
        filepath = ImageUploadForm(request.FILES)
        if filepath.is_valid():
            filepath.save()
    else:
        filepath = ImageUploadForm()

    form = request.POST

    # 投稿内容
    #media_url      = r'http://localhost:8000/media/images/kouyou.jpg' 
    media_url       = r'https://cdn.pixabay.com/photo/2015/12/01/20/28/road-1072823_1280.jpg'  # 画像
    media_path      = r"C:\Users\Hiroyuki Honda\Desktop\Pirowork\images\kouyou.jpg"
    mime = mimetypes.guess_type(media_url)
    print(mime)

    media_caption  = form["maintext"] # 投稿文

    check = form.getlist("check[]")
    if "1" in check:
        #Instagram
        instagram_upload_image(media_url, media_caption)
    if "2" in check:
        #Facebook
        facebookPost(media_path, media_caption)
    if "3" in check:
        #Line
        postData(media_caption)
    if "4" in check:
        #Twitter
        tweet(media_caption,media_path)
        #tweet(r'http://localhost:8000/media/images/kouyou.jpg')


    return render(
        request,
        'app/PostImage/Index.html',
        {
            'title':'SNS Post',
            'message':'SNS投稿機能',
            'response': '投稿が完了しました',
            'year':datetime.now().year,
        },
    )

def facebookPost(imgpath,context):
    graph = facebook.GraphAPI(access_token=getattr(settings, "FB_ACCESS_TOKEN", None), version="2.12")
    # Upload an image with a caption.
    graph.put_photo(image=open(imgpath, 'rb'),message=context)
    #graph.put_object(parent_object='me', connection_name='feed',message=context)

def basic_info_Instagram():
    # 初期
    config = dict()
    # アクセストークン
    config["access_token"]         = getattr(settings, "IS_ACCESS_TOKEN", None)
    # アプリID
    config["app_id"]               = getattr(settings, "IS_APP_ID", None)
    # アプリシークレット
    config["app_secret"]           = getattr(settings, "IS_APP_SECRET", None)
    # インスタグラムビジネスアカウントID
    config['instagram_account_id'] = getattr(settings, "IS_INSTAGRAM_ACCOUNT_ID", None)
    # グラフバージョン
    config["version"]              = getattr(settings, "IS_VERSION", None)
    # graphドメイン
    config["graph_domain"]         = getattr(settings, "IS_GRAPH_DOMAIN", None)
    # エンドポイント
    config["endpoint_base"]        = config["graph_domain"]+config["version"] + '/'
    # 出力
    return config

# APIリクエスト用の関数
def InstaApiCall(url, params, request_type):
    
    # リクエスト
    if request_type == 'POST' :
        # POST
        req = requests.post(url,params)
    else :
        # GET
        req = requests.get(url,params)
    
    # レスポンス
    res = dict()
    res["url"] = url
    res["endpoint_params"]        = params
    res["endpoint_params_pretty"] = json.dumps(params, indent=4)
    res["json_data"]              = json.loads(req.content)
    res["json_data_pretty"]       = json.dumps(res["json_data"], indent=4)
    
    # 出力
    return res

# メディア作成
def createMedia(params) :
    """
    ******************************************************************************************************
    【画像・動画コンテンツ作成】
    https://graph.facebook.com/v5.0/{ig-user-id}/media?image_url={image-url}&caption={caption}&access_token={access-token}
    https://graph.facebook.com/v5.0/{ig-user-id}/media?video_url={video-url}&caption={caption}&access_token={access-token}
    ******************************************************************************************************
    """
    # エンドポイントURL
    url = params['endpoint_base'] + params['instagram_account_id'] + '/media'
    # エンドポイント用パラメータ
    Params = dict() 
    Params['caption'] = params['caption']           # 投稿文
    Params['access_token'] = params['access_token'] # アクセストークン
    # メディアの区分け
    if 'IMAGE' == params['media_type'] :
        # 画像：メディアURLを画像URLに指定
        Params['image_url'] = params['media_url']    # 画像URL
    else :
        # 動画：メディアURLを動画URLに指定
        Params['media_type'] = params['media_type']  # メディアタイプ
        Params['video_url']  = params['media_url']   # ビデオURL
    # 出力
    return InstaApiCall(url, Params, 'POST')


# メディアID別ステータス管理
def getMediaStatus(mediaObjectId, params) :
    """
    ******************************************************************************************************
    【APIエンドポイント】
    https://graph.facebook.com/v5.0/{ig-container-id}?fields=status_code
    ******************************************************************************************************
    """
    # エンドポイントURL
    url = params['endpoint_base'] + '/' + mediaObjectId
    # パラメータ
    Params = dict()
    Params['fields']       = 'status_code'          # フィールド
    Params['access_token'] = params['access_token'] # アクセストークン
    # 出力
    return InstaApiCall(url, Params, 'GET')

# メディア投稿
def publishMedia(mediaObjectId, params):
    """
    ******************************************************************************************************
    【APIエンドポイント】
    https://graph.facebook.com/v5.0/{ig-user-id}/media_publish?creation_id={creation-id}&access_token={access-token}
    ******************************************************************************************************
    """
    # エンドポイントURL
    url = params['endpoint_base'] + params['instagram_account_id'] + '/media_publish'
    # エンドポイント送付用パラメータ
    Params = dict()
    Params['creation_id'] = mediaObjectId           # メディアID
    Params['access_token'] = params['access_token'] # アクセストークン
    # 出力
    return InstaApiCall(url, Params, 'POST')

# ユーザの公開レート制限・使用率を取得
def getContentPublishingLimit( params ) :
    """ 
    ******************************************************************************************************
    https://graph.facebook.com/v5.0/{ig-user-id}/content_publishing_limit?fields=config,quota_usage
    ******************************************************************************************************
    """
    # エンドポイントURL
    url = params['endpoint_base'] + params['instagram_account_id'] + '/content_publishing_limit' # endpoint url
    # エンドポイント送付用のパラメータ
    Params = dict() 
    Params['fields'] = 'config,quota_usage'         # フィールド
    Params['access_token'] = params['access_token'] # アクセストークン

    return InstaApiCall(url, Params, 'GET')

# 画像投稿
def instagram_upload_image(media_url, media_caption):
    # パラメータ
    params = basic_info_Instagram()
    params['media_type'] = 'IMAGE'         # メディアType
    params['media_url']  =  media_url      # メディアURL
    params['caption']    = media_caption
    
    # APIでメディア作成＆ID発行
    imageMediaId = createMedia(params)['json_data']['id']
    
    # メディアアップロード
    StatusCode = 'IN_PROGRESS';
    while StatusCode != 'FINISHED' :
        # メディアステータス取得
        StatusCode = getMediaStatus(imageMediaId,params)['json_data']['status_code']
        # 待ち時間
        #time.sleep(5)

    # Instagramにメディア公開 
    publishImageResponse = publishMedia(imageMediaId,params)
    # 出力
    print("Instagram投稿完了")
    return publishImageResponse['json_data_pretty']

# クライアント関数を作成
def ClientInfo():
    client = tweepy.Client(bearer_token    = getattr(settings, "TW_BEARER_TOKEN", None),
                           consumer_key    = getattr(settings, "TW_API_KEY", None),
                           consumer_secret = getattr(settings, "TW_API_SECRET", None),
                           access_token    = getattr(settings, "TW_ACCESS_TOKEN", None),
                           access_token_secret = getattr(settings, "TW_ACCESS_TOKEN_SECRET", None),
                          )
    
    return client

# 関数
def CreateTweet(message):
    tweet = ClientInfo().create_tweet(text=message)
    return tweet

def twitter_api():
    auth = tweepy.OAuthHandler(getattr(settings, "TW_API_KEY", None), getattr(settings, "TW_API_SECRET", None))
    auth.set_access_token(getattr(settings, "TW_ACCESS_TOKEN", None), getattr(settings, "TW_ACCESS_TOKEN_SECRET", None))
    return tweepy.API(auth)

def tweet(tweet_txt, img_pass):

    api = twitter_api()

    api.update_status_with_media(
        status=tweet_txt,
        filename=img_pass,
    )
    time.sleep(4)


def postData(data):
    if(data is None):
        print("params is empty")
        return False
    
    payload = {
        "data": data
    }
    url = "https://script.google.com/macros/s/AKfycbzbGqwh4UFGHqyBjSPZFP-mMypwxdWBPgsVEkV1mNp2PbCvkS6ToDxW-pvE35SKinnk/exec"
    headers = {
        'Content-Type': 'application/json',
    }
    response = requests.post(url, data=json.dumps(payload), headers=headers)
    if(response.status_code == 200 and response.text == "success"):
        print("post success!")
        return True
    print(response.text)
    return False







"""####################################################################################################
"""











def contact(request):
    """Renders the contact page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/contact.html',
        {
            'title':'Contact',
            'message':'Your contact page.',
            'year':datetime.now().year,
        }
    )

def about(request):
    """Renders the about page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/about.html',
        {
            'title':'About',
            'message':'Your application description page.',
            'year':datetime.now().year,
        }
    )
