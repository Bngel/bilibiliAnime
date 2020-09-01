# bilibiliAnime
A repository for my anime

Anime Version:1.0

Data Download_link:https://1drv.ms/u/s!AqWuZaQC1dE6hg8QEzEA0apK87M0?e=6YsLFh

## AnimeSpider.py
这就是最重要的爬虫了,能够爬下B站的番剧信息,一页一页爬的那种.(如果我不是为了更加详细还对每个番剧具体链接进行爬取的话)(但是为了更高的完成度我还是选了单个详情页具体爬取),幸好B站给了足够优秀的Json文件模板,以至于可以一口气将重要信息都爬取下来.接下来只需要在详情界面里补充一些小细节就OK.

## AnimeDataLoad.py
这就是读取数据的源文件了.通过将爬虫爬取下来的json文件进行依次分析后存入sqlite创建的数据库.db文件中.到这一步,准备工作也就算是完成了.

### AnimeMainUI.py
### AnimeIndexUI.py
#### AnimeChooseUI.py
#### AnimeDetailUI.py
#### AnimeFollowIndexUI.py
#### AnimeFollowRightclickUI.py
#### AnimeMessageBox.py
#### AnimeRightclickUI.py
#### AnimeTimelineIndexUI.py
#### AnimeToolUI.py
#### AnimeWatchedIndexUI.py
#### AnimeWatchedRightclickUI.py
有了基本的底层逻辑,接下来就是UI界面部分,如上文所说使用了PyQt作为程序的UI库,其中**AnimeMainUI.py**为主显示界面(也就是一开始显示的挂件界面),**AnimeIndexUI.py**为主索引界面,其余的均为*子界面*(只能说是两个最重要的界面的附属品吧,尽管这些界面都挺重要的),然后每个UI基本上都对应着一个对应的逻辑源文件(除了一些过于简单的就直接写在UI文件里了)
#### AnimeFollow.py
#### AnimeMonitor.py
#### AnimeRecommend.py
#### AnimeTimeline.py
#### AnimeVersion.py
#### AnimeWatched.py
其中值得一提的是**AnimeRecommend.py**,这个逻辑是事先写好结果没用上的...(摔),想着加个推荐番剧功能结果发现界面都塞满了.塞哪儿都不合适,于是就搁置了.具体实现就是通过对用户所搜索过的番剧Tag进行一个统计然后进行加权筛选出一些更**符合用户需求**(雾)的番剧推荐给用户(可惜没用上).

#### ipSpider.py
最后的话就是这个代理IP池创建的源文件了.我找了一个免费的IP代理网站(所以说免费的就是不太好使)然后通过每次使用都重新爬取使得能够更好的有IP的随机性.(尽管还是被阿B逮了不少次.)
