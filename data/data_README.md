### 补充-车牌字符数据集 num1   
应字符分割识别的需求，特制宽度较大的数字１字符数据集　　　     
8：2 划分train与test:  
trainset:800张，test：200张    

### 第七版-车牌字符数据集 pp_char_blur  
--相较于第六版进行了字体随机模糊预处理   

### 第六版-车牌字符数据集 pp_char  
--相较于第五版进行了字体随机旋转、笔画粘连断裂等预处理   
字体：“方正粗黑宋简体”、“黑体”、“方正兰亭黑长简体”  
8：2 划分train与test:  
['chuan', 'e1', 'gan', 'gan1', 'gui', 'gui1', 'hei', 'hu','ji', 'jin',  
'jing', 'jl', 'liao', 'lu', 'meng', 'min', 'ning', 'qing', 'qiong',  
'shan', 'su', 'sx', 'wan', 'xiang', 'xin', 'yu', 'yu1', 'yue', 'yun', 'zang', 'zhe']       
对应： 京沪津渝黑吉辽蒙冀新甘青陕宁豫鲁晋皖鄂湘苏川贵云桂藏浙赣粤闽琼    
每个字符trainset:876张，testset:222张

### 第五版-车牌字符数据集 c_char_2  
--修正1：类别已更正  
借助“方正粗黑宋简体”、“黑体”、“方正兰亭黑长简体”，  
生成省会简称的汉字字符数据集，  
8：2 划分chs_train与chs_test:  
['chuan', 'e1', 'gan', 'gan1', 'gui', 'gui1', 'hei', 'hu','ji', 'jin',  
'jing', 'jl', 'liao', 'lu', 'meng', 'min', 'ning', 'qing', 'qiong',  
'shan', 'su', 'sx', 'wan', 'xiang', 'xin', 'yu', 'yu1', 'yue', 'yun', 'zang', 'zhe']    
对应： 京沪津渝黑吉辽蒙冀新甘青陕宁豫鲁晋皖鄂湘苏川贵云桂藏浙赣粤闽琼    
每个字符trainset:800张，testset:199张  


### 第四版-车牌字符数据集 c_char
--修正1：类别已更正  
借助“方正粗黑宋简体”，生成省会简称的汉字字符数据集，  
8：2 划分chs_train与chs_test:  
['chuan', 'e1', 'gan', 'gan1', 'gui', 'gui1', 'hei', 'hu','ji', 'jin',  
'jing', 'jl', 'liao', 'lu', 'meng', 'min', 'ning', 'qing', 'qiong',  
'shan', 'su', 'sx', 'wan', 'xiang', 'xin', 'yu', 'yu1', 'yue', 'yun', 'zang', 'zhe']     
对应： 京沪津渝黑吉辽蒙冀新甘青陕宁豫鲁晋皖鄂湘苏川贵云桂藏浙赣粤闽琼    
每个字符trainset:1600张，testset:400张  


### 第三版-车牌字符数据集 char_data_3
分中英文字符chs,eng,按照8：2划分trainset与testset  
eng_test与eng_train下分34个文件夹  
['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'A',    
'B', 'C','D', 'E', 'F', 'G', 'H', 'J', 'K', 'L', 'M', 'N',   
'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']    
eng_train:  
文件夹： 0 图片数量： 1329     
文件夹： 1 图片数量： 948     
文件夹： 2 图片数量： 1067     
文件夹： 3 图片数量： 1049     
文件夹： 4 图片数量： 807     
文件夹： 5 图片数量： 1664     
文件夹： 6 图片数量： 1327     
文件夹： 7 图片数量： 1427     
文件夹： 8 图片数量： 1998     
文件夹： 9 图片数量： 2016     
文件夹： A 图片数量： 2016     
文件夹： B 图片数量： 719     
文件夹： C 图片数量： 482     
文件夹： D 图片数量： 336     
文件夹： E 图片数量： 459     
文件夹： F 图片数量： 332     
文件夹： G 图片数量： 344     
文件夹： H 图片数量： 273     
文件夹： J 图片数量： 229     
文件夹： K 图片数量： 330     
文件夹： L 图片数量： 320     
文件夹： M 图片数量： 340     
文件夹： N 图片数量： 284     
文件夹： P 图片数量： 245     
文件夹： Q 图片数量： 314     
文件夹： R 图片数量： 254     
文件夹： S 图片数量： 287     
文件夹： T 图片数量： 217     
文件夹： U 图片数量： 175     
文件夹： V 图片数量： 181     
文件夹： W 图片数量： 179     
文件夹： X 图片数量： 171     
文件夹： Y 图片数量： 200     
文件夹： Z 图片数量： 167     

eng_test:  
文件夹： 0 图片数量： 332     
文件夹： 1 图片数量： 236     
文件夹： 2 图片数量： 266     
文件夹： 3 图片数量： 262     
文件夹： 4 图片数量： 201     
文件夹： 5 图片数量： 416     
文件夹： 6 图片数量： 331     
文件夹： 7 图片数量： 356     
文件夹： 8 图片数量： 499     
文件夹： 9 图片数量： 504     
文件夹： A 图片数量： 504     
文件夹： B 图片数量： 179     
文件夹： C 图片数量： 120     
文件夹： D 图片数量： 83     
文件夹： E 图片数量： 114     
文件夹： F 图片数量： 82     
文件夹： G 图片数量： 86     
文件夹： H 图片数量： 68     
文件夹： J 图片数量： 57     
文件夹： K 图片数量： 82     
文件夹： L 图片数量： 79     
文件夹： M 图片数量： 85     
文件夹： N 图片数量： 71     
文件夹： P 图片数量： 61     
文件夹： Q 图片数量： 78     
文件夹： R 图片数量： 63     
文件夹： S 图片数量： 71     
文件夹： T 图片数量： 54     
文件夹： U 图片数量： 43     
文件夹： V 图片数量： 45     
文件夹： W 图片数量： 44     
文件夹： X 图片数量： 42     
文件夹： Y 图片数量： 50     
文件夹： Z 图片数量： 41     

chs_test与chs_train下分31个文件夹  
['chuan', 'e1', 'gan', 'gan1', 'gui', 'gui1', 'hei', 'hu','ji', 'jin',    
'jing', 'jl', 'liao', 'lu', 'meng', 'min', 'ning', 'qing', 'qiong',    
'shan', 'su', 'sx', 'wan', 'xiang', 'xin', 'yu', 'yu1', 'yue', 'yun', 'zang', 'zhe']  
chs_train:  
文件夹： chuan 图片数量： 428     
文件夹： e1 图片数量： 615     
文件夹： gan 图片数量： 177     
文件夹： gan1 图片数量： 500     
文件夹： gui 图片数量： 608     
文件夹： gui1 图片数量： 123     
文件夹： hei 图片数量： 164     
文件夹： hu 图片数量： 455     
文件夹： ji 图片数量： 678     
文件夹： jin 图片数量： 784     
文件夹： jing 图片数量： 867     
文件夹： jl 图片数量： 248     
文件夹： liao 图片数量： 663     
文件夹： lu 图片数量： 227     
文件夹： meng 图片数量： 480     
文件夹： min 图片数量： 669     
文件夹： ning 图片数量： 110     
文件夹： qing 图片数量： 606     
文件夹： qiong 图片数量： 49     
文件夹： shan 图片数量： 324     
文件夹： su 图片数量： 1021     
文件夹： sx 图片数量： 477     
文件夹： wan 图片数量： 411     
文件夹： xiang 图片数量： 694     
文件夹： xin 图片数量： 162     
文件夹： yu 图片数量： 160     
文件夹： yu1 图片数量： 180     
文件夹： yue 图片数量： 1021     
文件夹： yun 图片数量： 478     
文件夹： zang 图片数量： 24     
文件夹： zhe 图片数量： 807     

chs_test:  
文件夹： chuan 图片数量： 107     
文件夹： e1 图片数量： 153     
文件夹： gan 图片数量： 44     
文件夹： gan1 图片数量： 125     
文件夹： gui 图片数量： 152     
文件夹： gui1 图片数量： 30     
文件夹： hei 图片数量： 41     
文件夹： hu 图片数量： 113     
文件夹： ji 图片数量： 169     
文件夹： jin 图片数量： 196     
文件夹： jing 图片数量： 216     
文件夹： jl 图片数量： 62     
文件夹： liao 图片数量： 165     
文件夹： lu 图片数量： 56     
文件夹： meng 图片数量： 119     
文件夹： min 图片数量： 167     
文件夹： ning 图片数量： 27     
文件夹： qing 图片数量： 151     
文件夹： qiong 图片数量： 12     
文件夹： shan 图片数量： 80     
文件夹： su 图片数量： 255     
文件夹： sx 图片数量： 119     
文件夹： wan 图片数量： 102     
文件夹： xiang 图片数量： 173     
文件夹： xin 图片数量： 40     
文件夹： yu 图片数量： 39     
文件夹： yu1 图片数量： 45     
文件夹： yue 图片数量： 255     
文件夹： yun 图片数量： 119     
文件夹： zang 图片数量： 5     
文件夹： zhe 图片数量： 201     

### pro版-车牌字符数据集 char_data_pro
分中英文字符chs,eng,按照8：2划分trainset与testset  
eng_test与eng_train下分34个文件夹  
['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'A',    
'B', 'C','D', 'E', 'F', 'G', 'H', 'J', 'K', 'L', 'M', 'N',   
'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']   
train图片数量均为64张，test图片数量均为16张   

chs_test与chs_train下分31个文件夹  
['chuan', 'e1', 'gan', 'gan1', 'gui', 'gui1', 'hei', 'hu','ji', 'jin',  
'jing', 'jl', 'liao', 'lu', 'meng', 'min', 'ning', 'qing', 'qiong',  
'shan', 'su', 'sx', 'wan', 'xiang', 'xin', 'yu', 'yu1', 'yue', 'yun', 'zang', 'zhe']  
chs_test中：  
文件夹： chuan 图片数量： 80     
文件夹： e1 图片数量： 145     
文件夹： gan 图片数量： 26     
文件夹： gan1 图片数量： 114     
文件夹： gui 图片数量： 127     
文件夹： gui1 图片数量： 23     
文件夹： hei 图片数量： 19     
文件夹： hu 图片数量： 38     
文件夹： ji 图片数量： 98     
文件夹： jin 图片数量： 122     
文件夹： jing 图片数量： 149     
文件夹： jl 图片数量： 49     
文件夹： liao 图片数量： 144     
文件夹： lu 图片数量： 33     
文件夹： meng 图片数量： 97     
文件夹： min 图片数量： 108     
文件夹： ning 图片数量： 19     
文件夹： qing 图片数量： 134     
文件夹： qiong 图片数量： 6     
文件夹： shan 图片数量： 57     
文件夹： su 图片数量： 150     
文件夹： sx 图片数量： 93     
文件夹： wan 图片数量： 62     
文件夹： xiang 图片数量： 122     
文件夹： xin 图片数量： 31     
文件夹： yu 图片数量： 6     
文件夹： yu1 图片数量： 35     
文件夹： yue 图片数量： 147     
文件夹： yun 图片数量： 111     
文件夹： zang 图片数量： 4     
文件夹： zhe 图片数量： 97     
chs_train中：  
文件夹： chuan 图片数量： 321     
文件夹： e1 图片数量： 583     
文件夹： gan 图片数量： 104     
文件夹： gan1 图片数量： 459     
文件夹： gui 图片数量： 511     
文件夹： gui1 图片数量： 95     
文件夹： hei 图片数量： 80     
文件夹： hu 图片数量： 153     
文件夹： ji 图片数量： 393     
文件夹： jin 图片数量： 490     
文件夹： jing 图片数量： 598     
文件夹： jl 图片数量： 199     
文件夹： liao 图片数量： 577     
文件夹： lu 图片数量： 133     
文件夹： meng 图片数量： 390     
文件夹： min 图片数量： 432     
文件夹： ning 图片数量： 78     
文件夹： qing 图片数量： 538     
文件夹： qiong 图片数量： 24     
文件夹： shan 图片数量： 228     
文件夹： su 图片数量： 603     
文件夹： sx 图片数量： 374     
文件夹： wan 图片数量： 249     
文件夹： xiang 图片数量： 489     
文件夹： xin 图片数量： 126     
文件夹： yu 图片数量： 24     
文件夹： yu1 图片数量： 140     
文件夹： yue 图片数量： 591     
文件夹： yun 图片数量： 446     
文件夹： zang 图片数量： 19     
文件夹： zhe 图片数量： 391     



### 第一版-车牌字符数据集 char_data
下分65个标签文件夹，    
['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'A', 'B', 'C', 'cuan', 'D', 'E', 'e1', 'F',    
'G', 'gan', 'gan1', 'gui', 'gui1', 'H', 'hei', 'hu', 'J', 'ji', 'jin', 'jing', 'jl', 'K', 'L',    
'liao', 'lu', 'M', 'meng', 'min', 'N', 'ning','P', 'Q', 'qing', 'qiong', 'R', 'S', 'shan', 'su',    
'sx', 'T', 'U', 'V', 'W', 'wan', 'X', 'xiang', 'xin', 'Y', 'yu', 'yu1', 'yue', 'yun', 'Z', 'zang', 'zhe']   
文件夹： 0 图片数量： 715  
文件夹： 1 图片数量： 517  
文件夹： 2 图片数量： 601  
文件夹： 3 图片数量： 587  
文件夹： 4 图片数量： 401  
文件夹： 5 图片数量： 973  
文件夹： 6 图片数量： 758  
文件夹： 7 图片数量： 824  
文件夹： 8 图片数量： 1152  
文件夹： 9 图片数量： 1166  
文件夹： A 图片数量： 1013  
文件夹： B 图片数量： 422  
文件夹： C 图片数量： 300  
文件夹： cuan 图片数量： 126  
文件夹： D 图片数量： 213  
文件夹： E 图片数量： 299  
文件夹： e1 图片数量： 63  
文件夹： F 图片数量： 238  
文件夹： G 图片数量： 266  
文件夹： gan 图片数量： 80  
文件夹： gan1 图片数量： 46  
文件夹： gui 图片数量： 53  
文件夹： gui1 图片数量： 32  
文件夹： H 图片数量： 213  
文件夹： hei 图片数量： 101  
文件夹： hu 图片数量： 203  
文件夹： J 图片数量： 164  
文件夹： ji 图片数量： 95  
文件夹： jin 图片数量： 240  
文件夹： jing 图片数量： 147  
文件夹： jl 图片数量： 52  
文件夹： K 图片数量： 266  
文件夹： L 图片数量： 265  
文件夹： liao 图片数量： 79  
文件夹： lu 图片数量： 104  
文件夹： M 图片数量： 243  
文件夹： meng 图片数量： 53  
文件夹： min 图片数量： 67  
文件夹： N 图片数量： 203  
文件夹： ning 图片数量： 32  
文件夹： P 图片数量： 178  
文件夹： Q 图片数量： 126  
文件夹： qing 图片数量： 36  
文件夹： qiong 图片数量： 30  
文件夹： R 图片数量： 165  
文件夹： S 图片数量： 164  
文件夹： shan 图片数量： 73  
文件夹： su 图片数量： 219  
文件夹： sx 图片数量： 92  
文件夹： T 图片数量： 119  
文件夹： U 图片数量： 108  
文件夹： V 图片数量： 80  
文件夹： W 图片数量： 101  
文件夹： wan 图片数量： 172  
文件夹： X 图片数量： 103  
文件夹： xiang 图片数量： 90   
文件夹： xin 图片数量： 19  
文件夹： Y 图片数量： 134  
文件夹： yu 图片数量： 169  
文件夹： yu1 图片数量： 42  
文件夹： yue 图片数量： 160  
文件夹： yun 图片数量： 35  
文件夹： Z 图片数量： 98   
文件夹： zang 图片数量： 6  
文件夹： zhe 图片数量： 260  

### 第二版-车牌字符数据集 char_data_2
(由多个数据集拼凑而成，故而尺寸大小不一致，部分未进行二值化处理）  
下分65个标签文件夹，  
['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'A', 'B', 'C', 'cuan', 'D', 'E', 'e1', 'F',   
'G', 'gan', 'gan1', 'gui', 'gui1', 'H', 'hei', 'hu', 'J', 'ji', 'jin', 'jing', 'jl', 'K', 'L',   
'liao', 'lu', 'M', 'meng', 'min', 'N', 'ning','P', 'Q', 'qing', 'qiong', 'R', 'S', 'shan', 'su',   
'sx', 'T', 'U', 'V', 'W', 'wan', 'X', 'xiang', 'xin', 'Y', 'yu', 'yu1', 'yue', 'yun', 'Z', 'zang', 'zhe']  
文件夹： 0 图片数量： 1661  
文件夹： 1 图片数量： 1184  
文件夹： 2 图片数量： 1333  
文件夹： 3 图片数量： 1311  
文件夹： 4 图片数量： 1008  
文件夹： 5 图片数量： 2080  
文件夹： 6 图片数量： 1658  
文件夹： 7 图片数量： 1783  
文件夹： 8 图片数量： 2497  
文件夹： 9 图片数量： 2520  
文件夹： A 图片数量： 2520  
文件夹： B 图片数量： 898  
文件夹： C 图片数量： 602  
文件夹： chuan 图片数量： 550  
文件夹： D 图片数量： 419  
文件夹： E 图片数量： 573  
文件夹： e1 图片数量： 792  
文件夹： F 图片数量： 414  
文件夹： G 图片数量： 430  
文件夹： gan 图片数量： 235  
文件夹： gan1 图片数量： 628    
文件夹： gui 图片数量： 764  
文件夹： gui1 图片数量： 156  
文件夹： H 图片数量： 341  
文件夹： hei 图片数量： 205  
文件夹： hu 图片数量： 574  
文件夹： J 图片数量： 286  
文件夹： ji 图片数量： 848  
文件夹： jin 图片数量： 980  
文件夹： jing 图片数量： 1085  
文件夹： jl 图片数量： 311  
文件夹： K 图片数量： 412  
文件夹： L 图片数量： 399  
文件夹： liao 图片数量： 829  
文件夹： lu 图片数量： 284  
文件夹： M 图片数量： 425  
文件夹： meng 图片数量： 599  
文件夹： min 图片数量： 841  
文件夹： N 图片数量： 355  
文件夹： ning 图片数量： 139  
文件夹： P 图片数量： 306  
文件夹： Q 图片数量： 392  
文件夹： qing 图片数量： 758  
文件夹： qiong 图片数量： 75  
文件夹： R 图片数量： 317  
文件夹： S 图片数量： 358  
文件夹： shan 图片数量： 405  
文件夹： su 图片数量： 1276  
文件夹： sx 图片数量： 597  
文件夹： T 图片数量： 271  
文件夹： U 图片数量： 218  
文件夹： V 图片数量： 226  
文件夹： W 图片数量： 223  
文件夹： wan 图片数量： 518  
文件夹： X 图片数量： 213  
文件夹： xiang 图片数量： 867  
文件夹： xin 图片数量： 202  
文件夹： Y 图片数量： 250  
文件夹： yu 图片数量： 199  
文件夹： yu1 图片数量： 225  
文件夹： yue 图片数量： 1276   
文件夹： yun 图片数量： 597  
文件夹： Z 图片数量： 208  
文件夹： zang 图片数量： 29  
文件夹： zhe 图片数量： 1008  

### CCPD_simple 车牌图片数据集
下分9个文件夹：  
['base', 'blur', 'challenge', 'db', 'fn', 'np', 'rotate', 'tilt', 'weather']  
每个文件夹内含有3K张图片。  
'base', 通用车牌图片    
'blur', 由于摄像机镜头抖动导致的模糊车牌图片  
'challenge',在车牌检测识别任务中较有挑战性的图片  
'db', 车牌区域亮度较亮、较暗或者不均匀  
'fn',车牌离摄像头拍摄位置相对较近或较远  
'np', 没有安装车牌的新车图片  
'rotate',车牌水平倾斜20到50度,竖直倾斜-10到10度  
'tilt', 车牌水平倾斜15到45度,竖直倾斜15到45度  
'weather'车牌在雨雪雾天气拍摄得到   





