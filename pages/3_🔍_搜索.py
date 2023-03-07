from docarray import dataclass, Document, DocumentArray
from docarray.typing import Image, Text
from tqdm import tqdm
import time
from text2vec import SentenceModel, EncoderType
import numpy as np
# import jiagu
import pandas as pd
# from pandas import convert_df

from torchvision.models import resnet50
import numpy as np


# https://blog.streamlit.io/introducing-multipage-apps/ 多页面

import streamlit as st
import os, shutil

# st.set_page_config(page_title='妖怪搜索引擎', page_icon='🔍')
st.title('搜索 :mag:')

top_n = st.sidebar.slider("请选择最多同时显示的近似妖怪数量", value=1, min_value=1, max_value=5)

max_value = st.sidebar.slider("请选择最大几何距离", value=0.1, min_value=0.1, max_value=1.0)

# Using object notation
# add_selectbox = st.sidebar.selectbox(
#     "How would you like to be contacted?",
#     ("Email", "Home phone", "Mobile phone")
# )

# Using "with" notation
with st.sidebar:
    add_radio = st.radio(
        "请选择一种检索方式",
        ("模糊匹配", "精确匹配")
    )

# with st.sidebar:
#     with st.echo():
#         st.write("This code will be printed to the sidebar.")

with st.sidebar:
    options = st.multiselect(
        '请选择检索时的有效输入',
        ['妖怪名称', '图片', '原文描述', '种类', '作者', '出处', '朝代', '绘者'],
        ['妖怪名称'])

    # st.write('You selected:', options)
    print(type(options))
    flag1_main_text = 1 if '妖怪名称' in options else 0
    flag1_image = 1 if '图片' in options else 0
    flag1_description = 1 if '原文描述' in options else 0
    flag1_type = 1 if '种类' in options else 0
    flag1_creator = 1 if '作者' in options else 0
    flag1_book = 1 if '出处' in options else 0
    flag1_dynasty = 1 if '朝代' in options else 0
    flag1_artist = 1 if '绘者' in options else 0
    flag1 = [flag1_main_text, flag1_image, flag1_description, flag1_type, flag1_creator, flag1_book, flag1_dynasty, flag1_artist]
    # with st.spinner("Loading..."):
    #     time.sleep(5)
    # st.success("Done!")
    st.text(flag1)



webq_main_text = st.text_input('妖怪名称', '')
flag2_main_text = 1 if webq_main_text != '' else 0
st.text(flag2_main_text)

flag2_image = 0
flag = 0

uploaded_file = st.file_uploader("请上传相近的妖怪图片:")

if uploaded_file is not None:
    os.makedirs('tmp_image', exist_ok=True)
    with open('tmp_image/' + uploaded_file.name, 'wb') as f:
        f.write(uploaded_file.getvalue())
        flag = 1
    flag2_image = 1

webq_description = st.text_area('原文描述', '')
flag2_description = 1 if webq_description != '' else 0

webq_type = st.selectbox(
    '种类',
    ('统领', '妖', '精', '鬼', '怪'))
flag2_type = 1
## 统领因为是选择，没有空值

webq_creator = st.text_input('作者', '')
flag2_creator = 1 if webq_creator != '' else 0

webq_book = st.text_input('出处', '')
flag2_book = 1 if webq_book != '' else 0

webq_dynasty = st.text_input('朝代', '')
flag2_dynasty = 1 if webq_dynasty != '' else 0

webq_artist = st.text_input('绘者', '')
flag2_artist = 1 if webq_artist != '' else 0

flag2 = [flag2_main_text, flag2_image, flag2_description, flag2_type, flag2_creator, flag2_book, flag2_dynasty, flag2_artist]
st.text(flag2)
df = pd.DataFrame(columns=['妖怪名称', '原文描述', '种类', '作者', '出处', '朝代', '绘者'])

if add_radio == '模糊匹配':
    search_button = st.button('模糊搜索')

elif add_radio == '精确匹配':
    search_button = st.button('精确搜索')

@dataclass
class Page:
    main_text: Text
    image: Image = None
    description: Text = None
    type : Text = None
    creator: Text = None
    book: Text = None
    dynasty: Text = None
    artist : Text = None







# query.summary()

da = DocumentArray(
    [
        Document(
            Page(
                main_text = '白泽',
                image='白泽.jpg',
                description='传说黄帝巡狩，在海滨遇到了一只异兽，它不仅能说话，而且向黄帝详细\
介绍了天下鬼神之事，还将自古以来精气为物、游魂为变的一万一千五百二十\
种妖怪详细告诉了黄帝。黄帝命人将这些妖怪画成图册，以示天下，亲自写文\
章祭祀它们。\
黄帝令人编绘的图册便是《白泽图》（又称《白泽精怪图》）。\
关于白泽的形象，向来说法不一。《三才图会》中白泽是狮子身姿，头\
有两角，长着山羊胡子。日本人的图绘中，白泽的形象和《三才图会》相像,\
唯胁下生有三只眼睛。\
白泽不仅知道天下所有妖怪的名字和形象，而且知道驱除它们的方法。所\
以，在很早的时候，它就被当成驱鬼的祥瑞来供奉。人们将画有白泽的图画挂\
在墙上或者贴在大门上，还有做“白泽枕”的习俗。军队中，“白泽旗”是常\
见的旗帜。到了中古时期，人们对白泽的尊崇更加隆重，《白泽图》极为流行,\
人们一旦觉得自己遇到了妖怪，就会按图索骥查找，按照上面记载的方法加以\
驱除。\
因白泽，世人才得知天下妖怪的名字，所以白泽在妖怪中的地位极为特殊。',
            type = '统领',
            creator ='未知',
            book = '未知',
            dynasty = '未知',
            artist = '鸟山石燕',
            )
        ),
        Document(
            Page(
                main_text = '方相氏',
                image='方相氏.jpg',
                description='方相氏，是上古时期娛母的后代。娛母为黄帝的妃子，容貌极为丑陋。黄\
帝巡行天下时，元妃媛祖病逝。黄帝便命令娛母负责祀事，监护灵柩，并且授\
以“方相氏”的官位，利用她的相貌来驱邪。所谓的“方相氏”，便是“畏\
怕之貌”的意思。\
上古以降，方相氏都为官设，在宫廷傩祭之中成为最重要的角色。《周\
礼•夏官•方相氏》：“方相氏掌蒙熊皮，黄金四目，玄衣朱裳，执戈扬盾，帅\
百隶而时难，以索室驱疫。”\
自上古到汉、唐，大傩延绵不绝。汉朝“傩者……季春行于国中、仲秋行\
于宫禁，惟季冬谓之大傩则通上下行之也”（见《大学衍义补》）。唐时大傩场\
面更加宏大。《乐府杂录》载：“用方相四人，戴冠及面具，黄金为四目，衣熊\
裘，执戈扬盾，口作傩傩之声，以逐疫也。右十二人，皆朱发衣白画衣，各执\
麻鞭，辫麻为之，长数尺，振之声甚厉。”古人认为，季春的时候，世间凶气\
催发，与民为厉，方相氏则为家家户户驱逐邪物，作乱人间的各种鬼怪见到方\
相氏凶威的面目，便会自知恐怖逃走。戴着黄金面具，上生四目，披着熊皮,\
双手执戈、盾，领着象征世间精怪的“百鬼”前行的方相氏，从上古的祭司逐\
渐演变成百姓心目中的“大妖怪”。\
唐时，宫廷大傩传入日本。方相氏前行、百鬼跟随的场景，则被日本人演\
化成了 “百鬼夜行”。',
                type = '统领',
                creator='未知',
                book='未知',
                dynasty='未知',
                artist='未知',
            )
        ),
        Document(
            Page(
                main_text = '阿紫',
                image='阿紫.jpg',
                description='古人认为，有种狐妖叫紫狐，夜间甩尾巴能够冒出火星。这种狐狸将要成\
为妖怪时，会头戴死人头骨对着北斗七星叩头，死人头骨不掉下来，它就能变\
成人。\
东汉建安年间，沛国郡人陈羡担任西海都尉。他手下有一个叫王灵孝的人，\
突然无缘无故就逃跑了，怎么找也找不到。陈羡觉得王灵孝十有八九是被什么\
妖怪弄走了，于是就率领几十名骑兵，领着猎狗，在城外周旋寻找。果然，最\
后发现王灵孝躺在一个空空的坟墓里。当听到人和狗的声音，王灵孝惊慌失\
措，四处躲避，模样很奇怪。\
陈羡让人把他扶回来，发现王灵孝的样子变得很像狐狸。对于周围原本熟\
悉的环境，王灵孝很不适应，而且总是哭着喊着找“阿紫”，十几天之后，才\
渐渐清醒了些。王灵孝回忆说，有一天他在屋拐角的鸡窝旁看到了一位美丽的\
女子，自称阿紫，向他招手。如此不止一回两回，他就逐渐被迷惑了，跟着阿\
紫离开，并且成为阿紫的丈夫。和阿紫在一起，他觉得其乐无比。\
唐代，有个叫刘元鼎的人做蔡州刺史，当时蔡州刚被攻占下来，因为战乱\
频繁，人烟稀少，狐狸就特别多。刘元鼎派遣官吏捕捉，天天在球场一带放开\
猎犬，以追逐狐狸为乐趣，一年杀了有一百多只。\
有一次，刘元鼎追逐一只全身长满疥疮的狐狸，放出的五六只猎犬都不敢\
去追，狐狸也不跑。\
刘元鼎觉得特别奇怪，认为一般的猎狗对付不了，就命令人去找大将军,\
将他的那只大猎狗带来。手下带来了那只大猎狗，放出来，那只狐狸却正眼不\
看，众目睽睽之下，穿廊走巷，到了城墙，消失不见。\
刘元鼎知道自己碰到了阿紫，从此便不再下令捕捉狐狸。',
                type = '妖',
                creator='干宝',
                book='《搜神记》',
                dynasty='晋',
                artist='数星星的胖子',
            )
        ),
        Document(
            Page(
                main_text = '姑获鸟',
                image='姑获鸟.jpg',
                description='姑获鸟是中国古代非常著名的妖怪之一，又叫夜行游女、天地女、钓星、\
鬼车鸟、九头鸟、苍鵰、逆鸽。\
传说姑获鸟能收人魂魄，昼伏夜飞，作为鸟的时候，身大如簸箕，九个脑\
袋，十八个翅膀。原本姑获鸟有十个脑袋，其中一个曾经被天狗吃掉，所以它\
飞过的地方经常会滴下鲜血，而沾染上姑获鸟血的人家就会发生灾祸。\
七八月份，尤其是阴晦的天气，姑获鸟会呜咽飞出，它脱掉羽毛落下来，\
就会变成女人。也有的传说称，姑获鸟是产妇死后所化，所以喜欢偷取百姓的\
孩子作为自己的孩子。凡是有幼儿的人家晚上不能晾晒衣物，否则姑获鸟会先\
用滴下来的鲜血做记号，然后夜里化身女子前来行窃。\
传说姑获鸟只有雌鸟，没有雄鸟。它还有一个习惯，就是吃人的指甲，被\
吃的人同样会发生疾病和灾祸。',
                type = '妖',
                creator='周公旦',
                book='《周礼》',
                dynasty='西周',
                artist='数星星的胖子',
            )
        ),
        Document(
            Page(
                main_text = '旱魃',
                image='旱魃.jpg',
                description='魅，在我国的传说中，历史悠久。普遍认为，魅是种能够带来旱灾的妖怪，\
为人的尸体所化。事实上，旱魅从刚开始的天女，到清代的僵尸说，经过了长\
久的演变。\
传说黄帝和蚩尤作战时，因为蚩尤擅长制造兵器，并且纠集了很多精怪，所\
以黄帝打了不少败仗。后来，黄帝派遣应龙和天女魅前往作战，魅穿着青色的衣\
服，能够发出极强的光和热，破解了蚩尤制造出来的迷雾，帮助黄帝打了胜仗。\
胜利之后，魅丧失了神力，就留在了北方。她走到哪里，哪里就会干旱，\
所以人们诅咒她，称她为旱魅。\
从汉代开始，一直到明初，旱魅的形象逐渐向妖怪转变，到了明清时，旱\
魅逐渐变成了僵尸形象，成为极有威力的妖怪。\
旱魅的形象，依汉代的典籍记载，身高二三尺，身体赤裸，眼睛长在头顶，\
行走如风，又叫旱鼠。对付它的手段是把它扔到厕所里，就会死掉。\
清代时，旱魅被分为兽魅和鬼魅。兽魅像猿猴，披头散发，长着一只脚；鬼\
魅则是上吊而死的人变成的僵尸，出来迷惑凡人。将鬼魅焚烧，可以引来大雨。\
清代乾隆二十六年，北京一带大旱。有个叫张贵的邮差送公文到良乡，\
离开北京城的时候，已经是半夜了。他走到荒野无人的地方，忽然刮来一股黑风，吹灭了灯笼，又下起了雨，所以只能在邮亭里面暂时歇息。这时候，\
有个女子拎着灯笼走来,年纪十七八岁，长得十分美丽。女子将张贵带到家里，\
两个人恩爱了一晚，第二天早晨，张贵醒来时发现自己躺在荒坟之中，耽误\
了差事。后来上司怪罪，要彻底追査，才发现那个女子原来没出嫁前就和人\
交往，后来羞愧上吊而死，经常迷惑路人。事情调査清楚之后，打开了女子\
的棺椁，果然发现里面的尸体成了僵尸，相貌如生前，但是全身长满了白毛。\
大家用火烧了尸体，第二天瓢泼大雨倾盆而下。',
                type = '妖',
                creator='东方朔',
                book='《神异经》',
                dynasty='汉',
                artist='未知',
            )
        ),
        Document(
            Page(
                main_text = '鹿妖',
                image='鹿妖.jpg',
                description='很久以前，张盍蹋、宁成两个人，在四川云台山的石洞中出家修行。一天，\
忽然有个穿着黄色长衫、戴着葛布头巾的人来到两人跟前，说：“想请你们两\
位道士帮帮忙。”二人用古镜照了一下对方，发现是一头鹿，就呵斥说：“你是\
草中的老鹿，怎么敢口出人言？ ”说完，那人就变成一只鹿，跑了。\
晋代时，一个下雨天，淮南人车某在家里独坐，看见两个穿着紫色衣服的\
少女出现在自己面前，欢声笑语。外面雨下得那么大，这两个女子衣服完全没\
有湿，车某很奇怪，觉得对方肯定是妖怪。家里的墙上正好挂着一枚古铜镜，\
车某转过头看了看铜镜，发现镜中有两只鹿站在窗前。车某举起刀砍过去，一\
只鹿跑了，另一只被他杀死。他将其肉做成肉脯吃了，味道很好。\
唐代嵩山有个老和尚，搭了个茅舍在山里修行。一天，有个小孩前来施礼，\
请求老和尚收下自己当徒弟。老和尚闭目念经,不搭理，那小孩从早到晚哀求着，\
也不离开。老和尚就问：“这里荒山野岭，人迹罕至，你从哪里来？又为何求\
我收你为徒弟？ ”小孩说：“我住在前面的山里，父母都死了，只留下我自己，\
想必是前世不修善果所致。如今，我愿意舍离尘俗，求师父你收下我。”老和\
尚见他很机敏，知道是缘分，就收下他做了徒弟。\
小孩成了弟子后，修行精进，和别的僧人辩论，经常大获全胜，老和尚很\
看好他。过了几年，一个秋天，万木凋零，溪谷凄清。小和尚看着山川草木，\
有些悲伤，说：“我本生长在深山里，为何要当个和尚呢？不如寻找往日的伙\
伴去吧！”说罢，对着山川放声大喊。过了一会儿，来了一群鹿，小孩脱掉僧\
衣，变成一只鹿，跳跃着和鹿群消失在莽莽群山之中。',
                type = '妖',
                creator='葛洪',
                book='《抱朴子》',
                dynasty='晋',
                artist='喵九',
            )
        ),
        Document(
            Page(
                main_text = '落头民',
                image='落头民.jpg',
                description='落头民出自我国的南方，秦朝的时候有人见过，脑袋能够离体飞去，又叫\
“虫落”。\
三国时，东吴的将军朱桓有一个女婢，每天晚上睡着之后，脑袋就会飞走。\
有时候从墙下的狗洞里飞出去，有时从天窗出入，用两个耳朵当翅膀，等天亮\
了才回来。\
知道这件事的人都觉得很奇怪。有天晚上，朱桓挑着灯笼来到女婢的房间，\
发现她身体虽然在，但头不见了，摸一摸，身体微微冰冷，还喘着气。朱桓用\
被子将身体裹了起来。天快亮时，女婢的头飞回来了，因为隔着被子，脑袋无\
法回到身体，掉在地上，似乎很是着急。朱桓扯开被子，脑袋才复原，过了一\
会儿，女子安然无恙，好像什么事情都没有发生。\
这件事让朱桓觉得很不可思议，没多久就把这个女婢送走了。\
据说，在南方打仗的将领经常会抓到落头民，有的人恶作剧，把落头民\
的身体盖在巨大的铜盘之下，飞回来的脑袋因为长时间回不到脖子上，就会\
死掉。\
唐朝时，岭南龙城的西南地广千里，溪流和山洞之中经常有飞来飞去的脑\
袋，当地人称之为“飞头獴子”。据说这种人脑袋飞出去的前一天，脖子上会\
出现一条红色的印记，妻子见了，往往夜里就会格外小心看护。到了晚上，这\
个人的脑袋离身而去，飞到岸边，在湿泥里寻找螃蟹、蚯蚓之类的东西吃，天\
亮前飞回来。夜里发生的事情，他会觉得如同做梦一般，但是摸一摸肚子，里\
面可是装了不少东西，彳艮饱呢。',
                type = '妖',
                creator='干宝',
                book='《搜神记》',
                dynasty='晋',
                artist='未知',
            )
        ),
        Document(
            Page(
                main_text = '人鱼',
                image='人鱼.jpg',
                description='人鱼，是中国古代著名的妖怪之一。《山海经》里记载，龙侯之山的决水\
里面就有人鱼，长着四条腿，声音如同婴儿，吃了它，就不会变成痴呆。《史记》\
里记载，秦始皇的陵墓里用人鱼膏来点灯。\
东海里也有人鱼，传说大的长五六尺，样子像人。眉毛、眼睛、口、鼻子、\
手、脚和头都像美丽的女人，皮肉白得像玉石，身上没有鳞，有细毛，毛分五\
种颜色，又轻又柔软，毛长一两寸，头发像马尾巴一样长五六尺。人鱼的生殖\
器官和人一样，靠海的光棍、寡妇大多捉过海人鱼，放在池沼中养育。交合时，\
与人没什么两样，也不伤人。\
清代崇明岛，有人抓住过一条人鱼，长得像个美丽的女子，身体和船只一\
样大。船工问她：“你迷路了吗？ ”美人鱼点头，船工就放了她。',
                type = '妖',
                creator='未知',
                book='《山海经》',
                dynasty='先秦',
                artist='未知',
            )
        ),
        Document(
            Page(
                main_text = '三尸',
                image='三尸.jpg',
                description='三尸，指的是上尸、中尸、下尸，是人身体中的魂魄精华。如果想让人早\
死，三尸就会放纵四处，享受人间的祭祀之物。每年三尸都会上天，将人的罪\
过告诉司命，来减少人的寿命，所以求仙的人都会想尽办法斩除三尸。\
传说人死后，魂升天，魄入地，只有三尸游走，四时八节，享受祭祀，如\
果祭祀不足，就会作祟。\
三尸的形状如同小孩，也有的长得像马，都长着二寸的长毛。出来作祟,\
形状和人一模一样，连衣服都相同。\
上尸名为青姑，中尸名为白姑，下尸名为血姑。一个在人头部，令人多\
思欲，令人喜欢车马；一个在人腹部，令人好食饮、易怒；一个在人脚部,\
令人好色喜杀。',
                type = '妖',
                creator='葛洪',
                book='《抱朴子》',
                dynasty='晋',
                artist='未知',
            )
        ),
        Document(
            Page(
                main_text= '獭',
                image='獭.jpg',
                description='獭这种妖怪，最擅长变化为美丽的女子或者俊俏的男子与人交往。和其他\
妖怪不一样，或许是因为生存条件的原因，潺潺流水赋予了獭妖别样的美丽,\
它们出现时，往往是荷雨蒲风，小舟丽人，很有诗情画意。但它们的多情，往\
往总是受到伤害。\
河南有个人叫杨丑奴，常常到章安湖边拔蒲草。有一天，天快黑了，他\
看见一个女子，穿的衣服虽然不太鲜艳，可是容貌很美。这女子坐着船，船\
上载着苑菜，上前靠近杨丑奴。她说自己的家在湖的另一侧，天黑了一时回\
不了家，想停船借住一宿。她借杨丑奴的食器吃饭，吃完饭，两个人说笑起\
来，杨丑奴为她唱了一首歌，女子则回作了一首诗，这首诗写道:“家在西湖侧，\
日暮阳光颓。托荫遇良主，不觉宽中怀。”二人相处得很融洽，郎有情妾有意，\
于是吹灯歇息。黑暗中，杨丑奴摸到女子的手，发现她的手指很短，便怀疑\
女子是妖怪。女子很快察觉了杨丑奴的心思，伤心地走出船舱，变成一只水獭,\
跳到水中不见了。\
南朝宋文帝元嘉十八年，广陵这个地方，张方的女儿道香送丈夫去北方。\
归来的途中天黑了，道香就在庙门前歇息。夜间，有一个东西装扮成她丈夫的\
模样出现，并且说：“我太想你了，所以就回来了。”道香很快就被迷惑得失去\
常态。当时有个叫王纂的人擅长驱邪，他怀疑道香被妖怪迷惑了，来到道香的\
家中，刚开始施法，就看见一只水獭从道香的被子里跑出来，跳到水巷里消失\
不见。不久，道香的病也好了。',
                type = '妖',
                creator='干宝',
                book='《搜神记》',
                dynasty='晋',
                artist='喵九',
            )
        ),
        Document(
            Page(
                main_text = '仲能',
                image='仲能.jpg',
                description='传说老鼠能活到三百岁，满一百岁全身的毛色就会变得雪白，擅长附在人\
身上占卜，名为“仲能”，能知道一年中的凶吉和千里之外的事情。\
清代四川西部，有个伙夫陈某，身形粗悍，酒量也大。一天喝醉了，躺下\
后发现有东西趴在肚子上，抬头一看，是个老头，须发皆白，长相奇怪。陈某\
蒙胧中以为是同伴戏耍他，就没搭理。\
此时正是初秋，天气寒冷，陈某拿起薄薄的被褥裹紧身体，辗转反侧。到\
了第二天早晨整理被子的时候，发现被子里有一只白毛老鼠，三尺多长，已经\
被他压死了。陈某这才明白，昨晚的那个老头就是这只老鼠。如果陈某没把它\
压死，就可以凭借它成为能预测吉凶的占卜者。',
                type = '妖',
                creator='葛洪',
                book='《抱朴子》',
                dynasty='晋',
                artist='矢口',
            )
        ),
        Document(
            Page(
                main_text='八哥',
                image='八哥.jpg',
                description='清代时，某人养了一只八哥，教它说话，驯养得很灵巧。这人很喜欢这只\
八哥，连出门都和它形影不离，就这样过了好几年。\
一天，这人去绛州，离家很远，盘缠用光了，正在发愁，八哥说：“你为\
什么不把我给卖了呢？卖到王爷家里，肯定能有个好价钱，不愁回去没有路\
费。”这人说：“我怎么忍心呀！”八哥说：“没事，你拿到了钱，赶紧走，到城\
西二十里的那棵大树下等我。”这人就答应了。\
这人带着鸟进了城，八哥和他有问有答，引来很多人看热闹，王爷听说了，\
就把这人叫到了府里，问卖不卖。这人说：“小人我和这只鸟相依为命，不愿\
意卖。”王爷问鸟：“你愿意留下来吗？ ”八哥说：“我愿意！”王爷听了，很高\
兴。鸟说：“给十两银子，别多给。”\
王爷听了，更加高兴，让人拿来十两银子，交给了这人。这人故意做出后\
悔的样子，离开了。\
王爷买了鸟，和鸟说说笑笑，很高兴，还让人取来肉喂鸟。八哥吃完了，\
说：“我要洗澡！”王爷就让人用金盆盛水，开了笼子。鸟洗了澡，在屋檐外\
飞来飞去，与王爷说了一会儿话，大声道：“我走了哈！”言罢，展翅飞走。\
王爷和仆人们四处寻找，也没找到那只八哥。\
后来，有人在西安的集市上看到过那个人，还有那只八哥。',
                type = '精',
                creator='蒲松龄',
                book='《聊斋志异》',
                dynasty='清',
                artist='喵九',
            )
        ),
        Document(
            Page(
                main_text='枫鬼',
                image='枫鬼.jpg',
                description='传说云南、贵州和四川一带，有一种精怪叫枫子鬼，就是成年累月的老枫\
树，变成老人的模样，所以又叫灵枫。\
南北朝时，抚州的麻姑山，有人攀登到山顶，往四外望去，山川河岳，一\
览无余。山上生长着很多古树。有棵活了几千年的老树，已经化成人形，眼、\
鼻、口、臂全有，但是没有脚。进山的人经常能见到它，如果有人从它身上弄\
掉一小块儿，伤口就会出血。有的人曾经把蓝草像戴帽子那样盖到它的头上，\
第二天去看就全都没了，这个枫精就是枫鬼。\
唐代江东江西的山中，有许多枫人，生长在枫树之下，像人形，高三四尺。\
夜间有雷雨，它就长得和树一般高，见到人它就缩回去。曾经有人把竹笠扣到\
它的头上，第二天去看，竹笠居然挂到树梢上去了。旱天的时候想要求雨，用\
竹针扎它的头，然后举行求雨的仪式就下雨了。人们把它从山上弄回来做成占\
卜用的盘子，极其灵验。',
                type = '精',
                creator='任昉',
                book='《述异记》',
                dynasty='南北朝',
                artist='喵九',
            )
        ),
        Document(
            Page(
                main_text='鼓女',
                image='鼓女.jpg',
                description='清代时，有个常德的读书人，带着一个仆人从云南回老家。这天黄昏，眼\
见得天快黑了，找不到旅店，就到一个小村子求人借宿。村里人说：“我们这\
里没有旅馆，只有一个古庙，但是那里经常有妖怪杀人，不是住宿的地方。”\
读书人也没办法，只能说：“我不怕。”就向村里人要了一张桌子、一盏灯笼，\
进了古庙的一个房间，将笔墨纸砚放在桌子上，一边读书，一边静待其变。\
过了二更，仆人睡着了，读书人看到一个红衣女子，年纪大概十八九岁，\
婀娜而来。读书人知道是妖怪，就不搭理。这红衣女子就对着读书人唱歌，歌\
声婉转，含情脉脉。\
读书人取来笔，蘸着朱砂，在女子的脸上画了一道，女子大惊，慌忙逃出\
去消失了。\
第二天，读书人将事情告诉村里人，大家一起在庙中寻找，发现大殿的角\
落里，有一只破鼓，上面画有朱砂。打破那只鼓，发现里面有很多鲜血，还有\
人骨。自此之后，再也没有怪事发生。',
                type = '精',
                creator='乐钧',
                book='《耳食录》',
                dynasty='清',
                artist='喵九',
            )
        ),
        Document(
            Page(
                main_text='蕉女',
                image='蕉女.jpg',
                description='宋代隆兴二年，舒州怀宁县主簿章裕带着仆人顾超前去赴任，夜宿在一间\
书馆。晚上，顾超看到一个穿着绿衣裳的女子前来，说是被母亲逐出家门，没\
有去处，见顾超在此，特来相会。顾超问她住在哪里，她说在城南紫竹园。顾\
超就和她同床共枕，才过了几个晚上，顾超就觉得身体虚弱，好像生病一般。\
章裕发现情况不对劲，就询问顾超，顾超把事情说了，章裕认为那女子肯定是\
妖精，就和顾超定下计策。\
第二天晚上，女子又来，顾超拽住女子不放，章裕挑着灯前来捉拿，那女\
子逃窜不得，变成了一枚芭蕉叶。后来才听说，紫竹园里面，有一丛芭蕉年代\
久远，经常发生怪异的事。章裕就命人把芭蕉砍了，砍的时候，芭蕉流出了很\
多血。这件事情发生后，顾超闷闷不乐，过了不久，就死了。\
明代苏州有个书生，名叫冯汉，住在阊门石牌巷的一个小院子里。院中种\
着一些花草，青翠可爱。\
有一年夏天的晚上，月华朗照，冯汉洗完澡坐在榻上，看见一个穿着绿色\
衣裳的女子站在院子里。冯汉呵斥她，女子说:“我姓焦。”说完，女子走进屋里。\
冯汉抬头观看，发现这女子长得十分美丽，不像凡人，就一把抓住她。女子挣\
脱逃跑，冯汉只撕下了她的一片裙角，就放在了床下。第二天早晨起来，发现\
那裙角是一片蕉叶。\
冯汉曾经在院子里从寺庙移植过来一株芭蕉，于是就拿着这片芭蕉叶走过\
去，发现那株芭蕉果然缺了一片，比对一下，正是手里的这片。\
冯汉砍掉了那株芭蕉，发现芭蕉流出了很多血。后来冯汉把这件事告诉了\
寺里的和尚。和尚说，寺里面曾经有芭蕉作怪，魅惑死了好几个僧人。',
                type = '精',
                creator='洪迈',
                book='《夷坚志》',
                dynasty='宋',
                artist='Jerry Fu',
            )
        ),
        Document(
            Page(
                main_text='量人蛇',
                image='量人蛇.jpg',
                description='唐代时，有个叫邓甲的人，曾经设立祭坛召唤蛇王。有一条大蛇出现，粗\
如人腿，一丈多长，色彩斑斓，后面跟着一万多条小蛇。蛇王登坛与邓甲斗法，\
邓甲用拐杖顶着帽子往上举，蛇王虽然竭尽全力，身体还是超不过邓甲的帽子，\
就倒在地上化成一摊水死去，那些小蛇也死了。如果蛇王超过了帽子，那化成\
水而死的，就是邓甲了。\
琼州这地方，有蛇名叫量人蛇，长六七尺，遇到人就将身体树立起来，和\
人比长短、比高矮，并且大声叫道：“我高！”人若不答应或者承认蛇高，就\
会被吃掉。如果人回答：“我高！”蛇就会死掉。\
有人说，和量人蛇比高矮是有办法的。当蛇站立起来时，人可以随手拾\
件东西往上高高抛起，然后说：“你不如我高！”蛇就会翻身躺倒，伸出一千\
多只小脚，这时候，人就把自己的头发散开，对蛇说：“你的脚不如我的多！”\
量人蛇就会收起脚趴在地上。这时候，人就将身上的衣带弄断，对蛇说：“我\
走了！”做完这些，那条量人蛇必死。',
                type = '精',
                creator='裴铏',
                book='《传奇》',
                dynasty='唐',
                artist='喵九',
            )
        ),
        Document(
            Page(
                main_text='柳精',
                image='柳精.jpg',
                description='唐代东都洛阳渭桥铜驼坊，有一个隐士叫薛弘机。薛弘机在渭河边上盖了\
一所小草房，闭户自处。每到秋天，邻近的树叶飞落到院子里来，他就把它们\
扫到一块，装进纸口袋，找到那树归还。所以，薛弘机是个很有品行的隐士。\
有一天，残阳西斜，秋风入户，他正披着衣衫独坐，忽然有一客人来到\
门前。客人的样子挺古怪，高鼻梁，花白眉，口方额大，身穿早霞裘。他对薛\
弘机说：“先生您的性情喜尚幽静之道，颇有修养，造诣很深。我住的地方离\
这不远，一向仰慕您的德才，特意来拜见。”薛弘机一见就喜欢他，正好可以\
和他切磋一些今古学问。于是就问他的姓名，他说他姓柳，名藏经。于是就一\
起唱歌吟诗，直到夜深。\
柳藏经告辞的时候，走路发出窣窣窸窸的声音。薛弘机望着他，见他走出\
一丈多远就影影绰绰地隐没了。后来向邻居打听，都说没有见过这样的一个人。\
之后，柳藏经经常来，二人成了很好的朋友。但薛弘机每次想要接近他，\
他总是往后退。薛弘机逼近他，就能闻到略微有一点儿朽烂木材的气味。第二\
年五月，柳藏经又来了，与薛弘机吟诗作对，走的时候，却很不安。\
这天夜里刮大风，毁屋拔树。第二天，魏王池畔的一棵大枯柳被大风\
刮断。树洞里有经书一百多卷，全都朽烂腐坏了。薛弘机听说之后，才知道\
自己的这位朋友原来是柳树精。“因为树里面有经文，所以才叫柳藏经呀！”\
薛弘机叹道。\
清代杭州有个叫周起昆的人，担任龙泉县学教谕，每到晚上，县学明伦堂\
上的鼓就会无故自鸣。周起昆觉得奇怪，就派人偷偷盯着，发现有个身高一丈\
多的东西，长得像人，用手击鼓。周起昆有个学生叫俞龙，胆子很大，一天晚\
上对着怪物射了一箭，怪物狂奔而去，以后那面鼓深夜就再也不响了。两个\
月后，刮大风，县学门外一棵大柳树被连根拔起，周起昆让人把它锯断当柴火,\
结果发现树中有俞龙之前射的那支箭，这才知道那个妖精是柳树。\
唐代东都洛阳有一所旧宅子，富丽堂皇，厅堂众多，可凡是住进去的人，\
很多都没有什么原因就平白无故死去，所以空了很多年。\
贞元年间，有个叫卢虔的人,想买这所宅子。有人告诉他:“这宅子里有妖怪，\
不能住。”卢虔也不听，到底还是买了。\
晚上，卢虔和手下一起睡在屋里，这个手下非常勇猛，而且擅长射箭。因\
为听说有妖怪，所以手下就拿着弓箭坐在窗户下。\
快到半夜，忽然听到有人敲门，手下问是谁，声音回答：“柳将军有书信\
要给卢官人。”卢虔睡在里面，并没有搭理。\
过了一会儿，有一封书信从窗户那边塞过来。上面的字像是蘸着水写的那\
般，浸染得很厉害，写的是:“我家在这里好多年了，亭台楼阁都是我居住的地方，\
家中的门户神灵也都是我的手下。你突然跑到了我家，简直岂有此理！识相的，\
赶紧离开，否则我可不客气了！”卢虔读完这封信，书信就变成了灰烬飘散开去。\
一会儿，有声音说：“柳将军愿意和卢官人见一面。”很快，出现了一个大\
妖怪，身高十寻，站在院子里，手里拿着一个瓢。卢虔的手下见了，立刻拿起\
弓箭射去。大妖怪当胸中箭，被弓箭射得抱头鼠窜，丢下那个瓢，跑了。\
天明，卢虔命人寻找。来到宅子东边，看到一株大柳树，上面钉着一支箭，\
看来就是昨晚那个自称柳将军的妖怪了，屋檐下面有个瓢，应该就是“将军”\
手里的那个瓢了。',
                type = '精',
                creator='张读',
                book='《宣室志》',
                dynasty='唐',
                artist='喵九',
            )
        ),
        Document(
            Page(
                main_text='龙门鲤',
                image='龙门鲤.jpg',
                description='龙门在河东的界内。大禹凿平龙门山，又开辟龙门，有一里多长，黄河从\
中间流下去，两岸不能通车马。每到晚春时，就有黄色鲤鱼逆流而上，过了龙\
门的就变成龙。传说一年之中，登上龙门的鲤鱼不超过七十二条。刚一登上龙\
门，就有云雨跟随着它，天降大火从后面烧它的尾巴，就变化成龙了。\
从前，有个叫子英春的人，擅长潜水，他捉到一条红鲤鱼，因为喜欢鱼的\
颜色，就带回家去，放在池子里喂养。他经常用谷物和米饭喂鱼，一年后，鱼\
长到一丈多长，并且头上长出角，身上长出翅膀来。子英春很害怕，向鲤鱼行\
礼并道歉。鱼说：“我是来迎接你的，你骑到我背上来，我和你一起升天。”子\
英春就和鲤鱼一起升天了。',
                type = '精',
                creator='辛氏',
                book='《三秦记》',
                dynasty='汉',
                artist='吴青霞',
            )
        ),
        Document(
            Page(
                main_text='楠木大王',
                image='楠木大王.jpg',
                description='有个叫卢浚的人，泛舟江上，忽然起了狂风，船工赶紧跪拜，口呼：“楠\
木大王！”卢浚问船工缘由，船工说楠木大王是水里的精怪，最能作祟。卢浚\
很生气，就写下檄文投入水中，请求河神制服精怪。过了三天，一根巨大的楠\
木浮出水面。卢浚让人把木头捞上来，正好修建学宫缺少木材，就把那根大楠\
木做成了柱子。\
明代襄阳的襄河里，也有楠木作祟，经常撞翻船只，所以过往的船工都会\
祭祀它。相传是很久以前一根老木头年月久了成精。当地人不仅祈祷，还建立\
庙宇供奉它，叫它“南君”。',
                type = '精',
                creator='钱希言',
                book='《狯园》',
                dynasty='明',
                artist='喵九',
            )
        ),
        Document(
            Page(
                main_text='参翁',
                image='参翁.jpg',
                description='人参，在中国被视为百草之王，十分珍贵，有延年益寿、起死回生之效。\
传说有年头的人参，会吸收日月精华，出来作祟。\
南北朝时，上党这地方，有人半夜听到孩子的哭声，找到哭声的源头，发\
现来自地下。这个人就拿起锄头往下挖掘，挖出一枚人参，四肢倶全，和人一\
模一样。\
唐代天宝年间，有个姓赵的书生，兄弟数人，都读书考取了进士，当了官，\
唯独他生性鲁钝，虽然到了壮年，依然没有考取功名。参加宴会时，周围的朋\
友都穿着红色、绿色的官服，只有他是个穿着白衣的书生，所以很是郁闷。\
后来有一天，书生离开家，在晋阳山隐居，建起一间茅草屋，日夜苦学。\
吃的是粗茶淡饭，日子过得很清苦。可书生越是努力勤奋，进步越是不大，这\
让他既愤怒又痛苦。\
过了几个月，有一个老翁前来拜访。老翁说：“你独居深山，刻苦读书，是不\
是想考取功名做官呀？你学习了这么久，竟然连断句、弄懂文字的意思都不会,\
也太愚钝了吧。”书生说：“我生来就很笨，所以没希望考取功名，只想进山苦读,\
不给家里丢脸，就足够了。”老翁说:“你这个孩子，决心很大，我很喜欢。我老了，\
没什么才能，但能够帮你一把,你有时间去我那里一趟吧。”书生问老翁家住何处,\
老翁说：“我姓段，家在山西边的一棵大树下。”说完，老翁就不见了。书生觉得\
这老头恐怕是妖怪，就去大山的西边寻找，果然见到有一棵大概树，枝繁叶茂。\
书生想了想，说：“老翁说姓段，段和概同音，又说住在大树下，那应该\
就是这里了。”\
于是，书生用锄头往下挖，挖出来一根一尺多长的人参，模样长得和那个\
老翁很像。\
书生想起老翁的话，就把人参吃了。从此之后，书生变得格外聪慧，过目\
不忘，进步神速，过了一年多，果然考取了进士，做了官。',
                type = '精',
                creator='刘敬叔',
                book='《异苑》',
                dynasty='南北朝',
                artist='喵九',
            )
        ),
        Document(
            Page(
                main_text='罔象',
                image='罔象.jpg',
                description='罔象是一种水中的精怪，长得如同三岁的小儿，全身赤红，大耳，长爪。\
用绳索做成的圈套可以抓住它，据说将其烹吃，会有吉祥的事。\
据说，当年黄帝出游的时候，在水边丢失了宝贝“玄珠”，黄帝派遣了很\
多人前去寻找都没有找回，最后拜求了罔象，玄珠才失而复得。罔象的本领,\
连黄帝都不得不叹服。',
                type = '精',
                creator='干宝',
                book='《搜神记》',
                dynasty='晋',
                artist='溥心畲',
            )
        ),
        Document(
            Page(
                main_text='钟精',
                image='钟精.jpg',
                description='钟在古代多用于寺院等宗教场所，除此之外，也做计时之用，故有“晨钟\
暮鼓”之说。钟多为铜铁所造，故能长久流传，又因其上铸造的各种纹饰、神\
兽等，古人认为往往会发生蹊跷之事。\
唐朝开元年间，清江郡有一个老头在田间牧牛，忽然听到有一种怪异的声\
音从地下发出来，老头和几个牧童都吓得跑开了。回去之后，老头生病，发烧\
一天重似一天。过了十几天，病稍微好些，他梦见一位男子，穿着青色短衣，\
对他说：“把我搬迁到开元观去！”老头惊醒了，但不知这是什么意思。\
后来过了几天，他到野外去，又听到那怪异的声音。他就把这事报告给郡\
守，郡守生气地说:“这简直就是胡说八道！”让人把老头轰了出去。这天晚上，\
老头又梦见那个男子，告诉他说：“我寄身地下已经好长时间了，你赶快把我\
弄出来，不然你就会得病！”老头特别害怕，到了天明，和他的儿子一块来到\
郡南，挖那块地。大约挖了一丈多深，挖出一口钟，青色，就像梦见的那个男\
子的衣服颜色。于是又去报告郡守，郡守把钟放在了开元观。这一天辰时，没\
人敲钟，钟自己响了，声音特别响亮。郡守就把这事上奏给了唐玄宗，唐玄宗\
特意让宰相李林甫去画下钟的样子，并告示天下。\
宋代广宁寺有口大钟，一天，寺里的和尚撞钟，发现钟不响，反而在城西\
南桥下面传出了钟声，周围的行人听了，没有一个不被惊吓到的。有人告诉了\
寺里的僧人，僧人们带着法器前往桥下做了法事，第二天，寺里的这口大钟才\
恢复正常。\
晚唐天祐年间，吉州龙兴观有一口巨大的古钟，钟上铸有一行字：“晋元\
康年铸造。”大钟顶上有一个洞，相传武则天时，钟声震动长安，女皇不悦,\
令人凿坏了它。一天晚上，大钟突然丢失，第二天早晨又回到原处。但是钟上\
所铸的神兽蒲牢身上有血迹并挂着煮草。煮草是江南一带的水草,叶子像莲草。\
居住在龙兴观前长江边上的人们，有几天夜里都听到江水风浪的巨大响声。一\
天早晨，有一个渔人看见江心有一杆红旗，从上游漂下来，便划着小船去取红\
旗，看见浪涛汹涌的水中鳞片闪着金光，打鱼的人急忙掉船回来。这才知道是\
神兽蒲牢咬伤了江龙。\
清代，某个地方有个废弃的寺庙，传说有怪物，所以没人敢在那里待。有\
一伙贩羊的商人，为了躲避风雨夜宿寺中，听到呜呜的声响，看到一个怪物，\
身体臃肿肥硕，面目模糊，蹒跚而来，走得很迟缓。这伙贩羊的都是一些毛头\
小伙子，也不害怕，一起捡起砖块向那怪物砸去，发出很大的声响。看到那怪\
物没有反击的举动，这帮人胆子更大了，一起去追赶它，追到了寺门倒塌的墙\
跟前，发现竟然是一口破钟，里面有很多人的碎骨，应该是先前它吃掉的。第\
二天，这伙人把事情告诉了当地人，让他们把钟熔化了。自此之后，这座寺院\
再也没有怪事发生。',
                type = '精',
                creator='张读',
                book='《宣室志》',
                dynasty='唐',
                artist='喵九',
            )
        ),
        Document(
            Page(
                main_text='貘',
                image='貘.jpg',
                description='貘是中国古代传说中的一种怪兽，据说生在铜坑之中，以铜和铁为食物，\
用它的排泄物可以锻造出削铁如泥的兵器，它的尿可以溶解金属。\
清代北京附近的房山出现了貘兽，喜欢吃铜铁，但是不伤人，它看到老百\
姓家里犁子、锄头、刀斧之类的东西，就馋得流口水，吃起来就像吃豆腐一般，\
连城门上包裹的铁皮都被它吃光了。\
古人认为貘是辟邪之物。白居易曾经专门写过一首赞扬貘的诗，其中有这\
么两句：“寝其皮辟湿，图其形辟邪。”',
                type = '精',
                creator='王士祯',
                book='《居易录》',
                dynasty='清',
                artist='喵九',
            )
        ),
    ],
    subindex_configs={'@.[image]': None}, # 这个是啥？
)  # our dataset of pages


## 增加功能 extend
print(da)

print(da[:, 'main_text'][0].text)
da.summary()

# da.to_pydantic_model()


img_model = resnet50(pretrained=True)


# if uploaded_file is not None:
#     uploaded_file.set_image_tensor_shape(shape=(224, 224)).set_image_tensor_channel_axis(
#     original_channel_axis=-1, new_channel_axis=0
# ).set_image_tensor_normalization(channel_axis=0).embed(img_model)

# embed query



query_page = Page(
    main_text=None if flag2_main_text == 0 else webq_main_text,
    image=None if flag2_image==0 else 'tmp_image/' + uploaded_file.name,
    description = None if flag2_description == 0 else webq_description,
    type = None if flag2_type == 0 else webq_type,
    creator = None if flag2_creator == 0 else webq_creator,
    book = None if flag2_book == 0 else webq_book,
    dynasty = None if flag2_dynasty == 0 else webq_dynasty,
    artist = None if flag2_artist == 0 else webq_artist,
)
query = Document(query_page)  # our query Document
# query.summary()
# st.text(query.embedding)



        # dnew  = (
        #     Document(uri='tmp_image/' + uploaded_file.name),
        # )
        # dnew.uri.set_image_tensor_shape(shape=(224, 224)).set_image_tensor_channel_axis(
        #     original_channel_axis=-1, new_channel_axis=0
        # ).set_image_tensor_normalization(channel_axis=0).embed(img_model)
        # print(dnew.url.embedding)

        # dnew = (
        #     Document(uri='tmp_image/' + uploaded_file.name)
        #     .load_uri_to_image_tensor()
        #     .set_image_tensor_shape(shape=(224, 224))
        #     .set_image_tensor_normalization()
        #     .set_image_tensor_channel_axis(-1, 0)
        # )
        # dnew.uri.embed(img_model)
        # print(dnew['@.[uri]'].embeddings.shape)

        # # imagetensor = torch.flatten(imagetensor)
        # st.text(imagetensor)
        # # imagetensor = imagetensor.reshape(1)
        # query.image.embedding = imagetensor







# embed dataset
da['@.[image]'].apply(
    lambda d: d.set_image_tensor_shape(shape=(224, 224))
    .set_image_tensor_channel_axis(original_channel_axis=-1, new_channel_axis=0)
    .set_image_tensor_normalization(channel_axis=0)
).embed(img_model)



# for d in da:
#     print(d.image.embedding)
#     print(type(d.image.embedding))

# embed text data in query and dataset

model = SentenceModel("shibing624/text2vec-base-chinese", encoder_type=EncoderType.FIRST_LAST_AVG, device='cpu')
feature_vec = model.encode

progress_bar = st.progress(0)

count = 0
length = len(da)

for d in tqdm(da):
    # print(d.main_text)
    # print(type(d.main_text))
    # d.main_text.summary()
    # print(d.main_text.text)
    count += 1
    progress_bar.progress(round(count/length*100))

    # count += 1
    # progress_bar.progress(count/da.length)
    d.main_text.embedding = feature_vec(d.main_text.text)
    d.description.embedding = feature_vec(d.description.text)
    d.type.embedding = feature_vec(d.type.text)
    d.creator.embedding = feature_vec(d.creator.text)
    d.book.embedding = feature_vec(d.book.text)
    d.dynasty.embedding = feature_vec(d.dynasty.text)
    d.artist.embedding = feature_vec(d.artist.text)
    # print(d.main_text.embedding)
    # print(d.description.embedding)
    # print(type(d.description.embedding))
    # print(d.embedding.shape)
    # d.embedding = np.concatenate([feature_vec(d.main_text.text), feature_vec(d.description.text)])
    # print(d.embedding.shape)

    # d.main_text.embedding = feature_vec(d.main_text)
    # d.description.embedding = feature_vec(d.description)
    # d.embedding = np.concatenate([feature_vec(d.main_text), feature_vec(d.description)])

# for d in tqdm(da):
#     # d.summary()
#     print(d.embedding)

# query.main_text.embed_feature_hashing()
# query.description.embed_feature_hashing()改


# da['@.[description, main_text]'].apply(lambda d: feature_vec(d))


# print(query.main_text.embedding)
#
#
# combine embeddings to overall embedding

# 合并其实可以不要了，有内嵌的子索引
def combine_embeddings(d):
    # any (more sophisticated) function could go here
    # d.embedding = []
    # d.embeedding = np.array(d.embedding)
    d.embedding = np.empty(shape=(1))
    # d.embedding = np.zeros(8)
    if flag1_main_text== 1:
        # st.text(d.main_text.embedding)
        # st.text(d.main_text.embedding.shape)
        d.main_text.embedding = feature_vec(d.main_text.text)
        d.embedding = np.concatenate([d.embedding, d.main_text.embedding])
        # d.embedding = np.tile(d.embedding, 2)
    if flag1_image == 1:
        d.image.set_image_tensor_shape(shape=(224, 224)).set_image_tensor_channel_axis(
            original_channel_axis=-1, new_channel_axis=0
        ).set_image_tensor_normalization(channel_axis=0).embed(img_model)
        d.embedding = np.concatenate([d.embedding, d.image.embedding])
    if flag1_description == 1:
        d.description.embedding = feature_vec(d.description.text)
        d.embedding = np.concatenate([d.embedding, d.description.embedding])
    if flag1_type == 1:
        d.type.embedding = feature_vec(d.type.text)
        d.embedding = np.concatenate([d.embedding, d.type.embedding])
    if flag1_creator == 1:
        d.creator.embedding = feature_vec(d.creator.text)
        d.embedding = np.concatenate([d.embedding, d.creator.embedding])
    if flag1_book == 1:
        d.book.embedding = feature_vec(d.book.text)
        d.embedding = np.concatenate([d.embedding, d.book.embedding])
    if flag1_dynasty == 1:
        d.dynasty.embedding = feature_vec(d.dynasty.text)
        d.embedding = np.concatenate([d.embedding, d.dynasty.embedding])
    if flag1_artist == 1:
        d.artist.embedding = feature_vec(d.artist.text)
        d.embedding = np.concatenate([d.embedding, d.artist.embedding])
    print(d.embedding.shape)

    # 这里测试
    # d.embedding = np.concatenate(
    #     [d.image.embedding, d.main_text.embedding, d.description.embedding]
    # )
    return d

# 这里测试
# query = combine_embeddings(query)  # combine embeddings for query
# da.apply(combine_embeddings)  # combine embeddings in dataset
#
# for d in da:
#     print(d.embedding.shape)
    # print(d.embedding)

df = pd.DataFrame(columns=['妖怪名称', '原文描述', '种类', '作者', '出处', '朝代', '绘者'])

# da.find(query)[0][1].summary()

# 创建一个空列表，用来存储标签的名字和图片的地址
tabs = []


# st.text(length)

# 用st.tabs函数来创建100个标签页，并返回100个容器对象
# containers = st.tabs([f"Tab {i+1}" for i in range(top_n)])

if search_button and add_radio == '模糊匹配':
    # empty要素
    # da[0].plot_matches_sprites(top_k=top_n, channel_axis=-1, inv_normalize=False) 定义不太对
    # 验证是否检索数据为空
    flagerror = 0
    for i in range(8):
        if(flag1[i] == 1 and flag2[i] == 0):
            st.error("数据不一致，请重新选择有效输入模块或者增添输入")
            flagerror = 1
            break
    ## 从这行到后面所有增加了tab
    if flagerror == 0:

        query = combine_embeddings(query)  # combine embeddings for query
        da.apply(combine_embeddings)  # combine embeddings in dataset
        farest_match_page = da.find(query)[0][(top_n-1)]
        nearest_match_page = da.find(query)[0][0]
        if (nearest_match_page.scores['cosine'].value > max_value):
            st.error('目前的最大几何距离，未能得到有效结果，请更改对应参数')
            flagerror = 1
        elif (farest_match_page.scores['cosine'].value > max_value):
            st.warning('由于最大几何距离限定，无法输出全部'+ str(top_n) + '个结果', icon="⚠️")
        else:
            st.success('成功找到'+ str(top_n) + '个结果', icon="✅")
        if flagerror == 0:
            query.summary()
            for n in range(top_n):
                closest_match_page = da.find(query=query)[0][n]
                if(closest_match_page.scores['cosine'].value > max_value):
                    break
                name = closest_match_page.main_text.text
                tabs.append(name)
            containers = st.tabs(tabs)
                # 生成tab头
            for n in range(top_n):
                closest_match_page = da.find(query=query)[0][n]
                print(closest_match_page.main_text.text)
                print(str(closest_match_page.scores['cosine'].value))
                if(closest_match_page.scores['cosine'].value > max_value):
                    break
                # print(closest_match_page.scores['cosine'].value)
                # st.text('第'+str(n+1)+'相似的妖怪是'+closest_match_page.main_text.text+',相似距离是'+str(closest_match_page.scores['cosine'].value)+',下面是其详细信息')
                #
                # st.markdown('>'+closest_match_page.description.text)

                # st.image(closest_match_page.image.uri)

                tabs.append((closest_match_page.main_text.text, closest_match_page.description.text, closest_match_page.image.uri))
                # 获取当前的容器对象
                container = containers[n]
                # 在容器中添加标题和图片
                with container:
                    # st.header(closest_match_page.main_text.text)
                    # st.text('running though')
                    st.text('第' + str(n + 1) + '相似的妖怪是' + closest_match_page.main_text.text + ',几何距离是' + str(closest_match_page.scores['cosine'].value) + ',下面是其详细信息')
                    st.image(closest_match_page.image.uri)
                    st.markdown('>'+closest_match_page.description.text)
                    st.markdown('+ 种类: ' + closest_match_page.type.text)
                    st.markdown('+ 作者: '+closest_match_page.creator.text)
                    st.markdown('+ 出处: '+closest_match_page.book.text)
                    st.markdown('+ 朝代: '+closest_match_page.dynasty.text)
                    st.markdown('+ 绘者: '+closest_match_page.artist.text)

                # 生成dataframe

                df.loc[len(df.index)] = [closest_match_page.main_text.text, closest_match_page.description.text, closest_match_page.type.text, closest_match_page.creator.text, closest_match_page.book.text, closest_match_page.dynasty.text, closest_match_page.artist.text]

                # print(df)
                # da[:, 'main_text'][0].text

            # print(closest_match_page.description.text) 不太行
            # knowledge = jiagu.knowledge(closest_match_page.description.text)
            # print(knowledge)
            # st.text(knowledge)
            # closest_match_page.summary()

        # da.push(name="devilanddemon")

    actuallength = 0

    filter = []

if search_button and add_radio == '精确匹配':
    flagerror = 0
    for i in range(8):
        if(flag1[i] == 1 and flag2[i] == 0):
            st.error("数据不一致，请重新选择有效输入模块或者增添输入")
            flagerror = 1
            break
    ## 从这行到后面所有增加了tab
    if flagerror == 0:
        # query = combine_embeddings(query)  # combine embeddings for query
        # da.apply(combine_embeddings)  # combine embeddings in dataset
        # filter = {'modality': {'$eq': 'D'}}

        filter = {'main_text': {'$eq': '八哥'}}
        print(webq_main_text)
        for count in range(len(da)):

            print(da[:, 'main_text'][count].text)
        print(da.find(filter=filter))
        for n in range(length):
            try:
                closest_match_page = da.find(query,filter=filter)[0][n]
                print(actuallength)
                name = closest_match_page.main_text.text
                tabs.append(name)
                actuallength += 1
            except:
                break
        containers = st.tabs(tabs)
        # 生成tab头
        for n in range(actuallength):
            closest_match_page = da.find(query)[0][n]
            # st.text('第'+str(n+1)+'相似的妖怪是'+closest_match_page.main_text.text+',相似距离是'+str(closest_match_page.scores['cosine'].value)+',下面是其详细信息')
            #
            # st.markdown('>'+closest_match_page.description.text)

            # containers = st.tabs([name for name, _ in tabs])
            # st.image(closest_match_page.image.uri)

            tabs.append(
                (closest_match_page.main_text.text, closest_match_page.description.text, closest_match_page.image.uri))
            # 获取当前的容器对象
            container = containers[n]
            # 在容器中添加标题和图片
            with container:
                print("running")
                # st.header(closest_match_page.main_text.text)
                st.text('第' + str(n + 1) + '相似的妖怪是' + closest_match_page.main_text.text + ',几何距离是' + str(
                    closest_match_page.scores['cosine'].value) + ',下面是其详细信息')
                st.image(closest_match_page.image.uri)
                st.markdown('>' + closest_match_page.description.text)
                st.markdown('+ 种类: ' + closest_match_page.type.text)
                st.markdown('+ 作者: ' + closest_match_page.creator.text)
                st.markdown('+ 出处: ' + closest_match_page.book.text)
                st.markdown('+ 朝代: ' + closest_match_page.dynasty.text)
                st.markdown('+ 绘者: ' + closest_match_page.artist.text)


# 这后面开始是一个整体
@st.cache_data
def convert_df(df):
   return df.to_csv(index=False).encode('utf-8')


st.markdown("所有文本数据汇总如下：")
# Display an interactive table
st.dataframe(df)



## 可以编辑后下载
csv = convert_df(df)



st.download_button(
   "下载检索/编辑后所得文本数据",
   csv,
   "搜索结果.csv",
   "text/csv",
   key='download-csv'
)