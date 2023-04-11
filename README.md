# Tiny-skills-of-data
[![LICENSE](https://img.shields.io/badge/license-Anti%20996-blue.svg)](https://github.com/996icu/996.ICU/blob/master/LICENSE) <br>

This repository includes some tiny skills or tiny functions for data science analysis. <br>
Tiny, but maybe helpful sometime. Welcome to contribute.


## R scripts

| function | code | comment |
| :-- | :-: | :-: |
| China map | [script](https://github.com/LongxingTan/Tiny-skills-of-data/tree/master/R/map) | [Chinese blog](https://mp.weixin.qq.com/s/AMfcllfmZFR_8cV5hldcug) |
| World map | [script](https://github.com/LongxingTan/Tiny-skills-of-data/tree/master/R/map) | [Chinese blog]() |
| Crawl weather | [script](https://github.com/LongxingTan/Tiny-skills-of-data/tree/master/R/weather-data) | [Chinese blog](https://mp.weixin.qq.com/s/c6xrMpC4M5gpCSVFTuUGqQ) |

<br>

- This china province and world shp file are provided in `./assets`. 
If you want to download more specific province of China, you could download from [NGCC](http://www.webmap.cn/mapDataAction.do?method=forw&resType=5&storeId=2&storeName=%E5%9B%BD%E5%AE%B6%E5%9F%BA%E7%A1%80%E5%9C%B0%E7%90%86%E4%BF%A1%E6%81%AF%E4%B8%AD%E5%BF%83)

-  Get the data from RNCEP. Further reading [this posting](https://dominicroye.github.io/en/2018/access-to-climate-reanalysis-data-from-r/)

```bash
cd R/china-map
Rscript China_map_bubble.R
Rscript Chine_map_great_circle.R
```


## Python scripts

| function | code | comment |
| :-- | :-: | :-: |
| China map | [script](https://github.com/LongxingTan/Tiny-skills-of-data/tree/master/Python/map) | [Chinese blog](https://mp.weixin.qq.com/s/kXJ88hbZ9cE5Jlu3StTjyg) |
| World map | [script](https://github.com/LongxingTan/Tiny-skills-of-data/tree/master/Python/map) | [Chinese blog]() |
| Crawl weather | [script](https://github.com/LongxingTan/Tiny-skills-of-data/tree/master/Python/weather-data) | [Chinese blog]() |
| Send email | [script](https://github.com/LongxingTan/Tiny-skills-of-data/tree/master/Python/send-email) | [Chinese blog](https://mp.weixin.qq.com/s/WUR4jzTP8XPlppg0N8wtzw) |

<br>

- And, you can also check the official [China weather API](http://data.cma.cn/Market/MarketList.html), or download through FTP directly from [NOAA](https://www.esrl.noaa.gov/psd/data/gridded/help.html#FTP)


## Acknowledgement

Thanks for my former colleague Dr. Christian Weichsel to tell me the RNCEP library and share me his code.<br>

## Some visualization example
- https://www.kaggle.com/lucasmorin/umap-data-analysis-applications/notebook
